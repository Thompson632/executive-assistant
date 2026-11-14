#!/bin/bash
set -euo pipefail

ea_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd -P)
if (( BASH_VERSINFO[0] < 3 || (BASH_VERSINFO[0] == 3 && BASH_VERSINFO[1] < 2) )); then
  printf '%s\n' 'Install Bash 3.2 or later.' >&2
  exit 1
fi
bash "$ea_root/plugins/executive-assistant/scripts/unix/ea.sh" --help >/dev/null
printf '%s\n' 'Shell runtime prerequisites passed.'
