"""Static regressions, not agent behavior or Git/Beads/Entire integration tests."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class WorkflowSourceContracts(unittest.TestCase):
    def test_boundary_reports_are_contained_and_consistent(self):
        for name in ("commit-report.md", "session-report.md"):
            paths = sorted(SKILLS.glob("*/references/" + name))
            self.assertEqual(len(paths), 7, name)
            self.assertEqual(len({p.read_bytes() for p in paths}), 1, name)
        for p in SKILLS.glob("*/SKILL.md"):
            with self.subTest(skill=p.parent.name):
                self.assertIn("references/commit-report.md", p.read_text())
                self.assertIn("references/session-report.md", p.read_text())

    def test_handoff_records_verified_git_beads_and_optional_entire(self):
        for p in SKILLS.glob("*/references/commit-report.md"):
            text = p.read_text()
            self.assertIn("## Git, Beads and optional Entire linkage", text)
            self.assertIn("Entire", text)
            self.assertIn("unavailable", text)
        for p in SKILLS.glob("*/references/session-report.md"):
            self.assertIn("## Durable restart record", p.read_text())

    def test_behavior_first_guidance_is_explicit(self):
        text = (SKILLS / "implement/SKILL.md").read_text()
        self.assertIn("observed red", text)
        self.assertIn("independent oracle", text)
        self.assertIn("## Red, green and refactor evidence", text)

    def test_missing_capability_fixture_is_not_a_known_defect(self):
        facts = json.loads((SKILLS / "iterate/evals/files/scenario-facts.json").read_text())
        case = facts["cases"]["missing-capability"]
        self.assertEqual(case["known_defect"], False)
        self.assertIn("local slice works", case["result"])
        self.assertNotIn("Repair propagation", case["next"])

    def test_exhausted_budget_fixture_does_not_route_to_repair(self):
        facts = json.loads((SKILLS / "iterate/evals/files/scenario-facts.json").read_text())
        case = facts["cases"]["boundary"]
        self.assertEqual(case["correction_round"], case["max_rounds"])
        self.assertIn("Stop", case["next"])
        self.assertNotIn("Repair propagation", case["next"])

    def test_boundary_scenarios_require_their_reporting_dependencies(self):
        for p in SKILLS.glob("*/evals/evals.json"):
            for case in json.loads(p.read_text())["evals"]:
                reads = case["navigation_expectations"]["must_read"]
                if case["name"].endswith("-commit-report"):
                    self.assertIn("references/commit-report.md", reads)
                if case["name"].endswith("-session-end"):
                    self.assertIn("references/session-report.md", reads)

    def test_review_mode_is_frozen_before_implementation(self):
        for p in SKILLS.glob("*/references/judgment-rubric.md"):
            self.assertIn("Select the mode before implementation", p.read_text())
            self.assertIn("numeric score already required", p.read_text())

    def test_plan_mode_and_evaluation_rubric_pin_match(self):
        plan = SKILLS / "plan"
        self.assertIn("review mode before implementation", (plan / "SKILL.md").read_text())
        version = (plan / "references/judgment-rubric.md").read_text().splitlines()[0].split()[-1]
        cases = json.loads((plan / "evals/evals.json").read_text())["evals"]
        assertion = next(a for a in cases[0]["assertions"] if "default rubric version" in a)
        self.assertIn(version, assertion)

    def test_test_phase_distinguishes_preliminary_checks(self):
        text = (SKILLS / "test/SKILL.md").read_text()
        self.assertIn("acceptance-bound checks", text)
        self.assertIn("Preliminary near-change checks", text)

    def test_requirements_output_contract_is_direct_and_identical(self):
        refs = list(SKILLS.glob("*/references/requirements-output.md"))
        self.assertEqual(len(refs), 7)
        self.assertEqual(len({p.read_bytes() for p in refs}), 1)
        for p in SKILLS.glob("*/SKILL.md"):
            self.assertIn("references/requirements-output.md", p.read_text())

    def test_goals_behavior_and_measurable_nfr_formats(self):
        text = (SKILLS / "plan/references/requirements-output.md").read_text()
        for expected in ("Goals", "Non-goals", "Given", "When", "Then",
                         "Metric", "Target", "Unit", "Workload", "Environment",
                         "Measurement", "Approval", "Do not invent"):
            self.assertIn(expected, text)
        self.assertIn("research question", text)
        self.assertIn("N/A", text)

    def test_handoff_has_fixed_notification_fields(self):
        text = (SKILLS / "cycle/references/requirements-output.md").read_text()
        for expected in ("## 1. Objective and scope", "## 2. Result",
                         "## 3. Changes and evidence", "## 4. Verdict and uncertainties",
                         "## 5. Transition", "## 6. Next action and restart",
                         "Files", "Branches", "Commits", "Session recommendation",
                         "Session action", "none", "failed", "externally observed"):
            self.assertIn(expected, text)

    def test_phase_output_formats_are_explicit(self):
        text = (SKILLS / "cycle/references/requirements-output.md").read_text()
        for name in ("cycle", "research", "plan", "implement",
                     "test", "judge", "iterate"):
            self.assertIn("### " + name, text)
        self.assertIn("Unchanged criteria", text)
        self.assertIn("do not silently lower", text)

    def test_task_structure_is_in_the_state_template(self):
        text = (SKILLS / "cycle/assets/cycle-state.md").read_text()
        for expected in ("## Goals and Non-goals", "## Functional requirements",
                         "## Non-functional requirements", "Given", "When", "Then",
                         "Session recommendation", "Session action"):
            self.assertIn(expected, text)

    def test_all_source_markdown_links_resolve(self):
        paths = [ROOT / "README.md", *SKILLS.rglob("*.md")]
        for p in paths:
            for part in p.read_text().split("](")[1:]:
                target = part.split(")", 1)[0].split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                self.assertTrue((p.parent / target).exists(), (p, target))

    def test_shared_safety_policies_and_budget_guard_remain(self):
        for name in ("authorization-policy.md", "review-policy.md"):
            paths = list(SKILLS.glob("*/references/" + name))
            self.assertEqual(len(paths), 7)
            self.assertEqual(len({p.read_bytes() for p in paths}), 1)
        text = (SKILLS / "iterate/SKILL.md").read_text()
        self.assertIn("do not increment the round counter", text)
        self.assertIn("Never start a correction after its budget is exhausted", text)


if __name__ == "__main__":
    unittest.main()
