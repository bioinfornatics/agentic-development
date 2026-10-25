#!/usr/bin/env python3
"""Read-only operational payload inventory, not an installer or schema validator.

Invoke with one plugin root. Output sorted paths and byte hashes, never contents.
Only contained Skill resources and configured root Goose hooks/runtime are included.
Host activation, executable safety and official format validation are separate gates.
"""
import hashlib
import json
from pathlib import Path
import re
import shlex
import sys
from urllib.parse import unquote, urlsplit


class InventoryError(ValueError):
    """A bounded diagnostic with no payload or absolute-path content."""


def inventory(root):
    root = Path(root).resolve(strict=True)
    selected = {}

    def contained(path, boundary=root):
        path = Path(path)
        try:
            relative = path.relative_to(root)
        except ValueError:
            raise InventoryError("outside-root") from None
        cursor = root
        for part in relative.parts:
            if part in (".", ".."):
                raise InventoryError("ambiguous-path")
            cursor /= part
            if cursor.is_symlink():
                raise InventoryError("symlink-not-supported")
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(boundary)
        except (ValueError, OSError):
            raise InventoryError("missing-or-external-resource") from None
        return resolved

    def add(path, boundary=root):
        path = contained(path, boundary)
        if not path.is_file():
            raise InventoryError("resource-not-file")
        relative = path.relative_to(root).as_posix()
        selected[relative] = path

    def read_json(path):
        path = contained(path)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError):
            raise InventoryError("invalid-json") from None
        if not isinstance(value, dict):
            raise InventoryError("json-object-required")
        return value

    manifest = read_json(root / "plugin.json")
    if not isinstance(manifest.get("name"), str) or not manifest["name"].strip():
        raise InventoryError("plugin-name-required")
    # This inventory intentionally supports this repository's skills/hooks payload,
    # not MCP, custom agents, remote runtimes or client-specific extension bundles.
    if any(key in manifest for key in ("extensions", "mcpServers")) or any(
            (root / name).exists() for name in ("mcp.json", ".mcp.json")):
        raise InventoryError("unsupported-component-contract")
    add(root / "plugin.json")
    skills = root / "skills"
    contained(skills)
    if not skills.is_dir():
        raise InventoryError("skills-directory-required")
    for skill in sorted(skills.iterdir()):
        if skill.name.startswith("."):
            continue
        contained(skill)
        if not skill.is_dir():
            raise InventoryError("skill-child-not-directory")
        add(skill / "SKILL.md", skill)
        for directory in ("references", "scripts", "assets"):
            resources = skill / directory
            if resources.exists() or resources.is_symlink():
                contained(resources, skill)
                if not resources.is_dir():
                    raise InventoryError("resource-root-not-directory")
                for resource in sorted(resources.rglob("*")):
                    contained(resource, skill)
                    if not resource.is_file() and not resource.is_dir():
                        raise InventoryError("special-resource-not-supported")
                    if any(part in ("AGENTS.md", "evals", "__pycache__", "evidence", "research", "integration")
                           for part in resource.relative_to(skill).parts):
                        continue
                    if resource.is_file():
                        add(resource, skill)
        markdown = [path for name, path in selected.items()
                    if path.is_relative_to(skill) and path.suffix == ".md"]
        for source in markdown:
            text = source.read_text(encoding="utf-8")
            inline = re.findall(r"\]\(([^)]+)\)", text)
            definitions = []
            lines = text.splitlines()
            for index, line in enumerate(lines):
                # Conservatively inspect definitions in common containers too;
                # any referenced destination must exist even in an example.
                # Container prefixes are irrelevant to payload completeness.
                # Inspect any definition-shaped dependency, even in an example;
                # this is conservative inventory, not Markdown rendering.
                definition = re.search(r"\[[^]]+\]:[ 	]*(.*)$", line)
                if definition:
                    destination = definition[1].strip()
                    if not destination and index + 1 < len(lines):
                        destination = lines[index + 1].lstrip().lstrip(">").strip()
                    if not destination:
                        raise InventoryError("missing-reference-destination")
                    definitions.append(destination)
            for raw in inline + definitions:
                # The destination is separate from an optional Markdown title.
                # Unsupported shapes fail closed, never omit a local dependency.
                raw = raw.strip()
                if raw.startswith("<"):
                    end = raw.find(">")
                    if end < 0:
                        raise InventoryError("invalid-link-destination")
                    target, tail = raw[1:end], raw[end + 1:].strip()
                else:
                    parts = raw.split(None, 1)
                    target, tail = parts[0] if parts else "", parts[1] if len(parts) > 1 else ""
                if tail and not ((tail.startswith('"') and tail.endswith('"'))
                                 or (tail.startswith("'") and tail.endswith("'"))):
                    raise InventoryError("unsupported-link-title")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                local = unquote(parsed.path)
                if "\\" in local or ".." in Path(local).parts or Path(local).is_absolute():
                    raise InventoryError("escaping-resource-link")
                destination = contained(source.parent / local, skill)
                if destination.is_dir():
                    raise InventoryError("resource-link-not-file")
                if destination.relative_to(root).as_posix() not in selected:
                    raise InventoryError("excluded-resource-link")
    hooks_path = root / "hooks/hooks.json"
    alternate = root / "extensions/io.github.bioinfornatics.agent-plugins.goose/hooks.json"
    if alternate.exists() or alternate.is_symlink():
        raise InventoryError("unsupported-or-ambiguous-hook-layout")
    if hooks_path.exists() or hooks_path.is_symlink():
        hooks = read_json(hooks_path).get("hooks")
        if not isinstance(hooks, dict):
            raise InventoryError("hooks-object-required")
        add(hooks_path)
        for rules in hooks.values():
            if not isinstance(rules, list):
                raise InventoryError("hook-rules-required")
            for rule in rules:
                if not isinstance(rule, dict) or not isinstance(rule.get("hooks"), list):
                    raise InventoryError("hook-actions-required")
                for action in rule["hooks"]:
                    if not isinstance(action, dict) or action.get("type") != "command":
                        raise InventoryError("command-action-required")
                    command = action.get("command")
                    if not isinstance(command, str):
                        raise InventoryError("command-required")
                    try:
                        tokens = shlex.split(command)
                    except ValueError:
                        raise InventoryError("invalid-command") from None
                    prefix = chr(36) + "{PLUGIN_ROOT}/"
                    local = [token[len(prefix):] for token in tokens if token.startswith(prefix)]
                    # Accept the one known Python handler seam, not arbitrary shell,
                    # flags, secondary resources or executable expressions.
                    if len(tokens) != 2 or tokens[0] != "python3" or len(local) != 1:
                        raise InventoryError("unsupported-runtime-command")
                    path = Path(local[0])
                    if path.parts[:1] != ("scripts",) or ".." in path.parts or path.suffix != ".py":
                        raise InventoryError("runtime-path-required")
                    add(root / path)
    return {"format_version": 1, "mode": "dry-run", "files": [
        {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for name, path in sorted(selected.items())]}


def main(argv):
    if len(argv) != 1:
        sys.stderr.write("payload-inventory: expected-one-plugin-root\n")
        return 2
    try:
        result = inventory(argv[0])
    except (InventoryError, OSError, UnicodeError, ValueError, RecursionError):
        # Do not echo untrusted content, paths or exception messages.
        sys.stderr.write("payload-inventory: invalid-or-unsupported-payload\n")
        return 1
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
