"""User-request source contracts only; no workflow execution/effectiveness proof."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


FEASIBILITY_SCENARIOS = {
    'research': {'documented-components-unproven-deployment'},
    'plan': {'producer-consumer-and-goal-coverage', 'low-risk-existing-evidence'},
    'implement': {'failed-transition-local-pause'},
    'iterate': {'local-replan-no-progress'},
}
SCENARIO_KEYS = {'id', 'name', 'subject', 'language', 'target', 'coverage_tags',
                 'prompt', 'assertions', 'expected_output', 'files'}
TAG_DIMENSIONS = {'phase', 'language', 'rule'}


def scenario_problems(phase, case):
    """Return closed-subset violations for one inert feasibility scenario."""
    base = (ROOT / 'skills' / phase).resolve()
    problems = [f'extra key {key}' for key in sorted(set(case) - SCENARIO_KEYS)]
    if type(case.get('id')) is not int:
        problems.append('id is not an int')
    if case.get('language') != 'en':
        problems.append('language is not en')
    for key in ('prompt', 'assertions', 'expected_output', 'files'):
        if not case.get(key):
            problems.append(f'empty {key}')
    tags = case.get('coverage_tags', [])
    for tag in tags:
        dimension, _, value = tag.partition(':')
        if dimension not in TAG_DIMENSIONS or not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', value):
            problems.append(f'malformed coverage tag {tag}')
    if 'language:en' not in tags:
        problems.append('missing language tag')
    if 'phase:' + phase not in tags:
        problems.append('missing phase tag')
    for name in case.get('files', []):
        path = (base / name).resolve()
        if not path.is_relative_to(base) or not path.is_file() or 'SKILL.md' in name:
            problems.append(f'bad input {name}')
        elif name not in case.get('prompt', ''):
            problems.append(f'input not named in prompt {name}')
    return problems


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

    def test_feasibility_challenge_targets_indispensable_operation_not_docs(self):
        # FEAS-1: an unsupported necessary operation can invalidate a composition;
        # static wording checks detect omissions, not successful agent execution.
        for text in (self.research, self.plan):
            for rule in ('indispensable unproven operation', 'refute',
                         'risky compositions', 'documentation is not execution',
                         'no universal proof-of-concept'):
                self.assertIn(rule, ' '.join(text.lower().split()))

    def test_material_transitions_need_compatible_consumers_or_scoped_bridge(self):
        # JOIN-1: dependency ordering alone cannot establish consumability.
        for rule in ('output', 'next input/precondition', 'format', 'interface',
                     'state', 'environment', 'authority', 'named bridge',
                     'affected consumer', 'not a microtask per edge'):
            self.assertIn(rule, ' '.join(self.plan.lower().split()))

    def test_goal_coverage_is_bidirectional_and_not_graph_consistency(self):
        # GOAL-1: both missing requested outcomes and unjustified work matter.
        for rule in ('each material goal/criterion', 'contributing outcomes',
                     'independent verification', 'each planned outcome',
                     'enabling rationale', 'consistent graph is not goal sufficiency'):
            self.assertIn(rule, ' '.join(self.plan.lower().split()))

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


class FeasibilityScenarioSubset(unittest.TestCase):
    def test_new_feasibility_scenarios_use_the_closed_subset(self):
        import json
        for phase, names in FEASIBILITY_SCENARIOS.items():
            suite = json.loads((ROOT / 'skills' / phase / 'evals/evals.json').read_text())
            cases = {case['name']: case for case in suite['evals']}
            for name in names:
                with self.subTest(phase=phase, scenario=name):
                    self.assertIn(name, cases)
                    self.assertEqual(scenario_problems(phase, cases[name]), [])

    def test_subset_check_rejects_known_violations(self):
        case = {'id': '1', 'name': 'x', 'language': 'fr',
                'coverage_tags': ['rule', 'rule:', 'foo:bar', 'rule:Not_Kebab'],
                'prompt': 'p', 'assertions': ['a'], 'expected_output': 'e',
                'files': ['SKILL.md', '../research/evals/evals.json', 'evals/inputs/missing.md'],
                'execution_assertions': []}
        problems = scenario_problems('plan', case)
        for expected in ('extra key execution_assertions', 'id is not an int',
                         'language is not en', 'malformed coverage tag rule',
                         'malformed coverage tag rule:', 'malformed coverage tag foo:bar',
                         'malformed coverage tag rule:Not_Kebab', 'missing language tag',
                         'missing phase tag', 'bad input SKILL.md',
                         'bad input ../research/evals/evals.json', 'bad input evals/inputs/missing.md'):
            self.assertIn(expected, problems)

    def test_subset_check_rejects_empty_fields_and_unnamed_inputs(self):
        case = {'id': 1, 'name': 'x', 'language': 'en',
                'coverage_tags': ['phase:plan', 'language:en'],
                'prompt': 'no input named here', 'assertions': [],
                'expected_output': '', 'files': ['evals/inputs/ticket.md']}
        problems = scenario_problems('plan', case)
        for expected in ('empty assertions', 'empty expected_output',
                         'input not named in prompt evals/inputs/ticket.md'):
            self.assertIn(expected, problems)
        self.assertIn('empty files', scenario_problems('plan', {**case, 'files': []}))
        self.assertIn('empty prompt', scenario_problems('plan', {**case, 'prompt': ''}))


if __name__ == '__main__':
    unittest.main()
