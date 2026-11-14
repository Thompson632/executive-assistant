# Executive Assistant

Reusable Codex Desktop package for an executive-assistant workflow built around a local working folder on macOS and Linux. Optional integrations can use separately configured MCP servers or CLI tools such as the Atlassian CLIs and GitLab's `glab`.

This repository is for the package and integration code only. It must not contain a user's vault, email content, Outlook link index, Jira tokens, Confluence tokens, or private operating notes.

## Current Shape

- `plugins/executive-assistant/` is the Codex plugin package.
- `plugins/executive-assistant/skills/` contains workflow skills for briefings, calendar and task management, meeting notices, meeting prep, actions, Jira, Confluence, and sensitivity review.
- `plugins/executive-assistant/scripts/unix/` contains shell setup, reports, local input workflows, and scheduler configuration.
- `plugins/executive-assistant/assets/vault-template/` contains the clean Obsidian starter vault.
- `integrations/atlassian-cli/` documents the Jira/Confluence CLI integration boundary.
- [GitLab CLI](plugins/executive-assistant/references/gitlab-cli.md) documents setup and project review with `glab`.
- `.agents/plugins/marketplace.json` is a repo-local marketplace for testing this plugin in Codex Desktop.

## Design Rules

- macOS and Linux support the local vault and metadata workflows.
- Validate the installed shell workflow on each target platform.
- Local metadata review is read-first. Users send reviewed drafts from their chosen client.
- Skills should guide repeatable executive workflows; deterministic scripts should handle fragile local integration.
- MCP servers should own live system access once the integration shape is proven.
- Configuration belongs in local profile files or environment variables, not committed source.

## Quick Start

Follow the [macOS setup guide](docs/INSTALL-MACOS.md) or [Linux setup guide](docs/INSTALL-LINUX.md)
to install the plugin, connect the same folder in Obsidian and Codex, and generate a daily or weekly vault report.

1. Open the repository in a terminal.
2. Check prerequisites and install from the repo-local marketplace:

```sh
bash install/unix/check-prereqs.sh
bash install/unix/install-plugin.sh
```

3. Use `$executive-assistant-setup` to configure your profile. For an existing profile, use `$executive-assistant-config`.
4. Verify the configured vault:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh check
```

## Local Configuration

Create a local profile with a plain working folder:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh setup --vault "$HOME/Executive Assistant Vault"
```

The folder is created if needed. The profile is stored under
`${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/`.
Use a vault outside the repository. Add `--copy-template` only when you want the starter notes.

For an existing profile, use the non-destructive manager:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh config
./plugins/executive-assistant/scripts/unix/ea.sh config --vault "/absolute/path/to/other-vault"
```

Add `--apply` after reviewing the preview. The Codex equivalent is `$executive-assistant-config`.

## Local Outlook Mail and Calendar

Opt in to use a synced Apple Mail account and Apple Calendar on macOS, or use
synced Maildir and calendar metadata files on Linux or macOS. Mail triage,
calendar review, and reports read the configured local sources at runtime.
[Set up local Outlook access](plugins/executive-assistant/references/local-outlook.md).

## Calendar Management

Use `$executive-calendar-management` to locate conflicts and short transitions,
protect focus time, and align the meeting load with active priorities. Use the
configured calendar or supply a file in the
[local input format](plugins/executive-assistant/references/local-inputs.md).

Use `$executive-meeting-notices` to review supplied notices or prepare an invitation or response draft.
Show the exact draft before saving local text. The user sends it in their chosen client.

## Task Management

Use `$executive-todo-management` to review, prioritize, create, update, complete,
or remove vault tasks. Preview and confirm changes to vault notes. See the
[local input format](plugins/executive-assistant/references/local-inputs.md) for supplied task metadata.

## Distribution

For a coworker install, build a ZIP from committed files and follow
[the distribution guide](docs/DISTRIBUTION.md).

```sh
bash tools/package-unix.sh executive-assistant.zip
```
