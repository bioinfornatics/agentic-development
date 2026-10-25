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
                header = '| Order | Intent / condition | Skill | Required output / exit gate |' if path.parent.name == 'cycle' else '| Intent / condition | Execute | Required result |'
                self.assertIn(header, text)
                from test_cycle_disclosure import workflow_steps
                self.assertEqual(workflow_steps(text)[-1][1], 'Execute the handoff or stop')
                self.assertIn('Load the selected phase' if path.parent.name == 'cycle' else 'Load `agentic-development:', text)
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
        self.assertIn('these identifiers are not shell', text)
        self.assertIn('commands', text)
        self.assertIn('report direct reading rather than activation', text)
        self.assertNotIn('do not assume Goose support', text)


class ProgressiveCommits(unittest.TestCase):
    def test_coherent_units_have_task_bound_commit_decisions(self):
        text = (ROOT / 'skills/implement/SKILL.md').read_text()
        batch = text.split('4. [ ]', 1)[1].split('5. [ ]', 1)[0]
        for rule in ('before starting a distinct objective', 'verified task IDs', 'epic/US', 'not one commit per file or task', 'more than one commit'):
            self.assertIn(rule, batch)
        for rule in ('Gitmoji only when the project convention approves it', 'meaningful text', 'current scoped authority', 'propose the message', 'Never auto-push'):
            self.assertIn(rule, text)

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
            from test_cycle_disclosure import workflow_steps
            steps = workflow_steps(text)
            for reference in ('authorization-policy', 'beads-integration'):
                self.assertIn('references/' + reference + '.md', steps[0][2])
            for reference in ('requirements-baseline', 'review-policy', 'candidate-identity'):
                self.assertIn('references/' + reference + '.md', ''.join(body for _, _, body in steps[:-2]))
            self.assertIn('before', steps[0][2].lower())
            if path.parent.name == 'research':
                for ref in ('requirements-baseline', 'review-policy'):
                    self.assertLess(text.index('references/' + ref + '.md'), text.index('2. [ ]'))
                self.assertLess(text.index('references/candidate-identity.md'), text.index('- Retrieve likely entry points'))
            elif path.parent.name == 'implement':
                self.assertLess(text.index('references/review-policy.md'), text.index('2. [ ]'))
                self.assertLess(text.index('references/candidate-identity.md'), text.index('3. [ ]'))
            elif path.parent.name in ('test', 'judge'):
                self.assertLess(text.index('references/candidate-identity.md'), text.index('3. [ ]'))
                self.assertLess(text.index('references/review-policy.md'), text.index('3. [ ]'))
            else:
                self.assertLess(text.index('references/requirements-baseline.md'), text.index('3. [ ]'))


class CanonicalExecutionOrder(unittest.TestCase):
    def test_entrypoints_reference_one_artifact_format(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            text = path.read_text()
            self.assertEqual(text.count('references/requirements-output.md'), 1, path)
            self.assertIn('apply their checklists and five-section report', text, path)
            self.assertNotIn('with four separate sections', text, path)
            for filename in ('plan.md', 'research.md', 'changes.md', 'evidence.md', 'iteration.md'):
                self.assertNotIn('Use ' + filename + ' headings:', text, path)

    def test_handoff_is_last_after_lifecycle_safeguards(self):
        for path in (ROOT / 'skills').glob('*/SKILL.md'):
            from test_cycle_disclosure import workflow_steps
            steps = workflow_steps(path.read_text())
            self.assertEqual(steps[-1][1], 'Execute the handoff or stop', path)
            self.assertIn('references/common-output.md', steps[-2][2], path)

    def test_iteration_defines_and_records_attempt_before_dispatch(self):
        text = (ROOT / 'skills/iterate/SKILL.md').read_text()
        workflow = text.split('## Workflow', 1)[1].split('## Session', 1)[0]
        define = workflow.index('define the smallest corrective task')
        counter = workflow.index('Increment and record the before/after counter')
        dispatch = workflow.index('Load '+chr(96)+'agentic-development:implement'+chr(96))
        self.assertLess(define, counter)
        self.assertLess(counter, dispatch)
        self.assertIn('without starting an attempt', workflow)
        self.assertIn('BEFORE dispatch; stop if required recording is unavailable', workflow)
        self.assertIn('Diagnosis, planning and waiting never increment it', workflow)

if __name__ == '__main__':
    unittest.main()
