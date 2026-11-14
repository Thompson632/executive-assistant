---
name: executive-action-triage
description: Action extraction and prioritization workflow for an executive Obsidian vault. Use when the user asks to review open actions, clean task lists, extract follow-ups, find blocked work, prepare a next-action list, or promote commitments into Jira or notes.
---

# Executive Action Triage

Turn scattered notes into a clear, reviewed action model.

On macOS and Linux, if the vault is outside the current project, use `./scripts/unix/ea.sh config`
from the installed plugin root to resolve its folder. Use that folder for the note workflow.

## Workflow

1. Scan the requested vault areas for open checkboxes and action language.
2. Group items into today, this week, waiting on, blocked, delegate, and archive/review.
3. Prefer recent and strategically important items over stale historical items.
4. Recommend exact edits, moves, or Jira promotions, but do not mutate external systems without approval.
5. Preserve context links back to source notes using wiki-style links when possible.

## Output

Return a prioritized action review with:

- immediate actions
- delegated or waiting items
- blocked items
- stale items to archive
- suggested Jira candidates

