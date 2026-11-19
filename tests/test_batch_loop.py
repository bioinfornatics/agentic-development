"""Batch-loop source contracts for the cycle coordinator (FR-1..FR-4, FR-7).

Static source evidence only: these checks read instruction text in
skills/cycle/SKILL.md and AGENTS.md. They do not execute a scheduler, a tracker
or an agent workflow and do not prove agent behavior or effectiveness.
Expected rules come from the approved batch-delivery requirements, not from the
candidate prose; wording may vary while each local relationship must remain.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read_source(path):
    return (ROOT / path).read_text(encoding='utf-8')


def normalize(text):
    return re.sub(r'\s+', ' ', re.sub(r'[`*_]', '', text.lower())).strip()


def action_section(text, heading_pattern):
    starts = list(re.finditer(r'^\d+\.\s+\[.\]\s+(.+)$', text, re.M))
    for index, match in enumerate(starts):
        if re.search(heading_pattern, normalize(match.group(1))):
            end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
            return text[match.start():end]
    raise AssertionError('Missing governed action seam: ' + heading_pattern)


class BatchLoopSourceContracts(unittest.TestCase):
    def setUp(self):
        self.cycle = read_source('skills/cycle/SKILL.md')
        self.agents = read_source('AGENTS.md')
        self.focus = action_section(self.cycle, r'frame|recover|select.*slice')
        self.dispatch = action_section(self.cycle, r'dispatch|delegat')
        self.join = action_section(self.cycle, r'integrat')

    def assert_policy(self, text, *concepts):
        """Require related concepts within one paragraph or two adjacent ones."""
        blocks = re.split(r'\n\s*\n', text)
        spans = [normalize('\n'.join(blocks[i:i + width]))
                 for i in range(len(blocks)) for width in (1, 2)]
        self.assertTrue(
            any(len(span) <= 2200 and all(re.search(c, span) for c in concepts)
                for span in spans),
            'Missing local policy relationship: ' + ' / '.join(concepts))

    def test_fr1_one_active_epic_across_runs(self):
        # Given several open epics, When a run starts or resumes, Then work comes
        # only from the active epic and only the user switches it.
        self.assert_policy(self.focus, r'one active epic', r'across (runs|sessions)',
                           r'bd ready --parent', r'descendant')
        self.assert_policy(self.focus, r'switch.*active epic|active epic.*switch',
                           r'only', r'explicit user decision')
        self.assert_policy(self.agents, r'one active epic across runs')

    def test_fr2_wip_is_the_active_batch(self):
        self.assert_policy(self.focus, r'work in progress', r'active batch',
                           r'only', r'in.progress|claimed',
                           r'coordinator owns the batch', r'(each )?worker owns one task')
        self.assertNotIn('one main verifiable task', normalize(self.cycle))
        agents = normalize(self.agents)
        self.assertNotIn('one main task/agent', agents)
        self.assertRegex(agents, r'coordinator owns the batch')
        self.assertRegex(agents, r'one task per worker|each worker owns one task')

    def test_fr3_batch_holds_all_ready_independent_tasks_bounded_by_host(self):
        self.assert_policy(self.dispatch, r'all ready', r'unblocked',
                           r'mutually independent', r'active epic')
        self.assert_policy(self.dispatch, r'host', r'concurrency limit',
                           r'never.*plugin.*cap|no plugin.*cap')
        self.assert_policy(self.dispatch, r'one (subagent|worker) per task',
                           r'disjoint writable paths')

    def test_fr4_finish_the_batch_before_pulling_more(self):
        self.assert_policy(self.join, r'(do not|never) (pull|claim)', r'outside the active batch',
                           r'until', r'every batch task', r'closed', r'released',
                           r'named blocker')

    def test_fr7_refine_one_batch_ahead_when_no_ready_tasks(self):
        self.assert_policy(self.cycle, r'no ready tasks', r'next batch',
                           r'propose', r'research', r'plan', r'refine')
        self.assert_policy(self.cycle, r'next epic in line', r'complete',
                           r'one batch ahead', r'current authority')

    def test_baseline_epic_term_matches_single_active_epic(self):
        phases = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')
        for phase in phases:
            with self.subTest(phase=phase):
                text = (ROOT / 'skills' / phase / 'references/requirements-baseline.md').read_text()
                self.assertIn('one active epic across runs, switched only by explicit user decision', text)
                self.assertNotIn('one active epic per run', text)
    def test_implement_keeps_batch_for_the_active_batch_only(self):
        text = (ROOT / 'skills/implement/SKILL.md').read_text()
        # Implement works one task; 'batch' is reserved for the epic's active batch.
        self.assertNotRegex(text, r'(?i)\bbatch')
        self.assertIn('dependent node group', text)

if __name__ == '__main__':
    unittest.main()
