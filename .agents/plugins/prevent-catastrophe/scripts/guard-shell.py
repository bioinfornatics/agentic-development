#!/usr/bin/env python3
"""Conservative direct-shell guard; not a general shell or wrapper firewall."""
import json
import shlex
import sys

def block():
    print(json.dumps({'decision': 'block', 'reason': 'SHELL-GUARD: unsafe or malformed direct shell request; use an approved bounded workflow'}))

def main():
    try:
        value = json.load(sys.stdin)
        command = value['tool_input']['command']
        if not isinstance(command, str):
            raise ValueError('command')
        words = shlex.split(command)
    except Exception:
        block()
        return
    if not words:
        return
    # Detect dangerous verb/option pairs anywhere in shell text. This is a
    # conservative guard, not an interpreter or authorization verifier.
    if any(w == 'sudo' or w == 'wipefs' or w.startswith('mkfs.') for w in words):
        block(); return
    if any(w == '--no-preserve-root' for w in words) or ':(){' in command:
        block(); return
    if 'git' in words and 'reset' in words and '--hard' in words:
        block(); return
    if 'git' in words and 'clean' in words and any(w in ('--force', '--directories') or
        (w.startswith('-') and any(c in w[1:] for c in 'fd')) for w in words):
        block(); return
    if 'dd' in words and any(w.startswith('of=/dev/') for w in words):
        block(); return
    if 'rm' in words:
        recursive = '--recursive' in words or any(w.startswith('-') and not w.startswith('--') and 'r' in w for w in words)
        if recursive and any(w == '/' or w.startswith('/*') for w in words):
            block(); return

if __name__ == '__main__':
    main()
