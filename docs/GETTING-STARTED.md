# Get your first daily brief

Executive Assistant turns the notes and open tasks in a folder into a daily
brief. The folder is called a vault. You can view it in Codex, a Markdown
editor, or Obsidian. If you only want to run the local report from the
terminal, open the package as described below and then follow the
[terminal instructions](#terminal-alternative).

## 1. Open the package

Extract the Executive Assistant ZIP, or use your existing checkout. Keep
the extracted `executive-assistant` folder somewhere you plan to leave it.
Open Terminal and run the command below. Replace the example path inside
the quotes with the full path to the folder you extracted. The `ls` command
should show `README.md` and the `install` folder.

```sh
cd "/path/to/executive-assistant"
ls
```

## 2. Install the plugin

Check the prerequisites for [macOS](INSTALL-MACOS.md) or
[Linux](INSTALL-LINUX.md). Run this command in the terminal:

```sh
bash install/unix/install-plugin.sh
```

Look for `Added plugin` and `Installed plugin root` in the output. Open
Codex in a fresh chat after installing. If the skill does not appear, see
[Troubleshooting](#troubleshooting).

## 3. Connect your notes folder and save a brief

1. Create an empty folder named **Executive Assistant Vault** or choose an
   existing notes folder. Keep your notes and the extracted package in
   separate folders, such as two folders side by side. Open the notes
   folder as a local project in Codex and start a fresh chat.
2. Paste the setup prompt below. For an existing folder of notes, ask to use
   the existing notes without copying the starter notes.

   > Use $executive-assistant-setup to connect this folder and add the starter notes. Tell me which folder you connected.

3. Open `Action-Items.md` and add this line under **Inbox**. If you skipped
   the starter notes, add it to any Markdown note in your folder.

   ```markdown
   - [ ] Review the meeting agenda
   ```

4. Ask Codex to check the folder and preview the report.

   > Use $executive-assistant-proof to check my notes folder. Then use $executive-daily-brief to preview today's brief in chat.

5. When the preview shows your task, ask to save it.

   > Save today's brief in my notes folder and give me the file link.

Open the file under `_briefings/YYYY-MM/Week of YYYY-MM-DD/`. The
`YYYY-MM-DD Daily Report.md` filename uses today's date. Under **Needs
Attention Today**, follow the **Action-Items** link back to your task.
If you used another note, look for its title instead.

## Terminal alternative

This route needs Bash and Python 3.9 or later. From the package folder,
set `ea_vault` to the folder you want to connect.
Run setup once for a new profile. If you already have a profile, use
[profile configuration](../plugins/executive-assistant/references/profile-schema.md#routine-configuration).

```sh
ea_vault="$HOME/Executive Assistant Vault"
./plugins/executive-assistant/scripts/unix/ea.sh setup --vault "$ea_vault" --copy-template
./plugins/executive-assistant/scripts/unix/ea.sh check
```

Add the test line above to `Action-Items.md`, then preview and save the brief.
The save command prints the exact file path under `output_path`.

```sh
./plugins/executive-assistant/scripts/unix/ea.sh report daily
./plugins/executive-assistant/scripts/unix/ea.sh report daily --write
```

The save command keeps a report already saved for today. Add `--replace`
with `--write` if you want to regenerate it.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| The installer asks for Python | Install Python 3.9 or later, then open a new terminal and check `python3 --version`. |
| The installer cannot find Codex | Use the CLI setup for [macOS](INSTALL-MACOS.md#prerequisites) or [Linux](INSTALL-LINUX.md#prerequisites). |
| The Codex CLI cannot install plugins | Update Codex or rerun the installer with `--codex` and the full path to a compatible executable. |
| Setup says a profile already exists | Use `$executive-assistant-config` to check which notes folder is connected or preview switching it. |
| The notes folder contains the package | Choose a separate folder. If you've already set up a profile, ask `$executive-assistant-config` to preview switching to the new folder. |
| The proof skill is missing | Check the installer output, restart Codex, and open a fresh chat in the notes folder. See the [update instructions](DISTRIBUTION.md#update-or-move-an-installation). |
| `personal` already points to another folder | Follow [marketplace name conflicts](DISTRIBUTION.md#marketplace-name-conflicts). |
| The notes folder is available and Outlook reports an error | Open the reported settings file. [Disable Outlook for vault-only use or configure a file source](../plugins/executive-assistant/references/local-outlook.md#configure-a-source). |

## Try another workflow

- [Copy a prompt for meetings, tasks, or weekly reviews](SAMPLE-PROMPTS.md).
- [Use optional Outlook mail or calendar files](../plugins/executive-assistant/references/local-outlook.md).
- [Set up a recurring brief](CODEX-WORKFLOWS.md#scheduled-tasks).
- [Work on the package](../DEVELOPING.md).
