# Local Workflow Recipes

## Morning Inbox Triage

1. Run `./scripts/unix/ea.sh outlook mail --limit 5` for the configured folder or `./scripts/unix/ea.sh review mail --source PATH --folder Inbox --limit 5` for a supplied file.
2. Review sender, subject, received time, and flags. Read message content only
   when explicitly requested and supplied.
3. For a supplied file, use `--offset 5` for the next page. Suggest next actions without sending mail.

## Drafting Replies for Review

1. Identify the selected message from supplied metadata.
2. Draft a reply using the relevant supplied text.
3. Show `./scripts/unix/ea.sh draft --subject TEXT --source PATH` output for review.
4. Let the user perform the final send in their mail client.

## Composing a Generic Email Draft

1. Collect To, optional Cc/Bcc, subject, plain-text body, importance, and sensitivity.
2. Preview with `./scripts/unix/ea.sh draft --subject TEXT --source PATH`.
3. After confirmation, add `--output PATH --apply` to file the unsent text in the
   vault. Keep message bodies and private metadata out of the audit and repository.

## Weekly Calendar Digest

1. Run `./scripts/unix/ea.sh outlook calendar --date YYYY-MM-DD --days 7` with the focus Monday, or `./scripts/unix/ea.sh review calendar --source PATH` on a supplied snapshot for the focus week.
2. Review conflicts, transitions, long meetings, and focus blocks.
3. Use `$executive-weekly-review` to combine the findings with vault actions.

## Scheduling a Meeting With Attendees

1. Collect subject, start, end, time zone, attendees, location, agenda, busy state, and reminder.
2. Preview the invitation with `./scripts/unix/ea.sh draft --subject TEXT --source PATH`.
3. Confirm before saving local text. The user sends the invitation from their calendar client.

## Attachment Filing

1. Select the supplied local attachment and confirm the destination folder.
2. Run `./scripts/unix/ea.sh attachment --source PATH --destination PATH` for the preview.
3. Show the exact source and destination. After confirmation rerun with
   `--apply --confirm-save "SAVE ATTACHMENTS"`.
4. Report the saved path. Reject traversal, symlinks, and existing destinations.
