# Local Workflow Tool Reference

Run commands from the installed plugin root. See the [local input format](../../../references/local-inputs.md).

## Read-Only Commands

| Command | Use |
| --- | --- |
| `./scripts/unix/ea.sh outlook mail --days 7 --limit 5` | Read recent unread or flagged metadata from the configured local folder |
| `./scripts/unix/ea.sh outlook calendar --days 7` | Review the configured local calendar |
| `./scripts/unix/ea.sh review mail --source PATH --folder Inbox --limit 5` | Five metadata rows from a selected folder |
| `./scripts/unix/ea.sh report daily` or `report weekly` | Preview a report from vault signals and configured local mail or calendar |
| `./scripts/unix/ea.sh review calendar --source PATH` | Calendar review and meeting notices from supplied entries |
| `./scripts/unix/ea.sh review calendar --source PATH --compare PATH` | Compare two snapshots |
| `./scripts/unix/ea.sh review tasks --source PATH` | Local task metadata |
| `./scripts/unix/ea.sh resolve --path PATH` | Check a supplied local file |
| `./scripts/unix/ea.sh audit` | Aggregate local mutation counts |

## Mutating Commands

| Command | Mutation gate |
| --- | --- |
| `./scripts/unix/ea.sh draft --subject TEXT --source PATH` | Preview first. Add `--output PATH --apply` only after explicit confirmation. |
| `./scripts/unix/ea.sh attachment --source PATH --destination PATH` | Preview first. Add `--apply --confirm-save "SAVE ATTACHMENTS"` only after explicit confirmation. |
| `$executive-todo-management` | Show the exact local vault diff and apply only after confirmation. |

## Folder References

Use folder labels exactly as recorded in the supplied metadata.

## Link Rules

Check the exact local path before opening a file. Report missing files as
stale. Keep private mail identifiers and credentials out of shared notes.
