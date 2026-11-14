"""User-scope source checks and hypothetical routes; no agent/tracker execution."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')
CAPABILITY = ROOT / 'skills/task-authoring'

# Independently specified natural requests, not generated activation commands.
SCENARIOS = (
    ('Create a ticket for the approved report-preservation fix.', 'create', True),
    ('Repair this ticket so its criteria describe the expected outcome.', 'repair', True),
    ('Read this existing ticket.', 'read', False),
    ('Claim this task for the assigned worker.', 'claim', False),
    ('Record progress on the task.', 'progress', False),
    ('Close the completed task.', 'closure', False),
)


class TaskAuthoring(unittest.TestCase):
    def test_discovery_and_natural_route_scenarios(self):
        text = (CAPABILITY / 'SKILL.md').read_text()
        metadata = text.split('---', 2)[1]
        self.assertIn('name: task-authoring', metadata)
        for word in ('creating', 'repairing', 'routine reads', 'claims', 'progress updates', 'closure'):
            self.assertIn(word, metadata)
        self.assertEqual([intent for _, intent, load in SCENARIOS if load], ['create', 'repair'])
        self.assertLessEqual(len(text.splitlines()), 500)
        for phase in PHASES:
            source = (ROOT / 'skills' / phase / 'SKILL.md').read_text()
            with self.subTest(phase=phase):
                self.assertEqual(source.count('Load `agentic-development:task-authoring`'), 1)
                self.assertIn('Before creating or repairing task descriptions', source)
                self.assertIn('For routine reads, claims, progress updates or closure, do not load task-authoring.', source)
                self.assertIn('established goal, scope, criteria, native tracker context and current authority', source)

    def test_unavailable_and_already_loaded_routes(self):
        for phase in PHASES:
            source = (ROOT / 'skills' / phase / 'SKILL.md').read_text()
            with self.subTest(phase=phase):
                for rule in ('already available and current', 'do not load both routes',
                             'If the optional capability is unavailable',
                             'references/ticket-authoring.md', 'not activation',
                             'do not retry loading', 'Resume this caller'):
                    self.assertIn(rule, source)
        canonical = (CAPABILITY / 'references/ticket-authoring.md').read_bytes()
        for phase in PHASES:
            self.assertEqual((ROOT / 'skills' / phase / 'references/ticket-authoring.md').read_bytes(), canonical)

    def test_bounded_output_and_denied_failed_write_scenarios(self):
        text = (CAPABILITY / 'SKILL.md').read_text()
        for rule in ('actual tracker ID with verified readback', 'clearly labeled proposal',
                     'Failed writes remain errors', 'After an actual write, read back',
                     'verify preserved history', 'STOP and return to the caller',
                     'Do not recursively load Cycle, Research or Plan',
                     'Missing write capability or permission yields a proposal',
                     'Preserve criterion IDs, native owner/status/relationships',
                     'do not invent', 'No phase report'):
            self.assertIn(rule, text)
        self.assertNotRegex(text, r'Load `agentic-development:(cycle|research|plan)`')
        for absent in ('requirements-output.md', 'common-output.md', 'review-policy.md',
                       'candidate-identity.md', 'commit-report.md'):
            self.assertNotIn(absent, text)

    def test_contained_authority_and_conditional_native_bridge(self):
        text = (CAPABILITY / 'SKILL.md').read_text()
        for link in re.findall(r'\]\(([^)]+)\)', text):
            path = (CAPABILITY / link).resolve()
            self.assertTrue(path.is_relative_to(CAPABILITY.resolve()))
            self.assertTrue(path.is_file())
        self.assertIn('If Beads is used, before native operations', text)
        self.assertNotRegex(text, r'`bd [^`]+`')
        authority = (CAPABILITY / 'references/authorization-policy.md').read_text()
        for rule in ('Loading guidance grants no permission', 'historical task notes',
                     'Do not steal a', 'close/reopen tasks', 'second task database'):
            self.assertIn(rule, authority)
        bridge = (CAPABILITY / 'references/beads-integration.md').read_text()
        for rule in ('current installed CLI help', 'database identity',
                     'Preserve the assigned owner and claim', 'read back the', 'reject cycles'):
            self.assertIn(rule, bridge)

    def test_inventory_exact_allowlist_not_eighth_phase(self):
        import sys
        sys.path.insert(0, str(ROOT / 'tools'))
        from production import SKILLS
        self.assertEqual(SKILLS, frozenset(PHASES) | {'task-authoring'})
        self.assertEqual({p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}, SKILLS)
        self.assertFalse((CAPABILITY / 'evals/evals.json').exists())


if __name__ == '__main__':
    unittest.main()
