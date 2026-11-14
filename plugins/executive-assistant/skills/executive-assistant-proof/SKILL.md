---
name: executive-assistant-proof
description: Proof and inspection skill for the Executive Assistant Codex Desktop package. Use when the user asks to verify the plugin is installed, confirm a Desktop project can see the package, inspect available package layers, or run a safe no-write package smoke test.
---

# Executive Assistant Proof

Use this as the smallest safe proof that the Executive Assistant package is visible.

## macOS and Linux checks

Check for `scripts/unix/ea.sh` and run `./scripts/unix/ea.sh check` from the plugin root to inspect the profile without writing to the vault. A present `.obsidian` directory indicates the folder has Obsidian settings. The check lists configured Outlook sources. Use `outlook mail` or `outlook calendar` when asked to verify actual source access. A `report daily` preview reads configured sources along with the vault.

## Behavior

- State that `executive-assistant-proof` loaded successfully.
- Inspect the current workspace for vault signals such as `HOME.md`, `Action-Items.md`, `AI-Workflows.md`, `_briefings/`, `meetings/`, `projects/`, `notes/`, or `tasks/00-Inbox/`.
- Identify which package layers are present: plugin manifest, skills, shell setup scripts, local metadata workflows, profile references, Atlassian and GitLab CLI docs, and vault template.
- Do not read email bodies.
- Do not send email.
- Do not write Jira, Confluence, Outlook, or vault files unless the user explicitly asks.

## Output

Return a concise proof report:

```text
Executive Assistant plugin proof: loaded.
Workspace: <path or unknown>
Vault signals found: <yes/no>
Available layers: <short list>
Next missing layer: <one sentence>
```

## Real Plugin Checks

When the plugin root is visible, check for these paths:

- `.codex-plugin/plugin.json`
- `skills/executive-assistant-setup/SKILL.md`
- `skills/executive-assistant-config/SKILL.md`
- `skills/executive-calendar-management/SKILL.md`
- `skills/executive-meeting-notices/SKILL.md`
- `scripts/unix/ea.sh`
- `references/local-inputs.md`
- `assets/vault-template/HOME.md`
