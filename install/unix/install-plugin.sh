#!/bin/bash
set -euo pipefail

ea_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd -P)
ea_codex=codex
if [[ ${1:-} == --codex && $# == 2 && $2 == /* ]]; then
  ea_codex=$2
elif [[ $# != 0 ]]; then
  printf '%s\n' 'Usage: install-plugin.sh [--codex /absolute/path/to/codex]' >&2
  exit 2
fi
bash "$ea_root/install/unix/check-prereqs.sh"
if ! command -v "$ea_codex" >/dev/null; then
  printf '%s\n' 'Install Codex or provide its executable with --codex.' >&2
  exit 1
fi
"$ea_codex" plugin marketplace add "$ea_root"
"$ea_codex" plugin add executive-assistant@personal
