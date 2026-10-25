"""Static report usability and persistence boundaries, not agent execution."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
NAMES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')

class ReportPersistence(unittest.TestCase):
    def test_reports_defined_before_use_without_filename_obligations(self):
        for name in NAMES:
            text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
            self.assertIn('A phase report is the result of this Skill', text, name)
            for filename in ('research.md','plan.md','changes.md','evidence.md','judgment.md','iteration.md'):
                self.assertNotIn(filename, text, name)
            self.assertIn('inline by default', text, name)

    def test_shared_optional_save_contract(self):
        copies = []
        for name in NAMES:
            text = (ROOT / 'skills' / name / 'references/common-output.md').read_text()
            copies.append(text)
            for rule in ('## Report delivery and optional saving', 'inline by default',
                         'explicit destination', 'permission to write', 'Never overwrite',
                         'not saved', 'required durable', 'Beads remains task truth'):
                self.assertIn(rule, text, name)
        self.assertEqual(len(set(copies)), 1)

    def test_phase_contents_not_mandatory_files(self):
        for name in NAMES:
            text = (ROOT / 'skills' / name / 'references/requirements-output.md').read_text()
            self.assertIn('Report content:', text, name)
            self.assertIn('Optional filename:', text, name)
            self.assertIn('not a required input or automatic write', text, name)
            self.assertNotIn('Artifact:', text, name)
        judge = (ROOT / 'skills/judge/references/requirements-output.md').read_text()
        self.assertEqual(judge.count('judgment.md'), 1)
        self.assertIn('judgment report', judge)

if __name__ == '__main__':
    unittest.main()
