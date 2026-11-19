import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')
TERMS = ('Seam', 'Ready frontier', 'Phase-only request', 'Finalize', 'WIP', 'Entire')


class BaselineTerms(unittest.TestCase):
    def setUp(self):
        self.copies = {p: (ROOT / 'skills' / p / 'references/requirements-baseline.md').read_bytes()
                       for p in PHASES}

    def test_copies_are_identical(self):
        self.assertEqual(len(set(self.copies.values())), 1)

    def test_each_term_is_a_terms_bullet_in_every_copy(self):
        for phase, raw in self.copies.items():
            section = raw.decode().split('## Terms', 1)[1].split('\n## ', 1)[0]
            bullets = [line for line in section.splitlines() if line.startswith('- **')]
            for term in TERMS:
                with self.subTest(phase=phase, term=term):
                    matches = [b for b in bullets if b.startswith(f'- **{term}**')]
                    self.assertEqual(len(matches), 1)
                    self.assertRegex(matches[0], r'^- \*\*[^*]+\*\*( \([^)]+\))?: \S.*\.$')


if __name__ == '__main__':
    unittest.main()
