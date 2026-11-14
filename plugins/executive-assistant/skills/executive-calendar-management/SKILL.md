---
name: executive-calendar-management
description: Review one calendar for conflicts, back-to-back meetings, and time for focused work. Suggest changes for the user to make.
---

# Executive Review My Calendar

Run a calendar review first. It uses configured local or supplied metadata and keeps the source calendar read-only.

## Workflow

1. Run `./scripts/unix/ea.sh outlook calendar` for a configured local calendar. Use `./scripts/unix/ea.sh review calendar --source PATH` if the user supplied a file. Default to seven days and normal work hours unless the user provides a different planning horizon.
2. Review conflicts, short transitions, unresponded meetings, long meetings, outside-hours events, and suggested focus blocks.
3. Combine the calendar findings with the active work list using `$executive-action-triage` when the user wants priority decisions, not just schedule hygiene.
4. Return a concise calendar scrub with:
   - `Keep`: strategic, decision-critical, or time-sensitive meetings.
   - `Change`: shorten, move, combine, or add an agenda/decision owner.
   - `Delegate`: attendance or follow-up that does not require the executive.
   - `Decline`: low-value, duplicative, or misaligned meetings, with a brief rationale.
   - `Protect`: focus blocks reserved for the highest-priority work.
5. Use `$executive-meeting-prep` for a specific meeting that needs context or a decision plan. Use `$executive-meeting-notices` only after the user selects an invitation or response action.

## Command

```sh
./scripts/unix/ea.sh outlook calendar --days 7
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
```

## Safety

- Treat calendar review as read-only. Do not move, delete, shorten, accept, decline, or create meetings from this skill.
- Do not infer meeting content from private appointments or generic event titles. Check what metadata the configured source provides before drawing conclusions about attendees or recurrence.
- Do not let an optimization heuristic override an explicit executive commitment or customer-facing need.
- Convert a requested calendar change into a reviewed meeting draft or response draft through `$executive-meeting-notices`; the user must explicitly approve the write.
