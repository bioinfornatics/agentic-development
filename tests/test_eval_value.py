"""EV-1..4 risk-based source expectations, not measured agent defect detection."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Expected distinct decisions from the user scope and pre-edit risk review.
REQUIRED = {
    'cycle': {'cycle-beads-claim-boundary', 'cycle-beads-missing-capability',
              'cycle-non-beads-restraint', 'cycle-candidate-and-review-boundary',
              'cycle-closure-authorized', 'cycle-single-phase-activation',
              'cycle-resume-out-of-order', 'cycle-missing-roadmap-delivery',
              'local-streaming-cycle', 'dirty-ui-handoff', 'commit-to-session-handoff',
              'beads-tracker-to-handoff', 'adversarial-permission-and-drift'},
    'research': {'research-clear-feature-context-first', 'research-verified-context-reuse',
                 'research-missing-product-context', 'research-local-investigation-modes',
                 'research-recent-state-of-art', 'research-delegation-unavailable'},
    'plan': {'plan-normal', 'plan-numeric-score-preservation', 'plan-goals-gwt-quantified-nfr',
             'plan-test-value'},
    'implement': {'implement-public-seam-tdd', 'implement-change-session-output',
                  'implement-minimal-testability'},
    'test': {'test-normal', 'test-missing-capability', 'test-candidate-and-review-boundary',
             'test-unapproved-nfr', 'test-value-rationalization', 'test-value-missing-ci'},
    'judge': {'judge-normal', 'judge-boundary', 'judge-restraint',
              'judge-missing-capability', 'judge-green-suite-weak-oracle'},
    'iterate': {'iterate-normal', 'iterate-boundary', 'iterate-restraint',
                'iterate-capability-only-stop'},
}


def suite(phase):
    return json.loads((ROOT / 'skills' / phase / 'evals/evals.json').read_text())


class EvalValue(unittest.TestCase):
    def test_distinct_phase_risks_without_shared_cartesian_cases(self):
        for phase, required in REQUIRED.items():
            cases = suite(phase)['evals']
            names = {c['name'] for c in cases}
            self.assertTrue(required <= names, (phase, required - names))
            self.assertEqual(len({c['id'] for c in cases}), len(cases))
            if phase != 'cycle':
                for c in cases:
                    self.assertNotIn('closure-', c['name'])
                    for suffix in ('commit-report', 'session-end', 'beads-recovery',
                                   'beads-claim-boundary', 'beads-missing-capability',
                                   'non-beads-restraint', 'handoff-permission-injection'):
                        self.assertFalse(c['name'].endswith(suffix), c['name'])

    def test_merged_inputs_preserve_distinct_wrong_decisions(self):
        p = ROOT / 'skills/cycle/evals/files'
        closure = json.loads((p / 'closure-decisions.json').read_text())
        self.assertEqual(set(closure['cases']), {'authorized', 'no-authority',
                                                'already-committed', 'blocked'})
        self.assertFalse(closure['cases']['no-authority']['commit_authorized'])
        self.assertTrue(closure['cases']['blocked']['mandatory_check_failed'])
        tracker = json.loads((p / 'beads-tracker-to-handoff.json').read_text())
        self.assertEqual(tracker['blocked_readiness_variant']['depends_on']['TASK-17'], ['TASK-18'])
        injection = json.loads((p / 'adversarial-permission-and-drift.json').read_text())
        self.assertIn('issue_payload', injection)
        self.assertIn('tool_payload', injection)
        handoff = json.loads((p / 'commit-to-session-handoff.json').read_text())
        self.assertIs(handoff['saved_handoff'], False)

    def test_phase_specific_merges_and_no_blanket_repetition_budget(self):
        def text(phase, name):
            c = next(c for c in suite(phase)['evals'] if c['name'] == name)
            return ' '.join([c['prompt'], *c['assertions']]).lower()
        self.assertIn('frozen candidate', text('test', 'test-normal'))
        self.assertIn('installed-package', text('test', 'test-missing-capability'))
        self.assertIn('ascii', text('test', 'test-missing-capability'))
        self.assertIn('inferred', text('research', 'research-local-investigation-modes'))
        self.assertNotIn('aggregate_budget', suite('cycle'))


if __name__ == '__main__':
    unittest.main()
