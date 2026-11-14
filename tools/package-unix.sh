#!/bin/bash
set -euo pipefail

if [[ $# != 1 || $1 != *.zip ]]; then
  printf '%s\n' 'Usage: package-unix.sh OUTPUT.zip' >&2
  exit 2
fi
ea_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)
ea_output=$1
if [[ $ea_output != /* ]]; then
  ea_output=$PWD/$ea_output
fi
if [[ -e $ea_output || -L $ea_output ]]; then
  printf '%s\n' 'Choose a new ZIP path.' >&2
  exit 1
fi
ea_archive=$(mktemp "$(dirname -- "$ea_output")/.ea-archive.XXXXXX")
trap 'rm -f -- "$ea_archive"' EXIT
git -C "$ea_root" archive --format=zip --prefix=executive-assistant/ HEAD > "$ea_archive"
ln -- "$ea_archive" "$ea_output"
