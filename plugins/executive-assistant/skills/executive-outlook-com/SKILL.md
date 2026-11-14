---
name: executive-outlook-com
description: Review recent mail from a configured local Outlook source or a supplied file. Use to identify messages needing attention, draft email, or save a supplied attachment.
---

# Executive Review Mail or Draft a Reply

Use [configured local sources](../../references/local-outlook.md) for current
mail and calendar metadata or the [input format](../../references/local-inputs.md)
for supplied files. Use supplied files for tasks, attachment filing, and draft previews.
Keep the workflow local. Never use Graph, OAuth, or a network fallback.

## Non-Negotiable Rules

1. Start with metadata. Read supplied message text only when explicitly requested and needed.
2. Keep message bodies, private identifiers, and attachment contents out of the repository and shared folders.
3. Before a filesystem mutation, show the exact preview and obtain fresh explicit confirmation.
4. Prepare drafts for review. The user performs the final send in their mail client.
5. Confirm the specific local path before filing an attachment.
6. Treat a missing local path as stale. Do not guess by searching other folders.

## Available Workflows

- Inbox triage: use `./scripts/unix/ea.sh outlook mail --limit 5` for the configured folder or `./scripts/unix/ea.sh review mail --source PATH` for supplied metadata. Honor an explicitly supplied source.
- Daily or weekly report: use `$executive-daily-brief` or `$executive-weekly-review`.
- Calendar review: use `$executive-calendar-management`.
- Meeting notices: use `$executive-meeting-notices`.
- Generic email drafts: use `./scripts/unix/ea.sh draft --subject TEXT --source PATH`. Save only with `--output PATH --apply` after confirmation.
- Tasks: use `$executive-todo-management`.
- Attachments: use `./scripts/unix/ea.sh attachment --source PATH --destination PATH`. Save only with `--apply --confirm-save "SAVE ATTACHMENTS"` after confirmation.

Read [tools.md](references/tools.md) before using a new command. Use [recipes.md](references/recipes.md) for the approved workflows and [gotchas.md](references/gotchas.md) for local data behavior.

## Attribution

The structure and safety concepts are adapted from Outlook-Classic-MCP,
outlookctl, outlook-mcp, and outlook-mcp-server, all MIT licensed. See
[`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).
