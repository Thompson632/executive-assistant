---
name: executive-one-on-one
description: Save raw one-on-one notes by person and meeting date, summarize decisions and commitments, or prepare for the next 1:1 from prior notes and current actions.
---

# Executive One-on-One

Use this for “Save these notes from my 1:1 with Alex” or “Help me prepare
for my next 1:1 with Alex.” Resolve the user's selected local Obsidian vault
or read `vault_path` from `./scripts/unix/ea.sh config` at the installed
plugin root. Work inside that vault. Tell the user if the destination is
unavailable and give them the draft.

## Save a meeting

1. Identify the person and meeting date from the request or notes. Resolve
   relative dates in the user's local time. Use the existing folder for that
   person, or create `meetings/One-on-Ones/Person Name/` on the first save.
   Ask if the person or date is ambiguous. Use a safe folder name and keep
   all paths in the vault.
2. Use `YYYY-MM-DD.md` inside the person's folder. If a note exists for the
   same meeting, update it in place and keep previously captured material.
   Confirm before treating a second meeting on the same date as a separate
   note. Use a distinguishing suffix if needed.
3. Use the [meeting template](../../assets/vault-template/templates/One-on-One.md).
   Keep the summary short and the supplied raw notes intact. Record decisions,
   open questions, and actual commitments with the owner and due date when
   stated. Keep suggested follow-ups separate from agreed actions. Use
   plain bullets for meeting-note follow-ups.
4. If the user asks to add their commitments to the vault task list, preview
   them with [Executive Manage Tasks](../executive-todo-management/SKILL.md).
   Keep one checkbox per task and link back to the meeting note where the
   action list is private. In a shared list, use a shareable action title and
   include private links only when the user requests them.

Keep raw notes and prep in the private vault. For new meeting and prep notes,
start with the template's `type: executive-assistant-one-on-one` frontmatter
so routine shell briefs skip their contents. Keep private details in the
person's folder when writing other briefs or shared notes.

## Prepare for the next meeting

Read the latest meeting note, earlier notes needed for carryover, and the
current status of relevant vault tasks. Give a brief recap, open commitments
by owner with any recorded due dates, and up to three questions or decisions
to raise. Link back to the notes or tasks that support the brief. Use the
current checkbox state when an action was saved to the task list. Label
untracked follow-ups whose status still needs checking.

Return the prep in chat by default. If asked to save it and the next meeting
date is known, use `YYYY-MM-DD Prep.md` in the person's folder. Update an
existing prep note for that date in place. Keep the meeting record and
confirmed task changes in their own notes.
