---
name: executive-todo-management
description: Add tasks to Obsidian, including actions from a meeting or a supplied list. Edit, complete, or remove existing tasks after reviewing the change.
---

# Executive Manage Tasks

Use this to update a specific task, such as “Mark the room check complete,”
or to review a supplied task file. For a review of open vault priorities,
use `$executive-action-triage`.

## Workflow

1. Use the user's selected vault or read `vault_path` from
   `./scripts/unix/ea.sh config` at the installed plugin root. Use the
   existing task list, or the Inbox in `Action-Items.md` by default.
2. Match existing tasks by title, project, and source before adding a
   checkbox. Keep one checkbox per task. Link to the meeting, project, or
   task detail note when it exists. For a supplied list, preview the batch
   together and call out any ambiguous matches.
3. Record the due date if supplied. For new actions with no date, offer
   one question alongside the preview: “When is this due, or should I
   leave it undated?” Ask once for the batch if several dates are missing.
   If the user confirms the preview without a date, save it undated.
   Resolve relative dates using the user's local date. Clarify an ambiguous
   date before recording it. Follow the vault's convention, or put
   `due YYYY-MM-DD` on the checkbox line.
4. For completion, change the original checkbox from `[ ]` to `[x]`.
   Keep the source links and context. Daily and weekly reports are
   snapshots. Regenerate one only when the user asks for a refresh.
5. Show the exact edit and ask for confirmation. Reread the target before
   applying the approved change, then verify it and return a link.

## Commands

```sh
./scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
```

## Safety

- Apply only reviewed vault changes. A removal requires fresh explicit confirmation.
- Keep private task details out of the repository and shared folders.
