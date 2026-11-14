"""PROP-2..4 user audit intent: source wording, not executed agent behavior."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SourceObservationProportionality(unittest.TestCase):
    def test_cycle_resume_selects_provenance_before_exact_comparison(self):
        text = (ROOT / 'skills/cycle/SKILL.md').read_text()
        resume = text.split('- Resume at the first incomplete or invalidated phase,', 1)[1].split('\n\n', 1)[0]
        self.assertNotIn('Reinspect the working tree and compare candidate identity;', resume)
        self.assertRegex(resume, r'(?s)source-only.*preliminary.*exact-candidate')
        self.assertIn('stale', resume)

    def test_research_names_three_provenance_paths_and_exact_gate(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        provenance = text.split('[candidate identity](references/candidate-identity.md)', 1)[1].split('   - Retrieve', 1)[0]
        for concept in ('source-only', 'preliminary', 'exact-candidate', 'proof reuse',
                        'dirty state', 'limits', 'untracked', 'environment', 'freshness'):
            self.assertIn(concept, provenance.lower())

    def test_missing_roadmap_does_not_expand_research(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        framing = text.split('1. [ ]', 1)[1].split('2. [ ]', 1)[0]
        self.assertRegex(framing, r'(?s)Missing roadmap.*(?:does not|do not).*expand')
        self.assertIn('decision-blocking', framing)

    def test_safety_and_progressive_disclosure_survive(self):
        for phase in ('cycle', 'research'):
            text = (ROOT / f'skills/{phase}/SKILL.md').read_text()
            normalized = ' '.join(text.split())
            self.assertRegex(normalized, r'(?:required|mandatory) isolation or independence')
            for safeguard in ('absent, incomplete or outdated', 'never renews',
                              'selected delivery form (compact when eligible',
                              'source', 'permission'):
                self.assertIn(safeguard, text)
        research = (ROOT / 'skills/research/SKILL.md').read_text()
        self.assertIn('The coordinator may directly verify', research)
        self.assertIn('explicit permission for direct investigation', research)
        self.assertIn('product purpose, users and desired outcome', research)


if __name__ == '__main__':
    unittest.main()
