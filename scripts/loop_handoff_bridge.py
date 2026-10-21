#!/usr/bin/env python3
"""Serial caller-driven Beads handoff observations; never acceptance or closure.
Requires an external single-writer lease. bd read/update is NOT a transaction/CAS.
Explicit code and tracker roots; no JSONL, DB creation, Git writes or status writes.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

KEY = 'loop_handoff_v1'
PHASES = {'research', 'plan', 'implement', 'test', 'judge', 'iterate', 'drive'}
IDENTIFIER = re.compile(r'^[A-Za-z0-9._:-]{1,160}$')

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

def call(args, cwd):
    return subprocess.check_output(args, cwd=cwd, timeout=15, text=True).strip()

def git_root(path):
    path = Path(path).resolve(strict=True)
    root = Path(call(['git', 'rev-parse', '--show-toplevel'], path)).resolve()
    if root != path:
        raise ValueError('explicit repository root required')
    return root

def relative(root, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError('unsafe relative path')
    p = root / name
    if p.relative_to(root).as_posix() != name or name.startswith(('.git/', '.beads/')) or name in ('.git', '.beads'):
        raise ValueError('noncanonical or excluded path')
    return p

def snapshot(root, exclusions):
    if not isinstance(exclusions, list) or len(set(exclusions)) != len(exclusions):
        raise ValueError('invalid frozen exclusions')
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split(chr(0)))
    for name in exclusions:
        relative(root, name)
        if name in tracked:
            raise ValueError('tracked source cannot be output-only')
    index = subprocess.check_output(['git', 'ls-files', '--stage'], cwd=root)
    if any(line.split(None, 3)[2] != b'0' for line in index.splitlines()):
        raise ValueError('unmerged index')
    files = []
    # Do not follow directory links. Hash their raw target even if outside repo.
    def visit(directory):
        for p in sorted(directory.iterdir(), key=lambda x: x.name):
            name = p.relative_to(root).as_posix()
            if name in ('.git', '.beads'):
                continue
            info = p.lstat()
            if stat.S_ISLNK(info.st_mode):
                target = os.readlink(p)
                entry = {'path': name, 'kind': 'symlink', 'target': target, 'mode': oct(stat.S_IMODE(info.st_mode)), 'sha256': hashlib.sha256(target.encode()).hexdigest()}
            elif stat.S_ISDIR(info.st_mode):
                if name in exclusions:raise ValueError('directory cannot be output-only')
                visit(p)
                continue
            elif stat.S_ISREG(info.st_mode):
                entry = {'path': name, 'kind': 'file', 'mode': oct(stat.S_IMODE(info.st_mode)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            else:
                raise ValueError('unsupported candidate file kind')
            if name not in exclusions:files.append(entry)
    visit(root)
    files.sort(key=lambda x: x['path'])
    return {'format_version': 1, 'root': str(root), 'head': call(['git', 'rev-parse', 'HEAD'], root),
            'index_sha256': hashlib.sha256(index).hexdigest(), 'files': files,
            'output_only': sorted(exclusions), 'excluded_state': ['.git internals', '.beads mutable state; not a host security projection']}

def evidence(root, entries):
    if not isinstance(entries, list) or not entries:
        raise ValueError('explicit evidence required')
    result = []
    for entry in entries:
        p = relative(root, entry['path'])
        # Evidence must be contained regular bytes, never dereference links.
        if any(part.is_symlink() for part in [p] + list(p.parents)[:len(p.relative_to(root).parts)-1]) or not p.resolve(strict=True).is_relative_to(root) or not p.is_file():
            raise ValueError('unsafe evidence')
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != entry.get('sha256'):
            raise ValueError('evidence drift')
        result.append({'path': entry['path'], 'sha256': actual})
    if len({x['path'] for x in result}) != len(result):
        raise ValueError('duplicate evidence')
    return sorted(result, key=lambda x: x['path'])

def validate_state(state):
    if not isinstance(state, dict) or state.get('schema') != 'loop-handoff-v1':
        raise ValueError('invalid bridge state')
    previous = None
    for number, event in enumerate(state.get('events', [])):
        if event.get('seq') != number or event.get('previous') != previous:
            raise ValueError('broken event sequence')
        value = dict(event);saved = value.pop('event_sha256', None)
        if digest(value) != saved:raise ValueError('event digest mismatch')
        previous = saved
    if not state.get('events'):raise ValueError('empty bridge state')

def evolve(old, request, candidate, proofs, tracker):
    """Pure append/replay state transition. Observations are not authorizations."""
    for key in ('issue_id', 'run_id', 'slice_id', 'session_id', 'event_id'):
        if not isinstance(request.get(key), str) or not IDENTIFIER.fullmatch(request[key]):
            raise ValueError('invalid correlation identifier')
    kind = request.get('kind')
    if kind not in {'checkpoint', 'handoff', 'resume', 'commit'} or request.get('phase') not in PHASES:
        raise ValueError('unsupported kind or phase')
    if request.get('candidate_sha256') != digest(candidate):raise ValueError('candidate drift')
    correlation = {k: request[k] for k in ('issue_id', 'run_id', 'slice_id')}
    bound = dict(correlation, repo_root=candidate['root'], tracker_root=str(tracker))
    if old is not None:
        validate_state(old)
        if old.get('binding') != bound:raise ValueError('repository/tracker/correlation mismatch')
        if old.get('exclusions') != candidate['output_only']:raise ValueError('scope drift')
        for event in old['events']:
            if event['event_id'] == request['event_id']:
                if event['request_sha256'] != digest(request):raise ValueError('conflicting replay')
                # Replay does not waive freshness validation performed before evolve.
                if old['events'][-1] != event:raise ValueError('stale replay')
                if event['candidate_sha256'] != digest(candidate) or event['evidence'] != proofs:
                    raise ValueError('replay candidate/evidence drift')
                return old, False
        last = old['events'][-1]
        if request.get('seq') != len(old['events']) or request.get('previous') != last['event_sha256']:
            raise ValueError('stale/lost/out-of-order event')
        if kind == 'resume':
            if last['kind'] != 'handoff' or any(request['session_id'] == event['session_id'] for event in old['events']):
                raise ValueError('resume requires ended prior session and fresh session')
        elif last['kind'] == 'handoff' or request['session_id'] != last['session_id']:
            raise ValueError('explicit resume required; interrupted session needs recovery')
        if kind != 'commit' and (last['candidate_sha256'] != digest(candidate) or last['evidence'] != proofs):
            raise ValueError('prior candidate or evidence stale; explicit new run required')
        if kind == 'commit':
            before = dict(last['candidate']);after = dict(candidate)
            for key in ('head', 'index_sha256'):
                before.pop(key);after.pop(key)
            if before != after or last['evidence'] != proofs or candidate['head'] == last['candidate']['head']:
                raise ValueError('commit rebind requires unchanged content/evidence and new HEAD')
    else:
        if kind != 'checkpoint' or request.get('seq') != 0 or request.get('previous') is not None:
            raise ValueError('new run requires initial checkpoint')
    if kind == 'handoff':
        for key in ('outcome', 'remaining', 'next_session_name', 'restart_prompt'):
            if not isinstance(request.get(key), str) or not request[key].strip():raise ValueError('incomplete handoff')
    event = {k: request[k] for k in ('event_id', 'seq', 'previous', 'kind', 'phase', 'session_id')}
    event.update(request_sha256=digest(request), candidate_sha256=digest(candidate), candidate=candidate, evidence=proofs)
    if kind == 'handoff':event['handoff'] = {k: request[k] for k in ('outcome', 'remaining', 'next_session_name', 'restart_prompt')}
    if kind == 'commit':event['commit'] = request['observed_commit']
    event['event_sha256'] = digest(event)
    return {'schema': 'loop-handoff-v1', 'binding': bound, 'exclusions': candidate['output_only'],
            'authority': 'untrusted serial observations only; no acceptance or permissions',
            'events': ([] if old is None else old['events']) + [event]}, True

def process(repo, tracker, request, bd='bd'):
    repo = git_root(repo);tracker = Path(tracker).resolve(strict=True)
    if not (tracker / '.beads').is_dir():raise ValueError('explicit existing tracker required')
    if not isinstance(request, dict):raise ValueError('request must be object')
    issue = request.get('issue_id')
    if not isinstance(issue, str) or not IDENTIFIER.fullmatch(issue):raise ValueError('invalid issue')
    rows = json.loads(call([bd, 'show', issue, '--json'], tracker))
    rows = rows if isinstance(rows, list) else [rows]
    if len(rows) != 1 or rows[0].get('id') != issue:raise ValueError('issue lookup mismatch')
    if rows[0].get('status') != 'in_progress':raise ValueError('claimed active issue required')
    meta = rows[0].get('metadata') or {}
    old = meta.get(KEY)
    candidate = snapshot(repo, request.get('output_only', []))
    proofs = evidence(repo, request.get('evidence'))
    if request.get('kind') == 'commit':
        # Committed tracked bytes must match the tested working tree, not merely HEAD claims.
        subprocess.check_call(['git', 'diff', '--quiet', '--exit-code'], cwd=repo, timeout=15)
        subprocess.check_call(['git', 'diff', '--cached', '--quiet', '--exit-code'], cwd=repo, timeout=15)
        parent = call(['git', 'rev-parse', 'HEAD^'], repo)
        replay = old is not None and old['events'][-1].get('event_id') == request.get('event_id')
        if old is None or (not replay and parent != old['events'][-1]['candidate']['head']):
            raise ValueError('commit must directly descend from observed HEAD')
        observed = {'hash': candidate['head'], 'parent': parent, 'message': call(['git', 'show', '-s', '--format=%B', 'HEAD'], repo),
                    'files': call(['git', 'diff-tree', '--no-commit-id', '--name-status', '-r', 'HEAD'], repo).splitlines()}
        if request.get('observed_commit') != observed:raise ValueError('commit claim differs from Git')
    state, changed = evolve(old, request, candidate, proofs, tracker)
    if changed:
        # Targeted metadata merge preserves other keys; caller-held lease is mandatory.
        call([bd, 'update', issue, '--set-metadata', KEY + '=' + json.dumps(state, sort_keys=True, separators=(',', ':'))], tracker)
        after = json.loads(call([bd, 'show', issue, '--json'], tracker))
        after = after[0] if isinstance(after, list) else after
        if after.get('metadata', {}).get(KEY) != state:raise ValueError('persistence readback failed; reconcile before retry')
    return {'schema': 'loop-handoff-result-v1', 'written': changed, 'event_sha256': state['events'][-1]['event_sha256'],
            'candidate_sha256': digest(candidate), 'authority': False}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo-root', required=True);p.add_argument('--tracker-root', required=True)
    p.add_argument('--inspect-candidate', action='store_true')
    args = p.parse_args()
    try:
        request = json.load(sys.stdin)
        if args.inspect_candidate:
            value = snapshot(git_root(args.repo_root), request.get('output_only', []))
            result = {'candidate': value, 'candidate_sha256': digest(value)}
        else:result = process(args.repo_root, args.tracker_root, request)
        print(json.dumps(result, sort_keys=True));return 0
    except Exception:
        print('BRIDGE: invalid, stale or unpersisted observation; reconcile explicitly', file=sys.stderr);return 2

if __name__ == '__main__':raise SystemExit(main())
