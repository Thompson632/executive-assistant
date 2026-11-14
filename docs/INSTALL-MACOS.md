# Executive Assistant on macOS

Executive Assistant uses a local folder of Markdown notes, called a vault.
Open it in Codex for daily and weekly briefs, action triage, and meeting prep.
You can also open the same folder in Obsidian.

## Prerequisites

You need Bash 3.2 or later, Python 3.9 or later, and the Codex CLI or the
CLI bundled with ChatGPT Desktop. From the package folder, check the runtime:

```sh
bash install/unix/check-prereqs.sh
```

The [getting-started guide](GETTING-STARTED.md) walks through installation,
connecting a notes folder, and saving a report. If the CLI on PATH is
missing or cannot load the plugin command, the installer tries the copy
bundled with ChatGPT Desktop in `/Applications`. For a different location,
pass `--codex /absolute/path/to/codex` to `install-plugin.sh`.

To view the notes in Obsidian, select **Open folder as vault** and choose
the notes folder reported by setup or `config`.
[Obsidian's guide](https://obsidian.md/help/vault) shows where to find that option.

For updates or a moved checkout, follow the
[marketplace update steps](DISTRIBUTION.md#update-or-move-an-installation).
If installation stops because `personal` already points to another source, see
[marketplace name conflicts](DISTRIBUTION.md#marketplace-name-conflicts).

## Connect local Outlook mail and calendar (optional)

If an existing client or sync job keeps your Outlook mailbox in Maildir, or
produces a refreshed calendar metadata JSON file, enable the file-backed
provider in the [local Outlook setup guide](../plugins/executive-assistant/references/local-outlook.md).
Then run the commands for the feeds you configured:

```bash
./plugins/executive-assistant/scripts/unix/ea.sh outlook mail
./plugins/executive-assistant/scripts/unix/ea.sh outlook calendar
./plugins/executive-assistant/scripts/unix/ea.sh report daily
```

Use `report daily --write --replace` to regenerate a saved report.

## Optional local schedule

The following creates a 6 a.m. daily report for the signed-in Mac user. Run it
from a stable location the LaunchAgent can read. If the agent cannot read a
checkout under Desktop or Documents, use a checkout in an unprotected folder
such as `~/Developer` and regenerate the plist. The generated plist records the absolute script,
Python, and profile paths. Review the plist before loading it.

```bash
mkdir -p "$HOME/Library/LaunchAgents"
ea_agent="$HOME/Library/LaunchAgents/local.executive-assistant.daily.plist"
ea_domain="gui/$(id -u)"
(
  set -o noclobber
  ea_plist="$(./plugins/executive-assistant/scripts/unix/ea.sh schedule daily --at 06:00 --format launchd)" &&
    printf '%s\n' "$ea_plist" > "$ea_agent"
)
plutil -lint "$ea_agent"
```

After the plist passes validation:

```bash
launchctl bootstrap "$ea_domain" "$ea_agent"
launchctl kickstart "$ea_domain/local.executive-assistant.daily"
```

Check the output path in the agent's `StandardOutPath` log and open the
reported note. The agent uses the Mac's local time. To schedule a weekly
report, use `schedule weekly --at 05:30 --weekday Monday` and use `weekly` in
the filename and launchctl label. To unload an agent, run
`launchctl bootout "$ea_domain" "$ea_agent"`.

For scheduled Codex synthesis, use a standalone Codex schedule in the local
vault project and verify the first run.

If an existing LaunchAgent points to an older checkout or plugin cache, unload it
and regenerate the plist from the new stable path before reloading.
