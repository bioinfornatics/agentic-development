"""Public CLI checks; not evidence of agent effectiveness or acceptance."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills/cycle/scripts/candidate_identity.py"


class CandidateIdentity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "root"
        self.root.mkdir()
        (self.root / "src").mkdir()
        (self.root / "src/data.bin").write_bytes(b"\x00\xffinput")
        self.scope = self.base / "scope.json"
        self.scope.write_text(json.dumps({"include": ["src"], "exclude": [],
            "environment": {"python": "test-fixture"}, "criteria": "FR-fixture-v1"}))

    def cli(self, *args, code=0):
        result = subprocess.run([sys.executable, "-B", str(CLI), *map(str, args)],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stderr + result.stdout)
        return json.loads(result.stdout) if result.stdout else None

    def capture(self):
        return self.cli("capture", "--root", self.root, "--scope", self.scope)

    def save(self, name, value):
        path = self.base / name
        path.write_text(json.dumps(value))
        return path

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()

    def init_git(self):
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("add", ".")
        self.git("commit", "-qm", "baseline")

    def test_determinism_and_independent_digest(self):
        value = self.capture()
        self.assertEqual(value, self.capture())
        self.assertIsNone(value["git"])
        self.assertEqual(value["entries"][0]["sha256"], hashlib.sha256(b"\x00\xffinput").hexdigest())
        payload = {k: v for k, v in value.items() if k != "candidate_id"}
        expected = hashlib.sha256(json.dumps(payload, sort_keys=True,
            separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(value["candidate_id"], expected)
        self.cli("validate", self.save("manifest.json", value))

    def test_compare_change_add_delete_mode_symlink_and_ignored(self):
        self.init_git()
        before = self.save("before.json", self.capture())
        self.cli("compare", before, before)
        (self.root / ".gitignore").write_text("src/local*\n")
        local = self.root / "src/local.bin"
        local.write_bytes(b"local")
        after = self.save("after.json", self.capture())
        self.cli("compare", before, after, code=1)
        self.assertIn("src/local.bin", [e["path"] for e in self.capture()["entries"]])
        baseline = self.capture()["candidate_id"]
        local.unlink()
        self.assertNotEqual(baseline, self.capture()["candidate_id"])
        baseline = self.capture()["candidate_id"]
        (self.root / "src/data.bin").chmod(0o755)
        self.assertNotEqual(baseline, self.capture()["candidate_id"])
        (self.root / "src/link").symlink_to("data.bin")
        link = next(e for e in self.capture()["entries"] if e["kind"] == "symlink")
        self.assertEqual(link["target"], "data.bin")
        self.assertEqual(link["sha256"], hashlib.sha256(b"data.bin").hexdigest())

    def test_git_head_index_and_dirty_are_distinct(self):
        self.init_git()
        before = self.capture()
        (self.root / "src/data.bin").write_bytes(b"new")
        dirty = self.capture()
        self.assertEqual(before["git"], dirty["git"])
        self.assertNotEqual(before["candidate_id"], dirty["candidate_id"])
        self.git("add", ".")
        staged = self.capture()
        self.assertEqual(staged["entries"], dirty["entries"])
        self.assertNotEqual(staged["candidate_id"], dirty["candidate_id"])
        self.git("commit", "-qm", "new")
        self.assertNotEqual(staged["candidate_id"], self.capture()["candidate_id"])
        self.git("rm", "src/data.bin")
        # Git may remove the now-empty directory; retain the explicit scope.
        (self.root / "src").mkdir(exist_ok=True)
        self.assertEqual(self.capture()["entries"], [])

    def test_output_exclusions_and_environment(self):
        config = json.loads(self.scope.read_text())
        config["exclude"] = [{"path": "src/report.txt", "reason": "output only, not consumed"}]
        self.scope.write_text(json.dumps(config))
        before = self.capture()
        (self.root / "src/report.txt").write_text("report")
        self.assertEqual(before, self.capture())
        config["environment"]["python"] = "different"
        self.scope.write_text(json.dumps(config))
        self.assertNotEqual(before["candidate_id"], self.capture()["candidate_id"])

    def test_bad_scope_and_special_files_block(self):
        config = json.loads(self.scope.read_text())
        for path in ("../outside", "src/../src", "/tmp", "missing"):
            config["include"] = [path]
            self.scope.write_text(json.dumps(config))
            self.cli("capture", "--root", self.root, "--scope", self.scope, code=2)
        config["include"] = ["src"]
        self.scope.write_text(json.dumps(config))
        os.mkfifo(self.root / "src/pipe")
        self.cli("capture", "--root", self.root, "--scope", self.scope, code=2)

    def test_symlink_scope_escape_and_nested_root_block(self):
        (self.root / "src/escape").symlink_to(self.base)
        self.cli("capture", "--root", self.root, "--scope", self.scope, code=2)
        (self.root / "src/escape").unlink()
        self.init_git()
        self.cli("capture", "--root", self.root / "src", "--scope", self.scope, code=2)

    def test_broken_git_and_unresolved_index_block(self):
        (self.root / ".git").write_text("gitdir: missing-directory\n")
        self.cli("capture", "--root", self.root, "--scope", self.scope, code=2)
        (self.root / ".git").unlink()
        self.init_git()
        blob = self.git("rev-parse", "HEAD:src/data.bin")
        record = f"100644 {blob} 1\tsrc/data.bin\n"
        subprocess.run(["git", "-C", str(self.root), "update-index", "--index-info"],
            input=record, text=True, check=True)
        self.cli("capture", "--root", self.root, "--scope", self.scope, code=2)

    def test_invalid_tampered_and_duplicate_manifests(self):
        value = self.capture()
        value["entries"][0]["sha256"] = "0" * 64
        self.cli("validate", self.save("tampered.json", value), code=2)
        value = self.capture()
        value["entries"].append(value["entries"][0])
        self.cli("validate", self.save("duplicate.json", value), code=2)
        value = self.capture()
        value["unexpected"] = True
        self.cli("validate", self.save("extra.json", value), code=2)
        path = self.base / "invalid.json"
        path.write_text('{"format_version":1,"format_version":1}')
        self.cli("validate", path, code=2)

    def test_scope_coverage_and_nested_repository_block(self):
        (self.root / "other.txt").write_text("other")
        (self.root / "src/link").symlink_to("../other.txt")
        self.cli("capture", "--root", self.root, "--scope", self.scope, code=2)
        (self.root / "src/link").unlink()
        (self.root / "src/nested").mkdir()
        (self.root / "src/nested/.git").mkdir()
        self.cli("capture", "--root", self.root, "--scope", self.scope, code=2)

    def test_validation_rejects_rehashed_out_of_scope_entry(self):
        value = self.capture()
        value["entries"][0]["path"] = "outside.txt"
        payload = {k: v for k, v in value.items() if k != "candidate_id"}
        value["candidate_id"] = hashlib.sha256(json.dumps(payload, sort_keys=True,
            separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        self.cli("validate", self.save("outside.json", value), code=2)

    def test_all_skill_resources_are_identical_and_example_valid(self):
        for relative in ("scripts/candidate_identity.py", "references/candidate-identity.md",
                "references/candidate-identity.schema.json", "references/candidate-identity.example.json",
                "references/candidate-scope.example.json"):
            baseline = (ROOT / "skills/cycle" / relative).read_bytes()
            for skill in (ROOT / "skills").iterdir():
                self.assertEqual(baseline, (skill / relative).read_bytes(), str(skill))
        self.cli("validate", ROOT / "skills/cycle/references/candidate-identity.example.json")


if __name__ == "__main__":
    unittest.main()
