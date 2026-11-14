"""Read Outlook metadata from local sync files."""

from datetime import date, datetime, time, timedelta, timezone
from email import policy
from email.parser import BytesHeaderParser
import heapq
import os
import stat

import local_workflows


KINDS = ("mail", "calendar")
FILE_PROVIDER = "local"


def sources(profile):
    settings = profile.get("outlook")
    if not isinstance(settings, dict) or settings.get("enabled") is not True:
        return {}
    provider = settings.get("provider")
    if provider is None and ("protocolName" in settings or "mailboxName" in settings):
        # Profiles imported from the former Outlook runtime require a new source.
        return {}
    if provider != FILE_PROVIDER:
        raise ValueError("Set outlook.provider to local and configure outlook.maildir or outlook.calendarFile.")
    result = {}
    for kind, key in (("mail", "maildir"), ("calendar", "calendarFile")):
        if key not in settings:
            continue
        value = settings[key]
        if not isinstance(value, str) or not value.strip() or "\x00" in value:
            raise ValueError(f"Set outlook.{key} to a nonempty string.")
        try:
            path = local_workflows.local_path(value)
        except ValueError:
            raise ValueError(f"Set outlook.{key} to an absolute local path.") from None
        if not path.is_absolute():
            raise ValueError(f"Set outlook.{key} to an absolute local path.")
        result[kind] = path
    if not result:
        raise ValueError("Configure at least one Outlook mail or calendar source.")
    return result


def midnight(day):
    # Resolve each boundary in the host zone so windows spanning a clock change work.
    return datetime.combine(day, time.min).astimezone()


def maildir_headers(path):
    with local_workflows.open_regular(path, nofollow=True) as message:
        headers = bytearray()
        while len(headers) < 65536:
            line = message.readline(65536 - len(headers))
            if line in (b"", b"\n", b"\r\n"):
                return BytesHeaderParser(policy=policy.default).parsebytes(headers)
            headers.extend(line)
    raise ValueError("A selected Maildir message has headers larger than 64 KiB.")


def read_maildir(path, start, end, limit):
    first_modified, last_modified = start.timestamp(), end.timestamp()

    def candidates():
        for subdir in ("cur", "new"):
            with os.scandir(path / subdir) as entries:
                for entry in entries:
                    _, separator, flags = entry.name.rpartition(":2,")
                    if not separator:
                        flags = ""
                    if "T" in flags or ("S" in flags and "F" not in flags):
                        continue
                    try:
                        status = entry.stat(follow_symlinks=False)
                    except FileNotFoundError:
                        continue
                    if stat.S_ISREG(status.st_mode) and first_modified <= status.st_mtime < last_modified:
                        yield status.st_mtime, entry.path, flags

    # Open headers in recency order, retaining a small buffer for files moved by the client.
    rows = []
    for modified, file, flags in heapq.nlargest(limit * 2, candidates()):
        try:
            headers = maildir_headers(file)
        except FileNotFoundError:
            continue
        rows.append({
            "subject": str(headers.get("Subject", "")).strip() or "(No subject)",
            "sender": str(headers.get("From") or ""),
            "received": datetime.fromtimestamp(modified, timezone.utc).isoformat(),
            "folder": path.name,
            "unread": "S" not in flags,
            "flagged": "F" in flags,
        })
        if len(rows) == limit:
            break
    return rows


def read(kind, path, first_day, last_day, limit=5):
    start, end = midnight(first_day), midnight(last_day)
    if kind == "mail":
        return read_maildir(path, start, end, limit)
    records = local_workflows.read_records(str(path), "calendar", exclude_canceled=True)
    return sorted(
        (row for row in records
         if local_workflows.timestamp(row["start"]) < end
         and local_workflows.timestamp(row["end"]) > start),
        key=lambda row: local_workflows.timestamp(row["start"]),
    )


def register(commands):
    command = commands.add_parser("outlook", help="Read metadata from a configured local Outlook source")
    command.add_argument("kind", choices=KINDS)
    command.add_argument("--date", type=date.fromisoformat, help="Focus date (YYYY-MM-DD)")
    command.add_argument("--days", type=int, default=7, help="Calendar days forward or mail days back, including focus date")
    command.add_argument("--limit", type=int, help="Number of unread or flagged mail items (default 5)")


def review(args, profile):
    source = sources(profile).get(args.kind)
    if source is None:
        raise ValueError(f"Enable and configure a local Outlook {args.kind} source in the profile.")
    if not 1 <= args.days <= 31:
        raise ValueError("Use --days between 1 and 31.")
    if args.limit is not None and (args.kind != "mail" or not 1 <= args.limit <= 50):
        raise ValueError("Use --limit between 1 and 50 for mail.")
    focus = args.date or date.today()
    try:
        if args.kind == "mail":
            start, end = focus - timedelta(days=args.days - 1), focus + timedelta(days=1)
        else:
            start, end = focus, focus + timedelta(days=args.days)
    except OverflowError:
        raise ValueError("Choose a date range within the supported calendar.") from None
    return {"kind": args.kind, "provider": FILE_PROVIDER, "window_start": str(start),
            "window_end": str(end), "records": read(args.kind, source, start, end, args.limit or 5)}
