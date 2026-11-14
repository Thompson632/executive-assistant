---
name: executive-quick-note
description: Save a short observation, idea, or decision in Obsidian. Use when the user asks to jot something down or remember a detail.
---

# Executive Jot Down a Note

For example, “Jot down that the room layout worked well.”

Resolve the vault from the user's explicit selection or the Executive
Assistant profile. From the installed plugin root, run
`./scripts/unix/ea.sh config` to find the configured `vault_path`.
If the intended vault is unavailable, show the note and say it is unsaved.

Use the user's chosen note or their existing quick-capture convention.
Otherwise, use `notes/Quick Notes.md` in the vault and create it on the first
save. Add one concise bullet under the current local date (YYYY-MM-DD).
Preserve dates, names, decisions, and wording that affect meaning.
Include a vault-relative Obsidian link when the user identifies a matching
project or source note. Keep the entry as a note bullet.

If the user explicitly asks to track a commitment, use
[Pause or Resume Work](../executive-context-switch/SKILL.md) for that
action. When a quick note contains a possible follow-up, capture the note
and mention the follow-up as an option.

When the user asks to save, reread the target and make a targeted edit.
Create only the requested note or entry, preserve surrounding text, and
link to an identical entry already present. For requests to draft or preview,
show the text in chat. Verify any save and reply with one line and a note link.
