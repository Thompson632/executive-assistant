# Local workflow inputs

Run commands from the installed plugin root. For mail and calendar sources
that your client or sync job keeps current, see [local Outlook](local-outlook.md).
Keep supplied files in a private folder outside the package. Input JSON is
an array of objects.

| Kind | Required fields | Optional fields |
| --- | --- | --- |
| Mail | `subject` | `sender`, `received`, `folder`, `unread`, `flagged`, `attachment_count` |
| Calendar | `title`, `start`, `end` | `location`, `status`, `recurring`, `private`, `has_attendees`, `all_day` |
| Tasks | `title` | `due`, `status`, `priority`, `source` |

Use strings for text and dates, Booleans for flags, and an integer for
`attachment_count`. Include an ISO 8601 time zone offset in timestamps.

```sh
./scripts/unix/ea.sh review mail --source "/path/to/mail.json" --folder Inbox --limit 5 --offset 0
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json" --compare "/path/to/team-calendar.json"
./scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
./scripts/unix/ea.sh draft --subject "Decision review" --source "/path/to/body.md"
./scripts/unix/ea.sh audit
```

Use `--since "2026-11-14T00:00:00-05:00"` for a mail timestamp filter.
Prepare both snapshots for the same time range before comparing calendars.
The review command prints allowlisted metadata for analysis. It does not
export data or update a calendar, mailbox, or task service.

## Attachment Filing and Local Paths

Preview a supplied file and its destination before saving:

```sh
./scripts/unix/ea.sh attachment --source "/path/to/input.pdf" --destination "/absolute/path/to/vault/input.pdf"
./scripts/unix/ea.sh resolve --path "/path/to/input.pdf"
```

After reviewing the preview, add `--apply --confirm-save "SAVE ATTACHMENTS"`
to save it. For an email or meeting draft, add `--output PATH --apply` to
the draft command after confirmation. Use a new destination inside the vault. Reports skip drafts saved by the
draft command. Keep private attachments in a dot-prefixed folder to exclude
them from report scans.
