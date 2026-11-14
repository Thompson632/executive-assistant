"""Read Outlook metadata from locally synced clients and files."""

from datetime import date, datetime, time, timedelta, timezone
from email import policy
from email.parser import BytesHeaderParser
import heapq
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

import local_workflows


KINDS = ("mail", "calendar")
APPLE_SCRIPT = Path(__file__).with_name("outlook-apple.js")


def sources(profile):
    settings = profile.get("outlook")
    if not isinstance(settings, dict) or settings.get("enabled") is not True:
        return {}
    provider = settings.get("provider")
    if provider is None and ("protocolName" in settings or "mailboxName" in settings):
        # Profiles imported from the former Outlook runtime require a new source.
        return {}
    result = {}
    if provider == "apple":
        if sys.platform != "darwin":
            raise ValueError("The apple Outlook provider requires macOS.")
        names = (("mail", ("mailAccount", "mailFolder")), ("calendar", ("calendarName",)))
    elif provider == "local":
        names = (("mail", ("maildir",)), ("calendar", ("calendarFile",)))
    else:
        raise ValueError("Set outlook.provider to apple or local in the local profile.")
    for kind, keys in names:
        if not any(key in settings for key in keys):
            continue
        values = {}
        for key in keys:
            value = settings.get(key)
            if not isinstance(value, str) or not value.strip() or "\x00" in value:
                raise ValueError(f"Set outlook.{key} to a nonempty string.")
            if provider == "local" and not local_workflows.local_path(value).is_absolute():
                raise ValueError(f"Set outlook.{key} to an absolute local path.")
            values[key] = value
        if provider == "apple" and kind == "calendar":
            show_titles = settings.get("includeCalendarTitles", False)
            if type(show_titles) is not bool:
                raise ValueError("Set outlook.includeCalendarTitles to true or false.")
            values["includeCalendarTitles"] = show_titles
        result[kind] = (provider, values)
    if not result:
        raise ValueError("Configure at least one Outlook mail or calendar source.")
    return result


def midnight(day):
    # Resolve each boundary in the host zone so windows spanning a clock change work.
    return datetime.combine(day, time.min).astimezone()


def read_apple(kind, settings, start, end, limit):
    args = {**settings, "start": start.isoformat(), "end": end.isoformat(), "limit": limit}
    app = "Mail" if kind == "mail" else "Calendar"
    try:
        result = subprocess.run(
            ["/usr/bin/osascript", "-l", "JavaScript", str(APPLE_SCRIPT), kind, json.dumps(args)],
            capture_output=True, check=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        raise ValueError(f"Apple {app} did not respond. Check that it is open and responsive.") from None
    except subprocess.CalledProcessError as error:
        # Only forward our fixed diagnostic strings. App error messages can contain account data.
        stderr = error.stderr.decode(errors="replace")
        if "EA_SELECTION" in stderr:
            raise ValueError(f"Apple {app} needs one exact match for the configured source.") from None
        if "EA_NOT_RUNNING" in stderr:
            raise ValueError(f"Open Apple {app} before reading its local data.") from None
        if "-1743" in stderr:
            raise ValueError(
                f"Allow your terminal or Codex to control Apple {app} in macOS Automation settings."
            ) from None
        raise ValueError(f"Apple {app} could not be read. Check its local source and Automation access.") from None
    return local_workflows.validate_records(json.loads(result.stdout), kind)


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


def read(kind, source, first_day, last_day, limit=5):
    provider, settings = source
    start, end = midnight(first_day), midnight(last_day)
    if provider == "apple":
        records = read_apple(kind, settings, start, end, limit)
    elif kind == "mail":
        return read_maildir(local_workflows.local_path(settings["maildir"]), start, end, limit)
    else:
        records = local_workflows.read_records(settings["calendarFile"], "calendar")
    if kind == "mail":
        return records
    return sorted(
        (row for row in records
         if local_workflows.timestamp(row["start"]) < end
         and local_workflows.timestamp(row["end"]) > start
         and row.get("status", "").casefold() not in {"canceled", "cancelled"}),
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
    return {"kind": args.kind, "provider": source[0], "window_start": str(start),
            "window_end": str(end), "records": read(args.kind, source, start, end, args.limit or 5)}
