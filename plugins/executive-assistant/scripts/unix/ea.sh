#!/bin/bash
set -euo pipefail

case "$(uname -s)" in
  Darwin|Linux) ;;
  *) printf '%s\n' 'Executive Assistant requires macOS or Linux.' >&2; exit 1 ;;
esac
if ! command -v python3 >/dev/null || ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))'; then
  printf '%s\n' 'Install Python 3.9 or later and put python3 on PATH.' >&2
  exit 1
fi
ea_script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
exec python3 "$ea_script_dir/ea.py" "$@"
