#!/usr/bin/env python3
"""Run Executive Assistant workflows against a local Markdown vault."""

import argparse
from datetime import date, datetime, timedelta, timezone
import heapq
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
from typing import NamedTuple
from urllib.parse import quote

import local_workflows
import outlook
import schedules


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
REPORT_TYPES = ("daily", "weekly")
CUES = (
    ("blocked", r"\bblocked\b", 5),
    ("risk", r"\brisks?\b", 4),
    ("deadline", r"\bdeadlines?\b", 4),
    ("due", r"\bdue\b", 3),
    ("waiting", r"\bwaiting\b", 3),
    ("review requested", r"\breview requested\b", 3),
    ("open question", r"\bopen questions?\b", 2),
    ("follow-up", r"\bfollow[ -]ups?\b", 2),
)
CHECKBOX = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+\[(.)\]\s+")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
CAPTURE_DATE = re.compile(r"^#{1,6}\s+(\d{4}-\d{2}-\d{2})\s*$")


class Signal(NamedTuple):
    score: int
    modified: float
    path: str
    line: int
    kind: str
    excerpt: str


def profile_path(override):
    if override:
        return local_workflows.local_path(override).absolute()
    codex_home = local_workflows.local_path(os.environ.get("CODEX_HOME") or "~/.codex")
    return (codex_home / "executive-assistant" / "profiles" / "default.json").absolute()


def read_profile(path: Path) -> dict:
    try:
        text = local_workflows.read_input(path)
    except FileNotFoundError:
        raise ValueError(f"Profile missing at {path}. Run setup --vault /path/to/vault.") from None
    except UnicodeDecodeError:
        raise ValueError(f"Save the JSON profile as UTF-8: {path}") from None
    except ValueError:
        raise ValueError(f"Choose a regular JSON profile file: {path}") from None
    profile = json.loads(text)
    if not isinstance(profile, dict) or not isinstance(profile.get("vaultPath"), str):
        raise ValueError(f"Profile must contain a vaultPath string: {path}")
    return profile


def get_vault(profile, create=False):
    vault = local_workflows.local_path(profile["vaultPath"])
    if not vault.is_absolute():
        raise ValueError(f"Set vaultPath to an absolute folder: {vault}")
    vault = vault.resolve()
    if vault == PLUGIN_ROOT or PLUGIN_ROOT in vault.parents:
        raise ValueError("Choose a vault folder outside the plugin package.")
    if any(
        (folder / "plugins" / "executive-assistant" / ".codex-plugin" / "plugin.json").is_file()
        for folder in (vault, *vault.parents)
    ):
        raise ValueError("Choose a vault folder outside the package repository.")
    if create:
        vault.mkdir(parents=True, exist_ok=True)
    if not vault.is_dir():
        raise ValueError(f"Vault folder does not exist: {vault}")
    return vault


def write_file(path, content, replace=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Publish a complete file so Obsidian and concurrent runs never see a partial write.
    with NamedTemporaryFile(dir=path.parent, prefix=".ea-", delete=False) as temporary:
        temporary_path = Path(temporary.name)
        try:
            with temporary:
                temporary.write(content)
            if replace:
                temporary_path.replace(path)
            else:
                os.link(temporary_path, path)
        finally:
            temporary_path.unlink(missing_ok=True)


def setup(args, path):
    if path.exists() or path.is_symlink():
        raise ValueError(f"Profile already exists at {path}. Use config to change the vault.")
    vault = local_workflows.local_path(args.vault).resolve()
    profile = {
        "schemaVersion": 2,
        "profileName": "default",
        "vaultPath": str(vault),
        "timeZoneId": "Local",
        "obsidian": {"enabled": True},
        "outlook": {"enabled": False, "autoSend": False},
        "atlassian": {"enabled": False},
    }
    get_vault(profile, create=True)
    if args.copy_template:
        template = PLUGIN_ROOT / "assets" / "vault-template"
        for source in sorted(template.rglob("*")):
            if not source.is_file():
                continue
            destination = vault / source.relative_to(template)
            if destination.resolve() != destination:
                raise ValueError(f"Template destination uses a symlink: {destination}")
            if source.name == ".gitkeep":
                destination.parent.mkdir(parents=True, exist_ok=True)
                continue
            try:
                write_file(destination, source.read_bytes())
            except FileExistsError:
                continue
    write_file(path, (json.dumps(profile, indent=2) + "\n").encode("utf-8"))
    show_status(path, vault, profile)


def show_status(path: Path, vault: Path, profile: dict) -> None:
    status = {
        "ok": True,
        "profile_path": str(path),
        "vault_path": str(vault),
        "obsidian_settings_present": (vault / ".obsidian").is_dir(),
    }
    try:
        sources = outlook.sources(profile)
    except ValueError as error:
        sources = {}
        status["outlook_error"] = str(error)
    status["outlook_available"] = bool(sources)
    status["outlook_sources"] = dict.fromkeys(sources, outlook.FILE_PROVIDER)
    print(json.dumps(status, indent=2))


def configure(args, path, profile):
    if not args.vault:
        if args.apply:
            raise ValueError("--apply requires --vault.")
        show_status(path, get_vault(profile), profile)
        return
    vault = get_vault({"vaultPath": str(local_workflows.local_path(args.vault).resolve())})
    if args.apply:
        profile["vaultPath"] = str(vault)
        if isinstance(profile.get("obsidian"), dict) and "vaultPath" in profile["obsidian"]:
            profile["obsidian"]["vaultPath"] = str(vault)
        write_file(path, (json.dumps(profile, indent=2) + "\n").encode("utf-8"), replace=True)
        show_status(path, vault, profile)
    else:
        print(json.dumps({
            "profile_path": str(path),
            "current_vault_path": profile["vaultPath"],
            "proposed_vault_path": str(vault),
        }, indent=2))


def note_signals(vault, path, modified, capture_days, brain_dumps):
    relative = path.relative_to(vault).as_posix()
    capture_note = capture_days and path.relative_to(vault).parts[0].casefold() == "notes"
    quick_notes = capture_note and relative.casefold() == "notes/quick notes.md"
    capture_day = datetime.fromtimestamp(modified).date().isoformat() if capture_note else ""
    if quick_notes:
        capture_day = ""
    captured_excerpt = False
    fence = None
    in_frontmatter = False
    with path.open(encoding="utf-8-sig", errors="replace") as note:
        for number, line in enumerate(note, start=1):
            stripped = line.strip()
            if number == 1 and stripped == "---":
                in_frontmatter = True
                continue
            if in_frontmatter:
                key, _, value = stripped.partition(":")
                if key == "type" and value.strip().strip("'\"") in {
                    "executive-assistant-draft",
                    "executive-assistant-one-on-one",
                }:
                    return
                in_frontmatter = stripped not in ("---", "...")
                continue
            marker = FENCE.match(line)
            if fence:
                if marker and marker[1].startswith(fence) and not marker[2].strip():
                    fence = None
                continue
            if marker:
                fence = marker[1]
                continue
            checkbox = CHECKBOX.match(line)
            if checkbox and checkbox[1] != " ":
                continue
            if quick_notes and stripped.startswith("#"):
                heading = CAPTURE_DATE.fullmatch(stripped)
                if heading:
                    capture_day = heading[1]
            if not stripped or stripped.startswith("#"):
                continue
            excerpt = " ".join(stripped.split())[:220]
            if (capture_note and capture_day in capture_days and not checkbox
                    and (quick_notes or not captured_excerpt)):
                brain_dumps.append(Signal(0, modified, relative, number, capture_day, excerpt))
                captured_excerpt = True
            for kind, pattern, score in CUES:
                if re.search(pattern, stripped, re.IGNORECASE):
                    break
            else:
                if not checkbox:
                    continue
                kind, score = "open checkbox", 4
            yield Signal(score, modified, relative, number, kind, excerpt)


def vault_signals(vault, capture_days, brain_dumps):
    def candidates():
        def fail(error):
            raise error

        for directory, folders, files in os.walk(vault, onerror=fail):
            root = Path(directory)
            folders[:] = [
                name for name in folders
                if not name.startswith(".")
                and name.casefold() not in {"_briefings", "_setup"}
                and not (root / name).is_symlink()
                and (root / name).relative_to(vault).as_posix().casefold() != "inbox/outlook"
            ]
            for filename in files:
                path = root / filename
                if filename.startswith(".") or path.suffix.casefold() != ".md" or path.is_symlink():
                    continue
                if path.is_file():
                    yield from note_signals(vault, path, path.stat().st_mtime,
                                            capture_days, brain_dumps)

    now = datetime.now().timestamp()

    def rank(signal):
        age = (now - signal.modified) / 86400
        recent = 4 if age <= 3 else 2 if age <= 14 else -2 if age > 90 else 0
        return (-(signal.score + recent), -signal.modified, signal.path, signal.line)

    return heapq.nsmallest(30, candidates(), key=rank)


def markdown_text(value):
    return re.sub(r"([\\`*_\[\]<>!&~])", r"\\\1", value)


def signal_lines(signals, empty, report_folder):
    lines = []
    for signal in signals:
        label = markdown_text(Path(signal.path).stem)
        target = quote(os.path.relpath(signal.path, report_folder))
        excerpt = markdown_text(signal.excerpt)
        lines.append(f"- [{label}]({target}) · line {signal.line} · {signal.kind} · {excerpt}")
    return lines or [f"- {empty}"]


def outlook_lines(sources, kind, start, end):
    if kind not in sources:
        return f"- Live {kind} is unavailable. No local Outlook {kind} source is configured."
    records = outlook.read(kind, sources[kind], start, end, limit=10)
    if kind == "mail":
        lines = []
        for row in records:
            label = "Unread" if row["unread"] else "Read"
            if row["flagged"]:
                label += ", flagged"
            metadata = " · ".join(filter(None, (row["subject"], row["sender"], label)))
            lines.append("- " + markdown_text(" ".join(metadata.split())))
        return "\n".join(lines) or "- No recent unread or flagged messages in the configured folder."
    lines = []
    for row in records:
        begins = local_workflows.timestamp(row["start"]).astimezone()
        ends = local_workflows.timestamp(row["end"]).astimezone()
        window = f"{begins:%a %H:%M} to {ends:%a %H:%M}"
        if row.get("all_day"):
            last_day = (ends - timedelta(microseconds=1)).date()
            window = f"{begins:%a} · All day" if last_day == begins.date() else (
                f"{begins:%a} to {last_day:%a} · All day"
            )
        lines.append(f"- {window} · " + markdown_text(" ".join(row["title"].split())))
    return "\n".join(lines) or "- No events returned by the configured calendar in this window."


def render_report(report_type, focus, monday, signals, report_folder, sources, brain_dumps):
    weekly = report_type == "weekly"
    start = monday if weekly else focus
    end = start + timedelta(days=7 if weekly else 1)
    heading = f"Weekly Report - Week of {monday}" if weekly else f"Daily Report - {focus}"
    period = "This Week" if weekly else "Today"
    waiting = [signal for signal in signals if signal.kind == "waiting"]
    risks = [signal for signal in signals if signal.kind in {"risk", "blocked", "deadline", "due"}]
    attention = [signal for signal in signals if signal.kind != "waiting"]
    sections = [
        f"## Snapshot\n\n- {len(signals)} vault attention signals surfaced.",
        f"## Calendar {period}\n\n" + outlook_lines(sources, "calendar", start, end),
        "## Important Unread Emails\n\n" + outlook_lines(
            sources, "mail", focus - timedelta(days=6), focus + timedelta(days=1),
        ),
        f"## Needs Attention {period}\n\n" + "\n".join(
            signal_lines(attention[:12], "No open actions or attention signals surfaced.", report_folder)
        ),
        "## Waiting On\n\n" + "\n".join(signal_lines(waiting[:10], "No waiting items surfaced.", report_folder)),
        "## Risks To Watch\n\n" + "\n".join(signal_lines(risks[:10], "No risk or due items surfaced.", report_folder)),
    ]
    if not weekly:
        captures = sorted(brain_dumps, key=lambda item: (item.kind, item.modified), reverse=True)
        sections.append("## Brain Dumps\n\n" + "\n".join(
            signal_lines(captures, "No brain dumps captured today or yesterday.", report_folder)
        ))
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    metadata = (
        "---\n"
        "type: executive-assistant-report\n"
        f'report_type: "{report_type.title()}"\n'
        f'generated: "{generated}"\n'
        f'window_start: "{start}"\n'
        f'window_end: "{end}"\n'
        f"source: {'vault-and-local-outlook' if sources else 'vault'}\n"
        "---\n"
    )
    return metadata + f"\n# {heading}\n\n" + "\n\n".join(sections) + "\n"


def report(args, vault, profile):
    if args.replace and not args.write:
        raise ValueError("--replace requires --write.")
    focus = args.date or date.today()
    monday = focus - timedelta(days=focus.weekday())
    file_date = monday if args.type == "weekly" else focus
    path = vault / "_briefings" / monday.strftime("%Y-%m") / f"Week of {monday}" / (
        f"{file_date} {args.type.title()} Report.md"
    )
    report_folder = path.parent.relative_to(vault)
    capture_days = ()
    if args.type == "daily":
        capture_days = (focus.isoformat(), (focus - timedelta(days=1)).isoformat())

    def render():
        brain_dumps = []
        signals = vault_signals(vault, capture_days, brain_dumps)
        return render_report(args.type, focus, monday, signals, report_folder,
                             outlook.sources(profile), brain_dumps)

    if not args.write:
        print(render(), end="")
        return
    if path.resolve() != path:
        raise ValueError(f"Report destination uses a symlink: {path}")
    status = "existing"
    if args.replace or not path.exists():
        content = render()
        try:
            write_file(path, content.encode("utf-8"), replace=args.replace)
            status = "written"
        except FileExistsError:
            if not path.is_file():
                raise
    elif not path.is_file():
        raise ValueError(f"Report path is occupied by a folder: {path}")
    print(json.dumps({"status": status, "output_path": str(path)}))


def apply_local_file(args, path, vault):
    operation = args.command
    try:
        if operation == "draft":
            destination = local_workflows.destination_path(vault, args.output)
            draft = local_workflows.DRAFT_HEADER + local_workflows.draft_text(args)
            write_file(destination, draft.encode("utf-8"))
        else:
            if args.confirm_save != "SAVE ATTACHMENTS":
                raise ValueError('Apply requires --confirm-save "SAVE ATTACHMENTS".')
            destination = local_workflows.destination_path(vault, args.destination)
            local_workflows.write_attachment(local_workflows.local_path(args.source), destination)
    except (OSError, ValueError):
        try:
            local_workflows.append_audit(path, operation, "failed")
        except (OSError, ValueError):
            print("The local audit log could not be updated.", file=sys.stderr)
        raise
    try:
        local_workflows.append_audit(path, operation, "written")
    except (OSError, ValueError):
        print("The file was saved, but the local audit log could not be updated.", file=sys.stderr)
    print(json.dumps({"status": "written", "output_path": str(destination)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", help="Override the default local profile path")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("setup", help="Connect a new or existing vault")
    create.add_argument("--vault", required=True, help="Path to the vault folder")
    create.add_argument("--copy-template", action="store_true", help="Add missing starter notes")
    config = commands.add_parser("config", help="Inspect or update the vault connection")
    config.add_argument("--vault", help="Preview a change to an existing vault")
    config.add_argument("--apply", action="store_true", help="Save the previewed change")
    commands.add_parser("check", help="Verify the local vault connection without writing")
    briefing = commands.add_parser("report", help="Preview or save a daily or weekly report")
    briefing.add_argument("type", choices=REPORT_TYPES)
    briefing.add_argument("--date", type=date.fromisoformat, help="Focus date (YYYY-MM-DD)")
    briefing.add_argument("--write", action="store_true", help="Save a report to the vault")
    briefing.add_argument("--replace", action="store_true", help="Regenerate an existing report")
    scheduling = commands.add_parser("schedule", help="Print LaunchAgent or cron configuration")
    scheduling.add_argument("type", choices=REPORT_TYPES)
    scheduling.add_argument("--at", required=True, help="Local time (HH:MM)")
    scheduling.add_argument("--weekday", choices=schedules.WEEKDAYS, help="Weekly report day (default Monday)")
    scheduling.add_argument("--format", choices=("launchd", "cron"))
    commands.add_parser("schedule-prompts", help="Print standalone Codex schedule prompts")
    local_workflows.register(commands)
    outlook.register(commands)
    args = parser.parse_args()
    try:
        path = profile_path(args.profile)
        if args.command == "review":
            print(json.dumps(local_workflows.review(args), ensure_ascii=False, indent=2))
            return 0
        if args.command == "resolve":
            print(json.dumps({"exists": local_workflows.local_path(args.path).is_file()}))
            return 0
        if args.command == "draft":
            if args.apply != (args.output is not None):
                raise ValueError("Use --output and --apply together to save a draft.")
            if not args.apply:
                print(local_workflows.draft_text(args), end="")
                return 0
        if args.command == "setup":
            setup(args, path)
            return 0
        profile = read_profile(path)
        if args.command == "outlook":
            print(json.dumps(outlook.review(args, profile), ensure_ascii=False, indent=2))
            return 0
        if args.command == "check":
            vault = get_vault(profile)
            with os.scandir(vault) as entries:
                next(entries, None)
            show_status(path, vault, profile)
            return 0
        if args.command == "config":
            configure(args, path, profile)
            return 0
        if args.command == "audit":
            print(json.dumps(local_workflows.read_audit(path)))
            return 0
        vault = get_vault(profile)
        if args.command == "attachment" and not args.apply:
            source = local_workflows.local_path(args.source)
            if not source.is_file():
                raise ValueError("Choose an existing local attachment file.")
            destination = local_workflows.destination_path(vault, args.destination)
            print(json.dumps({"status": "preview", "source": str(source), "destination": str(destination)}))
        elif args.command in local_workflows.OPERATIONS:
            apply_local_file(args, path, vault)
        elif args.command == "report":
            report(args, vault, profile)
        elif args.command == "schedule-prompts":
            schedules.schedule_prompts(profile, path)
        elif args.command == "schedule":
            schedules.schedule(args, path, Path(__file__).resolve())
    except (OSError, ValueError, OverflowError) as error:
        print(f"Executive Assistant: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
