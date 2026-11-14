# Executive Assistant Repo Guide

## Purpose

This repo packages the reusable Codex Desktop executive-assistant workflow. It is separate from any individual executive's Obsidian vault or strategic memory repo.

## Operating Rules

- Do not commit personal vault content, email bodies, Outlook EntryIDs, StoreIDs, link-index files, tokens, or credentials.
- Keep user-specific values in local config, environment variables, or a private vault.
- Validate on macOS and Linux with Bash and Zsh where available.
- Keep calendar, mailbox, and task inputs local. Prepare drafts only on request. Never autosend.
- Use deterministic shell entry points and skills for repeatable reasoning workflows.
- Prefer MCP for durable live integrations once the script prototype is stable.
- Keep this package generic; put customer or executive-specific notes in their vault, not here.

## Implementation Boundaries

- Plugin: discovery, package identity, workflow entry points, and Desktop UX.
- Skills: daily brief, weekly review, meeting prep/debrief, action triage, Jira triage, Confluence refresh, and sensitivity review.
- Local inputs: supplied calendar, mail, and task metadata with local file previews.
- Atlassian CLI: project and page operations through installed `jira-cli` and `confluence-cli` until a dedicated MCP is justified.
- GitLab CLI: optional project review through an installed and authenticated `glab`.

## Validation

- Run plugin validation before handoff:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/executive-assistant
```

- Run skill validation after skill edits:

```bash
for skill in plugins/executive-assistant/skills/*; do
  python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$skill"
done
```

- Run `python3 -m unittest discover -s tests/unix -v` and `bash -n` on changed shell scripts. If the standalone plugin validator is unavailable, verify with a disposable plugin installation.
