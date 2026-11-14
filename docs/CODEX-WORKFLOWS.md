# Codex Desktop Notes

Use the local Executive Assistant plugin on macOS or Linux. Open the vault
as a local Codex project when a workflow needs its files.

## Runtime

The plugin uses a Bash launcher and Python. Mail and calendar can read
configured Outlook or Exchange metadata from local sources. The draft command
previews or saves local Markdown for the user to send in their chosen client.

## Plugin Proof

In a fresh session, invoke `$executive-assistant-proof`. From the repository
root, verify the configured vault:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh check
```

## Setup and Profile Management

Use `$executive-assistant-setup` for a new profile and
`$executive-assistant-config` to preview or apply updates. Follow the
[macOS](INSTALL-MACOS.md) or [Linux](INSTALL-LINUX.md) guide to connect Obsidian.

## Daily Reports, Calendar, and Tasks

Use the daily brief, calendar management, and task management skills. These
commands run from the repository root.

```sh
./plugins/executive-assistant/scripts/unix/ea.sh report daily --write
./plugins/executive-assistant/scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
./plugins/executive-assistant/scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
```

The shell report uses vault notes and configured mail and calendar sources.
Use the brief or weekly review skill to synthesize additional context from
supplied snapshots, prior briefings, and relevant Jira work. See the
[shell runtime reference](../plugins/executive-assistant/references/unix-runtime.md#daily-and-weekly-reports)
for report paths and write behavior.

Use calendar entries to plan focus time. For task changes, the skill previews
the exact Markdown note and checkbox edit.

## Which Commands the Skills Use

Invoke the skill in a Codex session and give it the relevant vault, local file,
or project. Shell launcher commands use `./scripts/unix/ea.sh` from the
installed plugin root. From a checkout, use the longer path shown above.

| Workflow | Skill | Command |
| --- | --- | --- |
| Profile setup and verification | `$executive-assistant-setup`, `$executive-assistant-config`, `$executive-assistant-proof` | `setup`, `config`, `check` |
| Vault report | `$executive-daily-brief`, `$executive-weekly-review` | `report daily`, `report weekly` |
| Mail triage | `$executive-outlook-com` (Executive Mail Review) | `outlook mail` or `review mail --source PATH` |
| Calendar review and comparison | `$executive-calendar-management`, `$executive-calendar-sync` | `outlook calendar` for the configured feed, `review calendar --source PATH` for a snapshot, or add `--compare PATH` for a second snapshot |
| Meeting or email draft | `$executive-meeting-notices`, `$executive-outlook-com` | `draft --subject TEXT --source PATH` |
| Meeting preparation and debrief | `$executive-meeting-prep` | Reads relevant notes and supplied meeting material |
| Tasks | `$executive-todo-management`, `$executive-action-triage` | `review tasks --source PATH` for JSON, or review vault checkboxes directly |
| Local attachment filing | `$executive-outlook-com` | `attachment --source PATH --destination PATH` |
| Schedule setup | `$executive-scheduled-tasks` | `schedule`, `schedule-prompts` |
| Jira triage | `$executive-jira-triage` | Configured Jira CLI |
| Confluence refresh | `$executive-confluence-refresh` | Drafts from reviewed notes and uses the configured Confluence CLI for approved updates |
| GitLab project review | `$executive-gitlab-review` | `glab issue list`, `glab mr list`, `glab ci list` |
| Shared-vault sensitivity review | `$executive-sensitivity-review` | Reviews notes for sharing and proposes edits or moves |

For example, ask “Use `$executive-calendar-management` to find conflicts in
my private snapshot at `/absolute/path/to/calendar.json`.” The launcher reads
the supplied records and the skill interprets them. See the
[local input formats](../plugins/executive-assistant/references/local-inputs.md).

Reports read the vault and can include mail and calendar from local clients
or sync files. [Configure local Outlook access](../plugins/executive-assistant/references/local-outlook.md).

Project workflows use separately installed and authenticated CLIs.
See the [Atlassian CLI guide](../integrations/atlassian-cli/README.md)
and the [GitLab CLI guide](../plugins/executive-assistant/references/gitlab-cli.md).

## Scheduled Tasks

```sh
./plugins/executive-assistant/scripts/unix/ea.sh schedule-prompts
```

Run each generated prompt in a fresh chat to verify it. Create a standalone
automation in the vault's local project through Codex, then verify the first
scheduled result. The runner prints prompts only. See the
[profile schedule settings](../plugins/executive-assistant/references/profile-schema.md#key-sections).

## Local Scheduled Report Fallback

Generate a reviewed LaunchAgent plist or cron line from the
[local runtime reference](../plugins/executive-assistant/references/unix-runtime.md).
Inspect the report and the run log after the first scheduled run.
