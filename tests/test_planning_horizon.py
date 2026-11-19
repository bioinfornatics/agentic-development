"""Planning-horizon SOURCE-CONTRACT checks for agentic-devlopment-gx9.3 (FR-6).

Static source evidence only: these inspect plan and ticket-authoring instruction
seams, not a tracker, scheduler or executed agent workflow. Expected rules come
from the approved task decision: tasks exist only for the active epic and the next
epic in line; other epics keep goal, outcomes and rough scope without child tasks;
detailed distant tasks need an explicit request in the current turn; refinement
stays one batch ahead; a coordinator batch may run one task per worker.
No behavioral TDD, agent effectiveness or acceptance is established.
"""
from pathlib import Path
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_source(path):
    return (ROOT / path).read_text(encoding='utf-8')


def normalize(text):
    return re.sub(r'\s+', ' ', re.sub(r'[`*_]', '', text.lower())).strip()


def local_spans(text):
    blocks = re.split(r'\n\s*\n', text)
    return [normalize('\n'.join(blocks[i:i + width]))
            for i in range(len(blocks)) for width in (1, 2)]


class PlanningHorizonSourceContracts(unittest.TestCase):
    def setUp(self):
        self.plan = read_source('skills/plan/SKILL.md')
        self.readiness = read_source('skills/plan/references/plan-readiness-review.md')
        self.tickets = read_source('skills/task-authoring/references/ticket-authoring.md')

    def assert_policy(self, text, *concepts):
        self.assertTrue(
            any(len(span) <= 2200 and all(re.search(c, span) for c in concepts)
                for span in local_spans(text)),
            'Missing local policy relationship: ' + ' / '.join(concepts))

    def test_tasks_only_for_active_and_next_epic(self):
        self.assert_policy(self.plan, r'tasks? only for the active epic',
                           r'next epic in line')

    def test_other_epics_hold_goal_outcomes_rough_scope_without_tasks(self):
        self.assert_policy(self.plan, r'other epics',
                           r'goal, outcomes and rough scope',
                           r'no child tasks')

    def test_distant_detail_needs_explicit_current_request(self):
        self.assert_policy(self.plan, r'distant epic',
                           r'explicitly asks? .*current request')
        # The former open-ended authorized-backlog carve-out must be gone.
        for source in (self.plan, self.tickets):
            self.assertNotRegex(normalize(source),
                                r'explicitly requested/authorized backlog authoring')
            self.assertNotRegex(normalize(source),
                                r'unless current scope authorizes backlog authoring')

    def test_refine_one_batch_ahead(self):
        self.assert_policy(self.plan, r'refine', r'one batch ahead')

    def test_readiness_review_checks_horizon(self):
        self.assert_policy(self.readiness, r'active epic', r'next epic',
                           r'child tasks|tasks')

    def test_ticket_authoring_allows_coordinator_batch(self):
        text = normalize(self.tickets)
        self.assertNotIn('not simultaneous execution by one agent', text)
        self.assert_policy(self.tickets, r'coordinator', r'batch',
                           r'one task per worker')
        self.assert_policy(self.tickets, r'active epic', r'next epic')

    def test_ticket_authoring_copies_identical(self):
        digests = {hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in ROOT.glob('skills/*/references/ticket-authoring.md')}
        self.assertEqual(len(digests), 1)


if __name__ == '__main__':
    unittest.main()
