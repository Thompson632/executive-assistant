from datetime import datetime
import json
import os
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "plugins" / "executive-assistant" / "scripts" / "unix" / "ea.py"
)


LAUNCHER = SCRIPT.with_suffix(".sh")


class VaultWorkflowTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.vault = self.root / "Test Vault"
        self.profile = self.root / "profiles" / "test.json"

    def command(self, *args, check=True):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--profile", str(self.profile), *args],
            capture_output=True, check=check,
        )

    def test_launcher_preserves_spaces_and_exit_status(self):
        for shell in filter(None, (shutil.which("bash"), shutil.which("zsh"))):
            with self.subTest(shell=shell):
                name = Path(shell).name
                profile = self.root / f"{name} profile.json"
                vault = self.root / f"{name} vault"
                prefix = [shell, "-c", 'exec "$@"', shell, str(LAUNCHER), "--profile", str(profile)]
                result = subprocess.run(prefix + ["setup", "--vault", str(vault)],
                                        cwd=self.root, capture_output=True, check=True)
                self.assertEqual(json.loads(result.stdout)["vault_path"], str(vault))
                bad = subprocess.run(prefix + ["unknown"], cwd=self.root, capture_output=True)
                self.assertEqual(bad.returncode, 2)

    def test_migrated_profile_preserves_unrelated_fields(self):
        self.vault.mkdir()
        self.profile.parent.mkdir()
        original = {"vaultPath": "C:/old-vault", "obsidian": {"vaultPath": "C:/old-vault"},
                    "customValue": "keep-me"}
        self.profile.write_text(json.dumps(original))
        before = self.profile.read_bytes()
        self.command("config", "--vault", str(self.vault))
        self.assertEqual(self.profile.read_bytes(), before)
        self.command("config", "--vault", str(self.vault), "--apply")
        saved = json.loads(self.profile.read_bytes())
        self.assertEqual(saved["vaultPath"], str(self.vault))
        self.assertEqual(saved["obsidian"]["vaultPath"], str(self.vault))
        self.assertEqual(saved["customValue"], "keep-me")

    def test_check_is_read_only(self):
        self.command("setup", "--vault", str(self.vault))
        before = self.profile.read_bytes()
        status = json.loads(self.command("check").stdout)
        self.assertEqual(status["vault_path"], str(self.vault))
        self.assertEqual(status["profile_path"], str(self.profile))
        self.assertTrue(status["ok"])
        self.assertEqual(self.profile.read_bytes(), before)
        self.assertEqual(list(self.vault.iterdir()), [])

    def test_profile_fifo_returns_a_regular_file_error(self):
        self.profile.parent.mkdir()
        os.mkfifo(self.profile)
        result = subprocess.run(
            [str(LAUNCHER), "--profile", str(self.profile), "check"],
            capture_output=True, timeout=3,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"Choose a regular JSON profile file", result.stderr)

    def test_check_accepts_a_symlink_to_a_regular_profile(self):
        self.vault.mkdir()
        self.profile.parent.mkdir()
        target = self.root / "target.json"
        target.write_text(json.dumps({"vaultPath": str(self.vault)}), encoding="utf-8-sig")
        self.profile.symlink_to(target)
        self.assertEqual(json.loads(self.command("check").stdout)["vault_path"], str(self.vault))

    def test_vault_cannot_contain_the_executing_package(self):
        containing = self.root / "Containing Folder"
        plugin = containing / "executive-assistant"
        shutil.copytree(LAUNCHER.parents[2], plugin)
        launcher = plugin / LAUNCHER.relative_to(LAUNCHER.parents[2])

        def run(*args):
            return subprocess.run(
                [str(launcher), "--profile", str(self.profile), *args],
                capture_output=True, timeout=5,
            )

        diagnostic = b"Choose a notes folder separate from the Executive Assistant package."
        result = run("setup", "--vault", str(containing), "--copy-template")
        self.assertEqual(result.returncode, 1)
        self.assertIn(diagnostic, result.stderr)
        self.assertFalse(self.profile.exists())
        self.assertFalse((containing / "Action-Items.md").exists())

        self.profile.parent.mkdir()
        self.profile.write_text(json.dumps({"vaultPath": str(containing)}))
        original = self.profile.read_bytes()
        for args in (("check",), ("report", "daily", "--write")):
            with self.subTest(args=args):
                result = run(*args)
                self.assertEqual(result.returncode, 1)
                self.assertIn(diagnostic, result.stderr)
        self.assertFalse((containing / "_briefings").exists())
        sibling = self.root / "Sibling Notes"
        sibling.mkdir()
        self.assertEqual(run("config", "--vault", str(sibling)).returncode, 0)
        self.assertEqual(self.profile.read_bytes(), original)
        moved = run("config", "--vault", str(sibling), "--apply")
        self.assertEqual(moved.returncode, 0, moved.stderr)
        self.assertEqual(json.loads(moved.stdout)["vault_path"], str(sibling))
        self.assertEqual(run("report", "daily").returncode, 0)

    def test_unknown_home_in_profile_or_vault_has_a_path_error(self):
        missing = "~ea-no-such-user-8731/Notes"
        self.profile.parent.mkdir()
        bad_profile = self.root / "bad-vault.json"
        bad_profile.write_text(json.dumps({"vaultPath": missing}))
        self.vault.mkdir()
        self.profile.write_text(json.dumps({"vaultPath": str(self.vault)}))
        for args in (
            ("--profile", missing, "check"),
            ("--profile", str(self.root / "new.json"), "setup", "--vault", missing),
            ("--profile", str(self.profile), "config", "--vault", missing),
            ("--profile", str(bad_profile), "check"),
        ):
            with self.subTest(args=args):
                result = subprocess.run([str(LAUNCHER), *args], capture_output=True, timeout=3)
                self.assertEqual(result.returncode, 1)
                self.assertIn(b"Use an absolute local path or ~ for your home folder.", result.stderr)
                self.assertNotIn(b"Traceback", result.stderr)

    def test_setup_preserves_existing_notes_and_config_requires_apply(self):
        self.vault.mkdir()
        note = self.vault / "Action-Items.md"
        note.write_text("# Existing actions\n", encoding="utf-8")
        self.command("setup", "--vault", str(self.vault), "--copy-template")
        self.assertEqual(note.read_text(encoding="utf-8"), "# Existing actions\n")
        self.assertTrue((self.vault / "HOME.md").is_file())
        self.assertTrue((self.vault / "tasks" / "00-Inbox").is_dir())
        self.assertTrue((self.vault / "One-on-Ones.md").is_file())
        self.assertTrue((self.vault / "meetings" / "One-on-Ones").is_dir())
        self.assertTrue((self.vault / "templates" / "One-on-One.md").is_file())
        status = json.loads(self.command("config").stdout)
        self.assertEqual(status["vault_path"], str(self.vault))
        self.assertFalse(status["outlook_available"])
        self.assertNotEqual(
            self.command("setup", "--vault", str(self.vault), check=False).returncode, 0
        )

        other = self.root / "Other Vault"
        other.mkdir()
        original = self.profile.read_bytes()
        self.command("config", "--vault", str(other))
        self.assertEqual(self.profile.read_bytes(), original)
        self.command("config", "--vault", str(other), "--apply")
        self.assertEqual(json.loads(self.profile.read_bytes())["vaultPath"], str(other))

    def test_starter_vault_reports_only_real_actions(self):
        self.command("setup", "--vault", str(self.vault), "--copy-template")
        args = ("report", "daily", "--date", "2026-11-14")
        preview = self.command(*args).stdout.decode()
        self.assertIn("0 vault attention signals surfaced.", preview)

        actions = self.vault / "Action-Items.md"
        with actions.open("a", encoding="utf-8") as note:
            note.write("\n- [ ] Review the meeting agenda\n")
        payload = json.loads(self.command(*args, "--write").stdout)
        report = Path(payload["output_path"])
        self.assertTrue(report.is_file())
        content = report.read_text(encoding="utf-8")
        self.assertIn("Review the meeting agenda", content)
        link = re.search(r"\[Action-Items\]\(([^)]+)\)", content)
        self.assertIsNotNone(link)
        self.assertEqual((report.parent / unquote(link.group(1))).resolve(), actions)

    def test_reports_read_vault_notes_and_preserve_existing_report(self):
        self.command("setup", "--vault", str(self.vault))
        notes = self.vault / "Project Notes"
        notes.mkdir()
        (notes / "Decision (test).md").write_text(
            "- [ ] Review next week\n"
            "- [x] Completed risk review\n"
            "```md\n- [ ] Ignore sample task\n```\n"
            "- Waiting on the decision\n",
            encoding="utf-8",
        )
        (self.vault / ".obsidian").mkdir()
        (self.vault / ".obsidian" / "private.md").write_text("- [ ] Ignore settings\n")
        (self.vault / "External.md").symlink_to(self.profile)
        (notes / "Private 1-1.md").write_text(
            "---\ntype: executive-assistant-one-on-one\n---\n"
            "- [ ] Private follow-up from the meeting\n",
            encoding="utf-8",
        )

        date = "2026-11-01"
        preview = self.command("report", "daily", "--date", date).stdout.decode()
        self.assertFalse((self.vault / "_briefings").exists())
        self.assertIn("Review next week", preview)
        self.assertIn("Waiting on the decision", preview)
        self.assertIn("../../../Project%20Notes/Decision%20%28test%29.md", preview)
        self.assertIn("Live calendar is unavailable", preview)
        self.assertIn("Live mail is unavailable", preview)
        self.assertNotIn("Completed risk", preview)
        self.assertNotIn("Ignore", preview)
        self.assertNotIn("Private follow-up", preview)

        result = json.loads(self.command("report", "daily", "--date", date, "--write").stdout)
        daily = Path(result["output_path"])
        self.assertEqual(
            daily.relative_to(self.vault).as_posix(),
            "_briefings/2026-10/Week of 2026-10-26/2026-11-01 Daily Report.md",
        )
        self.assertIn("Review next week", daily.read_text(encoding="utf-8"))
        daily.write_text("- [ ] Keep this existing report\n")
        result = json.loads(self.command("report", "daily", "--date", date, "--write").stdout)
        self.assertEqual(result["status"], "existing")
        self.assertIn("Keep this existing report", daily.read_text())

        result = json.loads(self.command("report", "weekly", "--date", date, "--write").stdout)
        weekly = Path(result["output_path"])
        self.assertEqual(weekly.name, "2026-10-26 Weekly Report.md")
        self.assertNotIn("Keep this existing report", weekly.read_text())

    def test_daily_brief_includes_recent_brain_dumps_with_source_links(self):
        self.command("setup", "--vault", str(self.vault))
        notes = self.vault / "notes"
        notes.mkdir()
        (notes / "Quick Notes.md").write_text(
            "# Quick Notes\n\n"
            "## 2026-11-14\n- Try a shorter agenda\n- Bring printed examples\n"
            "## 2026-11-13\n- Sketch a simpler handoff\n"
            "## 2026-11-12\n- Old capture\n",
            encoding="utf-8",
        )
        idea = notes / "Review idea.md"
        idea.write_text("# Review idea\n\nOpen with one discussion question.\n", encoding="utf-8")
        modified = datetime(2026, 11, 13, 12).timestamp()
        os.utime(idea, (modified, modified))
        (notes / "Private.md").write_text(
            "---\ntype: executive-assistant-one-on-one\n---\n"
            "Private observation\n",
            encoding="utf-8",
        )
        os.utime(notes / "Private.md", (modified, modified))

        daily = self.command("report", "daily", "--date", "2026-11-14").stdout.decode()
        actions, captures = daily.split("## Brain Dumps", 1)
        for phrase in ("Try a shorter agenda", "Bring printed examples",
                       "Sketch a simpler handoff", "Open with one discussion question"):
            self.assertIn(phrase, captures)
            self.assertNotIn(phrase, actions)
        self.assertIn("../../../notes/Quick%20Notes.md", captures)
        self.assertIn("../../../notes/Review%20idea.md", captures)
        self.assertNotIn("Old capture", captures)
        self.assertNotIn("Private observation", captures)
        weekly = self.command("report", "weekly", "--date", "2026-11-14").stdout.decode()
        self.assertNotIn("## Brain Dumps", weekly)

    def test_schedule_runs_the_same_command_with_absolute_paths(self):
        self.command("setup", "--vault", str(self.vault))
        plist = plistlib.loads(self.command(
            "schedule", "weekly", "--at", "05:30", "--weekday", "Monday", "--format", "launchd"
        ).stdout)
        self.assertEqual(plist["StartCalendarInterval"], {"Weekday": 1, "Hour": 5, "Minute": 30})
        result = subprocess.run(plist["ProgramArguments"], cwd=self.root, capture_output=True, check=True)
        self.assertTrue(Path(json.loads(result.stdout)["output_path"]).is_file())

    def test_report_rejects_redirected_briefings_folder(self):
        self.command("setup", "--vault", str(self.vault))
        outside = self.root / "Outside"
        outside.mkdir()
        (self.vault / "_briefings").symlink_to(outside, target_is_directory=True)
        result = self.command("report", "daily", "--write", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"symlink", result.stderr)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
