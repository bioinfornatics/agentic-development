#!/usr/bin/env sh
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 2
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'SHELL-GUARD: Python runtime unavailable' >&2
  exit 2
fi
exec python3 "$SCRIPT_DIR/guard-shell.py"
