---
name: executive-assistant-setup
description: Connect a local folder when setting up Executive Assistant for the first time. Create a profile and add Obsidian starter notes if requested.
---

# Executive First-Time Setup

Configure the local runtime without committing user data.

## macOS and Linux setup

Use `scripts/unix/ea.sh` from the installed plugin root. Ask for the vault folder only if the user has not provided it and the current workspace does not identify it. For a new vault, suggest `~/Executive Assistant Vault`. Store the profile under `${CODEX_HOME:-$HOME/.codex}/executive-assistant/profiles/default.json`. Keep the vault outside the package repository.

```bash
./scripts/unix/ea.sh setup --vault "$HOME/Executive Assistant Vault"
./scripts/unix/ea.sh config
```

Add `--copy-template` when the user wants starter notes. For an existing profile use `$executive-assistant-config`. To connect Obsidian, have the user choose **Open folder as vault** and select the reported `vault_path`.

## Safety

- Keep profiles local or gitignored.
- Do not store credentials in the profile.
- Do not enable autosend. Prepare draft text only when requested.
