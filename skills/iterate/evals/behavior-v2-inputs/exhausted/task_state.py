"""Controlled local task state, not Beads or an external authorization service."""
import argparse
import json
from pathlib import Path

path = Path(__file__).resolve().with_name('task.json')
parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['show', 'start'])
args = parser.parse_args()
task = json.loads(path.read_text())
if args.action == 'start':
    if not task['repair_authorized'] or task['attempts_started'] >= task['maximum']:
        parser.exit(2, 'No authorized correction remains.\n')
    task['attempts_started'] += 1
    path.write_text(json.dumps(task, indent=2) + '\n')
print(json.dumps(task, indent=2))
