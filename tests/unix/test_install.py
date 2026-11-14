import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
REMEDY = "Update Codex or pass --codex /absolute/path/to/codex."


class InstallerTest(unittest.TestCase):
    def install_with_cli(self, supports_add):
        with tempfile.TemporaryDirectory(prefix="ea installer ") as directory:
            workspace = Path(directory).resolve()
            log = workspace / "commands.log"
            cli = workspace / "fake codex"
            cli.write_text(
                '#!/bin/sh\n'
                'printf "%s\\n" "$*" >> "$EA_TEST_LOG"\n'
                'case "$*" in\n'
                '  "plugin marketplace --help"|"plugin marketplace add "*) exit 0 ;;\n'
                '  "plugin add --help"|"plugin add executive-assistant@personal")\n'
                '    exit "$EA_TEST_ADD_STATUS" ;;\n'
                'esac\n'
                'exit 2\n',
                encoding="utf-8",
            )
            cli.chmod(0o700)
            result = subprocess.run(
                ["bash", str(ROOT / "install/unix/install-plugin.sh"), "--codex", str(cli)],
                cwd=workspace, capture_output=True, text=True, timeout=10,
                env={**os.environ, "EA_TEST_LOG": str(log),
                     "EA_TEST_ADD_STATUS": "0" if supports_add else "2"},
            )
            return result, log.read_text(encoding="utf-8").splitlines()

    def test_installer_rejects_partial_cli_before_registration(self):
        result, commands = self.install_with_cli(supports_add=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(REMEDY, result.stderr)
        self.assertEqual(commands, ["plugin marketplace --help", "plugin add --help"])

    def test_installer_registers_then_installs_with_supported_cli(self):
        result, commands = self.install_with_cli(supports_add=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(commands, [
            "plugin marketplace --help", "plugin add --help",
            f"plugin marketplace add {ROOT}", "plugin add executive-assistant@personal",
        ])
