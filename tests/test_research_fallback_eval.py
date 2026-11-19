"""Static source evidence for epic FR-2 in the Research eval suite; not agent execution.

Expected values come from the user scope (FR-2): with worker capability verified
absent, Research proceeds directly and discloses `direct, reduced independence`;
with capability present but a failed dispatch, it reports a blocker; it asks the
user only for a missing permission. They are not copied from the eval file.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "skills/research/evals/evals.json"
NAME = "research-delegation-unavailable"
LABEL = "direct, reduced independence"


def scenario():
    cases = json.loads(SUITE.read_text())["evals"]
    return next(c for c in cases if c["name"] == NAME)


def text(case):
    return "\n".join([case["prompt"], case["expected_output"], *case["assertions"]]).lower()


class ResearchFallbackEval(unittest.TestCase):
    def test_no_permission_gate_for_direct_investigation(self):
        cases = json.loads(SUITE.read_text())["evals"]
        for case in cases:
            with self.subTest(case=case["name"]):
                body = text(case)
                self.assertNotIn("direct investigation requires explicit user permission", body)
                self.assertNotIn("no direct fallback has been approved", body)
                self.assertNotIn("direct investigation has not been authorized", body)

    def test_absent_capability_expects_disclosed_direct_fallback(self):
        case = scenario()
        self.assertEqual(case["id"], 22)
        self.assertIn(LABEL, text(case))
        assertions = "\n".join(case["assertions"]).lower()
        self.assertIn(LABEL, assertions)
        self.assertIn("silent", assertions)
        self.assertIn("missing permission", assertions)

    def test_failed_dispatch_with_capability_expects_blocker(self):
        case = scenario()
        self.assertIn("dispatch fails", case["prompt"].lower())
        self.assertTrue(any("blocker" in a.lower() and "dispatch" in a.lower()
                            for a in case["assertions"]))


if __name__ == "__main__":
    unittest.main()
