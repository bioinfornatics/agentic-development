"""Static instruction checks, not Judge behavioral validation."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class JudgeResultContract(unittest.TestCase):
    def test_visible_verdict_and_score_contract(self):
        text = (ROOT / 'skills/judge/SKILL.md').read_text()
        self.assertIn('**Result contract**', text)
        for value in ('accepted', 'needs-correction', 'indeterminate', 'not-run'):
            self.assertIn('`' + value + '`', text)
        self.assertIn('PASS/FAIL', text)
        self.assertIn('result block', text)

    def test_each_verdict_routes_to_a_distinct_action(self):
        text = (ROOT / 'skills/judge/SKILL.md').read_text().split('7. [ ]', 1)[1]
        rows = {line.split('|')[1].strip().strip('`'): line for line in text.splitlines() if line.strip().startswith('| `')}
        for verdict in ('accepted', 'needs-correction', 'indeterminate', 'not-run'):
            self.assertIn(verdict, rows)
        self.assertIn('agentic-development:iterate', rows['needs-correction'])
        self.assertIn('no speculative code repair', rows['indeterminate'])
        self.assertIn('Execute Judge', rows['not-run'])
        self.assertIn('no implicit closure', rows['accepted'])
        self.assertIn('owner, prerequisite and expected result', text)

    def test_explicit_delivery_fields_and_all_modes(self):
        text = (ROOT / 'skills/judge/references/requirements-output.md').read_text()
        for field in ('verdict', 'review_mode', 'rubric_id', 'rubric_version', 'score', 'score_max', 'score_status', 'assessment_coverage_percent', 'blocking_findings', 'limitations'):
            self.assertIn(field + ':', text)
        for rule in ('complete', 'partial', 'not-applicable', 'not-assessed', 'small-task', 'not-run', 'indeterminate', 'null', '75', '95', '71.25'):
            self.assertIn(rule, text)
        self.assertIn('No numerical acceptance threshold', text)
        self.assertIn('Keep the five outer headings', text)

if __name__ == '__main__':
    unittest.main()
