---
name: executive-scheduled-tasks
description: Scheduled workflow setup for the Executive Assistant plugin. Use when the user asks to create Codex Scheduled Tasks, schedule daily briefs, weekly reviews, follow-up monitors, action updates, recurring executive assistant workflows, or generate schedule-ready prompts for Codex Desktop.
---

# Executive Scheduled Tasks

Prepare scheduled workflows for Codex Desktop and recover deterministic local
reports when the Codex scheduler/provider path is unavailable.

## Local schedules

For Codex schedules, use the requested vault as the local project and reference the daily brief or weekly review skill with the configured macOS profile and an explicit instruction to write the Markdown report. Verify one scheduled run produces the expected note.

For a local daily or weekly report, print a LaunchAgent plist on macOS or
a cron entry on Linux. Use a stable path for the project. For follow-up
monitoring and action synthesis, use a Codex schedule.

## Boundary

Codex Scheduled Tasks are created and managed in ChatGPT Desktop or web. Generate durable prompts, test them manually, and use the available Codex scheduling surface to confirm them.

Create every recurring Executive Assistant workflow as a standalone scheduled
task. Do not attach daily briefs, weekly reviews, follow-up monitors, or action
updates to an existing conversation as a heartbeat. A standalone task avoids
depending on a particular prior conversation, but it does not repair provider
or scheduler tool-call failures.

## Workflow

1. Confirm the Executive Assistant profile exists. Use its `scheduledTasks` preferences when present.
2. Generate prompts with `./scripts/unix/ea.sh schedule-prompts`.
3. Ask the user to test each prompt manually in a fresh normal Codex Desktop task before enabling the schedule.
4. Open the scheduling surface only when the user wants to configure schedules now.
5. Configure every recurring Executive Assistant workflow as a standalone scheduled task in the configured local project. Do not use a heartbeat or target an existing conversation.
6. Before leaving a new recurring schedule active, trigger one scheduler-run acceptance test and verify its expected local artifact or result.
7. Before replacing an existing recurring workflow, inspect its name, schedule, target type, and status. Obtain approval before pausing, deleting, or enabling an automation.
8. Keep scheduled runs no-autosend and no external writes unless the prompt explicitly requires approval.

## Recovery

If a scheduled Executive Assistant workflow fails with a function-call result
that is missing `call_id`, the failure is in the Codex scheduling or provider
conversation state. This can affect either a heartbeat or a standalone task.

1. Verify the daily-brief command manually in a fresh task.
2. Pause the failed schedule after user approval.
3. Preserve the reviewed prompt and schedule, then report the failure and the
   missing `call_id` evidence.
4. For deterministic daily and weekly reports, use the local scheduler below.
5. Verify one scheduler-run report and inspect its local log.
6. Follow-up monitoring and action updates still require a working Codex
   provider path.

## Local Report Fallback

From the installed plugin root:

```sh
# macOS
./scripts/unix/ea.sh schedule daily --at 06:00 --format launchd
# Linux
./scripts/unix/ea.sh schedule weekly --at 05:30 --weekday Monday --format cron
```

After reviewing the output, load the plist with `launchctl` or add the cron
line with `crontab -e`. Run one acceptance test and verify the artifact and log.
Local schedules generate reports only. They preserve the no-autosend and
no-external-writes boundaries.

## Codex Schedule Prompts

```sh
./scripts/unix/ea.sh schedule-prompts
```

## Recommended Templates

- Daily brief: use `$executive-daily-brief`, daily at the configured local time.
- Weekly review: use `$executive-weekly-review`, weekly on the configured day/time.
- Follow-up monitor: use `$executive-action-triage`, daily or workday afternoon.
- Action update: use `$executive-action-triage`, end of day.

Each prompt must mention the Executive Assistant profile name and must say not to send email or modify Jira/Confluence without explicit approval.
