"""Generate local scheduler configuration and standalone Codex prompts."""

from pathlib import Path
import plistlib
import re
import shlex
import sys


WEEKDAYS = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
PROMPTS = (
    ("dailyBrief", "Daily Brief", "$executive-daily-brief", "daily"),
    ("weeklyReview", "Weekly Review", "$executive-weekly-review", "weekly"),
    ("followUpMonitor", "Follow-Up Monitor", "$executive-action-triage", "follow-up monitoring"),
    ("actionUpdate", "Action Update", "$executive-action-triage", "an action update"),
)


def time_parts(value):
    if not isinstance(value, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
        raise ValueError("Use HH:MM in 24-hour local time.")
    return tuple(map(int, value.split(":")))


def schedule(args, profile, script):
    hour, minute = time_parts(args.at)
    if args.weekday and args.type == "daily":
        raise ValueError("--weekday applies to weekly reports.")
    day = WEEKDAYS.index(args.weekday or "Monday") if args.type == "weekly" else None
    label = f"local.executive-assistant.{args.type}"
    command = [sys.executable, str(script), "--profile", str(profile),
               "report", args.type, "--write"]
    log = str(profile.parent / f"{label}.log")
    scheduler = args.format or ("launchd" if sys.platform == "darwin" else "cron")
    if scheduler == "cron":
        if any(any(ch in value for ch in "%\n\r") for value in [*command, log]):
            raise ValueError("Cron paths must not contain a percent sign or line break.")
        cron_day = "*" if day is None else day
        print(f"{minute} {hour} * * {cron_day} umask 077; {shlex.join(command)} >> {shlex.quote(log)} 2>&1")
        return

    interval = {"Hour": hour, "Minute": minute}
    if day is not None:
        interval["Weekday"] = day
    agent = {
        "Label": label,
        "ProgramArguments": command,
        "StartCalendarInterval": interval,
        "StandardOutPath": log,
        "StandardErrorPath": str(profile.parent / f"{label}.error.log"),
        "Umask": 0o077,
    }
    sys.stdout.buffer.write(plistlib.dumps(agent))


def schedule_prompts(profile: dict, path: Path) -> None:
    preferences = profile.get("scheduledTasks", {})
    if not isinstance(preferences, dict):
        raise ValueError("scheduledTasks must be a JSON object.")
    enabled = preferences.get("enabled", True)
    if not isinstance(enabled, bool):
        raise ValueError("scheduledTasks.enabled must be true or false.")

    default_enabled = "scheduledTasks" not in profile
    lines = ["# Executive Assistant Schedule Prompts", ""]
    for key, title, skill, purpose in PROMPTS:
        setting = preferences.get(key, {})
        field = f"scheduledTasks.{key}"
        if not isinstance(setting, dict):
            raise ValueError(f"{field} must be a JSON object.")
        entry_enabled = setting.get("enabled", default_enabled)
        if not isinstance(entry_enabled, bool):
            raise ValueError(f"{field}.enabled must be true or false.")
        if not enabled or not entry_enabled:
            continue

        day = setting.get("day") if key == "weeklyReview" else None
        if key == "weeklyReview" and "day" in setting and day not in WEEKDAYS:
            raise ValueError(f"{field}.day must be a weekday name such as Monday.")
        lines.extend([f"## {title}", ""])
        if "time" in setting:
            try:
                time_parts(setting["time"])
            except ValueError as error:
                raise ValueError(f"{field}.time: {error}") from None
            when = f"{day} at " if day else ""
            lines.extend([f"Preferred time {when}{setting['time']} (local).", ""])
        lines.extend([
            f'Use {skill} with profile "{path}" in its vault project for {purpose}.',
            "Run as a standalone scheduled task. Keep the no-autosend boundary and "
            "leave external systems unchanged unless the user approves the specific change.",
        ])
        if key in ("dailyBrief", "weeklyReview"):
            lines.append("Write the report to the configured vault.")
        lines.append("")
    print("\n".join(lines))
