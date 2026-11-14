# Codex Desktop Notes

Use the local Executive Assistant plugin on macOS or Linux. Open the vault
as a local Codex project when a workflow needs its files.

Use the [sample prompt guide](SAMPLE-PROMPTS.md) for requests you can paste
into Codex.

See the [workflow diagrams and schedule guide](WORKFLOW-DIAGRAMS.md) for
how the skills fit together.

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
[macOS](INSTALL-MACOS.md) or [Linux](INSTALL-LINUX.md) guide to connect a
notes folder and optionally open it in Obsidian.

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

To capture actions from a meeting, ask Executive Manage Tasks to add a known
task, or ask Executive Prepare for or Debrief a Meeting to extract a batch
from your notes. See the [task lifecycle diagram and vault file guide](WORKFLOW-DIAGRAMS.md#add-a-meeting-action-and-track-it-to-completion).

## Switching Context

Use `$executive-context-switch` in your vault's Codex project.

- **Switch away.** “Save where I left off on the launch decision. I compared both options. Next I need to add the support estimate.” Review the proposed edit to the Obsidian action.
- **Switch back.** “Pick up the launch decision.” Codex reads the action and returns its link, the current state, and the first next step. It includes a blocker if one is recorded.

The handoff lives with the action, so it is available from a fresh chat.
If the vault has no action list, the first saved action goes in
`Action-Items.md` under **Inbox**.

## Quick Notes

Ask “Use `$executive-quick-note` to jot down that the room layout worked
well.” By default, the skill adds a dated bullet to `notes/Quick Notes.md`.
The Daily Brief's **Brain Dumps** section includes that day's and the
previous day's entries, plus linked excerpts from other notes under
`notes/` updated on either day. If you keep a capture note elsewhere,
name it when asking Codex to synthesize a brief.
For a commitment you want to track, ask to capture it as an action.

## Which Commands the Skills Use

Invoke the skill in a Codex session and give it the relevant vault, local file,
or project. Shell launcher commands use `./scripts/unix/ea.sh` from the
installed plugin root. From a checkout, use the longer path shown above.

| Workflow | Skill | Command |
| --- | --- | --- |
| Profile setup and verification | `$executive-assistant-setup`, `$executive-assistant-config`, `$executive-assistant-proof` | `setup`, `config`, `check` |
| Vault report | `$executive-daily-brief`, `$executive-weekly-review` | `report daily`, `report weekly` |
| Mail review and drafts | `$executive-outlook-com` | `outlook mail` or `review mail --source PATH` |
| Calendar review and comparison | `$executive-calendar-management`, `$executive-calendar-sync` | `outlook calendar` for the configured feed, `review calendar --source PATH` for a snapshot, or add `--compare PATH` for a second snapshot |
| Meeting or email draft | `$executive-meeting-notices`, `$executive-outlook-com` | `draft --subject TEXT --source PATH` |
| Meeting preparation and debrief | `$executive-meeting-prep` | Reads relevant notes and supplied meeting material |
| One-on-one notes and prep | `$executive-one-on-one` | Saves notes by person and date and prepares the next conversation from open commitments |
| Switch context | `$executive-context-switch` | Saves a stopping point on an Obsidian action and reads it back when resuming |
| Quick note | `$executive-quick-note` | Saves a short dated bullet to an Obsidian note |
| Tasks | `$executive-todo-management`, `$executive-action-triage` | `review tasks --source PATH` for JSON, or review vault checkboxes directly |
| Local attachment filing | `$executive-outlook-com` | `attachment --source PATH --destination PATH` |
| Schedule setup | `$executive-scheduled-tasks` | `schedule`, `schedule-prompts` |
| Jira triage | `$executive-jira-triage` | Configured Jira CLI |
| Confluence refresh | `$executive-confluence-refresh` | Drafts from reviewed notes and uses the configured Confluence CLI for approved updates |
| GitLab project review | `$executive-gitlab-review` | `glab issue list`, `glab mr list`, `glab ci list` |
| Work intake | `$executive-work-intake` | Captures the request, coordinates approved epic and issue creation, and drafts the Scrum of Scrums update |
| Shared-vault sensitivity review | `$executive-sensitivity-review` | Reviews notes for sharing and proposes edits or moves |

For example, ask “Use `$executive-calendar-management` to find conflicts in
my private snapshot at `/absolute/path/to/calendar.json`.” The launcher reads
the supplied records and the skill interprets them. See the
[local input formats](../plugins/executive-assistant/references/local-inputs.md).

Reports read the vault and can include mail and calendar metadata from local
sync files. [Configure local Outlook access](../plugins/executive-assistant/references/local-outlook.md).

Project workflows use separately installed and authenticated CLIs.
See the [Atlassian CLI guide](../integrations/atlassian-cli/README.md)
and the [GitLab CLI guide](../plugins/executive-assistant/references/gitlab-cli.md).

For a recurring 1:1, see the [one-on-one workflow](WORKFLOW-DIAGRAMS.md#save-a-one-on-one-and-prepare-for-the-next-meeting).
For a new work request, see the [intake to Scrum of Scrums workflow](WORKFLOW-DIAGRAMS.md#take-a-new-work-request-from-intake-to-scrum-of-scrums).
Use `$executive-work-intake` to coordinate it, or request a local rehearsal
to save simulated GitLab and Confluence records in the vault.

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
