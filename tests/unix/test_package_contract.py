import json
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import unittest

from test_vault_workflow import LAUNCHER

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = LAUNCHER.parents[2]
LEGACY = re.compile(r"powershell|\.ps[1m]\b|\.psm1\b|[A-Z]:\\|%USERPROFILE%|scripts[/\\]windows",
                    re.IGNORECASE)


class PackageContractTest(unittest.TestCase):
    def test_packaged_launcher_and_skill_references(self):
        manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
        self.assertLessEqual(len(manifest["interface"]["defaultPrompt"]), 3)
        skills = sorted((PLUGIN / manifest["skills"]).glob("*/SKILL.md"))
        self.assertEqual(len(skills), 19)
        self.assertTrue(LAUNCHER.is_file())
        for skill in skills:
            self.assertIn(f"name: {skill.parent.name}\n", skill.read_text())
            self.assertTrue((skill.parent / "agents/openai.yaml").is_file())

    def test_no_legacy_runtime_in_package(self):
        self.assertEqual(sorted(str(p.relative_to(PLUGIN)) for p in PLUGIN.rglob("*")
                                if p.suffix in {".ps1", ".psm1"}), [])
        self.assertFalse((ROOT / "install/windows").exists())
        self.assertFalse((ROOT / "tools/package-windows.ps1").exists())

    def test_documented_workflows(self):
        broken = []
        legacy = []
        shell_subcommands = set()
        names = subprocess.check_output(
            ["git", "ls-files", "-co", "--exclude-standard", "-z", "--", "*.md"], cwd=ROOT,
        ).decode().split("\0")
        for name in sorted(set(filter(None, names))):
            relative = Path(name)
            path = ROOT / relative
            if not path.is_file() or relative.parts[:3] == ("docs", "superpowers", "plans"):
                continue
            text = path.read_text(encoding="utf-8-sig")
            if LEGACY.search(text):
                legacy.append(str(relative))
            for link in re.findall(r"\]\(([^() ]+)\)", text):
                target = link.split("#", 1)[0]
                if target and "://" not in target and not (path.parent / target).exists():
                    broken.append((str(relative), target))
            for line in text.splitlines():
                if line.startswith(("./scripts/unix/ea.sh ", "./plugins/executive-assistant/scripts/unix/ea.sh ")):
                    parts = shlex.split(line.rstrip("\\").strip())
                    script = (PLUGIN if parts[0].startswith("./scripts/") else ROOT) / parts[0]
                    self.assertTrue(script.is_file(), str(relative))
                    shell_subcommands.add(parts[1])
        self.assertEqual(broken, [])
        self.assertEqual(legacy, [])
        self.assertTrue({"setup", "config", "check", "report", "review", "draft",
                         "attachment", "resolve", "audit", "schedule", "schedule-prompts"}
                        <= shell_subcommands)

    def test_shell_examples_run_against_temporary_data(self):
        with tempfile.TemporaryDirectory(prefix="ea package ") as directory:
            workspace = Path(directory).resolve()
            vault = workspace / "vault"
            profile = workspace / "profile.json"
            draft = workspace / "draft.md"
            draft.write_text("Review this text.")
            empty = workspace / "metadata.json"
            empty.write_text("[]")
            commands = [
                ("setup", "--vault", str(vault), "--copy-template"),
                ("config",), ("check",), ("report", "daily", "--write"),
                ("report", "weekly", "--write"), ("review", "mail", "--source", str(empty)),
                ("review", "calendar", "--source", str(empty), "--compare", str(empty)),
                ("review", "tasks", "--source", str(empty)),
                ("draft", "--subject", "Preview", "--source", str(draft)),
                ("attachment", "--source", str(draft), "--destination", str(vault / "copy.md")),
                ("resolve", "--path", str(draft)), ("audit",), ("schedule-prompts",),
                ("schedule", "daily", "--at", "06:00", "--format", "launchd"),
                ("schedule", "weekly", "--at", "05:30", "--format", "cron"),
            ]
            for command in commands:
                with self.subTest(command=command[0]):
                    subprocess.run([str(LAUNCHER), "--profile", str(profile), *command],
                                   cwd=workspace, capture_output=True, check=True)
