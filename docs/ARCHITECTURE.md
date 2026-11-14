# Architecture

## Package Layers

The Executive Assistant package has five parts.

- The plugin manifest and marketplace register the package and expose its metadata to Codex.
- The [skills](CODEX-WORKFLOWS.md#which-commands-the-skills-use) guide workflows that Codex can invoke from chat.
- The Bash launcher delegates profile management, metadata review, report generation, and schedule output to a shared Python runtime on macOS and Linux.
- Optional integrations use local files or separately configured CLIs or MCP servers.
- The vault template under `assets/vault-template/` adds starter Markdown notes and folders during opt-in setup.

## Integration Direction

Calendar and mail can read explicitly configured local sync files.
Supplied metadata remains available for calendar, mail, and tasks. Keep the
inputs metadata-first. Drafts stay local for user review.

Atlassian skills invoke separately installed and authenticated
[`jira-cli` and `confluence-cli`](../integrations/atlassian-cli/README.md).

GitLab project review uses an existing authenticated `glab` installation. The
skill scopes reads to the selected project and uses GitLab links for follow-up.
The [Work Intake skill](WORKFLOW-DIAGRAMS.md#take-a-new-work-request-from-intake-to-scrum-of-scrums)
coordinates approved GitLab epic, issue, and comment writes when live access
is available. It stops at a Confluence preview. A local rehearsal uses
Markdown notes in the selected vault for both services.

Obsidian opens the vault as a local folder. The runtime reads and writes
Markdown through the filesystem.

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
The [Codex workflow guide](CODEX-WORKFLOWS.md#scheduled-tasks) covers
registration and verification of standalone schedules.

The macOS LaunchAgent and Linux user cron paths run the same deterministic
report command with absolute paths to Python, the script, and the profile.
They write a run log beside the profile. Follow-up monitoring and synthesis
use Codex.
