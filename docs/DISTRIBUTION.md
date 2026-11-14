# Distribution

Distribute a repository checkout or ZIP for macOS and Linux. Both include
the local marketplace manifest, plugin, installer, and documentation.

Keep vault data, profiles, tokens, credentials, and private notes outside the package.

## Build a ZIP

From the repository root, commit the files you intend to distribute.
The packaging script archives all tracked files from `HEAD` into an
`executive-assistant/` directory. Choose a ZIP path that does not exist.

```sh
bash tools/package-unix.sh executive-assistant.zip
unzip -tq executive-assistant.zip
```

## Coworker Install Flow

1. Share the ZIP or repository through an approved internal channel.
2. Extract the ZIP or open the checkout in a stable local folder.
3. Follow the [macOS](INSTALL-MACOS.md) or [Linux](INSTALL-LINUX.md) guide to configure a profile, install the plugin, and verify a daily brief.

## Update or move an installation

The installer registers the checkout or extracted folder as the `personal`
marketplace and installs `executive-assistant@personal`. To refresh the
installed copy, update the source in place and rerun the installer. Open a
fresh Codex chat to load the updated skills.

### Marketplace name conflicts

If the installer says `personal` is already added from a different source,
run `codex plugin marketplace list` and check the recorded folder. If it
points to your existing Executive Assistant folder, update that copy in place.
If you deliberately moved that checkout, run `codex plugin marketplace remove personal`
and rerun the installer from the new folder.

If `personal` belongs to another project, keep the existing registration.
Use the [isolated CLI install](../DEVELOPING.md#try-a-workflow-with-temporary-data)
to try this package with a separate Codex configuration.

## Dependency Policy

The local workflow requires Bash 3.2+, Python 3.9+, and filesystem access to the working folder.
Install Codex to use the plugin. Obsidian is optional. Additional workflows
can use separately configured MCP servers or CLI tools such as the
Atlassian CLIs and GitLab's `glab`.
See the [workflow guide](CODEX-WORKFLOWS.md) for the dependencies used by
each integration.

## Scheduled Tasks Boundary

Generate prompts with `./plugins/executive-assistant/scripts/unix/ea.sh schedule-prompts`.
Use standalone Codex schedules for synthesis and the local LaunchAgent or cron
commands for deterministic reports. Confirm one scheduler-run result.
