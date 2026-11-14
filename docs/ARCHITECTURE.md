# Architecture

## Package Layers

The executive assistant package should stay split across four layers:

- Plugin: installable Codex Desktop package, workflow entry points, and user-facing metadata.
- Skills: reusable executive workflows that Codex can invoke from chat.
- Plugin-local scripts: platform-specific profile and report commands, using the shared shell launcher on macOS and Linux.
- Integrations: MCP servers or CLI tools, alongside local files and optional Obsidian. Configure any external MCP servers separately in Codex.
- Vault template: clean Obsidian structure stored inside the plugin under `assets/vault-template/`.

## Integration Direction

Calendar and mail can read explicitly configured local clients or sync files.
Supplied metadata remains available for calendar, mail, and tasks. Keep the
inputs metadata-first. Drafts stay local for user review.

Atlassian starts through `jira-cli` and `confluence-cli`. A dedicated MCP only makes sense if CLI invocation becomes too brittle or if richer typed operations are needed.

GitLab project review uses an existing authenticated `glab` installation. The
skill scopes reads to the selected project and uses GitLab links for follow-up.

Obsidian is primarily filesystem-backed. Add an Obsidian MCP only if direct app/plugin APIs become necessary.

## Data Boundary

The package repo contains code, templates, and workflow instructions. Each executive's vault contains their notes and generated reports. Private link stores, email identifiers, credentials, and local profile configuration remain outside git.

## First-Run Configuration

First-run setup uses `./scripts/unix/ea.sh setup --vault PATH` and optionally copies
the starter vault template. The resulting JSON profile lives at
`${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json`.

Use the [macOS](INSTALL-MACOS.md) or [Linux](INSTALL-LINUX.md) guide to connect
the same folder in Obsidian and Codex.

## Scheduled Tasks

The plugin prints schedule prompts with `./scripts/unix/ea.sh schedule-prompts`.
Use standalone Codex schedules so recurring workflows do not depend on a prior
conversation. Verify a scheduler-run result before relying on a schedule. If
a provider reports a missing `call_id`, preserve the prompt and error details
and verify a manual run before relying on another scheduled result.

The macOS LaunchAgent and Linux user cron paths run the same deterministic
report command. They write a local run log and preserve the no-autosend boundary.
Follow-up monitoring and synthesis still use Codex.
