---
name: executive-meeting-prep
description: Prepare for one meeting from its agenda and related notes, or pull decisions and follow-ups from notes after it ends.
---

# Executive Prepare for or Debrief a Meeting

Support both pre-meeting preparation and post-meeting debrief.

On macOS and Linux, if the vault is outside the current project, use `./scripts/unix/ea.sh config`
from the installed plugin root to resolve its folder. Use that folder for the note workflow.

## Prep Workflow

1. Identify the meeting title, attendees, time, agenda, and relevant vault notes.
2. Search projects, meetings, notes, and action items for related context.
3. Surface open commitments, likely decisions, risks, and questions.
4. Produce a short prep note with objectives, context, key questions, and recommended moves.
5. For schedule conflicts, focus-time protection, or keep/change/delegate/decline decisions, use `$executive-calendar-management` before preparing the selected meeting.

## Debrief Workflow

1. Read the user's meeting notes or transcript-derived notes.
2. Extract decisions, actions, owners, due dates, blockers, and follow-up messages.
3. Suggest where durable items should land: vault action list, project note, Jira, or Confluence.
4. Do not create external tickets, pages, or emails until the user approves.

## Output

Prefer concise Markdown with wiki links when referencing vault notes.
