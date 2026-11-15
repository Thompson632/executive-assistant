# Developing Executive Assistant

Work from the repository root on macOS or Linux. The local runtime requires
Bash 3.2 or later and Python 3.9 or later. Install Zsh to verify the launcher
from that shell, and use the Codex CLI or Codex Desktop to test plugin
installation and skill discovery.

```sh
bash install/unix/check-prereqs.sh
python3 -m unittest discover -s tests/unix -v
```

The runtime tests use temporary profiles and vaults. You can run them without
configuring Outlook, Jira, Confluence, or GitLab.

## Where to make changes

- Put deterministic commands in `plugins/executive-assistant/scripts/unix/`
  and regression coverage in `tests/unix/`.
- Put workflow instructions in `plugins/executive-assistant/skills/` and
  shared reference material in `plugins/executive-assistant/references/`.
- Use `plugins/executive-assistant/assets/vault-template/` for reusable
  starter notes and `config/executive-assistant.example.json` for example
  settings.

See the [architecture guide](docs/ARCHITECTURE.md) for integration boundaries.

## Local implementation plans

Save working plans in `docs/superpowers/plans/` and companion specs in
`docs/superpowers/specs/`. Create the folders when you first need them. Git
ignores both folders, and release ZIPs exclude them. Keep any lasting
workflow guidance in the shared docs so it is available in a fresh checkout.

## Try a workflow with temporary data

From Bash or Zsh, create a separate profile and vault to exercise the
checkout.

```sh
ea_dev_dir=$(mktemp -d)
./plugins/executive-assistant/scripts/unix/ea.sh --profile "$ea_dev_dir/profile.json" \
  setup --vault "$ea_dev_dir/vault" --copy-template
./plugins/executive-assistant/scripts/unix/ea.sh --profile "$ea_dev_dir/profile.json" check
./plugins/executive-assistant/scripts/unix/ea.sh --profile "$ea_dev_dir/profile.json" report daily
```

To test installation with a separate Codex configuration, create a directory
for it and run the marketplace installer. Use the same `CODEX_HOME` when
listing the installed plugin from the CLI.

```sh
mkdir "$ea_dev_dir/codex"
CODEX_HOME="$ea_dev_dir/codex" bash install/unix/install-plugin.sh
CODEX_HOME="$ea_dev_dir/codex" codex plugin list
```

If needed, pass `--codex /absolute/path/to/codex` to select the CLI and use
that executable for the list command. Verify skill discovery separately
with a fresh Desktop chat opened to the test notes folder.
See the [distribution guide](docs/DISTRIBUTION.md) for installation updates
and building a ZIP from a commit.

## Validate changes

- Run the unit tests and check changed shell scripts with `bash -n`. Validate
  on macOS and Linux with Bash and Zsh where available. The
  [CI workflow](.github/workflows/unix.yml) runs the test suite and checks the
  distribution ZIP on both platforms. Each shell uses separate temporary
  settings and the default profile to preview, save, and rerun a daily brief.
- Follow [the repo validation instructions](AGENTS.md#validation) for plugin
  and skill checks. Install [development dependencies](requirements-dev.txt)
  in a virtual environment if the skill validator needs PyYAML. If the
  standalone plugin validator is unavailable, use the disposable install above.
- Use the [release checklist](docs/RELEASE-CHECKLIST.md) to verify the extracted
  ZIP, a fresh install, an update, and host workflows.
