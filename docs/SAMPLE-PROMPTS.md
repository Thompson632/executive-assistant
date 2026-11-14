# Executive Assistant Sample Prompts

Copy a prompt into Codex Desktop. For vault workflows, open your Obsidian
vault as a local Codex project. Replace bracketed examples with your own
names, dates, or paths. When a prompt refers to supplied notes or files,
paste the notes or attach the files in the same chat.

## Start here

| If you want to… | Go to |
| --- | --- |
| Capture something before you forget | [Quick note](#executive-jot-down-a-note) or [save a stopping point](#executive-pause-or-resume-work) |
| Add, reschedule, or finish a task | [Manage tasks](#executive-manage-tasks) |
| Turn meeting notes into actions | [Meeting debrief](#executive-prepare-for-or-debrief-a-meeting) or [one-on-one](#executive-one-on-one) |
| Decide what to do now or tomorrow | [Prioritize actions](#executive-prioritize-actions) or [prepare today’s brief](#executive-prepare-todays-brief) |
| Check or change a recurring brief | [Scheduled briefs](#set-up-scheduled-briefs) |

When Codex previews a change, review the destination and details. Continue
in the same chat with one of these replies:

> Apply that exact change.

> Change the due date to [date] and show me the revised preview.

> Leave it undated and save the proposed task.

## Browse by workflow

- [Set up and check your vault](#set-up-and-check-your-vault)
- [Capture and manage work](#capture-and-manage-work)
- [Review your day, week, and calendar](#review-your-day-week-and-calendar)
- [Work with meetings and email](#work-with-meetings-and-email)
- [Review project work and shared notes](#review-project-work-and-shared-notes)
- [Set up scheduled briefs](#set-up-scheduled-briefs)

## Set up and check your vault

### Executive First-Time Setup

> Use $executive-assistant-setup to connect my Obsidian vault at [absolute vault path]. Use my existing notes and show me which folder the profile points to.

> Use $executive-assistant-setup to create a vault at [absolute vault path] with the starter notes. Show me the folder to open in Obsidian.

### Executive Change Settings

> Use $executive-assistant-config to show my current vault path and preview changing it to [absolute vault path]. Wait for confirmation before saving the change.

### Executive Check Setup

> Use $executive-assistant-proof to check that the installed plugin can read my configured vault. Tell me which vault it found and whether local Outlook sources are configured.

> Use $executive-assistant-config to show which profile and vault this setup uses. Check the preferred brief times and tell me which schedule prompts this profile generates.

## Capture and manage work

### Executive Jot Down a Note

> Use $executive-quick-note to save this observation in my Obsidian vault: The shorter agenda gave us more time for decisions.

> Use $executive-quick-note to add this idea to my quick notes: Try sending decision questions a day before the meeting. Link it to [project note] if you find a match.

### Executive Pause or Resume Work

> Use $executive-context-switch to save where I left off on “Prepare the launch decision.” I compared both options. Next, add the support estimate. Preview the update to my existing action.

If a new task interrupts your current work, ask:

> Use $executive-context-switch. I’m pausing “Prepare the launch decision.” I compared both options and need to add the support estimate. A new task came up: confirm the room for Monday’s review. First step is to check the calendar invite. Preview the stopping point and the separate Inbox action.

In a fresh chat, ask:

> Use $executive-context-switch to pick up “Prepare the launch decision.” Show where I stopped, any blocker, and one next step.

### Executive Manage Tasks

> Use $executive-todo-management to preview adding these two tasks to my Obsidian Inbox: “Send the revised agenda,” due [date], and “Confirm the meeting room,” with no due date. Link them to [meeting note] if it exists. Wait for confirmation.

To update a deadline or add project context, ask:

> Use $executive-todo-management to find “Send the revised agenda,” preview changing its due date to [new date], and link it to [project note]. Keep it as one task.

To complete a task later, ask:

> Use $executive-todo-management to preview marking “Send the revised agenda” complete. Keep the due date and source link.

After reviewing the checkbox change, reply **Apply that exact change.**

### Executive Prioritize Actions

> Use $executive-action-triage to review my open Obsidian tasks. Give me up to three next actions, flag recorded deadlines and blockers, and link back to the original checkboxes.

> Use $executive-action-triage to show only what I’m waiting on. Include the owner, the next follow-up, and the source link where available.

At the end of the workday, ask:

> Use $executive-action-triage to propose my top three tasks for [next workday]. Include one first step and a link to each original action. Preview saving the plan to notes/Work Plans/[YYYY-MM-DD].md after I confirm the order.

## Review your day, week, and calendar

### Executive Prepare Today’s Brief

> Use $executive-daily-brief to show today’s meetings if calendar data is available, important mail if configured, and the open actions that need attention. Save today’s Markdown report in my configured vault and give me the link.

> Use $executive-daily-brief to start with today’s dated work plan if it exists. Check which linked tasks are still open, then tell me the first task to start. Give me the brief in chat.

### Executive Plan the Week

> Use $executive-weekly-review to summarize open commitments carrying into this week, calendar pressure, and decisions I need to make. Save the weekly review in my configured vault and give me the link.

> Use $executive-weekly-review to compare last week’s saved review with the current task list. Show what’s still open, what needs a decision, and three priorities for this week. Give me the review in chat.

### Executive Review My Calendar

> Use $executive-calendar-management to find overlapping meetings and short transitions on my calendar for [date range]. Suggest two possible focus blocks.

> Use $executive-calendar-management to review my next workday from this calendar snapshot. Flag back-to-back meetings and suggest where I can fit 45 minutes to work on [task].

### Executive Compare Two Calendars

Supply two calendar exports covering the same dates.

> Use $executive-calendar-sync to compare [first calendar export] with [second calendar export]. Show missing or changed events and flag ambiguous matches so I can review them.

> Use $executive-calendar-sync to compare my original export with the revised export for [date range]. Show each moved meeting with its old and new time and give me a list of changes to review.

## Work with meetings and email

### Executive Prepare for or Debrief a Meeting

> Use $executive-meeting-prep to prepare me for [meeting]. Read the supplied agenda and related vault notes. Give me the decisions I need, what to ask, and any open commitments.

After the meeting, paste the notes and ask:

> Use $executive-meeting-prep to pull decisions and follow-ups from these notes. Preview adding only my agreed actions to my task list. Keep stated due dates and flag missing ones.

After you see the preview, you can approve specific actions:

> Save only “Send the revised agenda” with the due date and meeting link shown in the preview.

### Executive One-on-One

> Use $executive-one-on-one to save these notes from my [date] 1:1 with [person]. Preserve the raw notes, summarize decisions, and preview adding only my agreed commitments to the Inbox. Wait for my confirmation before adding tasks.

After checking the task and date, reply:

> Add “[task title]” exactly as previewed, with its due date and link to the 1:1 note.

Before the next meeting, ask in a fresh chat:

> Use $executive-one-on-one to prepare for my next 1:1 with [person]. Give me a brief recap, commitments that are still open with known due dates, and up to three things to discuss.

> Use $executive-one-on-one to prepare for my [date] 1:1 with [person]. Check the latest notes and linked tasks, then save the prep as a separate note for that meeting date.

### Executive Draft a Meeting Invite or Reply

Supply the invitation or notice.

> Use $executive-meeting-notices to draft a reply declining this invitation and asking for the decision notes afterward. Show me the text I can send from my calendar app.

> Use $executive-meeting-notices to draft an invitation for [meeting title] on [date and time with time zone] for [attendees]. We need to decide [decision]. Show me a subject and agenda to review.

### Executive Review Mail or Draft a Reply

Use configured local Outlook metadata or attach a mail metadata file.

> Use $executive-outlook-com to show which recent messages need a reply. For [message], use the context I supplied to draft a short reply I can send myself.

> Use $executive-outlook-com to review these mail metadata records. Group them into needs a reply, waiting on someone else, and for reference. Flag anything you can’t tell from the supplied details.

## Review project work and shared notes

### Executive Review Jira Issues

> Use $executive-jira-triage to review open issues in [Jira project key]. Flag blocked or stale issues and propose any changes for me to review.

> Use $executive-jira-triage to compare open issues in [Jira project key] with the actions in [Obsidian note]. Show which already match and draft any missing tickets for review.

### Executive Review a GitLab Project

> Use $executive-gitlab-review to review [GitLab project URL]. Summarize blockers, merge requests waiting for review, and recent failed pipelines. Include links.

> Use $executive-gitlab-review to check recent pipelines for [branch or ref] in [GitLab project URL]. Link the failures and flag any merge requests waiting for review.

### Executive Draft a Confluence Update

> Use $executive-confluence-refresh to draft an update for [Confluence page] in [space] from these reviewed notes. Write it for [audience] and show me the draft before publishing.

> Use $executive-confluence-refresh to turn the confirmed decisions in these notes into a short FAQ for [audience]. Draft it for [space and parent page] and show it here for review.

### Executive Check Notes Before Sharing

> Use $executive-sensitivity-review to check [note or folder] before I share it with [audience]. Flag sections that should be redacted or kept private and explain each recommendation.

> Use $executive-sensitivity-review to review this draft for [audience]. Show the passages to remove and suggest replacement wording in chat.

## Set up scheduled briefs

### Executive Schedule Briefs and Follow-Ups

> Use $executive-scheduled-tasks to read my profile and preview standalone Codex automations for my daily brief and weekly review. Show the planned times, vault project, and report destination. Wait for my approval before creating or enabling them.

To check an existing schedule, ask:

> Use $executive-scheduled-tasks to check my existing daily brief automation. Show when it runs, which vault it targets, and whether its last run saved a report. Flag anything you can’t verify.

When ready, ask to create or enable the reviewed automations. The
[workflow diagrams and schedule guide](WORKFLOW-DIAGRAMS.md) show which
skills fit a recurring schedule.
