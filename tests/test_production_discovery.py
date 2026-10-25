"""Public projection seams: test data exclusion and recursive discovery safety."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProductionDiscovery(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        for name in ("skills", "hooks", "scripts", "tools", "tests", ".github"):
            shutil.copytree(ROOT / name, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("plugin.json", "README.md"):
            shutil.copyfile(ROOT / name, self.root / name)
        self.out = Path(self.temp.name) / "agentic-development"
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Discovery QA", "-c", "user.email=qa@example.invalid", "commit", "-qm", "fixture")

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)

    def call(self, mode):
        return subprocess.run([sys.executable, "-B", str(self.root / "tools/production.py"), mode, str(self.out)], capture_output=True, timeout=15)

    def put(self, name, text):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def test_repository_fixtures_excluded_but_operational_templates_preserved(self):
        for directory in ("evaluation-fixtures", "conformance-fixtures", "fixtures", "tests", "evaluations"):
            self.put("skills/cycle/assets/" + directory + "/demo/SKILL.md.fixture", "private fixture")
        self.put("skills/cycle/assets/materialize-fixtures.mjs", "test utility")
        self.put("skills/cycle/assets/study/synthetic-sessions.json", "[]")
        self.put("skills/cycle/assets/output-template.md", "# User output template")
        result = self.call("project")
        self.assertEqual(result.returncode, 0, result.stderr)
        files = [row["path"] for row in json.loads((self.out / "distribution.json").read_text())["files"]]
        self.assertFalse(any("fixture" in name or "synthetic-sessions" in name for name in files))
        self.assertIn("skills/cycle/assets/output-template.md", files)
        self.assertEqual(len(list(self.out.rglob("SKILL.md"))), 7)

    def test_unclassified_nested_skill_variants_rejected_before_output(self):
        for name in ("SKILL.md", "SKILL.md.fixture", "skill.md", "SKILL.md.backup"):
            with self.subTest(name=name):
                self.put("skills/cycle/assets/hidden/" + name, "nested instructions")
                result = self.call("project")
                self.assertNotEqual(result.returncode, 0, name)
                self.assertFalse(self.out.exists())
                (self.root / "skills/cycle/assets/hidden" / name).unlink()

    def test_resealed_nested_skill_and_fixture_inventory_still_rejected(self):
        self.assertEqual(self.call("project").returncode, 0)
        for name in ("skills/cycle/assets/hidden/SKILL.md.fixture", "skills/cycle/assets/conformance-fixtures/input.json"):
            with self.subTest(name=name):
                target = self.out / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("fixture")
                receipt = json.loads((self.out / "distribution.json").read_text())
                receipt["files"].append({"path": name, "mode": target.stat().st_mode & 0o777, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
                receipt["files"].sort(key=lambda row: row["path"])
                (self.out / "distribution.json").write_text(json.dumps(receipt))
                self.assertNotEqual(self.call("verify").returncode, 0)
                target.unlink()
                target.parent.rmdir()
                receipt["files"] = [row for row in receipt["files"] if row["path"] != name]
                (self.out / "distribution.json").write_text(json.dumps(receipt))


if __name__ == "__main__":
    unittest.main()
