#!/usr/bin/env python3
"""Best-effort shell closure guard, not an authorization or shell security boundary.
Recognized shell closure is disabled pending a protected host-mediated broker.
check_receipt is a non-authoritative consistency utility, never an unlock path.
It checks a receipt in issue metadata against a separately managed registry.
The registry is outside this repository and must be provisioned by a trusted host
or human, never by the builder. Same-UID file permissions do not isolate hostile
agents with arbitrary file-write access. Opaque wrappers require host policy.
"""
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

ID = re.compile(r'^[A-Za-z0-9._-]+$')

def deny(reason):
    print(json.dumps({'decision': 'block', 'reason': 'LOOP-GATE: ' + reason}))
    return 0

def closure_ids(command):
    # Retain quote/escape provenance while splitting only plain shell operators.
    # This bounded scanner is not a shell interpreter (wrappers remain host policy).
    quote = None;escaped = False;start = 0;segments = []
    for index, char in enumerate(command):
        if escaped:
            escaped = False;continue
        if char == chr(92) and quote != chr(39):
            escaped = True;continue
        if quote:
            if char == quote:quote = None
            continue
        if char in (chr(39), chr(34)):
            quote = char;continue
        if char in ';&|<>' or char == chr(10):
            segments.append(command[start:index]);start = index + 1
    if segments:
        segments.append(command[start:])
        for segment in segments:
            if segment.strip() and closure_ids(segment):
                raise ValueError('complex closure must use protected host workflow')
        return []
    try:
        tokens = shlex.split(command)
    except ValueError:
        raise ValueError('malformed shell syntax')
    if not tokens:
        return []
    direct = tokens[0] == 'bd'
    def closed_status(words):
        i = 0
        while i < len(words):
            word = words[i]
            if word in ('--notes', '--reason', '--title', '--description'):
                i += 2
                continue
            if word in ('--status', '-s'):
                if i + 1 < len(words) and words[i + 1] == 'closed':return True
                i += 2
                continue
            if word in ('--status=closed', '-sclosed', '-s=closed'):return True
            i += 1
        return False
    closing = len(tokens) > 1 and (tokens[1] == 'close' or
        (tokens[1] == 'update' and closed_status(tokens[2:])))
    if not direct:
        if 'bd' in tokens:
            tail = tokens[tokens.index('bd') + 1:]
            if 'close' in tail or ('update' in tail and closed_status(tail)):
                raise ValueError('wrapped closure is unsupported')
        return []
    if not closing:
        # Ordinary show/update arguments are data, not status or global options.
        if len(tokens) > 1 and tokens[1].startswith('-') and (
                'close' in tokens[2:] or ('update' in tokens[2:] and closed_status(tokens[2:]))):
            raise ValueError('unsupported global options for closure')
        return []
    if any(c in command for c in (';', '&', '|', chr(10), '$', chr(96), '(', ')', '<', '>')):
        raise ValueError('complex closure must use the explicit verified closure workflow')
    if len(tokens) < 3 or tokens[1] not in ('close', 'update'):
        raise ValueError('closure syntax is unsupported')
    ids = []
    index = 2
    while index < len(tokens):
        word = tokens[index]
        if word.startswith('--reason=') or word.startswith('--status='):
            index += 1
            continue
        if word in ('--reason', '--status', '-s'):
            index += 2
            continue
        if word in ('--json', '--silent'):
            index += 1
            continue
        if word.startswith('-') or not ID.fullmatch(word):
            raise ValueError('unsupported closure option or issue ID')
        ids.append(word)
        index += 1
    if not ids:
        raise ValueError('explicit issue IDs are required')
    return ids

def contained(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('receipt paths must be project-relative')
    path = root / value
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError('receipt path escapes project')
    return path

def check_receipt(root, issue, receipt):
    if not isinstance(receipt, dict) or receipt.get('schema') != 'loop-acceptance-v1':
        raise ValueError('independent acceptance receipt missing')
    if receipt.get('issue_id') != issue or receipt.get('verdict') != 'accepted':
        raise ValueError('receipt scope or verdict mismatch')
    # Host-owned registry: never auto-populate from issue/project content.
    trust_name = os.environ.get('GOOSE_LOOP_ACCEPTANCE_TRUST_FILE')
    if not trust_name or not Path(trust_name).is_absolute():
        raise ValueError('trusted host receipt registry unavailable')
    trust = Path(trust_name)
    if trust.is_symlink() or trust.resolve().is_relative_to(root):
        raise ValueError('trust registry must be outside candidate repository')
    stat = trust.stat()
    if stat.st_uid != os.getuid() or stat.st_mode & 0o022:
        raise ValueError('trust registry ownership or mode invalid')
    registry = json.loads(trust.read_text())
    digest = hashlib.sha256(json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    policy = registry.get('receipts', {}).get(issue)
    if registry.get('schema') != 'loop-trusted-acceptance-v1' or not isinstance(policy, dict):
        raise ValueError('host acceptance policy missing')
    if policy.get('receipt_sha256') != digest or policy.get('repo_root') != str(root):
        raise ValueError('receipt not approved for this repository')
    expected_criteria = policy.get('required_criteria')
    if not isinstance(expected_criteria, list) or not expected_criteria or len(set(expected_criteria)) != len(expected_criteria):
        raise ValueError('approved criteria unavailable')
    independence = receipt.get('independence', {})
    required = {'builder_participation': False, 'inherited_builder_conclusions': False,
                'raw_evidence_access': True, 'candidate_write_access': False}
    if any(independence.get(k) != v for k, v in required.items()):
        raise ValueError('required independence dimensions are not established')
    builder = receipt.get('builder_session'); verifier = receipt.get('verifier_session')
    if not builder or not verifier or builder == verifier:
        raise ValueError('distinct builder/verifier identities required')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True, timeout=5).strip()
    index = subprocess.check_output(['git', 'ls-files', '--stage'], cwd=root, timeout=5)
    if receipt.get('head') != head or receipt.get('index_sha256') != hashlib.sha256(index).hexdigest():
        raise ValueError('HEAD/index drift')
    manifest = contained(root, receipt.get('manifest_path'))
    data = manifest.read_bytes()
    if hashlib.sha256(data).hexdigest() != receipt.get('manifest_sha256'):
        raise ValueError('candidate manifest drift')
    candidate = json.loads(data)
    entries = candidate.get('files', [])
    if not entries or len({e['path'] for e in entries}) != len(entries):
        raise ValueError('invalid candidate inventory')
    excludes = candidate.get('output_only', [])
    if not isinstance(excludes, list) or any(not isinstance(x, str) for x in excludes):
        raise ValueError('invalid output-only exclusions')
    if sorted(excludes) != sorted(policy.get('output_only', [])):
        raise ValueError('exclusions not approved in host policy')
    if len(set(excludes)) != len(excludes) or set(excludes) & {e['path'] for e in entries}:
        raise ValueError('ambiguous exclusions')
    # Tracked source cannot be declared output-only by a receipt producer.
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=root, timeout=5).decode().split(chr(0)))
    if tracked & set(excludes):
        raise ValueError('tracked inputs cannot be excluded')
    for excluded in excludes:
        contained(root, excluded)
    # All Git inputs including ignored files must be accounted for explicitly.
    inventory = set()
    for path in root.rglob('*'):
        rel = path.relative_to(root).as_posix()
        if rel.startswith('.git/') or rel.startswith('.beads/'):
            continue  # DB isn't a code candidate input; hooks are separately governed.
        if path.is_file() or path.is_symlink():
            if rel not in excludes:
                inventory.add(rel)
    if inventory != {e['path'] for e in entries}:
        raise ValueError('working-tree inventory drift')
    for entry in entries:
        path = contained(root, entry['path'])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('candidate bytes drift')
        if entry.get('mode') != oct(path.stat().st_mode & 0o777):
            raise ValueError('candidate mode drift')
    evidence = receipt.get('evidence', [])
    criteria = receipt.get('criteria', [])
    if not criteria or any(c.get('status') != 'proven' for c in criteria) or not evidence:
        raise ValueError('required criterion evidence missing')
    criterion_ids = [c.get('id') for c in criteria]
    if len(set(criterion_ids)) != len(criterion_ids) or set(criterion_ids) != set(expected_criteria):
        raise ValueError('required criteria mismatch')
    for entry in evidence:
        path = contained(root, entry['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry.get('sha256'):
            raise ValueError('evidence drift')

def main():
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return deny('malformed payload')
        command = payload.get('tool_input', {}).get('command', '')
        if not isinstance(command, str):
            return deny('malformed shell command')
        ids = closure_ids(command)
        if not ids:
            return 0
        # No builder-selected registry can authorize closure. A protected host must
        # mediate DB mutations; this writable hook only denies intercepted requests.
        return deny('shell closure disabled; use protected host-mediated acceptance and closure')
    except Exception:
        # Bounded non-sensitive diagnostic. No payload/paths echoed.
        return deny('closure evidence unavailable, stale or unsupported; obtain current independent acceptance')

if __name__ == '__main__':
    raise SystemExit(main())
