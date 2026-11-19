"""Source contracts for shared phase wording; static readability guard, not behavior proof."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')


def protocol(phase):
    text = (ROOT / 'skills' / phase / 'SKILL.md').read_text()
    start = text.index('Apply contracts before their governed actions,')
    return text[start:text.index('\n\n', start)]


class SharedWording(unittest.TestCase):
    def test_protocol_is_concise(self):
        text = ' '.join(protocol('cycle').split())
        sentences = [s for s in re.split(r'(?<=[.])\s+', text) if s]
        self.assertLessEqual(len(text.split()), 95)
        self.assertLessEqual(max(len(s.split()) for s in sentences), 20)

    def test_bd_prime_only_when_missing_or_stale(self):
        for phase in PHASES:
            with self.subTest(phase=phase):
                text = ' '.join((ROOT / 'skills' / phase / 'SKILL.md').read_text().split())
                self.assertNotIn('Use fresh `bd prime` guidance', text)
                self.assertIn('Run `bd prime` only when Beads context is missing or stale', text)

    def test_cycle_budget_uses_attempts(self):
        text = (ROOT / 'skills/cycle/SKILL.md').read_text()
        self.assertNotIn('correction rounds', text)
        self.assertIn('three correction attempts', ' '.join(text.split()))


if __name__ == '__main__':
    unittest.main()
