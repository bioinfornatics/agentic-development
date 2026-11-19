"""Trigger-routing eval inputs and shared terms; static structure only, no model run."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / 'integration/trigger-routing.json'
SKILLS = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate', 'task-authoring', 'domain-modeling')
PHASES = SKILLS[:7]


def load_matrix():
    return json.loads(MATRIX.read_text())


def trigger_set(matrix, skill):
    """Derive the skill-creator trigger-eval list for one Skill."""
    return [{'query': case['query'], 'should_trigger': skill in case['expected_skills']}
            for case in matrix['cases']]


class TriggerRoutingMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = load_matrix()
        self.cases = self.matrix['cases']

    def test_cases_are_unique_and_reference_known_skills(self):
        self.assertGreaterEqual(len(self.cases), 20)
        queries = [case['query'] for case in self.cases]
        self.assertEqual(len(queries), len(set(queries)))
        for case in self.cases:
            with self.subTest(query=case['query']):
                self.assertEqual(set(case), {'query', 'expected_skills', 'near_miss_for', 'language'})
                self.assertTrue(set(case['expected_skills']) <= set(SKILLS))
                self.assertTrue(set(case['near_miss_for']) <= set(SKILLS))
                self.assertFalse(set(case['near_miss_for']) & set(case['expected_skills']))
                phases = set(case['expected_skills']) & set(PHASES[1:])
                self.assertLessEqual(len(phases), 1)
                if 'cycle' not in case['expected_skills'] and phases:
                    self.assertEqual(len(case['expected_skills']), 1)

    def test_phase_only_requests_load_the_phase_alone(self):
        # Decision qws.2 option A: cycle is not required for a request limited to one phase.
        self.assertIn('a request limited to one phase loads that phase Skill alone', self.matrix['description'])
        self.assertNotIn('cycle accompanies each development phase request', self.matrix['description'])
        alone = [c for c in self.cases if len(c['expected_skills']) == 1 and c['expected_skills'][0] in PHASES[1:]]
        self.assertGreaterEqual(len(alone), 6)
        housekeeping = [c for c in self.cases if c['expected_skills'] == ['cycle']]
        self.assertGreaterEqual(len(housekeeping), 2)
        self.assertIn('a request that also asks for a later phase is an objective', self.matrix['description'])
        objectives = ('Add a CSV export button', 'Le paiement échoue parfois', 'Coordinate the whole change')
        for prefix in objectives:
            case = next(c for c in self.cases if c['query'].startswith(prefix))
            self.assertIn('cycle', case['expected_skills'], prefix)

    def test_every_skill_has_positives_and_neighbour_near_misses(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                derived = trigger_set(self.matrix, skill)
                self.assertGreaterEqual(sum(d['should_trigger'] for d in derived), 2)
                near = [c for c in self.cases if skill in c['near_miss_for']]
                self.assertGreaterEqual(len(near), 2)

    def test_non_development_and_non_english_queries_exist(self):
        self.assertGreaterEqual(sum(not c['expected_skills'] for c in self.cases), 2)
        self.assertGreaterEqual(sum(c['language'] != 'en' for c in self.cases), 2)

    def test_run_is_recorded_not_performed(self):
        self.assertIn('skill-creator trigger-eval', self.matrix['run'])
        self.assertIn('authorization', self.matrix['run'])


class SharedTerms(unittest.TestCase):
    def test_terms_section_is_shared_and_defines_core_vocabulary(self):
        copies = {(ROOT / 'skills' / p / 'references/requirements-baseline.md').read_bytes()
                  for p in PHASES}
        self.assertEqual(len(copies), 1)
        text = copies.pop().decode()
        self.assertIn('Contract version: 1.6.0', text)
        terms = text.split('## Terms', 1)[1].split('\n## ', 1)[0]
        for term in ('Roadmap', 'Epic', 'User story', 'Task', 'Slice', 'Primary deliverable',
                     'Contribution', 'Candidate', 'Evidence level', 'Gate', 'Correction attempt'):
            self.assertIn(f'**{term}**', terms)


if __name__ == '__main__':
    unittest.main()
