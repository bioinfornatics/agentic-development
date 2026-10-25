#!/usr/bin/env python3
"""Build/verify an isolated working-tree distribution preview; never publish."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILLS = frozenset(("cycle", "research", "plan", "implement", "test", "judge", "iterate"))
DEVELOPMENT_COMPONENTS = frozenset(("AGENTS.md", "evals", "evaluations", "tests",
    "__pycache__", "evidence", "research", "integration", "evaluation-fixtures",
    "conformance-fixtures", "fixtures"))
DEVELOPMENT_FILES = frozenset(("materialize-fixtures.mjs", "synthetic-sessions.json"))


def plain(path):
    path = Path(os.path.abspath(path))
    for parent in [path, *path.parents]:
        if parent.is_symlink():
            raise ValueError("symlink")
    return path


def records(root):
    result = []
    directories = set()
    for path in sorted(root.rglob("*")):
        plain(path)
        if not path.is_file() and not path.is_dir():
            raise ValueError("special node")
        if path.is_dir():
            directories.add(path.relative_to(root))
        if path.is_file() and path != root / "distribution.json":
            result.append({"path": path.relative_to(root).as_posix(),
                           "mode": stat.S_IMODE(path.stat().st_mode),
                           "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    required_directories = {parent for entry in result
                            for parent in Path(entry["path"]).parents
                            if parent != Path(".")}
    if directories != required_directories:
        raise ValueError("unexpected directory")
    return result


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def build(output, committed=False):
    source_head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    source_tree = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD^{tree}"], text=True).strip()
    if committed and subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"]):
        raise ValueError("clean committed source required")
    output = plain(output)
    if output.exists() or output.is_relative_to(ROOT) or ROOT.is_relative_to(output):
        raise ValueError("unsafe or existing destination")
    plain(output.parent)
    if not output.parent.is_dir():
        raise ValueError("missing output parent")
    spec = importlib.util.spec_from_file_location("payload_inventory", ROOT / "tests/payload_inventory.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = module.inventory(ROOT)
    contents = {}
    for entry in source["files"]:
        name = entry["path"]
        data = (ROOT / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("source changed")
        if committed:
            tracked = subprocess.check_output(["git", "-C", str(ROOT), "show", source_head + ":" + name])
            if tracked != data:
                raise ValueError("uncommitted operational resource")
        if name == "scripts/observe.py":
            continue
        contents[name] = data
    handler = plain(ROOT / "scripts/observe.py").read_bytes()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as archive:
        item = zipfile.ZipInfo("__main__.py", date_time=(1980, 1, 1, 0, 0, 0))
        item.external_attr = 0o644 << 16
        archive.writestr(item, handler)
    contents["scripts/observe.pyz"] = buf.getvalue()
    hooks = json.loads(contents["hooks/hooks.json"])
    for rules in hooks["hooks"].values():
        for rule in rules:
            for action in rule["hooks"]:
                action["command"] = action["command"].replace("scripts/observe.py", "scripts/observe.pyz")
    contents["hooks/hooks.json"] = encode(hooks)
    readme = plain(ROOT / "README.md").read_bytes()
    if committed and readme != subprocess.check_output([
            "git", "-C", str(ROOT), "show", source_head + ":README.md"]):
        raise ValueError("uncommitted README")
    contents["README.md"] = readme
    contents["runtime.json"] = encode({"format_version": 1, "language": "python",
        "interpreter": "Python >=3.10", "mode": "stdlib-zipapp", "dependencies": [],
        "entrypoint": "scripts/observe.pyz", "source_sha256": hashlib.sha256(handler).hexdigest(),
        "native": "not-promised", "install_build": False})
    runtime_extension = {"version": 1, "language": "python", "mode": "stdlib-zipapp",
        "interpreter": "Python >=3.10", "manifest": "runtime.json",
        "entrypoint": "scripts/observe.pyz", "dependencies": [], "install_build": False}
    plugin = json.loads(contents["plugin.json"])
    plugin.setdefault("extensions", {})["io.github.bioinfornatics.agentic-development.runtime"] = runtime_extension
    contents["plugin.json"] = encode(plugin)
    workflow = plain(ROOT / ".github/workflows/production-checks.yml").read_bytes()
    if committed and workflow != subprocess.check_output([
            "git", "-C", str(ROOT), "show", source_head + ":.github/workflows/production-checks.yml"]):
        raise ValueError("uncommitted workflow")
    contents[".github/workflows/production-checks.yml"] = workflow
    if committed:
        if source_head != subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip():
            raise ValueError("source changed")
        if subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"]):
            raise ValueError("source changed")
    # Validate all source and construct every byte before creating the destination.
    output.mkdir(mode=0o755)
    for name, data in sorted(contents.items()):
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o644)
    receipt = {"format_version": 1, "source_state": "committed-source-candidate" if committed else "working-tree-preview",
               "release_ready": False, "source_tree": source_tree,
               "source_head": source_head,
               "source_files": source["files"], "files": records(output)}
    (output / "distribution.json").write_bytes(encode(receipt))
    (output / "distribution.json").chmod(0o644)
    verify(output)


def verify(output):
    output = plain(output)
    plain(output / "distribution.json")
    receipt = json.loads((output / "distribution.json").read_text())
    if receipt.get("source_state") not in ("working-tree-preview", "committed-source-candidate"):
        raise ValueError("unknown source state")
    if receipt.get("format_version") != 1 or receipt.get("release_ready") is not False:
        raise ValueError("preview provenance required")
    if receipt["files"] != records(output):
        raise ValueError("payload mismatch")
    paths = {entry["path"] for entry in receipt["files"]}
    required = {"plugin.json", "hooks/hooks.json", "scripts/observe.pyz", "README.md", "runtime.json",
                ".github/workflows/production-checks.yml"}
    if not required <= paths:
        raise ValueError("missing runtime")
    for name in paths:
        parts = Path(name).parts
        if name in required:
            continue
        if (len(parts) < 3 or parts[0] != "skills" or parts[1] not in SKILLS
                or any(p in DEVELOPMENT_COMPONENTS for p in parts[2:])
                or parts[-1] in DEVELOPMENT_FILES):
            raise ValueError("forbidden payload")
        if parts[-1].lower().startswith("skill.md") and (len(parts) != 3 or parts[-1] != "SKILL.md"):
            raise ValueError("nested skill entrypoint")
    if {name for name in paths if name.endswith("/SKILL.md")} != {"skills/" + name + "/SKILL.md" for name in SKILLS}:
        raise ValueError("unexpected skills")
    return receipt


def smoke(output):
    verify(output)
    messages = [b'{"event":"SessionStart"}', b'not-json',
                b'{"event":"Stop","last_assistant_message":"## step"}']
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
    for data in messages:
        result = subprocess.run([sys.executable, "-I", str(plain(output) / "scripts/observe.pyz")],
            input=data, capture_output=True, cwd=output, env=env, timeout=3)
        if result.returncode != 0 or result.stdout or len(result.stderr) > 2048:
            raise ValueError("runtime smoke failed")
        json.loads(result.stderr.decode().split(" ", 1)[1])


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("project", "candidate", "verify", "smoke"):
        sys.stderr.write("production: expected project|candidate|verify|smoke and destination\n")
        return 2
    try:
        output = Path(sys.argv[2])
        {"project": build, "candidate": lambda p: build(p, committed=True), "verify": verify, "smoke": smoke}[sys.argv[1]](output)
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError):
        sys.stderr.write("production: invalid-preview-or-unsafe-destination\n")
        return 1
    sys.stdout.write("production: " + sys.argv[1] + " passed (local preview only)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
