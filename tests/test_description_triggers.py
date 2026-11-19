"""Source tripwire for the qws.3 trigger wording; guards accidental edits, not routing evidence."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def description(skill):
    text = (ROOT / 'skills' / skill / 'SKILL.md').read_text()
    return text.split('description:', 1)[1].split('\n', 1)[0].strip()


class DescriptionTriggers(unittest.TestCase):
    def test_research_names_diagnosis_only_requests(self):
        text = description('research')
        for phrase in ('fails, regresses or is flaky', 'diagnosis-only requests', 'clear or familiar'):
            self.assertIn(phrase, text)

    def test_judge_names_branches_diffs_without_promising_merge_readiness(self):
        text = description('judge')
        for phrase in ('branch, diff or pull request', 'acceptance criteria', 'frozen software candidate'):
            self.assertIn(phrase, text)
        self.assertNotIn('ready to merge', text)

    def test_judge_body_handles_a_pull_request_without_test_evidence(self):
        body = (ROOT / 'skills/judge/SKILL.md').read_text().split('## Select the action from the intent', 1)[1]
        row = next(line for line in body.splitlines() if 'pull request without Test evidence' in line)
        for phrase in ('exact head commit', 'non-acceptance', 'indeterminate', 'not merge approval'):
            self.assertIn(phrase, row)

    def test_descriptions_stay_within_the_metadata_limit(self):
        for skill in ('research', 'judge'):
            with self.subTest(skill=skill):
                self.assertLessEqual(len(description(skill)), 1024)


if __name__ == '__main__':
    unittest.main()
