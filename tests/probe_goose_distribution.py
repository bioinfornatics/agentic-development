#!/usr/bin/env python3
"""Opt-in real Goose Git install/update/list probe; disposable roots only.

Usage: python3 -B tests/probe_goose_distribution.py <projected-plugin>
Never install into live user paths or publish the temporary Git repository.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = sorted(("cycle", "research", "plan", "implement", "test", "judge", "iterate"))


def probe(candidate, goose):
    spec = importlib.util.spec_from_file_location("production", ROOT / "tools/production.py")
    production = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(production)
    receipt = production.verify(candidate)
    production.smoke(candidate)
    executable = shutil.which(goose)
    if not executable:
        raise ValueError("Goose executable unavailable")
    with tempfile.TemporaryDirectory(prefix="agentic-development-goose-") as work:
        work = Path(work)
        repo, home, paths, foreign = (work / name for name in ("repo", "home", "goose", "foreign"))
        shutil.copytree(candidate, repo)
        home.mkdir()
        foreign.mkdir()
        env = dict(os.environ, HOME=str(home), GOOSE_PATH_ROOT=str(paths),
                   XDG_CONFIG_HOME=str(home / ".config"), XDG_DATA_HOME=str(home / ".local/share"),
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)

        def run(command, args, cwd=foreign):
            result = subprocess.run([command, *args], cwd=cwd, env=env, capture_output=True, text=True, timeout=120)
            if result.returncode:
                raise ValueError(command + " failed: " + result.stderr)
            return result.stdout

        version = run(executable, ["--version"]).strip()
        if version != "1.56.0":
            raise ValueError("Probe requires verified Goose 1.56.0")
        git = lambda *args: run("git", list(args), repo)
        git("init", "-q")
        git("config", "user.name", "Distribution QA")
        git("config", "user.email", "qa@example.invalid")
        git("add", "-A")
        git("commit", "-qm", "isolated distribution fixture")
        run(executable, ["plugin", "install", "--auto-update", repo.as_uri()])
        installed = paths / ".agents/plugins/agentic-development"

        def check():
            listing = run(executable, ["skills", "list"])
            rows = [line for line in listing.splitlines() if str(installed) in line]
            names = sorted(line.split("|")[0].strip().removeprefix("agentic-development:") for line in rows)
            if names != EXPECTED or any("/assets/" in line or "/references/" in line for line in rows):
                raise ValueError("Unexpected Skills: " + json.dumps(names))
            for name in ("tests", "tools", "evidence", "integration", ".beads", "AGENTS.md"):
                if (installed / name).exists():
                    raise ValueError("Development leakage: " + name)
            # Goose rewrites only the frontmatter name to its plugin-qualified form.
            for entry in receipt["files"]:
                data = (installed / entry["path"]).read_bytes()
                if entry["path"].endswith("/SKILL.md"):
                    data = re.sub(rb"(?m)^name: agentic-development:", b"name: ", data, count=1)
                if hashlib.sha256(data).hexdigest() != entry["sha256"]:
                    raise ValueError("Installed payload mismatch: " + entry["path"])
            meta = json.loads((installed / ".goose-plugin-install.json").read_text())
            if meta["source_type"] != "git" or not meta["auto_update"]:
                raise ValueError("Git update metadata lost")
            result = subprocess.run([sys.executable, "-I", str(installed / "scripts/observe.pyz")],
                input=b'{"event":"SessionStart"}', capture_output=True, cwd=foreign, env=env, timeout=5)
            if result.returncode or result.stdout:
                raise ValueError("Installed observer runtime failed")
            json.loads(result.stderr.decode().split(" ", 1)[1])

        check()
        legacy = installed / "skills/cycle/assets/evaluation-fixtures/demo"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md.fixture").write_text("obsolete fixture")
        marker = repo / "README.md"
        marker.write_bytes(marker.read_bytes() + b"\nIsolated update probe.\n")
        # Update a payload file and its receipt, retaining the source-state distinction.
        for entry in receipt["files"]:
            if entry["path"] == "README.md":
                entry["sha256"] = hashlib.sha256(marker.read_bytes()).hexdigest()
        (repo / "distribution.json").write_bytes(production.encode(receipt))
        # The transport repository now has .git/; verify installed payload bytes
        # against this updated receipt after replacement, not its Git metadata.
        git("add", "README.md", "distribution.json")
        git("commit", "-qm", "isolated update fixture")
        run(executable, ["plugin", "update", "agentic-development"])
        if legacy.exists():
            raise ValueError("Update retained obsolete fixture")
        check()
        return {"status": "passed", "goose": version, "git_install": True, "git_update": True,
                "skills_list_after_install": 7, "skills_list_after_update": 7,
                "obsolete_fixture_removed": True, "installed_payload_hashes": "verified after both",
                "runtime": "stdlib observer executed", "source_state": receipt["source_state"],
                "release_approval": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--goose", default=os.environ.get("GOOSE_EXECUTABLE", "goose"))
    args = parser.parse_args()
    try:
        print(json.dumps(probe(args.candidate.resolve(), args.goose), sort_keys=True))
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        parser.exit(1, "distribution-probe: " + str(error) + "\n")


if __name__ == "__main__":
    main()
