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
for it and run the marketplace installer. Then start a fresh chat in the
environment where the plugin is installed to verify skill discovery.

```sh
mkdir "$ea_dev_dir/codex"
CODEX_HOME="$ea_dev_dir/codex" bash install/unix/install-plugin.sh
```

If needed, pass `--codex /absolute/path/to/codex` to select the CLI.
See the [distribution guide](docs/DISTRIBUTION.md) for installation updates
and building a ZIP from a commit.

## Validate changes

- Run the unit tests and check changed shell scripts with `bash -n`. Validate
  on macOS and Linux with Bash and Zsh where available. The
  [CI workflow](.github/workflows/unix.yml) runs the test suite and checks the
  distribution ZIP on both platforms.
- Follow [the repo validation instructions](AGENTS.md#validation) for plugin
  and skill checks. Install [development dependencies](requirements-dev.txt)
  in a virtual environment if the skill validator needs PyYAML. If the
  standalone plugin validator is unavailable, use the disposable install above.
