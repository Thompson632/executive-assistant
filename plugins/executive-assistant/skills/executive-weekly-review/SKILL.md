---
name: executive-weekly-review
description: Plan the upcoming week using open actions, past briefs, and available calendar details. Use to review carryover, risks, and upcoming decisions.
---

# Executive Plan the Week

Prepare a forward-looking weekly report. Include meaningful carryover from the prior week, but avoid stale noise.

## Local reports

From the installed plugin root, run `./scripts/unix/ea.sh report weekly` to preview the vault-based report. Add `--write` if the user requested a file. The command returns the report path and preserves an existing report. Use `--replace` only when asked to regenerate it. For a nondefault profile, pass `--profile "/path/to/profile.json"` before `report`.

The preview includes configured local Outlook sources. Review explicitly supplied calendar or mail metadata using the local review commands. If a configured source fails, surface the error and check that source before retrying.

## Workflow

1. Compute the Monday for the focus week.
2. Review upcoming calendar load, critical meetings, travel/PTO indicators, and high-signal unread or flagged Outlook items.
3. Review latest `_briefings/` files for continuity, then scan vault action areas for unresolved commitments and risks.
4. Optionally review active Jira work when the user has configured a project and asks for Jira context.
5. Produce a concise Markdown plan. When file output is requested, use the vault's weekly report path under `_briefings/YYYY-MM/Week of YYYY-MM-DD/YYYY-MM-DD Weekly Report.md`. Use `./scripts/unix/ea.sh report weekly --write` for the shell-generated report.
6. Do not close Jira issues, publish Confluence, or send email without explicit approval.

## Synthesized Report Shape

Use these sections when synthesizing a review in Codex. The shell command
writes the standard sections listed in the [runtime reference](../../references/unix-runtime.md#daily-and-weekly-reports).

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
