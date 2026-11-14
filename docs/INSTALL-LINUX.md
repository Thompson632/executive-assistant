# Executive Assistant on Linux

The shell runner uses Bash 3.2+, Python 3.9+, and a local Markdown folder called
a vault. Obsidian can open the same folder. Use the Codex CLI to install the plugin.
For the desktop interface, see the
[ChatGPT desktop preview for Linux](https://learn.chatgpt.com/docs/linux/linux-app).

## Prerequisites

Install the [Codex CLI](https://developers.openai.com/codex/cli) and put
`codex` on PATH. From the package folder, check the runtime:

```sh
bash install/unix/check-prereqs.sh
```

The [getting-started guide](GETTING-STARTED.md) walks through installation,
connecting a notes folder, and saving a report. If the executable is outside
PATH, pass `--codex /absolute/path/to/codex` to `install-plugin.sh`.

To view the notes in Obsidian, select **Open folder as vault** and choose
the notes folder reported by setup or `config`.

For updates or a moved checkout, follow the
[marketplace update steps](DISTRIBUTION.md#update-or-move-an-installation).
If installation stops because `personal` already points to another source, see
[marketplace name conflicts](DISTRIBUTION.md#marketplace-name-conflicts).

## Connect local Outlook mail and calendar (optional)

If an existing client or sync job keeps your Outlook mailbox in Maildir, or
produces a refreshed calendar metadata JSON file, enable the file-backed
provider in the [local Outlook setup guide](../plugins/executive-assistant/references/local-outlook.md).
Then run the commands for the feeds you configured:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh outlook mail
./plugins/executive-assistant/scripts/unix/ea.sh outlook calendar
./plugins/executive-assistant/scripts/unix/ea.sh report daily
```

Use `report daily --write --replace` to regenerate a saved report.

## Optional local schedule

With a running user cron service, preview a report job from a stable checkout:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh schedule daily --at 06:00 --format cron
```

Run the report manually first. Add the reviewed line with `crontab -e`. To
verify one actual scheduled run, use a temporary test profile and time, then
verify the report and the combined output and error log beside the profile.
A status of `existing` means the job kept a previously saved report.
Remove the test line
afterward. To change or stop a regular report job, edit or remove its exact
line with `crontab -e`. The schedule uses the host's local time.

For weekly reports use `schedule weekly --at 05:30 --weekday Monday --format cron`.
For Codex schedules, generate reviewable prompts with `schedule-prompts`.
