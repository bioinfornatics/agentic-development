#!/usr/bin/env python3
"""Prepare/check a disposable behavioral pilot. Never launch models or Git."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PROTOCOL = "execution-pilot-v1"
VARIANTS = ("with_skill", "without_skill")
RESOURCE_DIRS = ("references", "assets", "scripts")
LIMIT = 4 * 1024 * 1024
ORACLE_TESTS = sorted([
    "criteria_test.CancellationContract.test_cancel_pending_delivery",
    "criteria_test.CancellationContract.test_cancel_before_start_and_idempotent",
    "criteria_test.CancellationContract.test_normal_exhaustion",
])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe(path):
    if ".." in Path(path).parts:
        raise ValueError("Parent traversal refused")
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError("Symlink refused: " + str(part))
    return path


def read(path):
    path = safe(path)
    if not path.is_file() or path.stat().st_size > LIMIT:
        raise ValueError("Missing, special or oversized input: " + str(path))
    return path.read_bytes()


def inventory(root):
    root = safe(root)
    if not root.is_dir():
        raise ValueError("Missing directory: " + str(root))
    result = {}
    for path in sorted(root.rglob("*")):
        safe(path)
        if not path.is_dir():
            result[path.relative_to(root).as_posix()] = read(path)
    if sum(map(len, result.values())) > 16 * LIMIT:
        raise ValueError("Input budget exceeded")
    return result


def hashes(files):
    return {name: digest(data) for name, data in files.items()}


def put(path, data):
    path = safe(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def inside(root, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError("Escaping manifest path")
    return safe(root / path)


def outside(source, path):
    path = safe(path)
    if path == source or source in path.parents:
        raise ValueError("Workspace must be outside source repository")
    # Refuse an ancestor too, to avoid covering source with workspace operations.
    if path in source.parents:
        raise ValueError("Workspace must not contain source repository")
    return path


def prepare(source, skill, workspace):
    source = safe(source)
    skill = safe(skill)
    if skill.parent != source / "skills":
        raise ValueError("Select a current source Skill under skills/")
    workspace = outside(source, workspace)
    if workspace.exists():
        raise ValueError("New destination required; overwrite refused")
    fixtures = source / "integration/execution-pilot/fixtures"
    project = inventory(fixtures / "project")
    brief = read(fixtures / "task.txt")
    oracle = read(fixtures / "criteria_test.py")
    resources = {"SKILL.md": read(skill / "SKILL.md")}
    for directory in RESOURCE_DIRS:
        base = skill / directory
        if base.exists() or base.is_symlink():
            for name, data in inventory(base).items():
                if not any(part in ("__pycache__", "evals", "evidence") for part in Path(name).parts):
                    resources[directory + "/" + name] = data
    # Retain the complete canonical execution requirements, not only this oracle.
    assertions = {}
    sources = {}
    for suite in sorted((source / "skills").glob("*/evals/evals.json")):
        raw = read(suite)
        name = suite.relative_to(source).as_posix()
        sources[name] = digest(raw)
        document = json.loads(raw)
        assertions[name] = [{"id": case["id"], "execution_assertions": case["execution_assertions"]}
                            for case in document["evals"] if "execution_assertions" in case]
    if not assertions or not any(assertions.values()):
        raise ValueError("Canonical execution_assertions required")
    staged = {"control/criteria_test.py": oracle,
              "control/execution_assertions.json": encoded(assertions),
              "control/test_runner.py": read(fixtures / "test_runner.py")}
    for variant in VARIANTS:
        prefix = "contexts/" + variant + "/"
        staged[prefix + "task.txt"] = brief
        staged.update({prefix + "project/" + name: data for name, data in project.items()})
        if variant == "with_skill":
            staged.update({prefix + "skill/" + name: data for name, data in resources.items()})
    manifest = {
        "protocol": PROTOCOL, "source": str(source),
        "provenance": {"kind": "working-tree-bytes-including-local-edits",
                       "clean_commit_asserted": False, "canonical_suite_hashes": sources,
                       "skill_hashes": hashes(resources), "fixture_hashes": hashes(project),
                       "task_sha256": digest(brief), "oracle_sha256": digest(oracle),
                       "preparer_sha256": digest(read(source / "tools/execution_eval.py"))},
        "frozen_inputs": hashes(staged), "project_inputs": hashes(project),
        "mutable_project_paths": ["streamer.py", "test_streamer.py"],
        "criteria": ["CANCEL-1: no post-cancel delivery; inactive",
                     "CANCEL-2: before-start and repeated cancellation safe",
                     "CANCEL-3: normal exhaustion unchanged",
                     "PRESERVE-1: exact user-notes.txt bytes",
                     "HISTORY-1: no Git metadata in project"],
        "execution_requirements": "control/execution_assertions.json",
        "coverage": "Subset only; does not enforce all canonical execution assertions",
        "isolation": {"status": "BLOCKED", "reason": "External host ambient exclusion not verified"},
        "tool_events": {"status": "unavailable", "events": None},
        "telemetry": {"tokens": None, "cost": None, "model_time_seconds": None},
    }
    # All source inputs were read and validated before any destination write.
    workspace.mkdir(parents=True, exist_ok=False)
    for name, data in staged.items():
        put(inside(workspace, name), data)
    raw = encoded(manifest)
    put(workspace / "manifest.json", raw)
    return {"workspace": str(workspace), "manifest_sha256": digest(raw),
            "isolation_status": "BLOCKED", "model_launches": 0}


def completed_tests(report, expected=None):
    """Validate observed structured completion; not hostile-code authentication."""
    if not isinstance(report, dict) or report.get("complete") is not True:
        return False
    planned, completed = report.get("planned"), report.get("completed")
    if (not isinstance(planned, list) or not planned
            or not all(isinstance(name, str) and name for name in planned)
            or len(set(planned)) != len(planned)
            or not isinstance(completed, list)
            or not all(isinstance(name, str) for name in completed)
            or sorted(planned) != sorted(completed)):
        return False
    if expected is not None and sorted(planned) != expected:
        return False
    counts = ("tests_run", "failures", "errors", "skipped",
              "expected_failures", "unexpected_successes")
    if any(type(report.get(key)) is not int for key in counts):
        return False
    return (report["tests_run"] == len(planned)
            and all(report[key] == 0 for key in counts if key != "tests_run"))


def run_tests(runner, oracle, cwd, mode):
    # This private parent path avoids mixing logs with structured outcomes. Code
    # in the same child interpreter can forge it; it is not an attestation.
    with tempfile.TemporaryDirectory(prefix="execution-check-") as directory:
        outcome = Path(directory) / "outcome.json"
        command = [sys.executable, "-I", "-B", str(runner), mode,
                   str(oracle), str(cwd), str(outcome)]
        try:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                                    timeout=15, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            report = None
            try:
                report = json.loads(read(outcome))
            except (ValueError, OSError):
                pass
            complete = completed_tests(report, ORACLE_TESTS if mode == "oracle" else None)
            return {"exit_code": result.returncode, "stdout": result.stdout[-16000:],
                    "stderr": result.stderr[-16000:], "completion": report,
                    "status": "PASS" if result.returncode == 0 and complete else "FAIL"}
        except subprocess.TimeoutExpired:
            return {"exit_code": None, "status": "TIMEOUT", "completion": None}


def check(workspace, manifest_sha256, variant, isolation=None):
    workspace = safe(workspace)
    raw = read(workspace / "manifest.json")
    if digest(raw) != manifest_sha256:
        raise ValueError("Frozen manifest hash mismatch")
    manifest = json.loads(raw)
    if manifest.get("protocol") != PROTOCOL or variant not in VARIANTS:
        raise ValueError("Unsupported protocol or variant")
    source = safe(manifest["source"])
    outside(source, workspace)
    base = workspace / "contexts" / variant
    project = base / "project"
    violations = []
    # Verify coordinator-only oracle and request/Skill inputs; project repair is allowed.
    def verify_frozen():
        for name, expected in manifest["frozen_inputs"].items():
            if "/project/" not in name and digest(read(inside(workspace, name))) != expected:
                raise ValueError("Changed frozen input: " + name)
        for treatment in VARIANTS:
            prefix = "contexts/" + treatment + "/"
            expected = {name[len(prefix):]: value for name, value in manifest["frozen_inputs"].items()
                        if name.startswith(prefix) and not name.startswith(prefix + "project/")}
            observed = {name: digest(value) for name, value in inventory(workspace / "contexts" / treatment).items()
                        if not name.startswith("project/")}
            if observed != expected:
                raise ValueError("Added or changed context input: " + treatment)
    verify_frozen()
    current = inventory(project)
    for name, expected in manifest["project_inputs"].items():
        if name not in manifest["mutable_project_paths"] and digest(current.get(name, b"")) != expected:
            violations.append("preserved bytes changed: " + name)
    if any(".git" in Path(name).parts for name in current) or (project / ".git").exists():
        violations.append("Git metadata present; no-commit condition violated")
    # New regression tests are allowed, but not instruction or hidden metadata injection.
    for name in current:
        if name not in manifest["project_inputs"] and not (name.startswith("test_") and name.endswith(".py") and "/" not in name):
            violations.append("unexpected project file: " + name)
    isolation_status = "BLOCKED"
    if isolation:
        attestation = json.loads(read(isolation))
        required = ("ambient_instructions_excluded", "source_and_tracker_inaccessible",
                    "sibling_context_inaccessible", "coordinator_criteria_inaccessible")
        if (attestation.get("manifest_sha256") != manifest_sha256
                or not isinstance(attestation.get("verified_by"), str)
                or not attestation["verified_by"].strip()
                or not all(attestation.get(key) is True for key in required)):
            raise ValueError("Incomplete external isolation attestation")
        isolation_status = "EXTERNALLY_REPORTED_VERIFIED"
    runner = workspace / "control/test_runner.py"
    oracle_path = workspace / "control/criteria_test.py"
    oracle = run_tests(runner, oracle_path, project, "oracle")
    local = run_tests(runner, oracle_path, project, "local")
    # Re-read after executable tests; they could have changed preserved files.
    after = inventory(project)
    if digest(read(workspace / "manifest.json")) != manifest_sha256:
        raise ValueError("Manifest changed during verification")
    verify_frozen()
    if after != current:
        violations.append("project bytes changed during verification")
    return {"variant": variant, "manifest_sha256": manifest_sha256,
            "candidate_hashes": hashes(after), "oracle": oracle, "project_tests": local,
            "violations": violations, "isolation_status": isolation_status,
            "behavior_status": "PASS" if not violations and oracle["status"] == local["status"] == "PASS" else "FAIL",
            "status": "BLOCKED" if isolation_status == "BLOCKED" else "CHECKED_NOT_ACCEPTED",
            "tool_events": manifest["tool_events"], "model_launches": 0,
            "limits": "Deterministic Python checks only; no agent effectiveness, authenticated host isolation, or historical no-commit proof. Candidate code is not sandboxed. Structured completion detects absent/premature runs but is forgeable by candidate code sharing the interpreter; it is not authenticated attestation or a hostile-code guarantee."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("prepare")
    p.add_argument("source")
    p.add_argument("skill")
    p.add_argument("workspace")
    c = commands.add_parser("check")
    c.add_argument("workspace")
    c.add_argument("variant", choices=VARIANTS)
    c.add_argument("--manifest-sha256", required=True)
    c.add_argument("--isolation", help="Externally produced host-verification attestation")
    args = parser.parse_args()
    try:
        result = (prepare(args.source, args.skill, args.workspace) if args.command == "prepare"
                  else check(args.workspace, args.manifest_sha256, args.variant, args.isolation))
        print(json.dumps(result, indent=2))
        return 0 if args.command == "prepare" or result["behavior_status"] == "PASS" else 1
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
