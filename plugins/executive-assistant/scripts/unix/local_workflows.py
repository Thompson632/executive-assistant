"""Review supplied metadata and prepare local files."""

from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import stat
from tempfile import NamedTemporaryFile


FIELDS = {
    "mail": {"subject": str, "sender": str, "received": str, "folder": str,
             "unread": bool, "flagged": bool, "attachment_count": int},
    "calendar": {"title": str, "start": str, "end": str, "location": str, "status": str,
                 "recurring": bool, "private": bool, "has_attendees": bool, "all_day": bool},
    "tasks": {"title": str, "due": str, "status": str, "priority": str, "source": str},
}
REQUIRED = {"mail": ("subject",), "calendar": ("title", "start", "end"), "tasks": ("title",)}
DRAFT_HEADER = "---\ntype: executive-assistant-draft\n---\n\n"
OPERATIONS = ("draft", "attachment")
STATUSES = ("written", "failed")


def local_path(value):
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", value):
        raise ValueError("Use a local filesystem path.")
    return Path(value).expanduser()


@contextmanager
def open_regular(path, *, nofollow=False):
    flags = os.O_RDONLY | os.O_NONBLOCK
    if nofollow:
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("Supply a regular file.")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            yield stream
    finally:
        os.close(fd)


def read_input(path):
    with open_regular(path) as stream:
        return stream.read().decode("utf-8-sig")


def timestamp(value):
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError("Timestamps need a time zone offset.")
    return parsed


def read_records(source: str, kind: str, *, exclude_canceled: bool = False) -> list[dict]:
    return validate_records(
        json.loads(read_input(local_path(source))), kind, exclude_canceled=exclude_canceled,
    )


def validate_records(payload: object, kind: str, *, exclude_canceled: bool = False) -> list[dict]:
    if not isinstance(payload, list):
        raise ValueError("Expected a JSON array of metadata objects.")
    records = []
    for index, item in enumerate(payload, 1):
        if not isinstance(item, dict):
            raise ValueError(f"Record {index} must be a JSON object.")
        safe = {name: item[name] for name in FIELDS[kind] if name in item}
        for name in REQUIRED[kind]:
            if not isinstance(safe.get(name), str) or not safe[name].strip():
                raise ValueError(f"Record {index} needs a nonempty {name}.")
        for name, value in safe.items():
            if type(value) is not FIELDS[kind][name]:
                raise ValueError(f"Record {index} has an invalid {name} field.")
        if kind == "calendar":
            if timestamp(safe["end"]) <= timestamp(safe["start"]):
                raise ValueError(f"Record {index} needs an end time after its start time.")
            if exclude_canceled and safe.get("status", "").casefold() in {"canceled", "cancelled"}:
                continue
            if safe.get("private"):
                safe = {"title": "Private event", "start": safe["start"], "end": safe["end"]}
        if kind == "mail" and "received" in safe:
            timestamp(safe["received"])
        if safe.get("attachment_count", 0) < 0:
            raise ValueError(f"Record {index} has a negative attachment count.")
        records.append(safe)
    return records


def review(args):
    result = {"kind": args.kind, "records": read_records(args.source, args.kind)}
    if args.compare is not None:
        if args.kind != "calendar":
            raise ValueError("--compare requires calendar metadata.")
        result["comparison_records"] = read_records(args.compare, "calendar")
    if args.kind != "mail":
        if any(value is not None for value in (args.folder, args.since, args.offset, args.limit)):
            raise ValueError("Folder, date and paging options require mail metadata.")
        return result
    offset = 0 if args.offset is None else args.offset
    limit = 5 if args.limit is None else args.limit
    if offset < 0 or limit < 1:
        raise ValueError("Use a nonnegative offset and positive limit.")
    since = timestamp(args.since) if args.since else None
    records = [
        row for row in result["records"]
        if (args.folder is None or row.get("folder") == args.folder)
        and (since is None or ("received" in row and timestamp(row["received"]) >= since))
    ]
    result["records"] = records[offset:offset + limit]
    return result


def draft_text(args):
    body = read_input(local_path(args.source))
    subject = " ".join(args.subject.split())
    if not subject or not body.strip():
        raise ValueError("Supply a nonempty subject and draft text.")
    return f"# {subject}\n\n{body.rstrip()}\n"


def destination_path(vault, value):
    path = local_path(value)
    if not path.is_absolute() or path != path.resolve() or vault not in path.parents:
        raise ValueError("Choose an absolute destination inside the vault without symlinks or traversal.")
    return path


def write_attachment(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=destination.parent, prefix=".ea-", delete=False) as tmp:
        temporary = Path(tmp.name)
        try:
            with tmp, open_regular(source) as stream:
                shutil.copyfileobj(stream, tmp)
            os.link(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)


def append_audit(profile, operation, status):
    path = profile.parent / "local-audit.jsonl"
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK
    line = json.dumps({"operation": operation, "status": status}) + "\n"
    with os.fdopen(os.open(path, flags, 0o600), "a", encoding="utf-8") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("The local audit must be a regular file.")
        stream.write(line)


def read_audit(profile):
    result = {operation: dict.fromkeys(STATUSES, 0) for operation in OPERATIONS}
    path = profile.parent / "local-audit.jsonl"
    if not path.exists():
        return result
    with open_regular(path, nofollow=True) as stream:
        for line in stream:
            record = json.loads(line)
            operation = record.get("operation") if isinstance(record, dict) else None
            status = record.get("status") if isinstance(record, dict) else None
            if operation in OPERATIONS and status in STATUSES:
                result[operation][status] += 1
    return result


def register(commands):
    parser = commands.add_parser("review", help="Read selected fields from local metadata")
    parser.add_argument("kind", choices=FIELDS)
    parser.add_argument("--source", required=True)
    parser.add_argument("--compare")
    parser.add_argument("--folder")
    parser.add_argument("--since")
    parser.add_argument("--offset", type=int)
    parser.add_argument("--limit", type=int)
    parser = commands.add_parser("draft", help="Preview or save local draft text")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output")
    parser.add_argument("--apply", action="store_true")
    parser = commands.add_parser("attachment", help="Preview or file a supplied attachment")
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-save")
    parser = commands.add_parser("resolve", help="Check an explicitly supplied local file")
    parser.add_argument("--path", required=True)
    commands.add_parser("audit", help="Read aggregate local operation counts")
