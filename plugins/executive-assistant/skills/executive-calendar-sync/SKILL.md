---
name: executive-calendar-sync
description: Compare dedicated calendar snapshots and prepare a reviewed reconciliation plan.
---

# Executive Calendar Sync

Use this skill for two explicitly supplied calendar snapshots. Compare them by title and time and produce a reviewed reconciliation plan.

## First Use

1. Confirm both snapshot files represent the calendars the user intends to compare.
2. Use a narrow date range for the first review.
3. Review both snapshots with the local command.
4. Inspect event counts, unsupported entries, differences, and conflicts. Keep credentials, bodies, attendees, and join links private.

```sh
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json" --compare "/path/to/team-calendar.json"
```

## Reviewed Workflow

- Start with a read-only plan. Show proposed creates, updates, deletions, and conflicts.
- Use exact matches as evidence of a pair. Report ambiguous matches.
- Show the plan before the user applies any reviewed changes in the source clients.
- Keep invitations, attendees, meeting links, and event bodies outside synchronization proposals.

## Boundaries

- Recurring, private, and attendee-bearing meetings are reported but
  never synchronized automatically.
- Recurring events and deletion propagation are reported for
  review, not applied automatically.
- When both ends of a linked event changed differently, report a conflict and
  ask the user which calendar is authoritative. Do not choose silently.
- Use exact calendar matching. Stop if the requested calendar is missing or
  ambiguous.
- Do not schedule this as an unattended mutating automation. A future monitor
  may run plan mode only and notify on meaningful changes or conflicts.
