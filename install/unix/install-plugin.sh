#!/bin/bash
set -euo pipefail

ea_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd -P)
ea_codex=
if [[ ${1:-} == --codex && $# == 2 && $2 == /* ]]; then
  ea_codex=$2
elif [[ $# != 0 ]]; then
  printf '%s\n' 'Usage: install-plugin.sh [--codex /absolute/path/to/codex]' >&2
  exit 2
fi
bash "$ea_root/install/unix/check-prereqs.sh"

supports_plugin_install() {
  command -v "$1" >/dev/null &&
    "$1" plugin marketplace --help >/dev/null 2>&1 &&
    "$1" plugin add --help >/dev/null 2>&1
}

ea_candidate=${ea_codex:-codex}
if ! supports_plugin_install "$ea_candidate"; then
  ea_bundled_codex=/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex
  if [[ -z $ea_codex && $(uname -s) == Darwin ]] && supports_plugin_install "$ea_bundled_codex"; then
    ea_candidate=$ea_bundled_codex
    printf '%s\n' 'Using the Codex CLI bundled with ChatGPT Desktop.'
  elif ! command -v "$ea_candidate" >/dev/null; then
    printf '%s\n' 'No Codex CLI found. Install Codex or pass --codex /absolute/path/to/codex.' >&2
    exit 1
  else
    printf '%s\n' 'This Codex CLI cannot install plugins. Update Codex or pass --codex /absolute/path/to/codex.' >&2
    exit 1
  fi
fi
"$ea_candidate" plugin marketplace add "$ea_root"
"$ea_candidate" plugin add executive-assistant@personal
