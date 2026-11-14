# Shell Runtime

Use the launcher from the installed plugin root in Bash or Zsh. It runs
under Bash and uses Python 3.9 or newer. From the repository root, use
`./plugins/executive-assistant/scripts/unix/ea.sh`.

## Profile Setup

```sh
./scripts/unix/ea.sh setup --vault "/absolute/path/to/vault"
./scripts/unix/ea.sh config
./scripts/unix/ea.sh config --vault "/absolute/path/to/other-vault"
./scripts/unix/ea.sh config --vault "/absolute/path/to/other-vault" --apply
```

Add `--copy-template` when you want the starter notes. Profile updates preview
the new path before applying it. Pass `--profile PATH` before a subcommand to
select a different local profile.

## Calendar Management

```sh
./scripts/unix/ea.sh outlook calendar --days 7
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
```

Use `outlook calendar` with a [configured local calendar](local-outlook.md).
For the configured mail folder, use `outlook mail`.

## Meeting Notice Drafts

```sh
./scripts/unix/ea.sh draft --subject "Decision Review" --source "/path/to/agenda.md"
```

After reviewing the exact draft, use `--output PATH --apply` to save a new
local draft inside the vault. The user handles sending.

## Task Management

```sh
./scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
```

The shell command reads a supplied task file. Use
[Executive Manage Tasks](../skills/executive-todo-management/SKILL.md) to
preview and apply edits to vault checkboxes.

## Daily and Weekly Reports

```sh
./scripts/unix/ea.sh check
./scripts/unix/ea.sh report daily
./scripts/unix/ea.sh report daily --write
./scripts/unix/ea.sh report weekly --write
```

The default focus date is today in the host time zone. Use
`--date YYYY-MM-DD` for a different day or to select its Monday-to-Sunday week.
The runner ranks open checkboxes and attention cues in Markdown notes and
adds metadata from configured local Outlook sources. It skips generated
briefings, setup notes, hidden paths, symbolic links, saved drafts, and
notes marked `type: executive-assistant-one-on-one`.

Previewing prints Markdown. With `--write`, the command returns JSON with the
file path and whether it wrote a file or found an existing one. Add
`--replace` with `--write` to regenerate the existing report.

Reports go under `_briefings/YYYY-MM/Week of YYYY-MM-DD/`. Both folder
components use the week's Monday, including when the focus date is in a
different month. Daily filenames use the focus date and end in
` Daily Report.md`. Weekly filenames use Monday and end in ` Weekly Report.md`.

The shell report includes Snapshot, Calendar, Important Unread Emails, Needs
Attention, Waiting On, and Risks To Watch. Daily reports also include Brain
Dumps for the focus date and the day before. The runner includes dated
entries from `notes/Quick Notes.md` and one excerpt per other Markdown note
under `notes/` based on its last-modified date. Entries link back to their
source notes. The Codex skills can synthesize additional sections from
supplied metadata and notes.

## Local Report Fallback

```sh
./scripts/unix/ea.sh schedule daily --at 06:00 --format launchd
./scripts/unix/ea.sh schedule weekly --at 05:30 --weekday Monday --format cron
```

The generated job calls `report daily --write` or `report weekly --write`
using the selected profile. Pick a stable installation path and follow the
optional local schedule steps in the platform guide from your checkout or ZIP
to install and verify the job.

The logs live beside the profile. On macOS, launchd sends results to
`local.executive-assistant.daily.log` and errors to
`local.executive-assistant.daily.error.log`. On Linux, cron sends both to
`local.executive-assistant.daily.log`. Weekly jobs use `weekly` in place of
`daily`. A successful run prints `output_path` and a status of `written`
for a new report or `existing` when it reused a saved report.

## Codex Schedule Prompts

```sh
./scripts/unix/ea.sh schedule-prompts
```

The command prints templates. Test the prompt in a fresh Codex chat, then
create a standalone automation in the notes project and open the result of
its first scheduled run. See [profile settings](profile-schema.md#key-sections)
to choose which templates are shown.
