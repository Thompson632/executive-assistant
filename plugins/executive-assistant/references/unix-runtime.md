# Shell Runtime

Use the launcher from the installed plugin root in Bash or Zsh.

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

Use vault checkboxes to maintain local tasks. Preview changes and confirm
removal before editing a note.

## Daily Report and Proof

```sh
./scripts/unix/ea.sh check
./scripts/unix/ea.sh report daily --write
```

## Local Report Fallback

```sh
./scripts/unix/ea.sh schedule daily --at 06:00 --format launchd
./scripts/unix/ea.sh schedule weekly --at 05:30 --weekday Monday --format cron
```

Review the output before registering a LaunchAgent or cron job. Verify one
scheduled report and its local log.

## Codex Schedule Prompts

```sh
./scripts/unix/ea.sh schedule-prompts
```

The command prints standalone prompts. Confirm schedules through Codex and
verify the first run. See [local inputs](local-inputs.md) for metadata schemas.
