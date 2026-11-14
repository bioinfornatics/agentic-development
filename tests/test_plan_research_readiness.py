"""User-request source contracts only; no workflow execution/effectiveness proof."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def source(phase, name):
    return (ROOT / 'skills' / phase / 'references' / name).read_text()


class ReadinessSourceContracts(unittest.TestCase):
    def setUp(self):
        self.plan = source('plan', 'plan-readiness-review.md')
        self.research = source('research', 'research-readiness-review.md')

    def test_step_local_contained_links_before_readiness_actions(self):
        for phase, name in [('plan', 'plan-readiness-review.md'),
                            ('research', 'research-readiness-review.md')]:
            text = (ROOT / 'skills' / phase / 'SKILL.md').read_text()
            self.assertEqual(text.count('references/' + name), 1)
            self.assertLess(text.index('references/' + name),
                            text.index('**Verify readiness and draft'))
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in link and not link.startswith('#'):
                    target = (ROOT / 'skills' / phase / link.split('#')[0]).resolve()
                    self.assertTrue(target.is_relative_to((ROOT / 'skills' / phase).resolve()))
                    self.assertTrue(target.is_file(), link)
            self.assertLessEqual(len(text.splitlines()), 500)

    def test_individual_ticket_questions_cover_usable_execution(self):
        for requirement in ('independently reviewable outcome', 'verified requirement',
                            'actual prerequisites', 'native blocking edges',
                            'independent observable checks', 'errors/boundaries',
                            'Read/Create/Modify/Preserve/Exclude', 'ownership conflicts',
                            'first restart action', 'accessible input', 'current permissions'):
            self.assertIn(requirement, self.plan)
        self.assertIn('actual user, maintainer or system', self.plan)
        self.assertIn('conditional task-authoring route', self.plan)
        self.assertIn('preserve criteria/history/native fields', self.plan)

    def test_open_questions_and_closed_three_state_gates_are_distinct(self):
        for text in (self.plan, self.research):
            rows = [line for line in text.splitlines() if line.startswith('|')][2:]
            self.assertGreaterEqual(len(rows), 6)
            for row in rows:
                fields = row.strip('|').split('|')
                self.assertEqual(len(fields), 2)
                self.assertTrue(all('?' in field for field in fields))
            for gate in ('yes / no / unknown', 'yes passes', 'no fails',
                         'unknown never passes', 'N/A', 'scope-based reason'):
                self.assertIn(gate.lower(), ' '.join(text.lower().split()))

    def test_complete_plan_review_is_separate_readonly_not_self_approval(self):
        for rule in ('separate read-only subagent', 'complete current plan',
                     'not have participated in candidate construction',
                     'criteria, not expected answers', 'No source, tracker, Git or candidate writes',
                     'implicit semantic dependencies', 'native edges', 'implicit cycles',
                     'foundation', 'consumer', 'architecture selection', 'security boundary',
                     'least viable ordering', 'ready frontier', 'completion', 'source identity',
                     'result locator', 'not plan approval'):
            self.assertIn(rule, self.plan)
        self.assertIn('Run this challenge once before approval', self.plan)
        self.assertIn('graph, criteria or material inputs', self.plan)
        self.assertIn('not for every minor wording edit', self.plan)
        for rule in ('If delegation is unavailable', 'exact prerequisite',
                     'global approval gate pending', 'no silent direct fallback',
                     'not unrelated authorized'):
            self.assertIn(rule, self.plan)

    def test_research_chain_keeps_hypotheses_and_evidence_distinct(self):
        self.assertIn('hypothesis → evidence → supported premise → decision → tasks → observable criteria', self.research)
        for rule in ('not a premise until supported', 'contrary findings',
                     'observed, inferred or', 'unverified', 'its premises',
                     'owner (or unknown)', 'deciding probe', 'observable resolving result',
                     'not fabricated approved tickets', 'Absence of a search result is not evidence'):
            self.assertIn(rule, self.research)

    def test_research_checks_actual_relevant_limits_and_impact_sources(self):
        for rule in ('functional, code, library or domain-principle problems',
                     'actual code/tests', 'dependency limitations', 'actual files/symbols/tests',
                     'consumers', 'preserve/exclude boundaries', 'source identity',
                     'library version', 'environment', 'freshness', 'unavailable/stale',
                     'ordered file/section/symbol pointers', 'symptom-specific reproduction'):
            self.assertIn(rule.lower(), self.research.lower())
        self.assertIn('not reproduced behavior', self.research)

    def test_proportional_scoped_stop_not_procedural_expansion(self):
        for text in (self.plan, self.research):
            for word in ('critical gaps', 'owner', 'probe', 'ready frontier',
                         'Stop', 'full test', 'evaluation campaign', 'performance',
                         'agent-effectiveness'):
                self.assertIn(word.lower(), text.lower())
        for rule in ('microticket per file', 'task count is not quality', 'distant work coarse'):
            self.assertIn(rule, self.plan)
        for rule in ('only when risk or', 'authorized channel', 'No implicit paid web access',
                     'not the rest of the ready frontier', 'No mandatory matrix',
                     'sufficient local evidence needs no external refresh'):
            self.assertIn(rule, self.research)


if __name__ == '__main__':
    unittest.main()
