---
name: executive-action-triage
description: Review open actions or pull follow-ups from Obsidian notes. Use for what to do next, what is blocked, and what is waiting on someone.
---

# Executive Prioritize Actions

Use this for “What should I work on next?” or “What am I waiting on?”
For a specific checkbox change, use `$executive-todo-management`.
For where you left off on one task, use `$executive-context-switch`.

On macOS and Linux, if the vault is outside the current project, use `./scripts/unix/ea.sh config`
from the installed plugin root to resolve its folder. Use that folder for the note workflow.

## Workflow

1. Scan the requested vault areas for open checkboxes and action language.
2. Group items into today, this week, waiting on, blocked, delegate, and archive/review.
3. Prefer recent and strategically important items over stale historical items.
4. Recommend exact edits, moves, or Jira promotions, but do not mutate external systems without approval.
5. Preserve context links back to source notes using wiki-style links when possible.

## Output

Lead with the actions to take next. Include waiting items, blockers,
stale items, or Jira candidates when relevant. Link to the source notes.

