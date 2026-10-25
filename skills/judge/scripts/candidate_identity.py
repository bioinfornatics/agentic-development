#!/usr/bin/env python3
"""Capture and compare explicit working-tree inputs; never grant acceptance.

Python >=3.10, standard library; Git CLI required only for Git workspaces.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys


class Invalid(ValueError):
    """A bounded diagnostic without source content."""


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Invalid("duplicate JSON key")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(Invalid("non-finite JSON")))


def shape(value, schema):
    """Validate the bundled schema's deliberately limited keyword vocabulary."""
    if "anyOf" in schema:
        for option in schema["anyOf"]:
            try:
                shape(value, option)
                return
            except Invalid:
                pass
        raise Invalid("schema alternatives failed")
    types = {"object": dict, "array": list, "string": str, "integer": int, "null": type(None)}
    if "type" in schema and type(value) is not types[schema["type"]]:
        raise Invalid("schema type mismatch")
    if "const" in schema and value != schema["const"]:
        raise Invalid("schema constant mismatch")
    if "enum" in schema and value not in schema["enum"]:
        raise Invalid("schema enum mismatch")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if not set(schema.get("required", [])).issubset(value):
            raise Invalid("missing required field")
        extra = set(value) - set(properties)
        if extra and schema.get("additionalProperties") is False:
            raise Invalid("unexpected field")
        for key, child in value.items():
            spec = properties.get(key, schema.get("additionalProperties", {}))
            if isinstance(spec, dict):
                shape(child, spec)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise Invalid("empty required array")
        for child in value:
            shape(child, schema.get("items", {}))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise Invalid("empty required string")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            raise Invalid("invalid string pattern")


def relative(value, allow_root=False):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise Invalid("invalid relative path")
    if value == "." and allow_root:
        return value
    if PurePosixPath(value).is_absolute() or any(p in ("", ".", "..", ".git") for p in value.split("/")):
        raise Invalid("ambiguous or reserved path")
    value.encode("utf-8", errors="strict")
    return value


def sorted_unique(values):
    if values != sorted(set(values)):
        raise Invalid("paths must be sorted and unique")


def check_scope(scope):
    shape(scope, {"type": "object", "required": ["include", "exclude", "environment", "criteria"],
        "additionalProperties": False, "properties": {
        "include": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "exclude": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["path", "reason"], "properties": {"path": {"type": "string"},
                "reason": {"type": "string", "minLength": 1}}}},
        "environment": {"type": "object", "additionalProperties": {"type": "string"}},
        "criteria": {"type": "string", "minLength": 1}}})
    for path in scope["include"]:
        relative(path, True)
    for entry in scope["exclude"]:
        relative(entry["path"])
        if not entry["reason"].strip():
            raise Invalid("exclusion reason required")
    sorted_unique(scope["include"])
    sorted_unique([e["path"] for e in scope["exclude"]])
    if not scope["environment"] or not scope["criteria"].strip():
        raise Invalid("environment and criteria identity required")


def validate(value):
    schema = load(Path(__file__).resolve().parent.parent / "references/candidate-identity.schema.json")
    shape(value, schema)
    check_scope(value["scope"])
    if not Path(value["root"]).is_absolute():
        raise Invalid("absolute root required")
    sorted_unique([e["path"] for e in value["entries"]])
    for entry in value["entries"]:
        name = relative(entry["path"])
        if not any(p == "." or name == p or name.startswith(p + "/") for p in value["scope"]["include"]):
            raise Invalid("entry outside scope")
        if any(name == e["path"] or name.startswith(e["path"] + "/") for e in value["scope"]["exclude"]):
            raise Invalid("excluded entry in manifest")
        if entry["kind"] == "symlink":
            if hashlib.sha256(entry["target"].encode("utf-8")).hexdigest() != entry["sha256"]:
                raise Invalid("symlink target digest mismatch")
    if value["git"] is not None:
        sorted_unique([e["path"] for e in value["git"]["index"]])
        for entry in value["git"]["index"]:
            relative(entry["path"])
    payload = {k: v for k, v in value.items() if k != "candidate_id"}
    if digest(payload) != value["candidate_id"]:
        raise Invalid("candidate digest mismatch")
    return value


def git_state(root):
    def git(*args, optional=False):
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
        if result.returncode and not optional:
            raise Invalid("Git metadata unavailable")
        return result
    marker = any((parent / ".git").exists() or (parent / ".git").is_symlink()
                 for parent in (root, *root.parents))
    try:
        top = git("rev-parse", "--show-toplevel", optional=True)
    except FileNotFoundError:
        if marker:
            raise Invalid("Git required for this workspace") from None
        return None
    if top.returncode:
        if marker or (root / "HEAD").exists():
            raise Invalid("broken or unsupported Git workspace")
        return None
    if Path(top.stdout.decode("utf-8").strip()).resolve() != root:
        raise Invalid("root must equal Git worktree root")
    head = git("rev-parse", "--verify", "HEAD", optional=True)
    if head.returncode:
        # Only an unborn branch is a supported no-HEAD state.
        branch = git("symbolic-ref", "-q", "HEAD").stdout.decode().strip()
        exists = git("show-ref", "--verify", branch, optional=True)
        if exists.returncode != 1:
            raise Invalid("HEAD unavailable")
        head_value = None
    else:
        head_value = head.stdout.decode().strip()
    entries = []
    for record in git("ls-files", "--stage", "-z").stdout.split(b"\x00"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, blob, stage = metadata.decode("ascii").split()
        if stage != "0" or mode == "160000":
            raise Invalid("unresolved index or unsupported submodule")
        entries.append({"path": relative(path.decode("utf-8")), "mode": mode, "blob": blob})
    return {"head": head_value, "index": sorted(entries, key=lambda e: e["path"])}


def capture(root, scope):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise Invalid("root directory required")
    check_scope(scope)
    git_before = git_state(root)
    entries = {}
    excluded = [e["path"] for e in scope["exclude"]]

    def visit(path):
        name = path.relative_to(root).as_posix()
        if name != ".":
            relative(name)
        if any(name == e or name.startswith(e + "/") for e in excluded):
            return
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            target = os.readlink(path)
            try:
                path.resolve(strict=True).relative_to(root)
            except (ValueError, OSError, RuntimeError):
                raise Invalid("external, broken or cyclic symlink") from None
            data = target.encode("utf-8")
            entry = {"path": name, "kind": "symlink", "mode": format(stat.S_IMODE(info.st_mode), "04o"),
                     "target": target, "sha256": hashlib.sha256(data).hexdigest()}
        elif stat.S_ISDIR(info.st_mode):
            for child in sorted(path.iterdir()):
                if child.name == ".git":
                    if path != root:
                        raise Invalid("nested repository unsupported")
                    continue
                visit(child)
            return
        elif stat.S_ISREG(info.st_mode):
            data = path.read_bytes()
            after = path.stat()
            if (info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns, info.st_mode) != (
                    after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_mode):
                raise Invalid("input changed during capture")
            entry = {"path": name, "kind": "file", "mode": format(stat.S_IMODE(info.st_mode), "04o"),
                     "sha256": hashlib.sha256(data).hexdigest()}
        else:
            raise Invalid("unsupported special input")
        entries[name] = entry

    for name in scope["include"]:
        path = root / name
        # Reject symlink ancestors, which can hide external input paths.
        for parent in path.parents:
            if parent == root:
                break
            if parent.is_symlink():
                raise Invalid("symlink ancestor unsupported")
        visit(path)
    for entry in entries.values():
        if entry["kind"] == "symlink":
            target_path = (root / entry["path"]).resolve(strict=True)
            target_name = target_path.relative_to(root).as_posix()
            if target_path.is_dir() or target_name not in entries or entries[target_name]["kind"] != "file":
                raise Invalid("symlink target must be a captured regular file")
    if git_before != git_state(root):
        raise Invalid("Git state changed during capture")
    payload = {"format_version": 1, "root": str(root), "projection": "working-tree",
               "scope": scope, "git": git_before,
               "entries": sorted(entries.values(), key=lambda e: e["path"])}
    payload["candidate_id"] = digest(payload)
    return validate(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    cap = commands.add_parser("capture", help="Print manifest to stdout; redirect outside input scope")
    cap.add_argument("--root", required=True)
    cap.add_argument("--scope", required=True)
    check = commands.add_parser("validate", help="Validate structure, semantics and manifest digest")
    check.add_argument("manifest")
    compare = commands.add_parser("compare", help="0 SAME, 1 DIFFERENT, 2 invalid/unavailable")
    compare.add_argument("before")
    compare.add_argument("after")
    args = parser.parse_args()
    try:
        if args.command == "capture":
            result = capture(args.root, load(args.scope))
        elif args.command == "validate":
            value = validate(load(args.manifest))
            result = {"status": "VALID", "candidate_id": value["candidate_id"]}
        else:
            before, after = validate(load(args.before)), validate(load(args.after))
            same = before["candidate_id"] == after["candidate_id"]
            print(json.dumps({"status": "SAME" if same else "DIFFERENT"}))
            return 0 if same else 1
        print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False))
        return 0
    except Invalid as error:
        print("BLOCKED: " + str(error), file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError, RuntimeError):
        print("BLOCKED: invalid or unavailable input; inspect scope, JSON and capabilities", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
