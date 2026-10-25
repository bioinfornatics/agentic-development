"""Static instruction-contract checks; not proof of agent behavior."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class InstructionQuality(unittest.TestCase):
    def test_reuse_branch_is_contained_and_decision_complete(self):
        entry = (ROOT / "skills/research/SKILL.md").read_text()
        self.assertIn("references/reuse-decision.md", entry)
        text = (ROOT / "skills/research/references/reuse-decision.md").read_text()
        for required in ("repository", "unavailable", "compatibility", "license",
                         "maintenance", "security", "integration cost",
                         "reuse", "extend", "build", "does not authorize installation"):
            self.assertIn(required, text)

    def test_review_branch_preserves_evidence_and_mandatory_failures(self):
        entry = (ROOT / "skills/judge/SKILL.md").read_text()
        self.assertIn("references/finding-verification.md", entry)
        text = (ROOT / "skills/judge/references/finding-verification.md").read_text()
        for required in ("reachability", "surrounding context", "observed", "inferred",
                         "severity", "impact", "duplicate", "taste", "unknown",
                         "mandatory", "not reproduced"):
            self.assertIn(required, text)

    def test_new_instructions_have_no_reference_brand_or_host_dependency(self):
        for name in ("research/references/reuse-decision.md",
                     "judge/references/finding-verification.md"):
            text = (ROOT / "skills" / name).read_text()
            self.assertNotIn("ecc", text.lower())
            self.assertNotIn("~/.claude", text)
            self.assertNotIn("Launches the researcher agent", text)

if __name__ == "__main__":
    unittest.main()
