"""User-approved CYC-P1..P4 source contracts, not behavioral efficiency evidence."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class Proportionality(unittest.TestCase):
    def test_roadmap_is_conditional_without_losing_scope(self):
        text = (ROOT / 'skills/cycle/SKILL.md').read_text()
        self.assertIn('Propose a missing roadmap only', text)
        self.assertIn('decision-blocking', text)
        self.assertIn('do not expand a bounded investigation', text)
        self.assertIn('goal, requirement, scope, dependencies', text)

    def test_source_observation_is_not_acceptance(self):
        for p in (ROOT / 'skills').glob('*/references/candidate-identity.md'):
            text = p.read_text()
            self.assertIn('Source-only observation', text)
            self.assertIn('no capture CLI or full manifest', text)
            self.assertIn('exact-candidate acceptance or proof reuse', text)
            self.assertIn('rerun the checks', text)

    def test_compact_delivery_preserves_facts_and_boundary_reports(self):
        for p in (ROOT / 'skills').glob('*/references/common-output.md'):
            text = p.read_text()
            self.assertIn('## Compact bounded delivery', text)
            for term in ('read-only', 'no actual handoff', 'goal and task',
                         'result', 'evidence and limits', 'preservation and current authority',
                         'next action', 'full five-section report', 'commit', 'judgment', 'session'):
                self.assertIn(term, text)
            self.assertIn('At an actual phase handoff, render one fenced YAML', text)

    def test_direct_context_verification_not_mandatory_deep_worker(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        self.assertIn('The coordinator may directly verify', text)
        self.assertIn('Delegate deeper selected investigations', text)
        self.assertIn('mandatory isolation or independence', text)
        self.assertIn('explicit permission for direct investigation', text)
        self.assertNotIn('Missing\n     delegation requires a blocker', text)

if __name__ == '__main__': unittest.main()
