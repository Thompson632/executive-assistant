# Executive Assistant on Linux

The shell runner uses Bash 3.2+, Python 3.9+, and a local Markdown folder.
Obsidian can open the same folder. Use the Codex CLI to install the plugin.

## 1. Connect a vault

From the repository root:

```sh
bash install/unix/check-prereqs.sh
./plugins/executive-assistant/scripts/unix/ea.sh setup \
  --vault "$HOME/obsidian/Rob-Local-Laptop" --copy-template
```

Use any absolute vault path outside the repository. Omit `--copy-template`
to use an existing vault without copying starter notes. For an existing
profile, use `config` to inspect it, then preview a new path with
`config --vault "/absolute/path/to/vault"`. Add `--apply` to save the change.

## 2. Open the same folder in Obsidian

In Obsidian, choose **Manage Vaults → Open folder as vault**, then select the
`vault_path` reported by setup or `config`.

## 3. Install and verify the Codex plugin

```sh
bash install/unix/install-plugin.sh
./plugins/executive-assistant/scripts/unix/ea.sh check
./plugins/executive-assistant/scripts/unix/ea.sh report daily --write
```

Open a new Codex session in the vault folder and invoke
`$executive-assistant-proof`. Look for the report under `_briefings` in
Obsidian and follow a link to its source note.

To upgrade an existing installation, use the same checkout path registered for
the `personal` marketplace and rerun the installer. To move to a new checkout,
first inspect `codex plugin marketplace list`. Remove the previous marketplace
registration only if it belongs to this checkout and you intend to replace it.

## 4. Connect local Outlook mail and calendar (optional)

If an existing client or sync job keeps your Outlook mailbox in Maildir, or
produces a refreshed calendar metadata JSON file, enable the file-backed
provider in the [local Outlook setup guide](../plugins/executive-assistant/references/local-outlook.md).
Then run the commands for the feeds you configured:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh outlook mail
./plugins/executive-assistant/scripts/unix/ea.sh outlook calendar
./plugins/executive-assistant/scripts/unix/ea.sh report daily
```

Use `report daily --write --replace` to refresh the test report from step 3.

## Optional local schedule

With a running user cron service, preview a report job from a stable checkout:

```sh
./plugins/executive-assistant/scripts/unix/ea.sh schedule daily --at 06:00 --format cron
```

Run the report manually first. Add the reviewed line with `crontab -e`. To
verify one actual scheduled run, use a temporary test profile and time, then
verify the report and the log beside the profile. Remove the test line
afterward. To change or stop a regular report job, edit or remove its exact
line with `crontab -e`. The schedule uses the host's local time.

For weekly reports use `schedule weekly --at 05:30 --weekday Monday --format cron`.
For Codex schedules, generate reviewable prompts with `schedule-prompts`.
