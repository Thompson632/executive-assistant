---
name: executive-meeting-notices
description: Review a supplied meeting notice or draft an invitation, acceptance, or decline for the user to send in their calendar app.
---

# Executive Draft a Meeting Invite or Reply

Use supplied meeting metadata to review notices and draft invitation or response text. Keep sending in the user's chosen client.

## Workflow

1. Review the supplied notice or calendar snapshot. Identify the intended response target.
2. For a new meeting, collect subject, start and end time, time zone, location, recipients, agenda, busy status, and reminder preference.
3. Preview the text and present the exact draft.
4. Ask for explicit confirmation before saving a proposed local draft file.
5. Save a reviewed draft with `--output PATH --apply`.
6. Report the draft path. The user sends the draft in their chosen client.

## Commands

```sh
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
./scripts/unix/ea.sh draft --subject "Decision Review" --source "/path/to/meeting.md"
```

## Safety

- `--apply` saves local draft text. The user sends the invitation or response.
- Never add `--apply` without the user's explicit confirmation of the preview.
- Keep attendee lists, meeting links, notes, and responses out of the repository and shared vault unless the user explicitly directs otherwise.
- Review a meeting cancellation in the calendar client; this helper only drafts responses to incoming meeting requests.
