"""Dry-run payload contract at the CLI seam; no installation evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tests/payload_inventory.py"


class PayloadInventory(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "plugin"
        self.root.mkdir()
        self.put("plugin.json", json.dumps({"name": "fixture", "version": "0.1.0"}))
        self.put("skills/review/SKILL.md", "---" + chr(10) + "name: review" + chr(10)
                 + "description: Reviews a change" + chr(10) + "---" + chr(10)
                 + "See [contract](references/contract.md)." + chr(10))
        self.put("skills/review/references/contract.md", "# Contract" + chr(10))
        self.put("scripts/observe.py", "# inert fixture" + chr(10))
        self.put("hooks/hooks.json", json.dumps({"hooks": {"Stop": [{"hooks": [{
            "type": "command", "command": 'python3 "' + chr(36) + '{PLUGIN_ROOT}/scripts/observe.py"', "timeout": 3}]}]}}))
        for path in ("AGENTS.md", "scripts/AGENTS.md", "hooks/AGENTS.md",
                     "skills/review/AGENTS.md", "skills/review/evals/evals.json",
                     "skills/review/evals/files/private.txt", "integration/evals.json",
                     "research/report.md", "evidence/run.json", "tests/fixture.py"):
            self.put(path, "SYNTHETIC-PRIVATE-CONTENT")

    def put(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def run_tool(self):
        return subprocess.run([sys.executable, "-B", str(TOOL), str(self.root)],
                              capture_output=True, timeout=5)

    def snapshot(self):
        return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}

    def test_operational_inventory_is_allowlisted_deterministic_and_read_only(self):
        before = self.snapshot()
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")
        value = json.loads(result.stdout)
        self.assertEqual([entry["path"] for entry in value["files"]], [
            "hooks/hooks.json", "plugin.json", "scripts/observe.py",
            "skills/review/SKILL.md", "skills/review/references/contract.md"])
        self.assertNotIn(b"SYNTHETIC-PRIVATE-CONTENT", result.stdout)
        self.assertEqual(self.run_tool().stdout, result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_missing_reference_and_missing_hook_handler_fail(self):
        for target in ("skills/review/references/contract.md", "scripts/observe.py"):
            original = (self.root / target).read_bytes()
            (self.root / target).unlink()
            result = self.run_tool()
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, b"")
            self.assertLessEqual(len(result.stderr), 2048)
            (self.root / target).write_bytes(original)

    def test_escape_excluded_resource_and_external_symlink_fail(self):
        for link in ("../../../../private.md", "../other/SKILL.md", "evals/files/private.txt"):
            self.put("skills/review/SKILL.md", "See [input](" + link + ").")
            result = self.run_tool()
            self.assertNotEqual(result.returncode, 0, link)
        self.put("skills/review/SKILL.md", "See [contract](references/contract.md).")
        path = self.root / "skills/review/references/contract.md"
        path.unlink()
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("private")
        path.symlink_to(outside)
        self.assertNotEqual(self.run_tool().returncode, 0)

    def test_symlinked_resource_directory_and_invalid_json_fail(self):
        reference = self.root / "skills/review/references"
        (reference / "contract.md").unlink()
        reference.rmdir()
        outside = Path(self.temp.name) / "external"
        outside.mkdir()
        (outside / "contract.md").write_text("private")
        reference.symlink_to(outside, target_is_directory=True)
        self.assertNotEqual(self.run_tool().returncode, 0)
        self.put("plugin.json", "not-json")
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(b"not-json", result.stderr)

    def test_hooks_without_contained_runtime_and_ambiguous_layout_fail(self):
        self.put("hooks/hooks.json", json.dumps({"hooks": {"Stop": [{"hooks": [{
            "type": "command", "command": "python3 /home/private/handler.py"}]}]}}))
        result = self.run_tool()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(b"/home/private", result.stderr)
        self.put("extensions/io.github.bioinfornatics.agent-plugins.goose/hooks.json", "{}")
        self.assertNotEqual(self.run_tool().returncode, 0)

    def test_nested_excluded_path_components_never_enter_inventory(self):
        for forbidden in ("evals", "AGENTS.md", "__pycache__", "evidence", "research", "integration"):
            self.put("skills/review/assets/" + forbidden + "/private.txt", "private")
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        for entry in json.loads(result.stdout)["files"]:
            for forbidden in ("evals", "AGENTS.md", "__pycache__", "evidence", "research", "integration"):
                self.assertNotIn(forbidden, entry["path"].split("/"))

    def test_reference_definitions_validate_missing_and_present_destinations(self):
        self.put("skills/review/SKILL.md", "See [contract][guide]." + chr(10) + chr(10)
                 + "[guide]: references/missing.md" + chr(10))
        self.assertNotEqual(self.run_tool().returncode, 0)
        self.put("skills/review/SKILL.md", "See [contract][guide]." + chr(10) + chr(10)
                 + '[guide]: references/contract.md "Contract"' + chr(10))
        self.assertEqual(self.run_tool().returncode, 0)

    def test_titled_inline_local_link_selects_existing_destination(self):
        self.put("skills/review/SKILL.md", 'See [contract](references/contract.md "Contract title").')
        self.assertEqual(self.run_tool().returncode, 0)

    def test_multiline_and_container_reference_destinations_are_checked(self):
        templates = ["[guide]:" + chr(10) + "  {}",
                     "> [guide]: {}",
                     "  [guide]:" + chr(10) + "    {}"]
        for template in templates:
            with self.subTest(template=template):
                self.put("skills/review/SKILL.md", "See [manual][guide]." + chr(10)
                         + chr(10) + template.format("references/missing.md") + chr(10))
                self.assertNotEqual(self.run_tool().returncode, 0)
                self.put("skills/review/SKILL.md", "See [manual][guide]." + chr(10)
                         + chr(10) + template.format("references/contract.md") + chr(10))
                self.assertEqual(self.run_tool().returncode, 0)

    def test_composed_containers_cannot_hide_reference_dependencies(self):
        for prefix in ("- > ", "> - > ", "1. > - > "):
            for name, expected in (("missing.md", 1), ("contract.md", 0)):
                with self.subTest(prefix=prefix, target=name):
                    self.put("skills/review/SKILL.md", prefix + "[guide]: references/" + name
                             + chr(10) + chr(10) + "  > [manual][guide]" + chr(10))
                    result = self.run_tool()
                    self.assertEqual(result.returncode, expected)
                    if expected:
                        self.assertEqual(result.stdout, b"")
                        self.assertLessEqual(len(result.stderr), 2048)

    @unittest.skipUnless(hasattr(__import__("os"), "mkfifo"), "FIFO unavailable")
    def test_special_operational_resource_is_rejected_without_reading(self):
        import os
        for directory in ("references", "scripts", "assets"):
            with self.subTest(directory=directory):
                pipe = self.root / "skills/review" / directory / "pipe"
                pipe.parent.mkdir(exist_ok=True)
                os.mkfifo(pipe)
                result = self.run_tool()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                self.assertLessEqual(len(result.stderr), 2048)
                pipe.unlink()
        self.assertEqual(self.run_tool().returncode, 0)

    def test_real_repository_inventory_excludes_eval_and_evidence(self):
        result = subprocess.run([sys.executable, "-B", str(TOOL), str(ROOT)], capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        files = [x["path"] for x in json.loads(result.stdout)["files"]]
        self.assertIn("scripts/observe.py", files)
        self.assertEqual(sum(p.endswith("/SKILL.md") for p in files), 7)
        for path in files:
            parts = path.split("/")
            self.assertNotIn(parts[0], ("tests", "integration", "research", "evidence"), path)
            self.assertNotIn("evals", parts, path)
            self.assertNotIn("AGENTS.md", parts, path)


if __name__ == "__main__":
    unittest.main()
