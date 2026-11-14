# Executive Assistant on macOS

Codex and Obsidian share a folder of Markdown notes. The Mac workflow supports
vault setup, daily and weekly briefs, action triage, and meeting prep from notes.
Mail and calendar can also read from configured local clients. Drafts remain
text for manual review.

## 1. Connect a vault

You need Python 3.9 or newer for the local runner. From the repository folder:

```bash
python3 --version
./plugins/executive-assistant/scripts/unix/ea.sh setup \
  --vault "$HOME/Executive Assistant Vault" --copy-template
```

To use an existing vault, replace the example folder with its full path and
omit `--copy-template`. Use the folder that contains its notes and
`.obsidian` settings. The template is optional and adds missing starter files
without replacing your notes.

If you already have a profile, run the following to inspect it and preview a
vault change. Rerun the second command with `--apply` to save the change.

```bash
./plugins/executive-assistant/scripts/unix/ea.sh config
./plugins/executive-assistant/scripts/unix/ea.sh config \
  --vault "/absolute/path/to/your/vault"
```

The profile defaults to
`${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json`.
Use `--profile "/absolute/path/to/profile.json"` before a subcommand to use a
different profile. Keep the vault and profile outside this repository.

## 2. Open the same folder in Obsidian (optional)

1. Open Obsidian and select **Manage Vaults** in the vault switcher.
2. Select **Open folder as vault** and choose the `vault_path` printed by
   setup or `config`. If the vault is already open, switch to it.
3. For a new vault with the template, open **HOME** and follow the link to
   **Action-Items**. Add a test line such as `- [ ] Review next week's priorities`.

[Obsidian's guide to opening an existing folder](https://obsidian.md/help/vault)

## 3. Install and verify the Codex plugin

From the repository folder, register the local **Personal** marketplace
and install **Executive Assistant** with the Codex CLI:

```bash
bash install/unix/check-prereqs.sh
bash install/unix/install-plugin.sh
```

If you use the CLI bundled with ChatGPT Desktop on macOS, pass
`--codex /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex` to
`install-plugin.sh`. Open the vault folder as a local Codex project and
start a fresh chat with this prompt. Use a vault with a test checkbox or
another actionable note to verify the report's source links.

> Use $executive-assistant-proof to check the configured vault. Then use
> $executive-daily-brief and save today's report to the vault.

Find the report under `_briefings`. If you use the starter notes, follow the
report's link to `Action-Items.md`.

You can also test the file connection directly from the repository folder:

```bash
./plugins/executive-assistant/scripts/unix/ea.sh report daily --write
./plugins/executive-assistant/scripts/unix/ea.sh report weekly --write
```

Omit `--write` to preview. Report reruns preserve existing notes. Add
`--replace` to `--write` when you want to regenerate a report.

For updates or a moved checkout, follow the
[marketplace update steps](DISTRIBUTION.md#update-or-move-an-installation).

## 4. Connect local Outlook mail and calendar (optional)

Verify that your Outlook or Exchange account already syncs in Apple Mail or
Calendar. Enable the Apple provider in the [local Outlook setup guide](../plugins/executive-assistant/references/local-outlook.md).
Open the apps, then run the commands for the feeds you configured:

```bash
./plugins/executive-assistant/scripts/unix/ea.sh outlook mail
./plugins/executive-assistant/scripts/unix/ea.sh outlook calendar
./plugins/executive-assistant/scripts/unix/ea.sh report daily
```

If macOS prompts for Automation access, allow the terminal or Codex app you
plan to use. Calendar event titles are hidden by default to protect private
appointments. The report preview displays exactly what the runner would save.
Use `report daily --write --replace` to refresh the test report from step 3.

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
