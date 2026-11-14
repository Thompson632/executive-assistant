from datetime import date, datetime, timedelta
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_vault_workflow import LAUNCHER

sys.path.insert(0, str(LAUNCHER.parent))
import outlook


class LocalOutlookTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.vault = self.root / "Vault"
        self.profile = self.root / "profile.json"
        self.maildir = self.root / "Synced Inbox"
        self.calendar = self.root / "synced-calendar.json"
        self.day = date(2026, 11, 2)
        self.command("setup", "--vault", str(self.vault))
        for folder in ("cur", "new", "tmp"):
            (self.maildir / folder).mkdir(parents=True)

    def command(self, *args, check=True):
        return subprocess.run(
            [str(LAUNCHER), "--profile", str(self.profile), *args],
            capture_output=True, text=True, check=check,
        )

    def configure(self, **options):
        profile = json.loads(self.profile.read_text())
        profile["outlook"] = {"enabled": True, "provider": "local", **options}
        self.profile.write_text(json.dumps(profile))

    def create_message(self, name, hour, subject, day_offset=0):
        message = self.maildir / name
        message.write_bytes(
            b"From: Example <person@example.invalid>\r\nSubject: " + subject
            + b"\r\nMessage-ID: <opaque-id@example.invalid>\r\n\r\nPrivate body marker\r\n"
        )
        stamp = outlook.midnight(self.day + timedelta(days=day_offset)).timestamp() + hour * 3600
        os.utime(message, (stamp, stamp))

    def create_calendar(self, title="Planning"):
        start = outlook.midnight(self.day)
        end = outlook.midnight(self.day + timedelta(days=1))
        rows = [
            {"title": title, "start": (start - timedelta(hours=1)).isoformat(),
             "end": (start + timedelta(hours=1)).isoformat()},
            {"title": "Secret appointment", "start": start.isoformat(), "end": end.isoformat(),
             "description": "Secret body", "private": True},
            {"title": "Ends at window start", "start": (start - timedelta(hours=1)).isoformat(),
             "end": start.isoformat()},
            {"title": "Starts at window end", "start": end.isoformat(),
             "end": (end + timedelta(hours=1)).isoformat()},
        ]
        self.calendar.write_text(json.dumps(rows))

    def test_mail_metadata_is_bounded_current_and_read_only(self):
        self.configure(maildir=str(self.maildir))
        self.create_message("new/MailSyncHost", 11, b"=?utf-8?q?Project_=E2=9C=93?=")
        self.create_message("cur/two:2,FS", 10, b"Flagged")
        self.create_message("cur/three:2,S", 12, b"Already read")
        self.create_message("cur/four:2,T", 12, b"Deleted")
        self.create_message("tmp/five", 13, b"Still syncing")
        self.create_message("new/six", 12, b"Previous day", day_offset=-1)
        (self.maildir / "new" / "symlink").symlink_to(self.maildir / "tmp" / "five")
        first = self.command("outlook", "mail", "--date", str(self.day), "--days", "1")
        payload = json.loads(first.stdout)
        self.assertEqual([row["subject"] for row in payload["records"]], ["Project ✓", "Flagged"])
        self.assertTrue(payload["records"][0]["unread"])
        self.assertTrue(payload["records"][1]["flagged"])
        self.assertFalse(payload["records"][1]["unread"])
        self.assertNotIn("Private body marker", first.stdout)
        self.assertNotIn("opaque-id", first.stdout)
        self.assertTrue((self.maildir / "new" / "MailSyncHost").is_file())
        self.create_message("new/seven", 14, b"Just synced")
        result = self.command("outlook", "mail", "--date", str(self.day), "--limit", "1")
        self.assertEqual([row["subject"] for row in json.loads(result.stdout)["records"]],
                         ["Just synced"])

    def test_calendar_window_privacy_and_report_refresh(self):
        self.configure(calendarFile=str(self.calendar), maildir=str(self.maildir))
        self.create_message("new/one", 11, b"[Markdown link](https://example.invalid)")
        self.create_calendar()
        result = self.command("outlook", "calendar", "--date", str(self.day), "--days", "1")
        self.assertEqual([row["title"] for row in json.loads(result.stdout)["records"]],
                         ["Planning", "Private event"])
        self.assertNotIn("Secret appointment", result.stdout)
        self.assertNotIn("Secret body", result.stdout)
        result = self.command("report", "daily", "--date", str(self.day), "--write")
        path = Path(json.loads(result.stdout)["output_path"])
        original = path.read_text()
        self.assertIn("Planning", original)
        self.assertIn("Private event", original)
        self.assertIn(r"\[Markdown link\](https://example.invalid)", original)
        self.create_calendar("Rescheduled")
        updated = self.command("report", "daily", "--date", str(self.day)).stdout
        self.assertIn("Rescheduled", updated)
        self.assertEqual(path.read_text(), original)
        self.command("report", "daily", "--date", str(self.day), "--write", "--replace")
        self.assertIn("Rescheduled", path.read_text())
        weekly = self.command("report", "weekly", "--date", str(self.day)).stdout
        self.assertIn("Starts at window end", weekly)

    def test_missing_source_is_a_failure_not_an_empty_report(self):
        self.assertNotEqual(self.command("outlook", "mail", check=False).returncode, 0)
        self.configure(calendarFile=str(self.calendar))
        result = self.command("report", "daily", "--write", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertFalse((self.vault / "_briefings").exists())
        self.calendar.write_text("[]")
        report = self.command("report", "daily").stdout
        self.assertIn("No events returned", report)
        self.assertIn("Live mail is unavailable", report)
        self.assertEqual(json.loads(self.command("check").stdout)["outlook_sources"],
                         {"calendar": "local"})


class AppleOutlookTest(unittest.TestCase):
    def test_old_profile_needs_an_explicit_local_source(self):
        self.assertEqual(outlook.sources({"outlook": {
            "enabled": True, "mailboxName": "old", "protocolName": "ea-outlook",
        }}), {})

    def test_adapter_invokes_fixed_script_and_allows_only_metadata(self):
        start = datetime.fromisoformat("2026-11-02T00:00:00-05:00")
        end = start + timedelta(days=1)
        record = {"title": "Calendar event", "start": start.isoformat(), "end": end.isoformat(),
                  "all_day": True, "notes": "private", "uid": "opaque"}
        reply = subprocess.CompletedProcess([], 0, stdout=json.dumps([record]).encode(), stderr=b"")
        with patch.object(outlook.subprocess, "run", return_value=reply) as run:
            rows = outlook.read_apple("calendar", {"calendarName": "Work"}, start, end, 5)
        args = run.call_args.args[0]
        self.assertEqual(args[:4], ["/usr/bin/osascript", "-l", "JavaScript", str(outlook.APPLE_SCRIPT)])
        self.assertEqual(json.loads(args[-1])["calendarName"], "Work")
        self.assertEqual(rows, [{key: record[key] for key in ("title", "start", "end", "all_day")}])
        self.assertEqual(run.call_args.kwargs["timeout"], 30)

    def test_adapter_reports_automation_denial_without_private_error_details(self):
        start = datetime.fromisoformat("2026-11-02T00:00:00-05:00")
        failure = subprocess.CalledProcessError(1, [], stderr=b"Hidden calendar name (-1743)")
        with patch.object(outlook.subprocess, "run", side_effect=failure):
            with self.assertRaisesRegex(ValueError, "^Allow your terminal or Codex"):
                outlook.read_apple("calendar", {}, start, start + timedelta(days=1), 5)
