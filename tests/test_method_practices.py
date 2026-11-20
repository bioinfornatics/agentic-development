"""Source contract for epics agentic-devlopment-0wm and agentic-devlopment-9f1: domain modeling, grill mode,
specification, expand-contract, TDD boundary rules and integration-branch mode.

Expected rules are stated from the user's approved scope (decisions D1-D4,
2026-11-19), not copied from implementation output. Static source evidence only;
it does not prove agent behavior.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
DOMAIN = SKILLS / 'domain-modeling'


def read(rel):
    return (ROOT / rel).read_text()


def flat(text):
    return re.sub(r'\s+', ' ', text)


class DomainModelingSkill(unittest.TestCase):
    def setUp(self):
        self.text = flat((DOMAIN / 'SKILL.md').read_text())

    def test_optional_capability_with_contained_references(self):
        meta = (DOMAIN / 'SKILL.md').read_text().split('---', 2)[1]
        self.assertIn('name: domain-modeling', meta)
        for word in ('domain terms', 'glossary', 'decision'):
            self.assertIn(word, meta)
        self.assertIn('not a development phase', self.text)
        for link in re.findall(r'\]\(([^)]+)\)', self.text):
            path = (DOMAIN / link).resolve()
            self.assertTrue(path.is_relative_to(DOMAIN.resolve()), link)
            self.assertTrue(path.is_file(), link)
        self.assertTrue((DOMAIN / 'references/glossary-format.md').is_file())
        self.assertTrue((DOMAIN / 'references/adr-format.md').is_file())
        self.assertFalse((DOMAIN / 'evals/evals.json').exists())

    def test_write_requires_authority_else_labeled_proposal(self):
        for rule in ('grants no permission', 'current scoped write authority',
                     'labeled as a proposal', 'never report a file as written',
                     'read the file back', 'STOP and return to the caller'):
            self.assertIn(rule, self.text)

    def test_decision_record_needs_all_three_conditions(self):
        adr = flat(read('skills/domain-modeling/references/adr-format.md'))
        self.assertIn('Offer a record only when every answer is yes', adr)
        for condition in ('Alternatives actually weighed?', 'Costly to undo?', 'Reason invisible in the code?'):
            self.assertIn(condition, adr)
        self.assertIn('alternatives were actually weighed, undoing it would be costly and its reason is invisible in the code',
                      self.text)

    def test_glossary_excludes_implementation_detail(self):
        glossary = flat(read('skills/domain-modeling/references/glossary-format.md'))
        for rule in ('Not:', 'It holds meanings only', 'infrastructure vocabulary belongs to the code'):
            self.assertIn(rule, glossary)


class ResearchGrillMode(unittest.TestCase):
    def test_intent_row_and_trigger_wording(self):
        text = read('skills/research/SKILL.md')
        meta = text.split('---', 2)[1]
        self.assertIn('grilling or stress-testing a plan or design', meta)
        table = text.split('## Workflow', 1)[0]
        self.assertIn('| Grill or stress-test a plan, design or idea', table)
        self.assertIn('no approval or write permission', table)

    def test_full_frontier_rounds_end_on_user_confirmation(self):
        text = flat(read('skills/research/references/clarification-interview.md'))
        self.assertIn('at most three per turn', text)
        grill = text.split('## Grill mode', 1)[1].split('## Example', 1)[0]
        for rule in ('only when the user asks', 'present all decisions that are ready under step 2',
                     'keep asking the ready decisions meanwhile', 'user confirms the recorded decisions are complete',
                     'NEEDS CLARIFICATION'):
            self.assertIn(rule, grill)


class PlanSpecification(unittest.TestCase):
    def setUp(self):
        self.plan = flat(read('skills/plan/SKILL.md'))
        self.template = flat(read('skills/plan/references/specification-template.md'))

    def test_template_maps_stories_to_criteria_without_paths(self):
        self.assertIn('references/specification-template.md', self.plan)
        for section in ('## Context', '## Goals', '## Non-goals', '## Stories', '## Criteria',
                        '## Errors and boundaries', '## Quality targets', '## Decisions', '## Test approach',
                        '## Open questions'):
            self.assertIn(section, self.template)
        self.assertIn('the specification describes behavior and decisions, not file paths or code', self.template)
        self.assertIn('every user story maps to at least one criterion', self.template)

    def test_expand_contract_and_fewest_highest_seams(self):
        for rule in ('expand-contract', 'each with a dependency on the introduce task', 'depends on all migrate tasks',
                     'prefer a public seam the code already has', 'A new seam is a cost',
                     'tracer-bullet', 'replan instead of accepting a red intermediate state'):
            self.assertIn(rule, self.plan)


class TddAdditions(unittest.TestCase):
    def test_boundary_mocking_in_identical_test_value_copies(self):
        impl = read('skills/implement/references/test-value.md')
        self.assertEqual(impl, read('skills/test/references/test-value.md'))
        text = flat(impl)
        for rule in ('Replace only system boundaries', 'Do not mock modules the project owns',
                     'pass the dependency in', 'not permission to add injection layers'):
            self.assertIn(rule, text)

    def test_tracer_bullet_and_refactor_stays_in_slice(self):
        text = flat(read('skills/implement/SKILL.md'))
        self.assertIn('tracer bullet', text)
        for rule in ('Refactoring stays inside the owned slice', 'starts only from green',
                     'without editing their assertions', 'separate planned task'):
            self.assertIn(rule, text)


class IntegrationBranchMode(unittest.TestCase):
    def test_opt_in_and_every_git_action_gated(self):
        text = flat(read('skills/cycle/SKILL.md'))
        mode = text.split('Integration-branch batch mode', 1)[1].split('Before Judge', 1)[0]
        for rule in ('optional', 'default above stays non-mutating', 'current scoped authority',
                     'creating the integration branch', 'removing each worktree',
                     'each worker commit', 'each merge or rebase that brings the integration tip',
                     'when authorized', 'Never merge it into develop, main or any protected branch',
                     'candidate for Test and Judge', 'falls back to the default'):
            self.assertIn(rule, mode)
        self.assertIn('pointers, not copies', text)
        self.assertIn('copy an item only when it has no saved locator', text)

    def test_plan_adr_candidate_uses_three_conditions(self):
        plan = flat(read('skills/plan/SKILL.md'))
        for criterion in ('costly to undo', 'its rationale will not be visible in the code',
                          'alternatives were actually weighed'):
            self.assertIn(criterion, plan)
        self.assertIn('skip it when any of these is missing', plan)

    def test_grill_is_the_only_interview_exception_for_clear_requests(self):
        text = flat(read('skills/research/references/clarification-interview.md'))
        self.assertIn('unless the user explicitly asks for grill mode', text)
        self.assertIn('evidenced facts are still verified, never asked', text)



class SpecificationFirst(unittest.TestCase):
    """9f1.2: approved specification before Implement (user request 2026-11-20)."""

    def test_plan_requires_approved_linked_specification(self):
        plan = flat(read('skills/plan/SKILL.md'))
        for rule in ('Specify before implementing', 'needs a written specification',
                     'its approved ticket criteria are the specification',
                     "approval status, approver and date", 'link it from every task',
                     'a drafted or proposed specification is not approval',
                     'implementation-ready only when its specification is approved'):
            self.assertIn(rule, plan)
        review = flat(read('skills/plan/references/plan-readiness-review.md'))
        self.assertIn('Which approved specification does this ticket implement', review)

    def test_implement_and_cycle_gate_on_approved_specification(self):
        implement = flat(read('skills/implement/SKILL.md'))
        for rule in ('Specification gate', 'since-changed specification returns to Plan before any edit',
                     'is a Plan decision, not a silent code choice'):
            self.assertIn(rule, implement)
        table = read('skills/cycle/SKILL.md').split('## Workflow', 1)[0]
        self.assertIn('whose specification or criteria are approved and whose failing checks are named', table)


class TestFirstEvidence(unittest.TestCase):
    """9f1.3: test list planned, test code written per slice, red shown per criterion."""

    def test_plan_lists_tests_without_writing_them(self):
        plan = flat(read('skills/plan/SKILL.md'))
        self.assertIn('This test list (criterion, behavior, seam, oracle) is planned here', plan)
        self.assertIn('not all tests in advance', plan)

    def test_red_recorded_per_criterion_and_checked_downstream(self):
        self.assertIn('per behavioral criterion ID, the red command',
                      flat(read('skills/implement/SKILL.md')))
        test = flat(read('skills/test/SKILL.md'))
        self.assertIn('For every behavioral criterion, confirm discrimination', test)
        self.assertIn('reported as undiscriminated for that criterion', test)
        judge = flat(read('skills/judge/SKILL.md'))
        self.assertIn('A check never shown to fail is an evidence gap for that criterion', judge)
        self.assertIn('indeterminate unless a known defect already requires correction', judge)
        self.assertIn('revert-the-fix or counterexample run on the candidate when the behavior already existed', judge)
        self.assertIn('Instruction-only criteria rely on labeled static evidence', judge)



class ApprovalStopAndOuterLoop(unittest.TestCase):
    """da4.1: Plan stops for specification approval; story-level acceptance check first."""

    def test_plan_stops_for_specification_approval(self):
        plan = flat(read('skills/plan/SKILL.md'))
        self.assertIn('present it with one approval question and stop', plan)
        self.assertIn('do not hand off to Implement until the user or designated owner approves', plan)
        self.assertIn('an unapproved specification stops for approval by the user or designated owner',
                      read('skills/cycle/SKILL.md').split('## Workflow', 1)[0])

    def test_outer_acceptance_check_fails_first_and_passes_last(self):
        plan = flat(read('skills/plan/SKILL.md'))
        self.assertIn('one outer acceptance check at the highest agreed seam', plan)
        implement = flat(read('skills/implement/SKILL.md'))
        for rule in ('write it first and observe it failing', 'keep it visibly pending, not deleted or silently skipped',
                     'name the story and the task that will make it pass',
                     'only then is the story complete', 'labeled static check'):
            self.assertIn(rule, implement)
        self.assertIn("Assign writing it to the story's first task", plan)
        self.assertIn('reported as story pending, not as a failure or weakening', flat(read('skills/test/SKILL.md')))
        self.assertIn('prefer an expected-failure mark', implement)
        self.assertIn('list the exclusion in the change ledger', implement)
        self.assertIn('or pending outer acceptance check naming its owner task; an unjustified entry blocks handoff', implement)
        test = flat(read('skills/test/SKILL.md'))
        self.assertIn('provided the task it names exists and is not closed', test)
        self.assertIn('a missing or closed owner task, or an unlisted suite exclusion, is a finding', test)
        self.assertIn("pending state is expected, not a defect", flat(read('skills/judge/SKILL.md')))
        doc = flat(read('docs/skill-flow.md'))
        self.assertIn('outer acceptance check fails first, stays marked pending, and passes last', doc)
        self.assertIn('Plan stops for approval by you or a designated owner', doc)


if __name__ == '__main__':
    unittest.main()
