# Distribution

The package is a repository checkout or ZIP for macOS and Linux containing:

- `.agents/plugins/marketplace.json`
- `plugins/executive-assistant/`
- `install/unix/install-plugin.sh`
- `install/unix/check-prereqs.sh`
- `docs/INSTALL-MACOS.md` and `docs/INSTALL-LINUX.md`
- `README.md`

Keep vault data, profiles, tokens, credentials, and private notes outside the package.

## Build A Zip

From the repository root, commit the files you intend to distribute and run:

```sh
bash tools/package-unix.sh executive-assistant.zip
```

## Coworker Install Flow

1. Share the ZIP or repository through an approved internal channel.
2. Extract it locally and open the repository root in a terminal.
3. Run `bash install/unix/check-prereqs.sh`.
4. Run `bash install/unix/install-plugin.sh`.
5. Configure a profile using the [macOS](INSTALL-MACOS.md) or [Linux](INSTALL-LINUX.md) guide.
6. Start a new Codex session and run the proof skill and a daily brief.

## Dependency Policy

The local workflow requires Bash 3.2+, Python 3.9+, and filesystem access to the working folder.
Install Codex to use the plugin. Obsidian is optional. Additional workflows
can use separately configured MCP servers or CLI tools such as the
Atlassian CLIs and GitLab's `glab`.
The plugin must degrade gracefully when optional dependencies are missing.

## Scheduled Tasks Boundary

Generate prompts with `./plugins/executive-assistant/scripts/unix/ea.sh schedule-prompts`.
Use standalone Codex schedules for synthesis and the local LaunchAgent or cron
commands for deterministic reports. Confirm one scheduler-run result.
