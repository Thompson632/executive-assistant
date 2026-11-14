from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[2] / "tools/check-skill-docs.py"
SKILL = "plugins/executive-assistant/skills/executive-example/SKILL.md"
METADATA = "plugins/executive-assistant/skills/executive-example/agents/openai.yaml"
GUIDES = (
    "docs/SAMPLE-PROMPTS.md",
    "docs/CODEX-WORKFLOWS.md",
    "docs/WORKFLOW-DIAGRAMS.md",
)


class SkillDocsTest(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory(prefix="ea skill docs ")
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
        self.git("init", "-q")
        for path in (SKILL, METADATA, *GUIDES):
            self.write(path, "Original\n")
        self.base = self.commit()

    def git(self, *args):
        result = subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
             "-c", "commit.gpgsign=false", *args],
            cwd=self.root, check=True, capture_output=True, text=True, timeout=10,
        )
        return result.stdout.strip()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-qm", "Test fixture")
        return self.git("rev-parse", "HEAD")

    def check(self, head="HEAD", base=None):
        return subprocess.run(
            [sys.executable, str(CHECKER), base or self.base, head],
            cwd=self.root, capture_output=True, text=True, timeout=10,
        )

    def test_existing_skill_update_requires_all_guides(self):
        self.write(METADATA, "Updated prompt\n")
        for path in (GUIDES[0], GUIDES[2]):
            self.write(path, "Updated workflow\n")
        result = self.check(self.commit())
        self.assertEqual(result.returncode, 1)
        self.assertIn(GUIDES[1], result.stderr)
        self.assertNotIn(GUIDES[0], result.stderr)
        self.assertNotIn(GUIDES[2], result.stderr)
        self.write(GUIDES[1], "Updated command\n")
        result = self.check(self.commit())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_added_or_removed_skill_file_requires_guides(self):
        self.write(SKILL.replace("example", "new"), "New skill\n")
        added = self.commit()
        (self.root / SKILL).unlink()
        removed = self.commit()
        for base, head in ((self.base, added), (added, removed)):
            with self.subTest(head=head):
                result = self.check(head, base)
                self.assertEqual(result.returncode, 1)
                for path in GUIDES:
                    self.assertIn(path, result.stderr)
                offsets = [result.stderr.index(path) for path in GUIDES]
                self.assertEqual(offsets, sorted(offsets))

    def test_repo_local_skill_does_not_trigger_packaged_guide_check(self):
        self.write(".agents/skills/sync-skill-docs/SKILL.md", "Maintenance instructions\n")
        result = self.check(self.commit())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unknown_base_is_reported(self):
        result = self.check(base="missing-audit-base")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing-audit-base", result.stderr)
