---
name: executive-weekly-review
description: Weekly executive planning workflow for Codex Desktop. Use when the user asks for a weekly report, Monday reset, upcoming week review, carryover review, or executive plan synthesized from Outlook, vault actions, Jira, and recent briefings.
---

# Executive Weekly Review

Prepare a forward-looking weekly report. Include meaningful carryover from the prior week, but avoid stale noise.

## Local reports

From the installed plugin root, run `./scripts/unix/ea.sh report weekly` to preview the vault-based report. Add `--write` if the user requested a file. The command returns the report path and preserves an existing report. Use `--replace` only when asked to regenerate it. For a nondefault profile, pass `--profile "/path/to/profile.json"` before `report`.

The preview includes configured local Outlook sources. Review explicitly supplied calendar or mail metadata using the local review commands. If a configured source fails, surface the error and check that source before retrying.

## Workflow

1. Compute the Monday for the focus week.
2. Review upcoming calendar load, critical meetings, travel/PTO indicators, and high-signal unread or flagged Outlook items.
3. Review latest `_briefings/` files for continuity, then scan vault action areas for unresolved commitments and risks.
4. Optionally review active Jira work when the user has configured a project and asks for Jira context.
5. Produce a concise Markdown plan under `_briefings/YYYY-MM/Week of YYYY-MM-DD/YYYY-MM-DD Weekly Report.md` when file output is requested. Use `./scripts/unix/ea.sh report weekly --write` from the plugin root.
6. Do not close Jira issues, publish Confluence, or send email without explicit approval.

## Recommended Sections

- `# Weekly Report - Week of YYYY-MM-DD`
- `## Snapshot`
- `## Calendar This Week`
- `## Important Unread Emails`
- `## Carryover From Last Week`
- `## Needs Attention This Week`
- `## Recommended Moves`
- `## Waiting On`
- `## Risks To Watch`
- `## PTOs` only when PTO entries exist

## Command

```sh
./scripts/unix/ea.sh report weekly --write
```
