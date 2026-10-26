"""Static creator-input and distribution-boundary checks, not agent execution."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/cycle"
NAMES = {"local-streaming-cycle", "dirty-ui-handoff", "commit-to-session-handoff",
         "beads-tracker-to-handoff", "adversarial-permission-and-drift"}

class CycleEvalSets(unittest.TestCase):
    def load(self):
        return json.loads((SKILL / "evals/evals.json").read_text())

    def test_canonical_cases_and_contained_distinct_fixtures(self):
        data = self.load()
        self.assertEqual(data["skill_name"], "cycle")
        cases = data["evals"]
        self.assertTrue(NAMES.issubset({c["name"] for c in cases}))
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        cases = [c for c in cases if c["name"] in NAMES]
        facts = []
        for case in cases:
            self.assertIs(type(case["id"]), int)
            self.assertEqual(case["target"]["execution"], "explain")
            self.assertEqual(case["target"]["path"], ".")
            self.assertTrue(case["expected_output"])
            self.assertTrue(case["assertions"])
            self.assertIn("language:" + case["language"], case["coverage_tags"])
            self.assertEqual(case["capabilities"]["tools"], ["developer"])
            self.assertGreater(case["budget"]["max_turns"], 0)
            self.assertGreater(case["budget"]["timeout_seconds"], 0)
            for name in case["files"]:
                path = (SKILL / name).resolve()
                self.assertTrue(path.is_relative_to(SKILL))
                self.assertIn(name, case["prompt"])
                fact = json.loads(path.read_text())
                self.assertEqual(fact["fixture_kind"], "hypothetical-input-not-execution-evidence")
                self.assertEqual(fact["case_id"], case["name"])
                facts.append(json.dumps(fact, sort_keys=True))
        self.assertEqual(len(set(facts)), 5)
        budget = data["aggregate_budget"]
        self.assertGreaterEqual(budget["max_runs"], 30)
        self.assertGreaterEqual(budget["max_turns"], sum(c["budget"]["max_turns"] for c in cases) * 6)
        self.assertGreaterEqual(budget["timeout_seconds"], sum(c["budget"]["timeout_seconds"] for c in cases) * 6)

    def test_scenario_specific_records(self):
        fixtures = {c["name"]: json.loads((SKILL / c["files"][0]).read_text()) for c in self.load()["evals"] if c["name"] in NAMES}
        self.assertIn("approved_plan", fixtures["local-streaming-cycle"])
        self.assertIn("dirty_user_hunks", fixtures["dirty-ui-handoff"])
        self.assertIn("commit_receipt", fixtures["commit-to-session-handoff"])
        self.assertIn("claim_readback", fixtures["beads-tracker-to-handoff"])
        self.assertIn("input_drift", fixtures["adversarial-permission-and-drift"])

    def test_evals_are_excluded_from_generated_installation(self):
        self.assertTrue((SKILL / "evals/evals.json").is_file())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "product"
            result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/production.py"), "project", str(out)], capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((out / "skills/cycle/evals").exists())
            self.assertFalse((out / "integration").exists())
            self.assertTrue((out / "skills/cycle/SKILL.md").is_file())

if __name__ == "__main__":
    unittest.main()
