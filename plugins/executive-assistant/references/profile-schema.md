# Profile Schema

The local JSON profile uses an absolute `vaultPath`. The default is
`${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json`.
Obsidian can open the same folder. Local report dates and schedules use the host time zone.

## Key Sections

- `vaultPath` identifies the working folder.
- `obsidian` records optional Obsidian preferences.
- `outlook` opts in to [local Outlook mail and calendar sources](local-outlook.md).
- `atlassian` records optional Jira and Confluence preferences.
- `scheduledTasks` can supply enabled flags, times, and a weekday for standalone Codex prompts.

## Migration

When a copied profile references a path on another host, preview a vault-path
change with `config --vault "/absolute/path/to/vault"`. Add `--apply` to write
the reviewed change. Preserve other profile fields.

## Routine Configuration

From the installed plugin root:

```sh
./scripts/unix/ea.sh config
./scripts/unix/ea.sh config --vault "/absolute/path/to/vault"
./scripts/unix/ea.sh config --vault "/absolute/path/to/vault" --apply
```

Keep profiles local or gitignored. Store credentials in the appropriate tool, outside the profile.
