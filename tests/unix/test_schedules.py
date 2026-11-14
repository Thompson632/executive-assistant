import json
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import unittest

from test_vault_workflow import SCRIPT


class SchedulesTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="ea schedule ")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.profile = self.root / "test profile.json"
        self.vault = self.root / "my vault"
        self.command("setup", "--vault", str(self.vault))

    def command(self, *args, check=True, profile=None):
        return subprocess.run([sys.executable, str(SCRIPT), "--profile", str(profile or self.profile),
                               *args], capture_output=True, check=check)

    def test_weekly_launchd_and_cron_arguments(self):
        args = ("schedule", "weekly", "--at", "05:30", "--weekday", "Monday")
        plist = plistlib.loads(self.command(*args, "--format", "launchd").stdout)
        self.assertEqual(plist["StartCalendarInterval"], {"Hour": 5, "Minute": 30, "Weekday": 1})
        result = subprocess.run(plist["ProgramArguments"], cwd=self.root, capture_output=True, check=True)
        self.assertTrue(Path(json.loads(result.stdout)["output_path"]).is_file())
        line = self.command(*args, "--format", "cron").stdout.decode().strip()
        self.assertTrue(line.startswith("30 5 * * 1 "))
        subprocess.run(["/bin/sh", "-c", line.split(maxsplit=5)[5]], cwd=self.root, check=True)
        log = self.root / "local.executive-assistant.weekly.log"
        self.assertEqual(json.loads(log.read_text())["status"], "existing")

    def test_schedule_rejects_invalid_inputs(self):
        bad = self.command("schedule", "daily", "--at", "24:00", check=False)
        self.assertNotEqual(bad.returncode, 0)
        for name in ("bad%profile.json", "bad\nprofile.json"):
            profile = self.root / name
            profile.write_bytes(self.profile.read_bytes())
            bad = self.command("schedule", "daily", "--at", "06:00", "--format", "cron",
                               profile=profile, check=False)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn(b"Cron paths", bad.stderr)

    def test_fresh_profile_prints_templates(self):
        prompts = self.command("schedule-prompts").stdout.decode()
        for heading in ("Daily Brief", "Weekly Review", "Follow-Up Monitor", "Action Update"):
            self.assertIn("## " + heading, prompts)

    def test_standalone_codex_prompt_uses_profile(self):
        payload = json.loads(self.profile.read_text())
        payload["scheduledTasks"] = {"enabled": True,
                                     "weeklyReview": {"enabled": True, "time": "07:45",
                                                      "day": "Thursday"}}
        self.profile.write_text(json.dumps(payload))
        prompts = self.command("schedule-prompts").stdout.decode()
        self.assertIn(str(self.profile), prompts)
        self.assertIn("$executive-weekly-review", prompts)
        self.assertIn("Thursday at 07:45", prompts)
        self.assertIn("standalone", prompts.lower())
        self.assertIn("no-autosend", prompts.lower())
        self.assertNotIn("## Daily Brief", prompts)
        payload.pop("scheduledTasks")
        self.profile.write_text(json.dumps(payload))
        prompts = self.command("schedule-prompts").stdout.decode()
        for heading in ("Daily Brief", "Weekly Review", "Follow-Up Monitor", "Action Update"):
            self.assertIn("## " + heading, prompts)
