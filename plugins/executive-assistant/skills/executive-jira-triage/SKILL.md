---
name: executive-jira-triage
description: Jira triage workflow for executive operating work. Use when the user asks to review Jira issues, clean stale tickets, identify active work, create reviewed work items, close outdated issues, or reconcile Jira with vault actions.
---

# Executive Jira Triage

Use Jira for active work that needs ownership, status, and follow-through. Do not use it as the only durable note system.

## Workflow

1. Confirm the Jira project, labels, and CLI command names from local config or user input.
2. Query active issues before proposing changes.
3. Separate issues into active, stale/archive, needs review, and candidate closure.
4. Summarize recommended changes first.
5. Make Jira writes only after explicit user approval, especially closing or deleting issues.
6. Mirror durable context back into the vault when it should survive beyond Jira.

## Safety

Never bulk-delete or bulk-close issues without a reviewed list and explicit approval.

