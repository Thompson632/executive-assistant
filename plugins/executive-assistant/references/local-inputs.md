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

Use strings for text and dates, Booleans for flags, and a nonnegative integer
for `attachment_count`. Required strings must be nonempty. Use an ISO 8601
offset or `Z` for mail and calendar timestamps. A calendar event must end
after it starts. The output for records marked private contains the start
and end times and a generic title.

## Try the metadata format

Save each JSON example in a separate file. These are snapshots, so the
commands review the file you supply. The [configured Outlook feed](local-outlook.md)
reads a local source that another client or sync job keeps current. The
configured calendar excludes canceled events.

### Mail

Save as `mail.json`.

```json
[
  {
    "subject": "Review the meeting agenda",
    "sender": "Taylor <taylor@example.invalid>",
    "received": "2026-11-14T14:00:00Z",
    "folder": "Inbox",
    "unread": true
  }
]
```

```sh
./scripts/unix/ea.sh review mail --source "/path/to/mail.json"
```

### Calendar

Save as `calendar.json`.

```json
[
  {
    "title": "Agenda review",
    "start": "2026-11-14T16:00:00Z",
    "end": "2026-11-14T16:30:00Z"
  }
]
```

```sh
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
```

### Tasks

Save as `tasks.json`.

```json
[
  {
    "title": "Review the meeting agenda",
    "status": "open",
    "due": "2026-11-14"
  }
]
```

```sh
./scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
```

## Review and draft commands

```sh
./scripts/unix/ea.sh review mail --source "/path/to/mail.json" --folder Inbox --limit 5 --offset 0
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json"
./scripts/unix/ea.sh review calendar --source "/path/to/calendar.json" --compare "/path/to/team-calendar.json"
./scripts/unix/ea.sh review tasks --source "/path/to/tasks.json"
./scripts/unix/ea.sh draft --subject "Decision review" --source "/path/to/body.md"
./scripts/unix/ea.sh audit
```

Mail review preserves file order and returns five records by default.
Use `--folder` for an exact folder match and `--since` for an inclusive
received-time filter. Paging applies after these filters.
For calendar comparison, supply both snapshots for the same time range.
The runner returns both sets of records for the Codex skill to compare.

## Attachment Filing and Local Paths

Preview a supplied file and its destination before saving:

```sh
./scripts/unix/ea.sh attachment --source "/path/to/input.pdf" --destination "/absolute/path/to/vault/input.pdf"
./scripts/unix/ea.sh resolve --path "/path/to/input.pdf"
```

After reviewing the preview, add `--apply --confirm-save "SAVE ATTACHMENTS"`
to copy the attachment. If preview reports that the destination exists,
choose a new filename. If it reports that a parent needs to be a folder,
choose a folder for the file. For a draft, put the body and any intended recipient
or meeting details in the source file. Add `--output PATH --apply` to save the
reviewed text. For both operations, use a new absolute destination inside the
vault without symlinks or parent traversal.

Reports skip drafts saved by the draft command and skip dot-prefixed folders.
Use `audit` for aggregate success and failure counts from the local audit
file beside the profile. It records operation and status only.
