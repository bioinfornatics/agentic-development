"""Disposable executable fixture checks, not model evaluation or acceptance."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("execution_eval", ROOT / "tools/execution_eval.py")
eval_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(eval_tool)


class ExecutionPilotTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.workspace = self.base / "pilot"
        self.prepared = eval_tool.prepare(ROOT, ROOT / "skills/cycle", self.workspace)
        self.binding = self.prepared["manifest_sha256"]

    def project(self, variant="with_skill"):
        return self.workspace / "contexts" / variant / "project"

    def check(self, variant="with_skill", **kwargs):
        return eval_tool.check(self.workspace, self.binding, variant, **kwargs)

    def repair(self, variant="with_skill"):
        path = self.project(variant) / "streamer.py"
        path.write_text(path.read_text().replace("        self.cancelled = True\n",
                                               "        self.cancelled = True\n        self.active = False\n"))

    def test_public_cancel_red_then_green(self):
        red = self.check()
        self.assertEqual(red["behavior_status"], "FAIL")
        self.assertNotEqual(red["oracle"]["exit_code"], 0)
        self.assertIn("cancel delivered a late chunk", red["oracle"]["stderr"])
        self.assertEqual(red["project_tests"]["exit_code"], 0)
        self.repair()
        green = self.check()
        self.assertEqual(green["oracle"]["exit_code"], 0)
        self.assertEqual(green["behavior_status"], "PASS")
        self.assertEqual(green["status"], "BLOCKED")
        self.assertEqual(green["isolation_status"], "BLOCKED")
        self.assertEqual(green["model_launches"], 0)
        self.assertIsNone(green["tool_events"]["events"])

    def test_import_exit_zero_cannot_pass_without_completed_tests(self):
        (self.project() / "streamer.py").write_text("import os; os._exit(0)\n")
        result = self.check()
        self.assertEqual(result["oracle"]["exit_code"], 0)
        self.assertEqual(result["project_tests"]["exit_code"], 0)
        self.assertEqual(result["oracle"]["stdout"], "")
        self.assertEqual(result["oracle"]["stderr"], "")
        self.assertNotEqual(result["oracle"]["status"], "PASS")
        self.assertNotEqual(result["project_tests"]["status"], "PASS")
        self.assertEqual(result["behavior_status"], "FAIL")

    def test_local_empty_or_premature_run_cannot_pass(self):
        self.repair()
        for source in ("# no tests\n", "import os; os._exit(0)\n",
                       "import unittest, os\nclass ExitTest(unittest.TestCase):\n"
                       "    def test_exit(self): os._exit(0)\n"):
            with self.subTest(source=source):
                (self.project() / "test_streamer.py").write_text(source)
                result = self.check()
                self.assertEqual(result["oracle"]["status"], "PASS")
                self.assertEqual(result["project_tests"]["exit_code"], 0)
                self.assertEqual(result["project_tests"]["status"], "FAIL")
                self.assertEqual(result["behavior_status"], "FAIL")

    def test_parent_requires_exact_oracle_identity_and_success_counts(self):
        report = {"complete": True, "planned": eval_tool.ORACLE_TESTS,
                  "completed": eval_tool.ORACLE_TESTS, "tests_run": 3,
                  "failures": 0, "errors": 0, "skipped": 0,
                  "expected_failures": 0, "unexpected_successes": 0}
        self.assertTrue(eval_tool.completed_tests(report, eval_tool.ORACLE_TESTS))
        for change in ({"complete": False}, {"tests_run": 0}, {"tests_run": True},
                       {"failures": 1}, {"errors": 1}, {"skipped": 1},
                       {"expected_failures": 1}, {"unexpected_successes": 1},
                       {"completed": eval_tool.ORACLE_TESTS[:-1]},
                       {"planned": ["fake"] * 3, "completed": ["fake"] * 3},
                       {"planned": ["a", "b", "c"], "completed": ["a", "b", "c"]}):
            with self.subTest(change=change):
                self.assertFalse(eval_tool.completed_tests({**report, **change}, eval_tool.ORACLE_TESTS))
        for invalid in (None, {}, [], "PASS"):
            self.assertFalse(eval_tool.completed_tests(invalid, eval_tool.ORACLE_TESTS))

    def test_equivalent_inputs_hidden_criteria_and_only_current_skill(self):
        self.assertEqual(eval_tool.inventory(self.project()),
                         eval_tool.inventory(self.project("without_skill")))
        contexts = self.workspace / "contexts"
        self.assertEqual((contexts / "with_skill/task.txt").read_bytes(),
                         (contexts / "without_skill/task.txt").read_bytes())
        baseline = eval_tool.inventory(contexts / "without_skill")
        self.assertFalse(any("skill/" in name or "AGENTS" in name for name in baseline))
        for variant in eval_tool.VARIANTS:
            inputs = eval_tool.inventory(contexts / variant)
            self.assertFalse(any("criteria" in name or "execution_assertions" in name or "/evals/" in name for name in inputs))
        skill = eval_tool.inventory(contexts / "with_skill/skill")
        self.assertEqual(skill["SKILL.md"], (ROOT / "skills/cycle/SKILL.md").read_bytes())
        self.assertTrue(all(name == "SKILL.md" or name.split("/")[0] in eval_tool.RESOURCE_DIRS for name in skill))

    def test_all_canonical_execution_assertions_retained(self):
        retained = json.loads((self.workspace / "control/execution_assertions.json").read_text())
        expected = {}
        for suite in (ROOT / "skills").glob("*/evals/evals.json"):
            expected[suite.relative_to(ROOT).as_posix()] = [
                {"id": case["id"], "execution_assertions": case["execution_assertions"]}
                for case in json.loads(suite.read_text())["evals"] if "execution_assertions" in case]
        self.assertEqual(retained, expected)
        self.assertGreater(sum(len(c["execution_assertions"]) for cases in retained.values() for c in cases), 0)

    def test_refuses_overwrite_and_source_destination(self):
        before = eval_tool.inventory(self.workspace)
        with self.assertRaises(ValueError):
            eval_tool.prepare(ROOT, ROOT / "skills/cycle", self.workspace)
        self.assertEqual(before, eval_tool.inventory(self.workspace))
        with self.assertRaises(ValueError):
            eval_tool.prepare(ROOT, ROOT / "skills/cycle", ROOT / "unused-pilot")
        self.assertFalse((ROOT / "unused-pilot").exists())

    def test_destination_and_candidate_symlinks_refused(self):
        link = self.base / "link"
        link.symlink_to(self.base, target_is_directory=True)
        with self.assertRaises(ValueError):
            eval_tool.prepare(ROOT, ROOT / "skills/cycle", link / "new")
        self.assertFalse((self.base / "new").exists())
        with self.assertRaises(ValueError):
            eval_tool.prepare(ROOT, ROOT / "skills/cycle", link / ".." / "unsafe")
        notes = self.project() / "user-notes.txt"
        notes.unlink()
        notes.symlink_to(ROOT / "AGENTS.md")
        with self.assertRaises(ValueError):
            self.check()

    def test_source_resource_symlink_refused_before_writes(self):
        fake = self.base / "source"
        skill = fake / "skills/cycle"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("fake")
        fixtures = fake / "integration/execution-pilot/fixtures"
        fixtures.mkdir(parents=True)
        # Use bytes, not links, to stage the authorized fixture inputs.
        for name, data in eval_tool.inventory(ROOT / "integration/execution-pilot/fixtures").items():
            eval_tool.put(fixtures / name, data)
        (skill / "references").symlink_to(ROOT / "skills/cycle/references", target_is_directory=True)
        with self.assertRaises(ValueError):
            eval_tool.prepare(fake, skill, self.base / "refused")
        self.assertFalse((self.base / "refused").exists())

    def test_preserved_bytes_violation_after_green(self):
        self.repair()
        (self.project() / "user-notes.txt").write_bytes(b"tidied user draft\n")
        result = self.check()
        self.assertEqual(result["oracle"]["status"], "PASS")
        self.assertEqual(result["behavior_status"], "FAIL")
        self.assertIn("preserved bytes changed: user-notes.txt", result["violations"])

    def test_git_metadata_and_added_instructions_rejected(self):
        self.repair()
        (self.project() / ".git").mkdir()
        (self.project() / "AGENTS.md").write_text("unapproved instructions")
        result = self.check()
        self.assertEqual(result["behavior_status"], "FAIL")
        self.assertIn("Git metadata present; no-commit condition violated", result["violations"])
        self.assertIn("unexpected project file: AGENTS.md", result["violations"])

    def test_external_isolation_requires_all_bound_claims(self):
        self.repair()
        attestation = self.base / "external.json"
        attestation.write_text(json.dumps({"manifest_sha256": self.binding, "verified_by": "test-double"}))
        with self.assertRaises(ValueError):
            self.check(isolation=attestation)
        attestation.write_text(json.dumps({
            "manifest_sha256": self.binding, "verified_by": "test-double-not-real-host-proof",
            "ambient_instructions_excluded": True, "source_and_tracker_inaccessible": True,
            "sibling_context_inaccessible": True, "coordinator_criteria_inaccessible": True}))
        result = self.check(isolation=attestation)
        self.assertEqual(result["status"], "CHECKED_NOT_ACCEPTED")
        self.assertEqual(result["isolation_status"], "EXTERNALLY_REPORTED_VERIFIED")

    def test_added_baseline_context_instructions_rejected(self):
        (self.workspace / "contexts/without_skill/AGENTS.md").write_text("contaminated baseline")
        with self.assertRaises(ValueError):
            self.check("without_skill")

    def test_verification_side_effects_rejected(self):
        self.repair()
        (self.project() / "test_streamer.py").write_text(
            "from pathlib import Path\nPath('user-notes.txt').write_text('damaged')\n")
        result = self.check()
        self.assertEqual(result["behavior_status"], "FAIL")
        self.assertIn("project bytes changed during verification", result["violations"])

    def test_frozen_manifest_and_oracle_tamper_rejected(self):
        with self.assertRaises(ValueError):
            eval_tool.check(self.workspace, "0" * 64, "with_skill")
        (self.workspace / "control/criteria_test.py").write_text("print('fake pass')")
        with self.assertRaises(ValueError):
            self.check()

    def test_source_unchanged_by_prepare_check_and_repair(self):
        paths = [ROOT / "tools/execution_eval.py", ROOT / "tools/session_eval.py"]
        before = {str(path): eval_tool.read(path) for path in paths}
        fixtures = eval_tool.inventory(ROOT / "integration/execution-pilot/fixtures")
        skill = eval_tool.inventory(ROOT / "skills/cycle")
        self.check()
        self.repair()
        self.check()
        self.assertEqual(before, {str(path): eval_tool.read(path) for path in paths})
        self.assertEqual(fixtures, eval_tool.inventory(ROOT / "integration/execution-pilot/fixtures"))
        self.assertEqual(skill, eval_tool.inventory(ROOT / "skills/cycle"))

    def test_cli_json_error_and_blocked_results(self):
        command = [sys.executable, "-B", str(ROOT / "tools/execution_eval.py"), "check",
                   str(self.workspace), "without_skill", "--manifest-sha256", self.binding]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
