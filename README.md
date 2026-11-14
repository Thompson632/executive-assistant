# Executive Assistant

Reusable Codex Desktop package for an executive-assistant workflow built around a local working folder on macOS and Linux. Optional integrations can use separately configured MCP servers or CLI tools such as the Atlassian CLIs and GitLab's `glab`.

- **Set up your assistant.** Follow [Get your first daily brief](docs/GETTING-STARTED.md).
- **Work on the package.** Start with the [development guide](DEVELOPING.md) and [contribution guide](CONTRIBUTING.md).

This repository is for the package and integration code only. It must not contain a user's vault, email content, Outlook link index, Jira tokens, Confluence tokens, or private operating notes.

## Current Shape

- `plugins/executive-assistant/` is the Codex plugin package.
- `plugins/executive-assistant/skills/` contains the Codex entry points listed in the [workflow guide](docs/CODEX-WORKFLOWS.md#which-commands-the-skills-use).
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

The [getting-started guide](docs/GETTING-STARTED.md) walks through installation
and a report in Codex or the terminal. For another workflow, pick a
[sample prompt](docs/SAMPLE-PROMPTS.md).

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

Opt in to use a synced Maildir folder or calendar metadata file on macOS or
Linux. Mail triage, calendar review, and reports read the configured local
sources at runtime.
[Set up local Outlook access](plugins/executive-assistant/references/local-outlook.md).

## Calendar Management

Use `$executive-calendar-management` to locate conflicts and short transitions,
protect focus time, and align the meeting load with active priorities. Use the
configured calendar or supply a file in the
[local input format](plugins/executive-assistant/references/local-inputs.md).

Use `$executive-meeting-notices` to review supplied notices or prepare an invitation or response draft.
Show the exact draft before saving local text. The user sends it in their chosen client.

## Task Management

Start with [Find the right skill](docs/WORKFLOW-DIAGRAMS.md#find-the-right-skill)
for examples of when to save a note, pause work, edit a task, or check priorities.

Use `$executive-context-switch` when you need to stop or pick up an action.
The skill saves a short stopping point on the existing Obsidian action and
uses it to give you one next step when you return.
[See example prompts](docs/CODEX-WORKFLOWS.md#switching-context).

Use `$executive-todo-management` to review, prioritize, create, update, complete,
or remove vault tasks. Preview and confirm changes to vault notes. See the
[local input format](plugins/executive-assistant/references/local-inputs.md) for supplied task metadata.

## Documentation

- [Sample prompts for every skill](docs/SAMPLE-PROMPTS.md) gives you requests to copy into Codex.
- [Codex workflows](docs/CODEX-WORKFLOWS.md) lists the skills and their commands.
- [Workflow diagrams](docs/WORKFLOW-DIAGRAMS.md) show how actions, quick notes, briefs, and schedules fit together.
- [Architecture](docs/ARCHITECTURE.md) describes the runtime, integrations, and data boundaries.
- [Profile schema](plugins/executive-assistant/references/profile-schema.md) describes profile fields and local overrides.
- [Distribution](docs/DISTRIBUTION.md) covers packaging, installation, and updates.
- [Roadmap](docs/ROADMAP.md) tracks pending validation and potential work.

## Distribution

For a coworker install, build a ZIP from the current Git commit and follow
[the distribution guide](docs/DISTRIBUTION.md).

```sh
bash tools/package-unix.sh executive-assistant.zip
```

## License

[MIT License](LICENSE).
