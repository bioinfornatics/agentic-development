#!/usr/bin/env sh
# Tests for loop-gate plugin
set -e
PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$PLUGIN_ROOT/scripts/gate-reviewed.sh"

# 1. Script is executable
[ -x "$SCRIPT" ] || { echo "FAIL: gate-reviewed.sh not executable"; exit 1; }

# 2. Non-bd command passes through
payload='{"tool_input":{"command":"echo hello"}}'
result=$(printf '%s' "$payload" | sh "$SCRIPT" 2>&1)
[ -z "$result" ] && echo "PASS: non-bd command passes" || { echo "FAIL: unexpected output: $result"; exit 1; }

# 3. Closure must emit an explicit denial; exit 0 alone is not safety proof.
payload='{"tool_input":{"command":"bd close fake-id-xyz"}}'
result=$(printf '%s' "$payload" | sh "$SCRIPT")
printf '%s' "$result" | python3 -c 'import json,sys; assert json.load(sys.stdin)["decision"] == "block"'
echo "PASS: recognized closure explicitly denied"

# 4. No .loop state created
[ ! -d "$PLUGIN_ROOT/../../.loop" ] || { echo "FAIL: .loop state created"; exit 1; }
echo "PASS: no .loop state"

echo "All loop-gate plugin tests passed."
