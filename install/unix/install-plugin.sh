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

if [[ -z $ea_codex ]]; then
  ea_codex=codex
  if ! "$ea_codex" plugin marketplace --help >/dev/null 2>&1 && [[ $(uname -s) == Darwin ]]; then
    ea_bundled_codex=/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex
    if "$ea_bundled_codex" plugin marketplace --help >/dev/null 2>&1; then
      ea_codex=$ea_bundled_codex
      printf '%s\n' 'Using the Codex CLI bundled with ChatGPT Desktop.'
    fi
  fi
fi

if ! command -v "$ea_codex" >/dev/null; then
  printf '%s\n' 'No Codex CLI found. Install Codex or pass --codex /absolute/path/to/codex.' >&2
  exit 1
fi
"$ea_codex" plugin marketplace add "$ea_root"
"$ea_codex" plugin add executive-assistant@personal
