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

    def test_a_test_reads_as_an_executable_example_of_the_rule(self):
        """FR-1: a reader learns the rule from name, conditions, action and outcome."""
        text = ' '.join((ROOT / 'skills/test/references/test-value.md').read_text().split())
        self.assertIn('## Write tests as living documentation', text)
        for requirement in ('name states the rule', 'test_site_without_approval_cannot_be_published',
                            'test_publish_returns_409', 'conditions that matter',
                            'rule out other causes', 'one action', 'unchanged',
                            'bounds the rule', 'public API contract', 'docstring or marker',
                            'without opening the implementation',
                            'still expresses the intended rule'):
            self.assertIn(requirement, text)

    def test_an_input_only_variant_needs_a_distinct_branch_or_specified_case(self):
        """FR-2: same branch is not a new test, but a specified case the code ignores is a gap."""
        text = ' '.join((ROOT / 'skills/test/references/test-value.md').read_text().split())
        self.assertIn('## Same branch is not a new test', text)
        for requirement in ('differs from a neighbour only in an input value',
                            'production code or the specification', 'passthrough field',
                            'one guard', 'reveals a gap, not a duplicate',
                            'cross-file duplicates', 'token', 'Ido Shamun',
                            'not benchmarks'):
            self.assertIn(requirement, text)

    @staticmethod
    def _skill(phase):
        return ' '.join((ROOT / 'skills' / phase / 'SKILL.md').read_text().split())

    def test_implement_names_tests_after_the_rule_and_reads_the_shared_contract(self):
        """FR-3: the phase that writes tests applies its own copy of the contract."""
        implement = self._skill('implement')
        self.assertIn('references/test-value.md', implement)
        self.assertIn('Name each new test after the rule (protected behavior) it protects', implement)
        self.assertIn('docstring or marker', implement)
        self.assertNotIn('Name each new test after the protected behavior and cite its criterion ID', implement)

    def test_plan_bounds_each_rule_with_allowed_and_refused_examples(self):
        """FR-4: planned cases bound the rule instead of enumerating inputs."""
        plan = self._skill('plan')
        self.assertIn('an allowed and a refused example', plan)
        self.assertIn('the specification distinguishes', plan)

    def test_judge_treats_unreadable_or_same_branch_tests_as_non_blocking(self):
        """FR-5: the review question is asked; its findings do not block by default."""
        judge = self._skill('judge')
        for requirement in ('without opening the implementation', 'same-branch duplicate', 'non-blocking'):
            self.assertIn(requirement, judge)

    def test_test_reports_a_same_branch_duplicate_as_a_finding_not_a_failure(self):
        """FR-6: redundancy is reported, never counted as a failed criterion."""
        test = self._skill('test')
        self.assertIn('same-branch duplicate', test)
        self.assertIn('redundancy finding, not a failure', test)

    def test_skill_flow_shows_implement_reading_test_value(self):
        """FR-7: the user map mirrors the new conditional read."""
        flow = (ROOT / 'docs/skill-flow.md').read_text()
        self.assertRegex(flow, r'\| implement \| Candidate identity, test value')

    def _case_text(self, phase, name):
        cases = json.loads((ROOT / 'skills' / phase / 'evals/evals.json').read_text())['evals']
        case = next((c for c in cases if c['name'] == name), None)
        self.assertIsNotNone(case, f'{phase} eval scenario {name!r} is missing')
        return ' '.join([case['prompt'], *case['assertions']])

    def test_implement_scenario_refuses_same_branch_variants_but_tests_a_specified_gap(self):
        """FR-8: a writer adds no passthrough variants, yet writes the failing specified case."""
        text = self._case_text('implement', 'implement-same-branch-living-documentation')
        for requirement in ('passthrough', 'one guard', 'specification', 'fails',
                            'names the rule', 'docstring or marker', 'unchanged'):
            self.assertIn(requirement, text)

    def test_judge_scenario_reports_unreadable_and_duplicate_tests_without_blocking(self):
        """FR-9: readability and redundancy findings do not turn into a rejection."""
        text = self._case_text('judge', 'judge-readable-non-redundant-tests')
        for requirement in ('without opening the implementation', 'same-branch',
                            'non-blocking', 'does not edit', 'neither relaxes a criterion'):
            self.assertIn(requirement, text)

    def test_user_guide_explains_tests_as_living_documentation(self):
        """FR-10: users learn both rules from the cycle guide."""
        guide = ' '.join((ROOT / 'docs/cycle.md').read_text().split())
        self.assertIn('living documentation', guide)
        self.assertIn('same branch is not a new test', guide.lower())

    def test_scenarios_cover_distinct_decisions_without_execution_claims(self):
        expected = {
            'test': {'test-value-rationalization', 'test-value-missing-ci'},
            'plan': {'plan-test-value'},
            'implement': {'implement-minimal-testability', 'implement-same-branch-living-documentation'},
            'judge': {'judge-green-suite-weak-oracle', 'judge-readable-non-redundant-tests'},
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
