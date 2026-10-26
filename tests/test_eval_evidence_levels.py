"""Independent source regressions for FIX-1/FIX-2; not behavioral proof."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
COUNTS = {"cycle": 29, "research": 24, "plan": 18, "implement": 18,
          "test": 17, "judge": 16, "iterate": 17}
# Requirements from the authorized defect report, not generated suite output.
ORDER_REQUIREMENTS = (
    "The common output contract is read after investigation before drafting delivery.",
    "The phase delivery contract is read before drafting delivery.",
    "Operational requirements are resolved before governed actions.",
    "Permission prerequisites are resolved before governed actions.",
)
OTHER_ORDER_REQUIREMENTS = (
    "Output contracts are read after investigation before drafting delivery.",
    "Operational prerequisites are not deferred.",
)


def suite(skill):
    return json.loads((ROOT / f"skills/{skill}/evals/evals.json").read_text())


def facts(skill):
    return json.loads((ROOT / f"skills/{skill}/evals/files/scenario-facts.json").read_text())["cases"]


class EvalEvidenceLevels(unittest.TestCase):
    def test_section_contract_has_no_six_heading_instruction(self):
        contract = (ROOT / "skills/implement/references/requirements-output.md").read_text()
        self.assertIn("five-heading", contract)
        for skill in COUNTS:
            for case in suite(skill)["evals"]:
                with self.subTest(skill=skill, case=case["id"]):
                    text = "\n".join([case["prompt"], case["expected_output"], *case["assertions"]])
                    self.assertIsNone(re.search(r"six[- ](?:ordered[- ]?)?section", text, re.I))
        case = suite("implement")["evals"][13]
        self.assertRegex(case["prompt"], r"five-section")
        self.assertTrue(any("five ordered sections" in a for a in case["assertions"]))

    def test_execution_requirements_are_retained_not_semantically_graded(self):
        for skill, count in COUNTS.items():
            cases = suite(skill)["evals"]
            self.assertEqual(len(cases), count)
            self.assertEqual([c["id"] for c in cases], list(range(1, count + 1)))
            for case in cases:
                with self.subTest(skill=skill, case=case["id"]):
                    self.assertEqual(case["target"]["execution"], "explain")
                    self.assertIn("navigation_expectations", case)
                    for requirement in ORDER_REQUIREMENTS + OTHER_ORDER_REQUIREMENTS:
                        self.assertNotIn(requirement, case["assertions"])
                    # The original 131 common cases have four frozen order requirements;
                    # cycle 22-24 have their own two, and cycle 25-29 are user additions.
                    required = (OTHER_ORDER_REQUIREMENTS if skill == "cycle" and 22 <= case["id"] <= 24
                                else () if skill == "cycle" and case["id"] >= 25
                                else ORDER_REQUIREMENTS)
                    retained = case.get("execution_assertions", [])
                    self.assertEqual([r["criterion"] for r in retained], list(required))
                    for requirement in retained:
                        self.assertEqual(requirement["evidence_requirement"], "tool-events/order")
                        self.assertEqual(requirement["grading"], "instrumented-execution-only")

    def test_history_fixtures_do_not_assert_cancellation_results(self):
        for skill, key in (("cycle", "normal"), ("plan", "normal"),
                           ("plan", "boundary"), ("implement", "boundary")):
            with self.subTest(skill=skill, case=key):
                record = facts(skill)[key]
                self.assertIn("history" if key == "boundary" or skill == "cycle" else "save", record["original_scenario"].lower())
                self.assertNotRegex(record["result"].lower(), r"cancellation|transport|ui stop")
        for skill in COUNTS:
            with self.subTest(skill=skill, case="commit-report"):
                record = facts(skill)["commit-report"]
                self.assertIn("history", record["result"].lower())
                self.assertNotRegex(record["result"].lower(), r"cancellation|transport|ui stop")
                self.assertEqual(record["commit"], "abc1234")
                self.assertEqual(record["committed_files"], ["src/history.ts", "tests/history.test.ts"])
                self.assertEqual(record["remaining_user_edit"], "src/view.ts")

    def test_blocking_fixtures_do_not_assert_success_or_ready_execution(self):
        for skill in COUNTS:
            records = facts(skill)
            with self.subTest(skill=skill, case="beads-claim-boundary"):
                record = records["beads-claim-boundary"]
                self.assertEqual(record["claim_result"], "conflict")
                self.assertRegex(record["result"].lower(), r"claim.*(?:fail|conflict)|(?:fail|conflict).*claim")
                self.assertRegex(record["next"].lower(), r"claim|owner|coordinator")
            with self.subTest(skill=skill, case="beads-recovery"):
                record = records["beads-recovery"]
                self.assertIn("TASK-18", record["result"])
                self.assertRegex(record["next"].lower(), r"block|depend|task-18")
            with self.subTest(skill=skill, case="session-end"):
                record = records["session-end"]
                self.assertEqual(record["judge"], "not-run")
                self.assertNotIn("Judge finding", record["result"])
                self.assertNotIn("complete acceptance evidence", record["result"])
                self.assertRegex(record["result"].lower(), r"old|stale")
                self.assertIn("package", record["next"].lower())
        self.assertNotIn("source trace links", facts("research")["missing-capability"]["result"])
        self.assertNotIn("owned cancellation changes", facts("implement")["missing-capability"]["result"])
        self.assertNotIn("complete acceptance evidence", facts("judge")["boundary"]["result"])
        self.assertNotIn("independent review context", facts("judge")["missing-capability"]["result"])


if __name__ == "__main__":
    unittest.main()
