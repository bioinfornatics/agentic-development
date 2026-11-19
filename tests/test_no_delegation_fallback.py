"""FR-2 (agentic-devlopment-qu2) no-delegation fallback: static source evidence.

These checks inspect instruction text only. They do not execute an agent, a host
without workers or a review, and establish no behavioral effectiveness.
Expected requirements come from epic FR-2: without worker/subagent capability,
Research and Plan proceed directly and disclose reduced independence as a limit;
the user is asked only for a missing permission; Judge acceptance independence
rules are unchanged.
"""
from pathlib import Path
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LABEL = 'direct, reduced independence'


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def flat(text):
    return ' '.join(text.split())


class NoDelegationFallback(unittest.TestCase):
    sources = {
        'research skill': 'skills/research/SKILL.md',
        'research contract': 'skills/research/references/delegated-investigation.md',
        'plan skill': 'skills/plan/SKILL.md',
        'plan readiness': 'skills/plan/references/plan-readiness-review.md',
    }

    def test_fallback_proceeds_directly_with_disclosed_limit(self):
        for name, path in self.sources.items():
            with self.subTest(source=name):
                text = flat(read(path))
                self.assertIn(LABEL, text)
                # Absence of capability, not mere non-use, triggers the fallback.
                self.assertRegex(text, r'no worker capability[^.]*not merely unused'
                                 r'|not merely unused[^.]*no worker capability')
                # The proceed-directly sentence: direct work, disclosed limit, then proceed.
                self.assertRegex(text, r'directly[^.]*records? `direct, reduced independence` '
                                 r'in report limits and (may )?proceed')

    def test_absence_evidence_is_the_tool_list_observation(self):
        for name, path in self.sources.items():
            with self.subTest(source=name):
                text = flat(read(path))
                self.assertRegex(text, r"available tool list[^.]*no subagent or delegation tool")
                self.assertRegex(text, r'record (that|this) observation in (the )?report limits')

    def test_failed_dispatch_despite_capability_reports_blocker(self):
        text = read(self.sources['research contract'])
        item3 = flat(next(line for line in text.splitlines() if line.startswith('3. ')))
        self.assertIn('If dispatch fails despite capability, report the blocker.', item3)

    def test_user_is_asked_only_for_missing_permission(self):
        for name, path in self.sources.items():
            with self.subTest(source=name):
                text = flat(read(path))
                self.assertRegex(text, re.compile(r'ask the user only for a missing permission', re.I))

    def test_stalling_permission_and_waiver_wording_removed(self):
        stalls = ('explicit permission for direct investigation',
                  'explicit direct-investigation waiver',
                  'do not substitute ticket readback or self-review for this gate')
        for name, path in self.sources.items():
            text = flat(read(path))
            for stall in stalls:
                with self.subTest(source=name, stall=stall):
                    self.assertNotIn(stall, text)

    def test_fallback_is_not_independence_or_acceptance(self):
        research = flat(read(self.sources['research skill']))
        self.assertRegex(research, r'(required|mandatory) isolation or independence')
        self.assertIn('never fall back silently', research.lower())
        readiness = flat(read(self.sources['plan readiness']))
        for rule in ('no silent direct fallback', 'not independent review or acceptance',
                     'global approval gate pending', 'exact prerequisite'):
            self.assertIn(rule, readiness)

    def test_acceptance_independence_policy_unchanged(self):
        policy = read('skills/research/references/review-policy.md')
        for rule in ('a builder\'s saved plan or an\nabsence of reviewer tools is not a waiver',
                     'If independence is required and unavailable, use indeterminate'):
            self.assertIn(rule.lower(), policy.lower())
        copies = {hashlib.sha256((p).read_bytes()).hexdigest()
                  for p in ROOT.glob('skills/*/references/review-policy.md')}
        self.assertEqual(len(copies), 1, 'review-policy copies diverged')
        judge = flat(read('skills/judge/SKILL.md'))
        self.assertIn('never claim independence', judge)
        self.assertNotIn(LABEL, judge)


if __name__ == '__main__':
    unittest.main()
