---
name: executive-calendar-sync
description: Compare two calendar metadata JSON files covering the same dates. List missing or changed events and conflicts for the user to resolve.
---

# Executive Compare Two Calendars

Use this skill when the user supplies two files in the
[local calendar metadata format](../../references/local-inputs.md). Compare events
by title and time and show the differences. The user applies any changes
in their calendar app. To find conflicts on one calendar, use
`$executive-calendar-management`.

## First Use

1. Confirm both snapshot files represent the calendars the user intends to compare.
2. Use snapshots exported for the same narrow date range. The launcher reads the supplied files in full.
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

- Flag recurring and attendee-bearing meetings when those fields are available.
  Private records may contain only times and a generic title, so report
  ambiguous matches for manual review.
- When both ends of a linked event changed differently, report a conflict and
  ask the user which calendar is authoritative. Do not choose silently.
- Use exact calendar matching. Stop if the requested calendar is missing or
  ambiguous.
- Do not schedule this as an unattended mutating automation. A future monitor
  may run plan mode only and notify on meaningful changes or conflicts.
