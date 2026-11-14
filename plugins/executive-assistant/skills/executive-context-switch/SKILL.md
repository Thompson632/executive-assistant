---
name: executive-context-switch
description: Save where the user stopped on an Obsidian action, capture an interrupting task, or give the next step when they return to an action.
---

# Executive Pause or Resume Work

Put the context needed to resume next to the action in the user's Obsidian vault.
Use this for “Save where I left off,” “Capture this interruption as a task,”
or “Pick up the agenda.” For a detail to remember, use `$executive-quick-note`.
Resolve the vault from the user's selection or the configured profile. From
the installed plugin root, `./scripts/unix/ea.sh config` reports the profile's
`vault_path`. Read the relevant action list and any linked notes needed for the
handoff. If you cannot find or access the intended vault, say the handoff is
unsaved and show the proposed text.

## Save a stopping point

1. Find the existing action by its source link, title, and project. Use the
   action's current note and format. When a named action has two plausible
   matches, show the candidates and ask which one to update. For genuinely new
   work, follow the vault's conventions for incoming actions. If the vault
   has no action list, use the **Inbox** section of `Action-Items.md`.
2. Keep the checkbox title focused on the outcome. Add or update the stopping
   point directly below it or in the linked task note. Use one short line for
   the latest state and one for the first concrete step to take on return.
   Include a blocker or waiting condition and a source link when supplied and
   relevant. If the next step is a suggestion, label it as such. Preserve
   existing owners, due dates, status, and unrelated note content.
   For a new action, capture the stated due date or offer the optional
   due-date question from Manage Tasks in the same preview.
3. Preview the exact note change and use the local edit workflow in
   [Manage Tasks](../executive-todo-management/SKILL.md).
   Read the target again before applying the reviewed edit. Verify the saved
   change and reply with the action link. If the same handoff is already
   present, link to it without adding another copy.

Example entry for a plain Markdown action list

```markdown
- [ ] Prepare the launch decision [[projects/Launch]]
  - Left off — Compared both rollout options.
  - Resume — Add the support estimate to the rollout table.
```

## Pick up an action

Find the matching action and read its current stopping point and relevant
linked context. Give the action link, where it stands, and one concrete next
step. Surface a known blocker before the next step. When the saved context is
missing or conflicts with newer evidence, say so and label any proposed step.
If the user names no action and several could fit, offer up to three with one
line each and ask which to resume.

Resuming is read-only. For a request to save one action and resume another,
give the incoming action brief while the outgoing note edit is under review.
Treat a switch as a pause. Completion, reprioritization, and changes to other
systems belong to the user's separate instructions.
