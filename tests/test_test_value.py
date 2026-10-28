"""User TQ-1..6 source obligations; not application or agent behavior proof."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestValueContracts(unittest.TestCase):
    def test_selection_and_testability_start_from_guarantees(self):
        for phase in ('plan', 'implement', 'test'):
            text = (ROOT / 'skills' / phase / 'SKILL.md').read_text()
            with self.subTest(phase=phase):
                self.assertIn('product guarantee', text)
                self.assertIn('incorrect behavior', text)
                self.assertIn('cheapest valid', text)
        text = (ROOT / 'skills/implement/SKILL.md').read_text()
        self.assertIn('Do not add speculative abstractions', text)

    def test_rationalization_preserves_acceptance_not_legacy_count(self):
        text = ' '.join((ROOT / 'skills/test/references/test-value.md').read_text().split())
        for requirement in ('retain', 'merge', 'remove', 'replace',
                            'not a preservation obligation', 'not a fixed test-count ceiling',
                            'lost or preserved', 'actual or proposed',
                            'do not weaken product acceptance', 'confidence question', 'stop rule'):
            self.assertIn(requirement, text)
        self.assertIn('test-value.md', (ROOT / 'skills/test/SKILL.md').read_text())

    def test_oracles_and_cost_claims_are_discriminating(self):
        text = (ROOT / 'skills/test/references/test-value.md').read_text()
        for requirement in ('mock', 'copied production logic', 'exact',
                            'success or error', 'actually detected',
                            'end-to-end', 'wall time', 'aggregate', 'UNKNOWN'):
            self.assertIn(requirement, text)
        judge = (ROOT / 'skills/judge/SKILL.md').read_text()
        self.assertIn('marginal detection value', judge)
        self.assertIn('green test count', judge)

    def test_scenarios_cover_distinct_decisions_without_execution_claims(self):
        expected = {
            'test': {'test-value-rationalization', 'test-value-missing-ci'},
            'plan': {'plan-test-value'},
            'implement': {'implement-minimal-testability'},
            'judge': {'judge-green-suite-weak-oracle'},
        }
        for phase, names in expected.items():
            cases = json.loads((ROOT / 'skills' / phase / 'evals/evals.json').read_text())['evals']
            found = {c['name']: c for c in cases if c['name'] in names}
            self.assertEqual(set(found), names)
            for case in found.values():
                self.assertEqual(case['target']['execution'], 'explain')
                self.assertIn('hypothetical', case['prompt'])
                self.assertGreater(len(case['assertions']), 0)


if __name__ == '__main__':
    unittest.main()
