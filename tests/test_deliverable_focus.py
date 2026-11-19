"""FC1–7 frozen user-scope SOURCE-CONTRACT checks for agentic-devlopment-lwg.

These inspect instruction seams, not a scheduler, tracker or executed agent workflow.
The competing-objectives, unfinished-switch, independent-contributions, failed-worker
and future-ideas cases come from the approved requirements, not candidate prose.
No hypothetical execution, causal effectiveness or behavioral TDD is established.
Numbers in the motivating report are not quotas or required instruction wording.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_source(path):
    return (ROOT / path).read_text(encoding='utf-8')


def normalize(text):
    # Ignore Markdown emphasis, case, hyphen style and line wrapping.
    return re.sub(r'\s+', ' ', re.sub(r'[`*_]', '', text.lower())).strip()


def action_section(text, heading_pattern):
    """Select a numbered workflow action by meaning, not ordinal or exact title."""
    starts = list(re.finditer(r'^\d+\.\s+\[.\]\s+(.+)$', text, re.M))
    for index, match in enumerate(starts):
        if re.search(heading_pattern, normalize(match.group(1))):
            end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
            return text[match.start():end]
    raise AssertionError('Missing governed action seam: ' + heading_pattern)


class DeliverableFocusSourceContracts(unittest.TestCase):
    def setUp(self):
        self.cycle = read_source('skills/cycle/SKILL.md')
        self.plan = read_source('skills/plan/SKILL.md')
        self.readiness = read_source('skills/plan/references/plan-readiness-review.md')
        self.tickets = read_source('skills/task-authoring/references/ticket-authoring.md')
        self.focus = action_section(self.cycle, r'frame|recover|select.*slice')
        self.dispatch = action_section(self.cycle, r'dispatch|delegat')
        self.join = action_section(self.cycle, r'integrat')
        self.frontier = action_section(self.plan, r'build.*frontier|select.*frontier')

    def assert_policy(self, text, *concepts):
        """Require related concepts locally, not a whole-file keyword inventory.

        Adjacent paragraphs permit a rule plus its qualification/example; bounded
        spans tolerate bullets, tables and wrapping without prescribing sentences.
        This deliberately remains a lexical guard, not semantic policy execution.
        """
        blocks = re.split(r'\n\s*\n', text)
        spans = [normalize('\n'.join(blocks[i:i + width]))
                 for i in range(len(blocks)) for width in (1, 2)]
        self.assertTrue(
            any(len(span) <= 2200 and all(re.search(c, span) for c in concepts)
                for span in spans),
            'Missing local policy relationship: ' + ' / '.join(concepts))

    def test_fc1_select_one_outcome_not_sequential_multi_wip(self):
        # Given competing ready objectives and one agent: select an outcome/exit,
        # not several sequentially claimed objectives masquerading as concurrency.
        self.assert_policy(self.focus, r'(one|single).*primary.*(deliverable|outcome)',
                           r'exit|completion criteria|success criteria')
        self.assert_policy(self.focus, r'sequential|serial',
                           r'(not|no|avoid|never)', r'(multiple|several|multi)',
                           r'(active|live|running).*(worker|delegat)|(worker|delegat).*(active|live|running)')

    def test_fc2_switch_preserves_unfinished_work_before_replacement(self):
        self.assert_policy(self.focus, r'switch|replac|suspend', r'before',
                           r'candidate|artifact|diff', r'evidence', r'resum|restart',
                           r'worker|delegat')
        self.assert_policy(self.focus, r'switch|replac|suspend', r'(not|no|never|without)',
                           r'clos', r'cancel', r'reset|discard')

    def test_fc3_useful_ready_dispatch_launches_before_await(self):
        self.assert_policy(self.dispatch, r'independent', r'ready',
                           r'(launch|dispatch|invok|start)', r'before', r'await|wait|join')
        self.assert_policy(self.dispatch, r'serial', r'reason|justif|explain|record')
        self.assert_policy(self.dispatch, r'actual|observed|verified',
                           r'handle|invocation|worker id|identifier', r'status|completion')
        self.assert_policy(self.dispatch, r'(available|capabilit)', r'useful|worthwhile',
                           r'exclusive|disjoint|isolation')
        self.assert_policy(self.dispatch, r'(no|not|need no|avoid|never)',
                           r'trivial|bounded question|baseline verification|unnecessary')

    def test_fc4_required_workers_join_before_dependent_work_not_independent_work(self):
        self.assert_policy(self.join, r'required|mandatory', r'worker|contribution',
                           r'verif', r'join|completion', r'dependent|depend on')
        self.assert_policy(self.join, r'live|running|incomplete|failed',
                           r'block|wait|stop|pending', r'dependent|depend on')
        self.assert_policy(self.join, r'independent|unrelated', r'may|can|permit',
                           r'proceed|continue|work')
        self.assert_policy(self.join, r'partial|failed|incomplete',
                           r'provisional|not accepted|not acceptance|never accept')

    def test_fc5_planning_bounds_frontier_without_prohibiting_authorized_backlog(self):
        self.assert_policy(self.frontier, r'primary.*(deliverable|outcome)',
                           r'frontier', r'roadmap|backlog')
        self.assert_policy(self.frontier, r'future|distant', r'coarse',
                           r'(not|no|avoid|never)', r'speculative|ticket|detail')
        # Backlog detail is legitimate only on an explicit current-request override.
        self.assert_policy(self.frontier, r'explicitly asks?.*current request',
                           r'requested backlog',
                           r'not.*active|non.?active|not.*running|not.*execution')
        # Planning review must challenge focus/joins, not merely count ticket fields.
        self.assert_policy(self.readiness, r'primary.*(deliverable|outcome)',
                           r'frontier|ready', r'exit|completion criteria|success criteria')
        self.assert_policy(self.readiness, r'parallel|delegat|worker',
                           r'join|completion', r'depend')

    def test_fc6_reporting_distinguishes_plan_claim_and_observed_execution(self):
        for label, text in [('selection', self.focus), ('ticket authoring', self.tickets)]:
            with self.subTest(seam=label):
                self.assert_policy(text, r'planned|planning|selected|selection',
                                   r'claim', r'running|execution|executing',
                                   r'observed|actual|verif')
        self.assert_policy(self.tickets, r'(not|no|never|without)',
                           r'invent|fabricat|simulat', r'status|state|delegat|worker')
        self.assert_policy(self.tickets, r'claim|ownership',
                           r'(not|no|never|without)', r'permission|authority|authoriz')

    def test_fc7_preservation_and_nonbuilder_gates_remain_at_action_seams(self):
        # Preserve reference-mediated authority/review rather than duplicate policy.
        prerequisites = action_section(self.cycle, r'prerequisite|authority')
        for link in ('authorization-policy.md', 'review-policy.md'):
            with self.subTest(link=link):
                self.assertIn('references/' + link, prerequisites)
        self.assert_policy(self.dispatch, r'parallel', r'(never|not|no)', r'share.*file')
        self.assert_policy(self.dispatch, r'independent', r'self.review|self.accept',
                           r'not|never|no')
        self.assert_policy(self.join, r'clos', r'criteria', r'judge', r'exact candidate')
        self.assert_policy(self.tickets, r'preserve.*history|history.*preserve',
                           r'criterion ids|criteria', r'authority|authoriz')
        self.assert_policy(self.readiness, r'not.*participated|non.builder',
                           r'candidate construction|reviewer', r'read.only')
        self.assert_policy(self.readiness, r'no|not', r'agent.effectiveness', r'source')
        self.assert_policy(self.join, r'source.only|source contract', r'static')


if __name__ == '__main__':
    unittest.main()
