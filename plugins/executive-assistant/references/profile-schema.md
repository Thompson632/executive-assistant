# Profile Schema

The local JSON profile uses an absolute `vaultPath`. The default is
`${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json`.
Obsidian can open the same folder. Local report dates and schedules use the host time zone.
Pass `--profile PATH` before the subcommand to select a different file.

## Key Sections

- `vaultPath` identifies the working folder. The runner uses this field,
  and `check` reports whether the folder contains Obsidian settings.
- `obsidian` records optional preferences. If it already contains
  `vaultPath`, a vault move through `config` updates both paths.
  Copying starter notes is controlled by `setup --copy-template`.
- `outlook` opts in to [local Outlook mail and calendar sources](local-outlook.md).
- `atlassian` records optional Jira and Confluence preferences for Codex skills.
- `scheduledTasks` controls which templates `schedule-prompts` prints.
  Use `enabled` for the whole group and for each of `dailyBrief`,
  `weeklyReview`, `followUpMonitor`, and `actionUpdate`. Each enabled
  template can specify a 24-hour `time`. `weeklyReview` can also specify
  a `day` such as `Monday`. A fresh profile prints all four templates.
  Configure the actual Codex automation separately. LaunchAgent and cron
  output uses the arguments passed to `schedule`.

The source repository's `config/executive-assistant.example.json` is a
reference. Add settings you want to use to your active profile. The runner
reads the default profile above unless you use `--profile`.
Older profiles may contain fields such as `timeZoneId` or
`obsidian.copyVaultTemplate`. Report dates use the host's time zone and
`setup --copy-template` controls whether starter notes are copied.

## Migration

When a copied profile references a path on another host, preview a vault-path
change with `config --vault "/absolute/path/to/vault"`. Add `--apply` to write
the reviewed change. The command preserves unrelated profile fields.

## Routine Configuration

From the installed plugin root:

```sh
./scripts/unix/ea.sh config
./scripts/unix/ea.sh config --vault "/absolute/path/to/vault"
./scripts/unix/ea.sh config --vault "/absolute/path/to/vault" --apply
```

Keep profiles local or gitignored. Store credentials in the appropriate tool, outside the profile.
