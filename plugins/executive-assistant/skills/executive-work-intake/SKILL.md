---
name: executive-work-intake
description: Turn a new work request into an Obsidian action, a GitLab epic and linked delivery issues, and a Confluence Scrum of Scrums preview. Supports a local rehearsal in Obsidian.
---

# Executive Work Intake

Use this for a new request that needs delivery planning across Obsidian,
GitLab, and Confluence. Resolve the selected vault or run
`./scripts/unix/ea.sh config` from the installed plugin root. For a
rehearsal, read [Local rehearsal](references/local-rehearsal.md) and use its
local paths for every step. If live access is unavailable, offer the local
rehearsal or return the drafts. Keep the two modes distinct.

## Capture and plan

1. Capture the requester, desired outcome, source, and any stated deadline.
   Use [Executive Manage Tasks](../executive-todo-management/SKILL.md) to
   preview one Inbox action. Check for an existing action first. Apply the
   approved capture and link it to the epic once the epic exists.
2. Draft the epic title and description from the request. Include the
   outcome, scope, acceptance criteria, and open questions. Break that
   description into delivery issues with a title, outcome, acceptance
   criteria, and known dependencies for each. Flag assumptions and leave
   unconfirmed owners and dates unset. Show the epic and issue drafts together
   with the target group and project before creation.

## Create and verify

For live work, resolve the epic's GitLab group and each issue's project.
Use the available authenticated integration or `glab` and the target host's
supported [GitLab work-item workflow](https://docs.gitlab.com/api/graphql/epic_work_items_api_migration_guide/).
Executive GitLab Review can inspect existing issues and remains read-only.
Create the reviewed epic and issues after the user approves those writes.
Create the epic first, then create and verify each issue as a child of that
epic. Verify and retain the returned URLs. Reuse matching records when
resuming, check the actual state after any uncertain write, and report partial
progress with links before retrying. Use the same approach for local notes.

## Record the meeting and preview the update

When the user confirms the initial meeting happened, post exactly
`STATUS: Initial meeting held` to the epic once, using the approved target.
Check for an existing exact comment before posting. While the meeting is
unconfirmed, leave the comment pending and report that accurately.

Use [Executive Draft a Confluence Update](../executive-confluence-refresh/SKILL.md)
to preview the Scrum of Scrums entry for the specified page. Include the epic
and issue links, the confirmed meeting status, the next milestone if known,
and any blockers or open questions. Show the preview and stop there.
Return links to the Obsidian action, epic, issues, and any local preview,
with any pending steps called out.
