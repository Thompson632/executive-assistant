---
name: executive-daily-brief
description: Daily executive briefing workflow for Codex Desktop. Use when the user asks for a daily report, daily brief, morning reset, today plan, Outlook-plus-vault summary, or Obsidian briefing generated from calendar, important email metadata, and vault action signals.
---

# Executive Daily Brief

Generate a concise Markdown report for the user's current day. Treat configured local Outlook sources, supplied metadata, and the vault as read-only inputs.

## Local reports

From the installed plugin root, run `./scripts/unix/ea.sh report daily` to preview the vault-based report. Add `--write` if the user requested a file. The command returns the report path and preserves an existing report. Use `--replace` only when asked to regenerate it. For a nondefault profile, pass `--profile "/path/to/profile.json"` before `report`.

The preview includes configured local Outlook sources. Review explicitly supplied calendar or mail metadata using the local review commands. If a configured source fails, surface the error and check that source before retrying.

## Workflow

1. Resolve the local profile from `${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json` or a user-provided profile path.
2. Use `./scripts/unix/ea.sh report daily` from the plugin root.
3. Scan the vault for recent actionable signals: open checkboxes, follow-up, waiting, risk, open question, due, deadline, review requested, blocked, or decision needed.
4. Prioritize recent, actionable, blocked, time-sensitive, strategically important, or supplied priority-folder mail items.
5. Write or draft the report under `_briefings/YYYY-MM/Week of YYYY-MM-DD/YYYY-MM-DD Daily Report.md` when the user wants a file.
6. Do not autosend email. Create a draft only when explicitly requested.

## Report Shape

Use these sections unless the user asks otherwise:

- `# Daily Report - YYYY-MM-DD`
- `## Snapshot`
- `## Calendar Today`
- `## Important Unread Emails`
- `## Needs Attention Today`
- `## Recommended Moves`
- `## Waiting On`
- `## Risks To Watch`
- `## PTOs` only when PTO entries exist

Do not include `Recent Decisions` or `People And Projects In Motion` unless the user explicitly asks.

## Link Handling

Use links to source notes when available. Keep raw mail identifiers and email bodies out of the Markdown by default.

## Command

```sh
./scripts/unix/ea.sh report daily --write
```

## Scheduled Tasks

Create a recurring daily brief as a standalone scheduled task in the configured
local project. Do not attach it to an existing conversation as a heartbeat.
Before leaving the schedule active, verify one scheduled run produces its local
report. If either a heartbeat or a standalone task reports a missing function
`call_id`, pause it after user approval and treat the problem as a Codex
provider or gateway failure. For local report recovery, use the scheduler command in `$executive-scheduled-tasks`.
