import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_vault_workflow import SCRIPT


class LocalWorkflowTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.profile = self.root / "profiles" / "test.json"
        self.vault = self.root / "Vault"

    def command(self, *args, check=True):
        return subprocess.run([sys.executable, str(SCRIPT), "--profile", str(self.profile), *args],
                              capture_output=True, check=check, timeout=5)

    def fixture(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return str(path)

    def test_unknown_home_in_metadata_source_has_a_path_error(self):
        result = self.command("review", "tasks", "--source", "~ea-no-such-user-8731/Notes", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"Use an absolute local path or ~ for your home folder.", result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_mail_projects_metadata_and_pages_five(self):
        rows = [{"subject": str(index), "body": "private", "id": "secret",
                 "received": "2026-11-14T09:00:00-05:00", "folder": "Inbox"}
                for index in range(8)]
        rows.insert(1, {"subject": "other", "folder": "Sent"})
        rows.insert(2, {"subject": "old", "folder": "Inbox",
                        "received": "2026-11-13T09:00:00-05:00"})
        result = json.loads(self.command("review", "mail", "--source", self.fixture("mail.json", rows),
                                         "--folder", "Inbox", "--since", "2026-11-14T08:00:00-05:00",
                                         "--offset", "2").stdout)
        self.assertEqual([item["subject"] for item in result["records"]], list("23456"))
        self.assertNotIn("body", result["records"][0])
        self.assertNotIn("id", result["records"][0])
        self.assertFalse(self.profile.exists())

    def test_calendar_batches_and_rejects_bad_dates(self):
        private = {"title": "Secret", "start": "2026-11-14T10:00:00Z",
                   "end": "2026-11-14T11:00:00Z", "private": True,
                   "status": "Canceled", "location": "Secret room"}
        empty = self.fixture("empty.json", [])
        source = self.fixture("calendar.json", [private])
        comparison = json.loads(self.command("review", "calendar", "--source", source,
                                              "--compare", empty).stdout)
        self.assertEqual(comparison["comparison_records"], [])
        self.assertEqual(comparison["records"][0], {
            "title": "Private event", "start": private["start"], "end": private["end"]
        })
        private["start"] = "impossible"
        source = self.fixture("calendar.json", [private])
        self.assertNotEqual(self.command("review", "calendar", "--source", source,
                                         check=False).returncode, 0)
        tasks = self.fixture("tasks.json", [{"title": "Task", "priority": "high", "notes": "Private"}])
        self.assertEqual(json.loads(self.command("review", "tasks", "--source", tasks).stdout)["records"],
                         [{"title": "Task", "priority": "high"}])

    def test_draft_preview_and_apply_preserve_no_send(self):
        self.command("setup", "--vault", str(self.vault))
        source = self.root / "body.txt"
        source.write_text("Waiting on fixture-private-body\n", encoding="utf-8")
        draft = self.vault / "Draft.md"
        args = ("draft", "--subject", "Reply", "--source", str(source))
        self.assertIn(b"fixture-private-body", self.command(*args).stdout)
        self.assertFalse(draft.exists())
        self.assertNotEqual(self.command(*args, "--output", str(draft), check=False).returncode, 0)
        self.command(*args, "--output", str(draft), "--apply")
        self.assertEqual(draft.read_text(), "---\ntype: executive-assistant-draft\n---\n\n"
                         "# Reply\n\nWaiting on fixture-private-body\n")
        draft.write_text(draft.read_text().replace("type: executive-assistant-draft", "edited: true\ntype: \"executive-assistant-draft\""))
        report = self.command("report", "daily").stdout
        self.assertNotIn(b"Waiting on fixture-private-body", report)
        audit = self.profile.parent / "local-audit.jsonl"
        self.assertNotIn("fixture-private-body", audit.read_text())

    def test_attachment_cannot_escape_or_overwrite(self):
        self.command("setup", "--vault", str(self.vault))
        source = self.root / "source.txt"
        source.write_bytes(b"source")
        redirected = self.vault / "redirect"
        redirected.symlink_to(self.root, target_is_directory=True)
        existing = self.vault / "existing.txt"
        existing.write_bytes(b"keep")
        args = ("attachment", "--source", str(source), "--apply")
        self.assertNotEqual(self.command(*args, "--destination", str(existing), check=False).returncode, 0)
        self.assertNotEqual(self.command(*args, "--destination", str(existing),
                                         "--confirm-save", "SAVE ATTACHMENTS", check=False).returncode, 0)
        self.assertEqual(existing.read_bytes(), b"keep")
        self.assertNotEqual(self.command(*args, "--destination", str(redirected / "escape.txt"),
                                         "--confirm-save", "SAVE ATTACHMENTS", check=False).returncode, 0)
        self.assertFalse((self.root / "escape.txt").exists())
        copied = self.vault / "copied.txt"
        self.command(*args, "--destination", str(copied), "--confirm-save", "SAVE ATTACHMENTS")
        self.assertEqual(copied.read_bytes(), b"source")

    def test_attachment_preview_rejects_occupied_destinations(self):
        self.command("setup", "--vault", str(self.vault))
        source = self.root / "source.txt"
        source.write_bytes(b"new attachment")
        occupied = self.vault / "Existing.txt"
        occupied.write_bytes(b"keep this file")
        args = ("attachment", "--source", str(source), "--destination")
        apply = ("--apply", "--confirm-save", "SAVE ATTACHMENTS")

        for destination, diagnostic in (
            (occupied, b"Attachment destination already exists. Choose a new file."),
            (occupied / "child.txt", b"Attachment destination needs a folder as its parent."),
        ):
            with self.subTest(destination=destination):
                result = self.command(*args, str(destination), check=False)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(diagnostic, result.stderr)
        self.assertEqual(occupied.read_bytes(), b"keep this file")
        self.assertFalse((self.profile.parent / "local-audit.jsonl").exists())

        destination = self.vault / "New Folder" / "Saved.txt"
        preview = json.loads(self.command(*args, str(destination)).stdout)
        self.assertEqual(preview["status"], "preview")
        self.assertFalse(destination.parent.exists())
        self.command(*args, str(destination), *apply)
        self.assertEqual(destination.read_bytes(), source.read_bytes())

        conflict = self.vault / "Conflict.txt"
        self.command(*args, str(conflict))
        conflict.write_bytes(b"written after preview")
        result = self.command(*args, str(conflict), *apply, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(conflict.read_bytes(), b"written after preview")

    def test_local_commands_reject_named_pipes(self):
        self.command("setup", "--vault", str(self.vault))
        source = self.root / "input.fifo"
        os.mkfifo(source)
        target = self.vault / "output.txt"
        for args in (
            ("review", "mail", "--source", str(source)),
            ("draft", "--subject", "draft", "--source", str(source)),
            ("attachment", "--source", str(source), "--destination", str(target),
             "--apply", "--confirm-save", "SAVE ATTACHMENTS"),
        ):
            with self.subTest(command=args[0]):
                result = self.command(*args, check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(b"regular file", result.stderr)
                self.assertFalse(target.exists())

    def test_resolve_missing_file_and_audit_output(self):
        result = json.loads(self.command("resolve", "--path", str(self.root / "missing")).stdout)
        self.assertEqual(result, {"exists": False})
        self.assertNotEqual(self.command("resolve", "--path", "ea-outlook://open/token",
                                         check=False).returncode, 0)
        self.command("setup", "--vault", str(self.vault))
        self.assertEqual(json.loads(self.command("audit").stdout),
                         {"draft": {"written": 0, "failed": 0}, "attachment": {"written": 0, "failed": 0}})
