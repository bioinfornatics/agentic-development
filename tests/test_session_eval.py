"""Deterministic session bridge tests; synthetic outputs are not agent evidence."""
import importlib.util
import json
from pathlib import Path
import tempfile
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

    def test_snapshot_tamper_blocks_status(self):
        self.prepare()
        (self.ws / "eval-1/with_skill/run-1/request.json").write_text("{}")
        with self.assertRaises(ValueError): self.api.status(self.ws)

if __name__ == "__main__": unittest.main()
