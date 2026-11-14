# Codex Desktop Notes

Use the local Executive Assistant plugin on macOS or Linux. Open the vault
as a local Codex project when a workflow needs its files.

## Runtime

The plugin uses the local shell launcher and Python. Mail and calendar can
read configured Outlook or Exchange metadata from local sources. Drafts are
plain text for review.

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

Use the daily brief, calendar management, and task management skills. From
the repository root, run:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh report daily --write
./plugins/executive-assistant/scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
./plugins/executive-assistant/scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
```

Use calendar entries to plan focus time. Preview vault task edits and use
the exact note and checkbox as the target.

## Which Commands the Skills Use

Invoke the skill in a Codex session and give it the relevant vault, local file,
or project. Shell launcher commands use `./scripts/unix/ea.sh` from the
installed plugin root. From a checkout, use the longer path shown above.

| Workflow | Skill | Command |
| --- | --- | --- |
| Profile setup and verification | `$executive-assistant-setup`, `$executive-assistant-config`, `$executive-assistant-proof` | `setup`, `config`, `check` |
| Vault report | `$executive-daily-brief`, `$executive-weekly-review` | `report daily`, `report weekly` |
| Mail triage | `$executive-outlook-com` (Executive Mail Review) | `outlook mail` or `review mail --source PATH` |
| Calendar review and comparison | `$executive-calendar-management`, `$executive-calendar-sync` | `outlook calendar` or `review calendar --source PATH`, with `--compare PATH` for a second snapshot |
| Meeting or email draft | `$executive-meeting-notices`, `$executive-outlook-com` | `draft --subject TEXT --source PATH` |
| Tasks | `$executive-todo-management`, `$executive-action-triage` | `review tasks --source PATH` for JSON, or review vault checkboxes directly |
| Local attachment filing | `$executive-outlook-com` | `attachment --source PATH --destination PATH` |
| Schedule setup | `$executive-scheduled-tasks` | `schedule`, `schedule-prompts` |
| GitLab project review | `$executive-gitlab-review` | `glab issue list`, `glab mr list`, `glab ci list` |

For example, ask “Use `$executive-calendar-management` to find conflicts in
my private snapshot at `/absolute/path/to/calendar.json`.” The launcher reads
the supplied records and the skill interprets them. See the
[local input formats](../plugins/executive-assistant/references/local-inputs.md).

Reports read the vault and can include mail and calendar from local clients
or sync files. [Configure local Outlook access](../plugins/executive-assistant/references/local-outlook.md).

GitLab review uses your existing CLI login and the project you specify.
[Set up GitLab CLI access](../plugins/executive-assistant/references/gitlab-cli.md).

## Scheduled Tasks

```sh
./plugins/executive-assistant/scripts/unix/ea.sh schedule-prompts
```

Test each prompt manually in a fresh session, then test the standalone
schedule and verify its output. Keep the no-autosend boundary.

## Local Scheduled Report Fallback

Generate a reviewed LaunchAgent plist or cron line from the
[local runtime reference](../plugins/executive-assistant/references/unix-runtime.md).
Inspect the report and the run log after the first scheduled run.
