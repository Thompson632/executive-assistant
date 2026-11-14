---
name: executive-assistant-proof
description: Check that the Executive Assistant plugin and its configured notes folder are available. Use after installing or changing the setup, or when a skill cannot find the vault.
---

# Executive Check Setup

Use this as the smallest safe proof that the Executive Assistant package is visible.

## macOS and Linux checks

Check for `scripts/unix/ea.sh` and run `./scripts/unix/ea.sh check` from the plugin root to inspect the profile without writing to the vault. A present `.obsidian` directory indicates the folder has Obsidian settings. The check lists configured Outlook sources. Use `outlook mail` or `outlook calendar` when asked to verify actual source access. A `report daily` preview reads configured sources along with the vault.

If the result includes `outlook_error`, report that the notes folder is
available and give the `profile_path` with the Outlook diagnostic. Explain
how to disable Outlook for vault-only use or
[configure a file source](../../references/local-outlook.md).

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
