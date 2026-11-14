---
name: executive-assistant-config
description: Inspect and safely update a local Executive Assistant profile for Codex Desktop. Use when the user says "Executive Assistant config," wants to view or open their profile JSON, change vault/project location, inspect saved preferences, or preview a vault path change.
---

# Executive Assistant Config

Use the local profile manager for normal profile changes. It preserves fields the user did not name and writes only after an explicit preview and confirmation.

## macOS and Linux configuration

Use `./scripts/unix/ea.sh config` from the installed plugin root to inspect the active profile and vault. Add `--profile "/path/to/profile.json"` before `config` for a different profile. To change the vault, run `config --vault "/absolute/path/to/vault"` to preview. Add `--apply` after the user confirms the change, then rerun `config`.

## Safety

- Use `config` for routine updates. The `setup` command requires a new profile path.
- Do not put profiles, Outlook identifiers, link stores, credentials, or vault content in this repository.
