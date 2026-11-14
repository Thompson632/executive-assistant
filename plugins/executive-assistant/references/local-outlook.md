# Local Outlook Mail and Calendar

The shell launcher can read Outlook or Exchange metadata from a local client
or sync folder. It reads the configured source each time you run a command.
The client or sync job controls how current that source is and handles account
authentication. Executive Assistant makes its reads through macOS Automation
or the local filesystem.

## Configure a source

Edit the `outlook` object in your local profile. Run `./scripts/unix/ea.sh config`
to find its path. The default profile is
`${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json`.
If you migrated a profile from the former Outlook integration, replace its
`outlook` object with one of the examples below.

### Apple Mail and Calendar on macOS

Use an Outlook or Exchange account already syncing to Apple Mail or Calendar.
Use exact names as shown in the apps. Choose a top-level folder in the
specified Mail account and a uniquely named calendar.

```json
"outlook": {
  "enabled": true,
  "provider": "apple",
  "mailAccount": "Work Exchange",
  "mailFolder": "Inbox",
  "calendarName": "Work Calendar"
}
```

Omit both mail fields for calendar only, or omit `calendarName` for mail only.
Open the configured apps in your signed-in macOS session. The first read may
ask you to allow Automation for the terminal or Codex session making the
request. Apple Calendar supplies event times and generic titles by default.
For a calendar whose titles are safe to copy to your private reports, you can
set `"includeCalendarTitles": true`. The Calendar scripting interface does
not identify private events, and recurring occurrences depend on what the
app returns through its scripting interface.

Confirm the account already syncs in Apple Mail or Calendar before enabling
this provider. If Apple Mail or Calendar can no longer sign in to Exchange
Online or sync, ask your Exchange administrator to check the tenant's
settings. [Apple's Exchange sync guidance](https://support.apple.com/en-us/149092)

### Local sync files on Linux or macOS

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

The Apple provider requires a signed-in session with the apps open and
Automation available to the process running the command. Verify a scheduled
read independently if you plan to use it. File-backed sources can be used by
scheduled jobs with local read access. To return to vault-only reports, set
`outlook.enabled` to `false`.
