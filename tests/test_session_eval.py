"""Deterministic session bridge tests; synthetic outputs are not agent evidence."""
import importlib.util
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SessionEvaluation(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("session_eval", ROOT / "tools/session_eval.py")
        self.api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.api)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / "skill"
        self.skill.mkdir()
        (self.skill / "SKILL.md").write_text("Follow the task.")
        (self.skill / "facts.json").write_text('{"value":42}')
        self.case = {"id":1, "name":"demo", "prompt":"Read facts.json and explain the value.",
                     "files":["facts.json"], "target":{"execution":"explain"},
                     "budget":{"max_turns":2,"timeout_seconds":60},
                     "assertions":["The response reports forty-two."], "expected_output":"SECRET ANSWER"}
        (self.skill / "evals.json").write_text(json.dumps({"skill_name":"demo","evals":[self.case]}))
        self.ws = self.root / "campaign"

    def prepare(self):
        self.api.prepare(self.skill, self.skill / "evals.json", self.ws, "model-a", [1])

    def record(self, run="eval-1/with_skill/run-1", delegate="candidate-a"):
        output = self.root / "reply.txt"
        output.write_text("The value is forty-two.")
        return self.api.record(self.ws, run, output, delegate, "model-a")

    def test_requests_hide_criteria_and_stage_equal_fixtures(self):
        self.prepare()
        for variant in ("with_skill", "without_skill"):
            base = self.ws / "eval-1" / variant / "run-1"
            request = (base / "request.json").read_text()
            self.assertNotIn("SECRET ANSWER", request)
            self.assertNotIn(self.case["assertions"][0], request)
            self.assertEqual((base / "inputs/facts.json").read_bytes(), (self.skill / "facts.json").read_bytes())
            self.assertEqual((base / "inputs/skill/SKILL.md").exists(), variant == "with_skill")

    def test_no_overwrite_or_symlink_fixture(self):
        self.prepare()
        with self.assertRaises(ValueError): self.prepare()
        other = self.root / "other"
        (self.skill / "facts.json").unlink()
        (self.skill / "facts.json").symlink_to(self.skill / "SKILL.md")
        with self.assertRaises(ValueError):
            self.api.prepare(self.skill, self.skill / "evals.json", other, "model-a", [1])
        self.assertFalse(other.exists())

    def test_execution_levels_and_selection_fail_before_writes(self):
        self.case["target"]["execution"] = "execute"
        (self.skill / "evals.json").write_text(json.dumps({"skill_name":"demo","evals":[self.case]}))
        with self.assertRaises(ValueError): self.prepare()
        self.assertFalse(self.ws.exists())

    def test_record_rejects_duplicate_stale_model_and_escape(self):
        self.prepare()
        with self.assertRaises(ValueError):
            self.api.record(self.ws,"../escape", self.skill / "facts.json", "a", "model-a")
        self.record()
        with self.assertRaises(ValueError): self.record()
        (self.ws / "eval-1/without_skill/run-1/inputs/facts.json").write_text("changed")
        with self.assertRaises(ValueError): self.record("eval-1/without_skill/run-1", "b")

    def test_blind_grading_quotes_independence_and_exact_membership(self):
        self.prepare(); packet = self.record()
        text = json.dumps(packet)
        self.assertNotIn("with_skill", text)
        self.assertNotIn("candidate-a", text)
        grade = self.root / "grade.json"
        result = [{"id":1,"verdict":"pass","evidence_quote":"forty-two","rationale":"Matches the fixture."}]
        grade.write_text(json.dumps(result))
        with self.assertRaises(ValueError):
            self.api.grade(self.ws, "eval-1/with_skill/run-1", grade, "candidate-a", "model-a")
        result[0]["evidence_quote"] = "invented"
        grade.write_text(json.dumps(result))
        with self.assertRaises(ValueError):
            self.api.grade(self.ws, "eval-1/with_skill/run-1", grade, "grader-a", "model-a")
        result[0]["evidence_quote"] = "forty-two"
        grade.write_text(json.dumps(result))
        self.api.grade(self.ws,"eval-1/with_skill/run-1",grade,"grader-a","model-a")
        self.assertEqual(self.api.status(self.ws)["graded"], 1)
        self.assertFalse(self.api.status(self.ws)["official_full_eval_accepted"])

    def test_write_rejects_symlink_ancestors_before_mkdir(self):
        outside = self.root / "outside"
        outside.mkdir()
        link = self.root / "linked-output"
        link.symlink_to(outside, target_is_directory=True)
        for relative in ("result.json", "new/nested/result.json"):
            with self.subTest(relative=relative):
                with self.assertRaises(ValueError):
                    self.api.write(link / relative, {"value": 42})
                self.assertEqual(list(outside.iterdir()), [])
                self.assertTrue(link.is_symlink())

    def test_write_refuses_leaf_links_and_preserves_existing_bytes(self):
        for exists in (False, True):
            with self.subTest(target_exists=exists):
                target = self.root / ("existing.json" if exists else "missing.json")
                if exists:
                    target.write_bytes(b"user bytes")
                link = self.root / ("live-link.json" if exists else "dangling-link.json")
                link.symlink_to(target)
                with self.assertRaises(ValueError):
                    self.api.write(link, {"value": 42})
                self.assertTrue(link.is_symlink())
                if exists:
                    self.assertEqual(target.read_bytes(), b"user bytes")
                else:
                    self.assertFalse(target.exists())
        ordinary = self.root / "ordinary.json"
        self.api.write(ordinary, {"value": 42})
        before = ordinary.read_bytes()
        with self.assertRaises(ValueError):
            self.api.write(ordinary, {"value": 99})
        self.assertEqual(ordinary.read_bytes(), before)
        self.assertEqual(json.loads(before), {"value": 42})

    def test_report_preflights_outputs_and_creates_exclusively(self):
        self.prepare()
        viewer = self.root / "viewer.mjs"
        viewer.write_text("// mocked external renderer; no Node or model invocation")
        rendered = b"<!doctype html><title>Fixture report</title>"
        result = subprocess.CompletedProcess([], 0, stdout=rendered, stderr=b"")
        for name in ("review.html", "session-summary.json"):
            for exists in (False, True):
                with self.subTest(destination=name, target_exists=exists):
                    target = self.root / ("external-" + name)
                    if exists:
                        target.write_bytes(b"user bytes")
                    link = self.ws / name
                    link.symlink_to(target)
                    with patch.object(self.api.subprocess, "run", return_value=result) as renderer:
                        with self.assertRaises(ValueError):
                            self.api.report(self.ws, viewer)
                        renderer.assert_not_called()
                    self.assertTrue(link.is_symlink())
                    if exists:
                        self.assertEqual(target.read_bytes(), b"user bytes")
                        target.unlink()
                    else:
                        self.assertFalse(target.exists())
                    other = "session-summary.json" if name == "review.html" else "review.html"
                    self.assertFalse((self.ws / other).exists())
                    link.unlink()
        with patch.object(self.api.subprocess, "run", return_value=result) as renderer:
            report = self.api.report(self.ws, viewer)
            renderer.assert_called_once()
            self.assertEqual((self.ws / "review.html").read_bytes(), rendered)
            summary = json.loads((self.ws / "session-summary.json").read_text())
            self.assertEqual(summary["status"], "pending")
            self.assertFalse(summary["official_full_eval_accepted"])
            self.assertEqual(report["report"], str(self.ws / "review.html"))
            with self.assertRaises(ValueError):
                self.api.report(self.ws, viewer)
            renderer.assert_called_once()
            self.assertEqual((self.ws / "review.html").read_bytes(), rendered)

    def grade_fixture(self, run, delegate):
        results = self.root / "grade-results.json"
        results.write_text(json.dumps([{"id": 1, "verdict": "pass",
                                       "evidence_quote": "forty-two",
                                       "rationale": "Matches the independent fixture."}]))
        return self.api.grade(self.ws, run, results, delegate, "model-a")

    def test_added_directory_link_invalidates_all_campaign_operations(self):
        self.prepare()
        first = "eval-1/with_skill/run-1"
        second = "eval-1/without_skill/run-1"
        self.record(first)
        external = self.root / "external-inputs"
        external.mkdir()
        (external / "user.txt").write_bytes(b"preserve external bytes")
        link = self.ws / second / "inputs/unexpected-directory"
        link.symlink_to(external, target_is_directory=True)
        before = {str(p.relative_to(self.ws)): p.read_bytes()
                  for p in self.ws.rglob("*") if p.is_file() and not p.is_symlink()}
        for operation in (lambda: self.api.status(self.ws),
                          lambda: self.record(second, "candidate-b"),
                          lambda: self.grade_fixture(first, "grader-a")):
            with self.subTest(operation=operation):
                with self.assertRaises(ValueError):
                    operation()
                after = {str(p.relative_to(self.ws)): p.read_bytes()
                         for p in self.ws.rglob("*") if p.is_file() and not p.is_symlink()}
                self.assertEqual(after, before)
                self.assertEqual((external / "user.txt").read_bytes(), b"preserve external bytes")
                self.assertTrue(link.is_symlink())

    def test_inventory_refuses_linked_root_or_ancestor(self):
        external = self.root / "empty-target"
        external.mkdir()
        link = self.root / "inventory-link"
        link.symlink_to(external, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.api.inventory(link)
        child = external / "child"
        child.mkdir()
        with self.assertRaises(ValueError):
            self.api.inventory(link / "child")
        self.assertEqual(self.api.inventory(child), {})

    def test_role_collisions_rejected_in_both_orders_before_writes(self):
        self.prepare()
        first = "eval-1/with_skill/run-1"
        second = "eval-1/without_skill/run-1"
        self.record(first, "candidate-a")
        with self.assertRaises(ValueError):
            self.grade_fixture(first, "candidate-a")
        self.assertFalse((self.ws / first / "grading.json").exists())
        self.grade_fixture(first, "grader-a")
        with self.assertRaises(ValueError):
            self.record(second, "grader-a")
        self.assertFalse((self.ws / second / "execution.json").exists())
        self.assertFalse((self.ws / second / "grading-request.json").exists())
        self.record(second, "candidate-b")
        with self.assertRaises(ValueError):
            self.grade_fixture(second, "candidate-a")
        self.grade_fixture(second, "grader-b")
        self.assertEqual(self.api.status(self.ws)["status"], "complete-local")
        self.assertFalse(self.api.status(self.ws)["official_full_eval_accepted"])

    def test_readback_rejects_rebound_cross_role_campaign(self):
        self.prepare()
        first = "eval-1/with_skill/run-1"
        second = "eval-1/without_skill/run-1"
        self.record(first, "candidate-a")
        self.grade_fixture(first, "grader-a")
        self.record(second, "candidate-b")
        self.grade_fixture(second, "grader-b")
        grade = self.ws / first / "grading.json"
        document = json.loads(grade.read_text())
        document["delegate_id"] = "candidate-b"
        grade.write_text(json.dumps(document))
        import hashlib
        binding = self.ws / first / "grade-binding.json"
        binding.write_text(json.dumps({"grading_sha256": hashlib.sha256(grade.read_bytes()).hexdigest()}))
        with self.assertRaises(ValueError):
            self.api.status(self.ws)
        with self.assertRaises(ValueError):
            self.grade_fixture(second, "grader-c")

    def test_snapshot_tamper_blocks_status(self):
        self.prepare()
        (self.ws / "eval-1/with_skill/run-1/request.json").write_text("{}")
        with self.assertRaises(ValueError): self.api.status(self.ws)

if __name__ == "__main__": unittest.main()
