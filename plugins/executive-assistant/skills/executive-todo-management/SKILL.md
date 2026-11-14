---
name: executive-todo-management
description: Review and prioritize supplied task metadata or create, update, complete, and remove vault tasks using preview-first edits.
---

# Executive Todo Management

Review task metadata or maintain Markdown tasks in the configured vault. Use the existing preview and confirmation steps for proposed changes.

## Workflow

1. List incomplete tasks first and organize them by urgency, importance, due date, and strategic value. Include completed work when asked.
2. For a task edit, collect the exact title, due date, reminder, importance, and category changes.
3. Show the proposed create, update, completion, or removal as a vault note diff.
4. Ask for explicit confirmation before applying the change.
5. Use the existing vault note and checkbox as the specific target.
6. Pair task prioritization with `$executive-calendar-management` for focus time and `$executive-action-triage` for vault commitments.

## Commands

```sh
./scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
```

## Safety

- Apply only reviewed vault changes. A removal requires fresh explicit confirmation.
- Keep private task details out of the repository and shared folders.
