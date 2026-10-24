"""Source-contract checks only; not evidence of agent execution quality."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SkillOperability(unittest.TestCase):
    def test_every_entrypoint_selects_actions_and_explicit_transitions(self):
        entries = list((ROOT / 'skills').glob('*/SKILL.md'))
        self.assertEqual(len(entries), 7)
        for path in entries:
            text = path.read_text()
            with self.subTest(skill=path.parent.name):
                self.assertIn('## Select the action from the intent', text)
                self.assertIn('| Intent / condition | Execute | Required result |', text)
                self.assertIn('## Execute the handoff or stop', text)
                self.assertIn('Load \u0060agentic-development:', text)
                self.assertIn('specific missing input', text)
                self.assertNotIn('full name in Goose', text)
                self.assertLessEqual(len(text.splitlines()), 500)

    def test_plan_directs_hierarchy_and_verified_tracker_writes(self):
        text = (ROOT / 'skills/plan/SKILL.md').read_text()
        for token in ('roadmap', 'epic', 'user story', 'Create or update',
                      'read back', 'tracker', 'authorized'):
            self.assertIn(token, text)

    def test_implementation_workflow_puts_red_before_production_edits(self):
        text = (ROOT / 'skills/implement/SKILL.md').read_text()
        workflow = text.split('## Workflow', 1)[1].split('## Commit safeguard', 1)[0]
        self.assertLess(workflow.index('observed red'), workflow.index('production change'))
        self.assertIn('rerun the same checks', workflow)

    def test_loading_contract_does_not_invent_host_command(self):
        text = (ROOT / 'skills/cycle/SKILL.md').read_text()
        self.assertIn('host', text)
        self.assertIn('not a universal shell command', text)
        self.assertNotIn('do not assume Goose support', text)


class ShortSkillNames(unittest.TestCase):
    def test_exact_seven_short_entrypoints(self):
        names = {'cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate'}
        self.assertEqual({p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}, names)
        for name in names:
            path = ROOT / 'skills' / name / 'SKILL.md'
            if path.exists():
                self.assertIn('name: ' + name, path.read_text().split('---', 2)[1])

    def test_operational_sources_use_only_current_names(self):
        legacy = ('drive' + '-cycle', *[n + '-slice' for n in
                  ('research', 'plan', 'implement', 'test', 'judge', 'iterate')])
        paths = [ROOT / 'README.md', *(ROOT / 'docs').glob('*.md'),
                 *(ROOT / 'skills').rglob('*.md'), *(ROOT / 'skills').rglob('*.json'),
                 ROOT / 'integration/evals.json']
        for path in paths:
            for old in legacy:
                self.assertNotIn(old, path.read_text(), str(path))

    def test_each_routed_skill_is_bundled(self):
        import re
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            for name in re.findall(r'agentic-development:([a-z-]+)', path.read_text()):
                self.assertTrue((ROOT / 'skills' / name / 'SKILL.md').is_file(), (path, name))

    def test_contribution_guide_directs_operable_authoring(self):
        text = (ROOT / 'docs/contributing.md').read_text()
        self.assertIn('intention', text)
        self.assertIn('action', text)
        self.assertIn('prerequisites', text)


class PhaseScope(unittest.TestCase):
    def test_phase_only_request_returns_instead_of_auto_executing_handoff(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            with self.subTest(skill=path.parent.name):
                self.assertIn('For a phase-only request', path.read_text())
                self.assertIn('proposed handoff, then stop', path.read_text())

    def test_safety_gates_precede_execution(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            text = path.read_text()
            workflow = text.index('## Start or resume' if path.parent.name == 'cycle' else '## Workflow')
            self.assertLess(text.index('## Trust, candidate and review gates'), workflow)
            self.assertLess(text.index('## Conditional durable tracking'), workflow)

class CanonicalExecutionOrder(unittest.TestCase):
    def test_entrypoints_reference_one_artifact_format(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            text = path.read_text()
            self.assertIn('canonical', text, path)
            self.assertNotIn('with four separate sections', text, path)
            for filename in ('plan.md', 'research.md', 'changes.md', 'evidence.md', 'iteration.md'):
                self.assertNotIn('Use ' + filename + ' headings:', text, path)

    def test_handoff_is_last_after_lifecycle_safeguards(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            sections = [line for line in path.read_text().splitlines() if line.startswith('## ')]
            self.assertEqual(sections[-1], '## Execute the handoff or stop', path)

    def test_iteration_defines_and_records_attempt_before_dispatch(self):
        text = (ROOT / 'skills/iterate/SKILL.md').read_text()
        workflow = text.split('## Workflow', 1)[1].split('## Session', 1)[0]
        define = workflow.index('define the smallest corrective task')
        counter = workflow.index('Increment the round counter')
        dispatch = workflow.index('Load Implement then Test')
        self.assertLess(define, counter)
        self.assertLess(counter, dispatch)
        self.assertIn('without starting an attempt', workflow)

if __name__ == '__main__':
    unittest.main()
