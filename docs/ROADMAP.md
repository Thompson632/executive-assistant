# Roadmap

The [workflow guide](CODEX-WORKFLOWS.md) describes currently available
features. The remaining work below covers live validation and possible
extensions.

The [repository usability plan](superpowers/plans/2026-11-14-repository-usability.md)
tracks the first-run guide, recovery fixes, and release verification.

## Live validation

- Confirm a fresh Codex Desktop chat can load the installed proof skill and write a daily report to a test vault.
- Validate guided setup with a new user.
- Verify a standalone Codex automation writes to its intended local vault and capture any setup friction.
- Verify a scheduled run on each platform.
- Validate Work Intake against a live GitLab group and project with an authorized test request. Verify the Confluence preview against the intended page.

## Next

- Review whether additional local inputs need a dedicated MCP interface.
- Extend guided setup to collect Jira project and Confluence space preferences when requested. The [example profile](../config/executive-assistant.example.json) already shows where to store them.

## Later

- Add an Obsidian companion plugin only if filesystem-based vault operations are insufficient.
- Add admin-friendly documentation for deployment to other executives.
