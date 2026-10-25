"""Static ticket instruction coverage, not proof of agent ticket quality."""
from pathlib import Path
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
        for section in ('## Why', '## What', '## How', '## Scope and non-goals',
                        '## Acceptance criteria', '## Reading references',
                        '## Verification', '## Ownership and dependencies', '## Restart'):
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
