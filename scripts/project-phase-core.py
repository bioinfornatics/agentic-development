#!/usr/bin/env python3
"""Create a fresh operational plugin projection; never install or overwrite it."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def project(destination):
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError('destination must not exist')
    source = ROOT / 'plugins/agentic-development'
    files = [source / 'plugin.json']
    for skill in sorted((source / 'skills').iterdir()):
        files.append(skill / 'SKILL.md')
        for folder in ('references', 'assets'):
            if (skill / folder).exists():
                files.extend(p for p in (skill / folder).rglob('*') if p.is_file())
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise ValueError('invalid source file: ' + str(path))
    destination.mkdir(parents=True)
    try:
        for path in files:
            target = destination / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        return {'schema': 'phase-core-projection-v1', 'files': [
            {'path': p.relative_to(source).as_posix(),
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(files)]}
    except Exception:
        shutil.rmtree(destination)
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination')
    args = parser.parse_args()
    print(json.dumps(project(args.destination), sort_keys=True, indent=2))
