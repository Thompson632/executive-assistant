# Local Outlook Mail and Calendar

The shell launcher reads local Outlook or Exchange metadata on demand from a
Maildir folder or calendar metadata file. Your client or sync job keeps the
source current and handles account authentication.

## Configure a source

Edit the `outlook` object in your local profile. The default profile is
`${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json`.
If you run commands with `--profile PATH`, edit that file.
If your profile uses an older provider, replace its `outlook` object with the
example below and set the paths for your sources. For vault-only use, set
`outlook.enabled` to `false`.

Use a Maildir already maintained by your mail client or sync job. For the
calendar, point to a metadata JSON file kept current by your existing local
calendar workflow. The file uses the [local calendar format](local-inputs.md).
Include concrete event occurrences and have the producer publish its file
atomically so reports always read a complete copy.

```json
"outlook": {
  "enabled": true,
  "provider": "local",
  "maildir": "/absolute/path/to/maildir/Inbox",
  "calendarFile": "/absolute/path/to/synced-calendar.json"
}
```

Omit either path to enable just one source. The Maildir folder must contain
`cur/` and `new/`. The launcher uses file modification times for mail
recency, as supplied by the sync client, and extracts subject and sender
from the headers of selected messages. The calendar reader uses date ranges
from the JSON and redacts records marked `private`.

## Test and use in reports

From the installed plugin root, run the commands for the sources you enabled:

```sh
./scripts/unix/ea.sh check
./scripts/unix/ea.sh outlook mail --days 7 --limit 5
./scripts/unix/ea.sh outlook calendar --days 7
./scripts/unix/ea.sh report daily
./scripts/unix/ea.sh report weekly
```

`check` reports configured providers. The `outlook` reads verify actual access.
Mail looks back from the focus date, includes unread or flagged messages,
and sorts newest first. Calendar looks forward from the focus date and
includes events overlapping that window. The window includes the focus date
and uses the local time zone. Both commands default to seven days and accept
`--days` from 1 to 31 and `--date YYYY-MM-DD`. Mail defaults to five records
and accepts `--limit` from 1 to 50.

Daily and weekly reports include their calendar window and up to ten unread
or flagged items from the seven days ending on the focus date. A source read
error stops generation with an error so it cannot appear as an empty inbox
or free calendar. Add `--write` to save a report, and use `--write --replace`
to refresh an existing report. Keep a vault receiving mail subjects and
calendar metadata private.

Scheduled jobs need local read access to the configured sources. To return to
vault-only reports, set `outlook.enabled` to `false`.
