"""Public CLI tests of committed-source projection, not host installation."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CommittedProjection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "source"
        self.root.mkdir()
        for name in ("skills", "hooks", "scripts", "tools", "tests", ".github"):
            shutil.copytree(ROOT / name, self.root / name, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(ROOT / "plugin.json", self.root / "plugin.json")
        self.git("init", "-q")
        self.git("config", "user.name", "Projection test")
        self.git("config", "user.email", "qa@example.invalid")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.out = Path(self.tmp.name) / "product"
    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()
    def call(self, action="candidate", output=None):
        return subprocess.run([sys.executable, "-B", str(self.root / "tools/production.py"), action, str(output or self.out)], capture_output=True, timeout=15)
    def test_clean_candidate_binds_commit_and_tree_and_is_deterministic(self):
        r = self.call()
        self.assertEqual(r.returncode, 0, r.stderr)
        receipt = json.loads((self.out / "distribution.json").read_text())
        self.assertEqual(receipt["source_state"], "committed-source-candidate")
        self.assertEqual(receipt["source_head"], self.git("rev-parse", "HEAD"))
        self.assertEqual(receipt["source_tree"], self.git("rev-parse", "HEAD^{tree}"))
        self.assertFalse(receipt["release_ready"])
        self.assertEqual(self.call("verify").returncode, 0)
        self.assertEqual(self.call("smoke").returncode, 0)
        other = Path(self.tmp.name) / "second"
        self.assertEqual(self.call(output=other).returncode, 0)
        files = lambda p: {str(f.relative_to(p)): f.read_bytes() for f in p.rglob("*") if f.is_file()}
        self.assertEqual(files(self.out), files(other))
    def test_dirty_and_untracked_source_reject_before_destination(self):
        (self.root / "plugin.json").write_text("{}")
        self.assertNotEqual(self.call().returncode, 0)
        self.assertFalse(self.out.exists())
        self.git("checkout", "--", "plugin.json")
        (self.root / "unknown.txt").write_text("unknown")
        self.assertNotEqual(self.call().returncode, 0)
        self.assertFalse(self.out.exists())
    @unittest.skipUnless(hasattr(__import__("os"), "mkfifo"), "FIFO unavailable")
    def test_ignored_special_resource_rejects_before_destination(self):
        import os
        (self.root / ".gitignore").write_text("/skills/research/assets/pipe" + chr(10))
        self.git("add", ".gitignore")
        self.git("commit", "-qm", "ignore special probe")
        pipe = self.root / "skills/research/assets/pipe"
        pipe.parent.mkdir(exist_ok=True)
        os.mkfifo(pipe)
        self.assertEqual(self.git("status", "--porcelain", "--untracked-files=all"), "")
        self.assertNotEqual(self.call().returncode, 0)
        self.assertFalse(self.out.exists())

    def test_ignored_operational_resource_is_not_committed_evidence(self):
        (self.root / ".gitignore").write_text("/skills/research/assets/hidden.txt\n")
        self.git("add", ".gitignore")
        self.git("commit", "-qm", "ignore")
        p = self.root / "skills/research/assets/hidden.txt"
        p.parent.mkdir(exist_ok=True)
        p.write_text("not committed")
        self.assertNotEqual(self.call().returncode, 0)
        self.assertFalse(self.out.exists())

if __name__ == "__main__":
    unittest.main()
