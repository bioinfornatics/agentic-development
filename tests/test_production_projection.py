"""Copied production preview, not real Goose installation proof."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools/production.py"

class ProductionProjection(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / "product"
    def call(self, action, path=None):
        return subprocess.run([sys.executable, "-B", str(CLI), action, str(path or self.out)],
                              capture_output=True, timeout=10)
    def test_isolated_built_runtime_and_determinism(self):
        r = self.call("project")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.out / "scripts/observe.pyz").is_file())
        self.assertFalse((self.out / "scripts/observe.py").exists())
        for name in ("apps", "tests", "tools", "evidence", ".beads", "CLAUDE.md", "CONTRIBUTING.md"):
            self.assertFalse((self.out / name).exists(), name)
        self.assertEqual(self.call("verify").returncode, 0)
        self.assertEqual(self.call("smoke").returncode, 0)
        other = Path(self.temp.name) / "second"
        self.assertEqual(self.call("project", other).returncode, 0)
        snapshot = lambda p: {x.relative_to(p).as_posix(): x.read_bytes() for x in p.rglob("*") if x.is_file()}
        self.assertEqual(snapshot(self.out), snapshot(other))
        self.assertNotEqual(self.call("project").returncode, 0)
        receipt = json.loads((self.out / "distribution.json").read_text())
        self.assertFalse(receipt["release_ready"])
        self.assertEqual(receipt["source_state"], "working-tree-preview")
    def test_missing_extra_tampered_and_symlink_runtime_fail(self):
        self.assertEqual(self.call("project").returncode, 0)
        p = self.out / "scripts/observe.pyz"
        original = p.read_bytes()
        p.write_bytes(original + b"tampered")
        self.assertNotEqual(self.call("verify").returncode, 0)
        p.unlink()
        self.assertNotEqual(self.call("verify").returncode, 0)
        p.write_bytes(original)
        extra = self.out / "private.txt"
        extra.write_text("private")
        self.assertNotEqual(self.call("verify").returncode, 0)
        extra.unlink()
        p.unlink()
        p.symlink_to(ROOT / "scripts/observe.py")
        self.assertNotEqual(self.call("smoke").returncode, 0)
    def test_nested_receipt_and_special_node_are_rejected(self):
        import os
        self.assertEqual(self.call("project").returncode, 0)
        extra = self.out / "skills/research/assets/evidence/distribution.json"
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text("private")
        self.assertNotEqual(self.call("verify").returncode, 0)
        extra.unlink()
        if hasattr(os, "mkfifo"):
            pipe = self.out / "extra-pipe"
            os.mkfifo(pipe)
            self.assertNotEqual(self.call("verify").returncode, 0)

    def test_unsafe_destination_is_rejected_before_write(self):
        target = Path(self.temp.name) / "target"
        target.mkdir()
        link = Path(self.temp.name) / "link"
        link.symlink_to(target, target_is_directory=True)
        self.assertNotEqual(self.call("project", link / "product").returncode, 0)
        self.assertNotEqual(self.call("project", ROOT / "skills/unsafe-preview").returncode, 0)
        self.assertFalse((ROOT / "skills/unsafe-preview").exists())

if __name__ == "__main__":
    unittest.main()
