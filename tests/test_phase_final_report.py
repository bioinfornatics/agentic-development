"""Static instruction checks, not proof of agent or hook execution."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("cycle", "research", "plan", "implement", "test", "judge", "iterate")
FIELDS = ("current goal {step: <cycle|research|plan|implement|test|judge|iterate>}", "roadmap position", "modified files", "closed tasks", "explanation")

class PhaseFinalReport(unittest.TestCase):
    def test_every_entrypoint_requires_final_report(self):
        for name in NAMES:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            self.assertIn("apply their checklists and five-section report", text, name)
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
            self.assertNotIn("Before starting work, read", text)
            self.assertIn("references/requirements-baseline.md", text)
            from test_cycle_disclosure import workflow_steps
            steps = workflow_steps(text)
            self.assertGreaterEqual(len(steps), 5, name)
            self.assertEqual([number for number, _, _ in steps], list(range(1, len(steps) + 1)), name)
            delivery = steps[-2][2]
            self.assertRegex(delivery, r'After investigation and (?:immediately )?before drafting')
            self.assertIn('including blocked or unchanged results', delivery)
            for reference in ('references/common-output.md', 'references/requirements-output.md'):
                self.assertIn(reference, delivery, name)
                self.assertEqual(text.count(reference), 1, (name, reference))
            self.assertEqual(steps[-1][1], 'Execute the handoff or stop')
            self.assertNotIn('## Before delivery or handoff', text)
            self.assertNotIn('## Execute the handoff or stop', text)

    def test_integration_aggregation_uses_current_final_report(self):
        import json
        cases = json.loads((ROOT / "integration/evals.json").read_text())["scenarios"]
        case = next(c for c in cases if c["id"] == "local-streaming-cycle")
        self.assertIn("The coordinator aggregates five-section final reports with phase-specific explanation.", case["assertions"])
        self.assertNotIn("The coordinator aggregates six-field checkpoints.", case["assertions"])

    def test_closure_is_evaluation_not_permission(self):
        for name in NAMES:
            text = (ROOT / "skills" / name / "references/beads-integration.md").read_text()
            for required in ("## Post-closure commit evaluation", "perform", "propose", "skip", "blocked", "already committed", "not permission", "Never auto-push", "readback"):
                self.assertIn(required, text, name)

if __name__ == "__main__":
    unittest.main()
