"""Static instruction checks, not proof of agent or hook execution."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("cycle", "research", "plan", "implement", "test", "judge", "iterate")
FIELDS = ("step", "modified files", "next step", "current goal", "next goal", "closed tasks", "explanation")

class PhaseFinalReport(unittest.TestCase):
    def test_every_entrypoint_requires_final_report(self):
        for name in NAMES:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            self.assertIn("End every phase delivery with the mandatory seven-field final report", text, name)
            self.assertIn("evaluate commit suitability after each confirmed closure", text, name)

    def test_final_fields_are_ordered_and_truthful(self):
        for name in NAMES:
            text = (ROOT / "skills" / name / "references/common-output.md").read_text()
            positions = [text.index("## " + field + "\n") for field in FIELDS]
            self.assertEqual(positions, sorted(positions), name)
            for required in ("blocked", "N/A", "confirmed closed", "preserved", "loop again", "done", "Pedagogical"):
                self.assertIn(required, text, name)

    def test_delivery_checklist_loads_both_contracts_before_handoff(self):
        for name in NAMES:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            self.assertIn("Before starting work, read", text)
            self.assertIn("## Before delivery or handoff", text)
            block = text.split("## Before delivery or handoff", 1)[1].split("## ", 1)[0]
            self.assertIn("references/common-output.md", block)
            self.assertIn("references/requirements-output.md", block)
            self.assertIn("- [ ]", block)
            self.assertLess(text.index("## Before delivery or handoff"), text.index("## Execute the handoff or stop"))

    def test_integration_aggregation_uses_current_final_report(self):
        import json
        cases = json.loads((ROOT / "integration/evals.json").read_text())["scenarios"]
        case = next(c for c in cases if c["id"] == "local-streaming-cycle")
        self.assertIn("The coordinator aggregates seven-field final reports with phase-specific explanation.", case["assertions"])
        self.assertNotIn("The coordinator aggregates six-field checkpoints.", case["assertions"])

    def test_closure_is_evaluation_not_permission(self):
        for name in NAMES:
            text = (ROOT / "skills" / name / "references/beads-integration.md").read_text()
            for required in ("## Post-closure commit evaluation", "perform", "propose", "skip", "blocked", "already committed", "not permission", "Never auto-push", "readback"):
                self.assertIn(required, text, name)

if __name__ == "__main__":
    unittest.main()
