"""Source contracts for implement/iterate audit gaps; static, not agent-behavior proof."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def flat(phase):
    return ' '.join((ROOT / 'skills' / phase / 'SKILL.md').read_text().split())


def description(phase):
    text = (ROOT / 'skills' / phase / 'SKILL.md').read_text()
    return text.split('description:', 1)[1].split('\n', 1)[0]


class ImplementGaps(unittest.TestCase):
    def setUp(self):
        self.text = flat('implement')

    def test_description_is_distinctive_and_scoped(self):
        text = description('implement')
        for term in (r'\bred\b', r'\bgreen\b', r'change ledger', r'\bPlan\b', r'\bIterate\b'):
            self.assertRegex(text, term)
        self.assertNotIn('Supports', text)

    def test_characterization_precedes_unprotected_change(self):
        self.assertRegex(self.text, r'no discriminating test.{0,160}characterization test')
        self.assertRegex(self.text, r'characterization test.{0,200}green before')
        self.assertIn('characterization, not specification', self.text)

    def test_ledger_records_red_and_test_weakening(self):
        self.assertIn('red command and a failing-output excerpt', self.text)
        self.assertRegex(self.text, r'deleted, skipped, renamed or loosened test.{0,200}approved criterion change')
        self.assertIn('unjustified entry blocks handoff', self.text)

    def test_tests_read_as_living_documentation(self):
        self.assertRegex(self.text, r'new test.{0,60}behavior.{0,60}criterion ID')

    def test_parallel_writer_default(self):
        self.assertRegex(self.text, r'default.{0,40}disjoint paths in the shared tree')
        self.assertRegex(self.text, r'approved worktree per writer.{0,160}otherwise serialize')
        self.assertIn('grants no Git authority', self.text)


class IterateGaps(unittest.TestCase):
    def setUp(self):
        self.text = flat('iterate')

    def test_description_states_routing_without_code_edits(self):
        text = description('iterate')
        self.assertIn('routes', text)
        self.assertIn('does not edit code', text)

    def test_unknown_cause_names_root_cause_investigation(self):
        self.assertRegex(self.text, r'unknown causes?.{0,120}root-cause investigation')

    def test_budget_uses_one_term(self):
        for legacy in ('correction round', 'round counter', 'three-correction counter'):
            self.assertNotIn(legacy, self.text)
        self.assertIn('attempt counter', self.text)
        self.assertIn('Default maximum: three authorized attempts', self.text)
        self.assertIn('consumes zero attempts', self.text)


if __name__ == '__main__':
    unittest.main()
