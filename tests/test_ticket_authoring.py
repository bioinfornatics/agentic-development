"""Static ticket instruction coverage, not proof of agent ticket quality."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')

class TicketAuthoring(unittest.TestCase):
    def test_contained_guidance_and_conditional_links(self):
        copies = []
        for name in NAMES:
            base = ROOT / 'skills' / name
            text = (base / 'references' / 'ticket-authoring.md').read_text()
            copies.append(text)
            entry = (base / 'SKILL.md').read_text()
            self.assertIn('references/ticket-authoring.md', entry)
            self.assertIn('Before creating or repairing task descriptions', entry)
        self.assertEqual(len(set(copies)), 1)

    def test_readable_template_and_readiness(self):
        text = (ROOT / 'skills/plan/references/ticket-authoring.md').read_text()
        for section in ('## Why', '## Expected outcome', '## Scope and non-goals',
                        '## Acceptance criteria', '## Open decisions',
                        '## Technical starting point', '## Reading references',
                        '## Verification', '## Restart'):
            self.assertIn(section, text)
        for rule in ('Given:', 'When:', 'Then:', 'one observable outcome',
                     'non-behavioral', 'required/supporting', 'source identity',
                     'acceptance field', 'notes', 'not an enforcement engine',
                     'block the affected work', 'Do not change criterion IDs'):
            self.assertIn(rule, text)

    def test_targeted_ticket_quality_rules_and_example(self):
        text = (ROOT / 'skills/plan/references/ticket-authoring.md').read_text()
        for rule in ('verb and specific outcome', 'not by file',
                     'current behavior', 'expected behavior', 'minimal reproduction',
                     'hypothesis is not an observed cause', 'implementation steps',
                     'Decision / owner / readiness impact', 'only the ticket',
                     '## Filled example', '## Readiness checklist',
                     'Preserve the required facts; combine headings'):
            self.assertIn(rule, text)
        example = text.split('## Filled example', 1)[1].split('## Readiness checklist', 1)[0]
        self.assertIn('Given:', example)
        self.assertIn('When:', example)
        self.assertIn('Then:', example)
        self.assertIn('Hypothetical', example)

    def test_product_questions_precede_technical_details(self):
        text = (ROOT / 'skills/plan/references/ticket-authoring.md').read_text()
        template = text.split('## Description template', 1)[1].split('~~~markdown', 1)[1].split('~~~', 1)[0]
        headings = [line for line in template.splitlines() if line.startswith('## ')]
        self.assertEqual(headings[:6], [
            '## Why', '## Expected outcome', '## Scope and non-goals',
            '## Acceptance criteria', '## Open decisions', '## Technical starting point'])
        self.assertNotIn('current permission scope/prohibitions', template)
        self.assertNotIn('verify workspace, ownership, candidate and permissions', template)

    def test_no_generic_policy_copies_or_hidden_product_choices(self):
        text = (ROOT / 'skills/plan/references/ticket-authoring.md').read_text()
        for rule in ('Do not copy general work instructions', 'task-specific restrictions',
                     'Do not invent an end user', 'Verify current facts',
                     'A commit or prior decision is context, not the problem',
                     'without technical vocabulary', 'scope change, not a wording repair'):
            self.assertIn(rule, text)
        entry = (ROOT / 'skills/plan/SKILL.md').read_text()
        self.assertIn('problem, expected user change, observable success and open decisions', entry)
        self.assertIn('Do not copy general work instructions', entry)

    def test_concrete_frontier_and_consolidated_updates(self):
        text = (ROOT / 'skills/plan/references/ticket-authoring.md').read_text()
        for rule in ('## Concrete execution frontier', 'managed versus self-hosted',
                     'producer → transport → consumer', '| Read |', '| Create |',
                     '| Modify |', '| Preserve |', '| Exclude |',
                     'Proposed files are not existing assets',
                     '## Consolidate updates, do not append competing specifications',
                     'reject cycles', 'architecture selection depend on',
                     'Readback checks', 'not only nonempty fields'):
            self.assertIn(rule, text)
        self.assertIn('Contract version: 1.3.0', text)
        for phase in ('cycle', 'plan', 'implement'):
            entry = (ROOT / 'skills' / phase / 'SKILL.md').read_text()
            self.assertIn('name: ' + phase + '\n', entry)
            self.assertNotIn('name: agentic-development:', entry)
        plan = (ROOT / 'skills/plan/SKILL.md').read_text()
        self.assertIn('Read/Create/Modify/Preserve/Exclude', plan)
        self.assertIn('consolidate current solution/steps/files', plan)
        implement = (ROOT / 'skills/implement/SKILL.md').read_text()
        self.assertIn('Missing delivery design is a readiness gap', implement)
        cycle = (ROOT / 'skills/cycle/SKILL.md').read_text()
        self.assertIn('a populated tracker record alone', cycle)

    def test_backported_scenarios_are_neutral_and_additive(self):
        base = ROOT / 'skills/plan'
        suite = json.loads((base / 'evals/evals.json').read_text())
        cases = suite['evals']
        self.assertEqual(len({case['id'] for case in cases}), len(cases))
        existing = {'plan-normal', 'plan-boundary', 'plan-missing-capability',
                    'plan-numeric-score-preservation', 'plan-goals-gwt-quantified-nfr',
                    'plan-test-value', 'plan-readable-ticket-repair'}
        added = {'concrete-managed-service-ticket', 'consolidate-updated-ticket',
                 'changed-scope-dependency-readiness'}
        self.assertTrue(existing | added <= {case['name'] for case in cases})
        allowed = {'id', 'name', 'subject', 'language', 'target', 'coverage_tags',
                   'prompt', 'assertions', 'expected_output', 'files'}
        for case in cases:
            if case['name'] not in added:
                continue
            self.assertTrue(set(case) <= allowed)
            self.assertIs(type(case['id']), int)
            self.assertEqual(case['language'], 'en')
            self.assertTrue(case['prompt'])
            self.assertTrue(case['assertions'])
            self.assertTrue(case['expected_output'])
            for tag in case['coverage_tags']:
                dimension, value = tag.split(':', 1)
                self.assertIn(value, suite['coverage_dimensions'][dimension])
            for name in case['files']:
                path = (base / name).resolve()
                self.assertTrue(path.is_relative_to(base))
                self.assertTrue(path.is_file())
                self.assertIn(name, case['prompt'])
                self.assertNotIn('SKILL.md', name)
        ticket = (base / 'evals/inputs/ticket.md').read_text()
        self.assertIn('IAM-7-AC1', ticket)
        self.assertIn('IAM-7-AC2', ticket)
        self.assertIn('assignee alex', ticket)
        deps = (base / 'evals/inputs/dependencies.md').read_text()
        self.assertIn('ARCH-2 waits on IMPL-3', deps)

    def test_beads_bridge_preserves_separate_fields(self):
        copies = []
        for name in NAMES:
            text = (ROOT / 'skills' / name / 'references/beads-integration.md').read_text()
            copies.append(text)
            self.assertIn('acceptance field', text)
            self.assertIn('description', text)
            self.assertIn('notes', text)
            self.assertIn('readback', text)
        self.assertEqual(len(set(copies)), 1)

if __name__ == '__main__':
    unittest.main()
