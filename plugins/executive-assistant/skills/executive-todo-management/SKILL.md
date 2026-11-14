---
name: executive-todo-management
description: Add, edit, check off, or remove a specific Obsidian task after reviewing the change. Also review and sort tasks from a supplied file.
---

# Executive Manage Tasks

Use this to update a specific task, such as “Mark the room check complete,”
or to review a supplied task file. For a review of open vault priorities,
use `$executive-action-triage`.

## Workflow

1. List incomplete tasks first and organize them by urgency, importance, due date, and strategic value. Include completed work when asked.
2. For a task edit, identify the exact task and the fields the user wants to change.
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
