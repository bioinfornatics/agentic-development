"""Source contract: the documented Skill workflow graph matches the Skill handoffs.

Expected routes, loop bounds and tool rules are stated here independently from the
guide so that drift in either a SKILL.md handoff or docs/skill-flow.md fails.
This is static source evidence, not proof of agent behavior.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PHASES = ['cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate']
SKILL_REF = re.compile(r'agentic-development:([a-z-]+)')
EDGE = re.compile(r'^\s*(\w+)\s*-(?:-|\.-)>\|([^|]*)\|\s*(\w+(?:\s*&\s*\w+)*)', re.M)
COMMAND = re.compile(r'`((?:bd|git|node|python3)\b[^`]*|[\w.-]+\.py)`')
COUNT = r'(\d+|one|two|three|four|five|once|twice)'
NUMBERS = {'one': '1', 'once': '1', 'two': '2', 'twice': '2', 'three': '3', 'four': '4', 'five': '5'}
ATTEMPT_BOUND = re.compile(r'\b' + COUNT + r'\s+(?:[\w-]+\s+){0,2}?attempts\b', re.I)
ATTEMPT_OF = re.compile(r'\battempt\s+\d+\s+of\s+(\d+)', re.I)
INDETERMINATE_ORDINAL = re.compile(r'\b(\w+)\s+indeterminate\s+verdict', re.I)
RETRY_BEFORE = re.compile(r'\b' + COUNT + r'\s+(?:[\w-]+\s+){0,3}?retr(?:y|ies)\b', re.I)
RETRY_AFTER = re.compile(r'\bretried\s+' + COUNT, re.I)

# Handoff routes named in each phase's final "Execute the handoff or stop" step.
HANDOFF_ROUTES = {
    'cycle': set(),
    'research': {'plan'},
    'plan': {'implement', 'research'},
    'implement': {'test', 'iterate', 'plan'},
    'test': {'judge', 'iterate'},
    'judge': {'iterate'},
    'iterate': {'implement', 'test', 'research', 'plan'},
}
# Edges the guide must draw: handoffs, cycle dispatch, loops and exits.
DOC_EDGES = {(s, t) for s, targets in HANDOFF_ROUTES.items() for t in targets} | {
    ('cycle', p) for p in PHASES[1:]} | {
    ('research', 'research'), ('implement', 'implement'), ('judge', 'test'),
    ('judge', 'finalize'), ('plan', 'halt'), ('judge', 'halt'), ('iterate', 'halt'),
    ('research', 'halt'), ('test', 'halt')}
# Edges outside the Load routes, each tied to the Skill sentence that grounds it.
EDGE_SOURCES = {
    ('research', 'research'): ('research', 'execute the next bounded probe within permission'),
    ('implement', 'implement'): ('implement', 'observe red, implement green, then refactor'),
    ('judge', 'test'): ('judge', 'route missing checks to Test only when authorized'),
    ('judge', 'halt'): ('judge', 'A second indeterminate verdict on the same candidate'),
    ('judge', 'finalize'): ('cycle', 'After accepted judgment, persist results'),
    ('plan', 'halt'): ('plan', 'For roadmap-only work, return the planning artifact'),
    ('iterate', 'halt'): ('iterate', 'Stop corrective execution on exhaustion or repeated no-progress'),
    ('research', 'halt'): ('research', 'Block Plan on decision-critical gaps'),
    ('test', 'halt'): ('test', 'An unavailable mandatory check stays open'),
}
# Decisive condition keyword per edge: it must appear in the guide label and in
# the grounding Skill text, so swapped or dropped conditions fail while rewording passes.
EDGE_KEYWORDS = {
    ('cycle', 'research'): ('objective', 'cycle'),
    **{('cycle', p): ('first incomplete', 'cycle') for p in PHASES[2:]},
    ('research', 'research'): ('probe', 'research'),
    ('research', 'plan'): ('decision', 'research'),
    ('plan', 'research'): ('prerequisite', 'plan'),
    ('plan', 'implement'): ('authorized', 'plan'),
    ('plan', 'halt'): ('roadmap-only', 'plan'),
    ('implement', 'implement'): ('refactor', 'implement'),
    ('implement', 'test'): ('focused checks', 'implement'),
    ('implement', 'iterate'): ('correction decision', 'implement'),
    ('implement', 'plan'): ('missing context', 'implement'),
    ('research', 'halt'): ('decision-critical', 'research'),
    ('test', 'halt'): ('unavailable mandatory check', 'test'),
    ('test', 'judge'): ('record', 'test'),
    ('test', 'iterate'): ('repair', 'test'),
    ('judge', 'finalize'): ('accepted', 'judge'),
    ('judge', 'iterate'): ('needs-correction', 'judge'),
    ('judge', 'test'): ('missing checks', 'judge'),
    ('judge', 'halt'): ('second indeterminate', 'judge'),
    ('iterate', 'implement'): ('implementation', 'iterate'),
    ('iterate', 'test'): ('proof', 'iterate'),
    ('iterate', 'research'): ('unknown cause', 'iterate'),
    ('iterate', 'plan'): ('scope', 'iterate'),
    ('iterate', 'halt'): ('budget', 'iterate'),
}


def skill(name):
    return (ROOT / 'skills' / name / 'SKILL.md').read_text()


def flat(text):
    return ' '.join(text.split())


def normalize_source(text):
    return flat(re.sub(r'[(),]', ' ', text.replace('"', '')))


def normalized_sources():
    files = [*(ROOT / 'skills').rglob('*.md'), *(ROOT / 'skills').rglob('*.py'), ROOT / 'hooks/hooks.json']
    return [normalize_source(path.read_text()) for path in files]


def command_found(command, texts):
    """True when one source text, never a concatenation of two, contains the command."""
    needle = flat(command.replace('"', ''))
    return any(needle in normalize_source(text) for text in texts)


def stated_bounds(text):
    """Return (attempt bounds, retry counts, indeterminate ordinals) stated in text."""
    number = lambda word: NUMBERS.get(word.lower(), word)
    attempts = {number(n) for n in ATTEMPT_BOUND.findall(text)} | set(ATTEMPT_OF.findall(text))
    retries = {number(n) for n in RETRY_BEFORE.findall(text) + RETRY_AFTER.findall(text)}
    return attempts, retries, {w.lower() for w in INDETERMINATE_ORDINAL.findall(text)}


def duplicate_edges(doc):
    edges = [(s, t.strip()) for s, _, ts in EDGE.findall(doc) for t in ts.split('&')]
    return {edge for edge in edges if edges.count(edge) > 1}


def doc_labels(doc):
    return {(s, t.strip()): label.lower() for s, label, ts in EDGE.findall(doc) for t in ts.split('&')}


def doc_edges(doc):
    return set(doc_labels(doc))


def handoff_step(text):
    return text.split('**Execute the handoff or stop**', 1)[1]


class SkillFlowContract(unittest.TestCase):
    def setUp(self):
        self.doc = (ROOT / 'docs/skill-flow.md').read_text()

    def test_skill_handoffs_match_expected_routes(self):
        for phase, expected in HANDOFF_ROUTES.items():
            with self.subTest(phase=phase):
                found = set(SKILL_REF.findall(handoff_step(skill(phase))))
                self.assertEqual(found - {'task-authoring'}, expected)

    def test_cycle_routing_table_names_every_phase(self):
        table = skill('cycle').split('## Workflow', 1)[0]
        self.assertEqual(set(SKILL_REF.findall(table)), set(PHASES[1:]))

    def test_guide_draws_every_route_loop_and_exit(self):
        self.assertEqual(doc_edges(self.doc), DOC_EDGES)

    def test_edge_conditions_keep_their_decisive_keyword(self):
        labels = doc_labels(self.doc)
        self.assertEqual(set(EDGE_KEYWORDS), DOC_EDGES)
        for edge, (keyword, phase) in EDGE_KEYWORDS.items():
            with self.subTest(edge=edge):
                self.assertIn(keyword, labels.get(edge, ''))
                self.assertIn(keyword, flat(skill(phase)).lower())

    def test_non_route_edges_are_grounded_in_skill_text(self):
        routes = {(s, t) for s, ts in HANDOFF_ROUTES.items() for t in ts}
        cycle = {('cycle', p) for p in PHASES[1:]}
        self.assertEqual(set(EDGE_SOURCES), DOC_EDGES - routes - cycle)
        for edge, (phase, sentence) in EDGE_SOURCES.items():
            with self.subTest(edge=edge):
                self.assertIn(sentence, flat(skill(phase)))

    def test_cited_commands_exist_in_skill_or_hook_sources(self):
        sources = normalized_sources()
        for command in COMMAND.findall(self.doc):
            with self.subTest(command=command):
                self.assertTrue(command_found(command, sources), command)

    def test_command_match_never_crosses_file_boundaries(self):
        self.assertTrue(command_found('git ls-files --stage', ['x git(ls-files, --stage, -z) y']))
        self.assertFalse(command_found('bd init --skip-hooks', ['run bd init', '--skip-hooks only']))

    def test_bound_extraction_handles_wording_variants(self):
        self.assertEqual(stated_bounds('Iterate allows 5 corrective attempts')[0], {'5'})
        self.assertEqual(stated_bounds('Judge is retried twice')[1], {'2'})
        self.assertEqual(stated_bounds('one Judge indeterminate retry via Test')[1], {'1'})
        self.assertEqual(stated_bounds('One Test retry; attempt 1 of 3')[0:2], ({'3'}, {'1'}))

    def test_guide_and_agents_state_no_contradicting_bound(self):
        attempts, retries, ordinals = stated_bounds(self.doc)
        self.assertEqual((attempts, retries), ({'3'}, {'1'}))
        self.assertLessEqual(ordinals, {'second', 'repeated'})
        attempts, retries, _ = stated_bounds((ROOT / 'AGENTS.md').read_text())
        self.assertEqual((attempts, retries), ({'3'}, {'1'}))

    def test_guide_draws_each_edge_once(self):
        self.assertEqual(duplicate_edges('  a -->|x| b\n  a -->|y| b & c'), {('a', 'b')})
        self.assertEqual(duplicate_edges(self.doc), set())

    def test_entire_is_described_as_observed_links_not_a_command(self):
        self.assertIn('record observed session/checkpoint links', flat(skill('cycle')))
        self.assertIn('observed session/checkpoint links', self.doc)
        self.assertNotIn('Entire status', self.doc)

    def test_git_operations_are_documented_with_their_gates(self):
        gate = 'separate authorized worktree or clean checkout'
        reference = ROOT / 'skills/research/references/root-cause-investigation.md'
        self.assertIn('`git bisect` in a ' + gate, flat(reference.read_text()))
        agents = flat((ROOT / 'AGENTS.md').read_text())
        for name, text in [('guide', flat(self.doc)), ('AGENTS.md', agents)]:
            with self.subTest(file=name):
                self.assertIn('git bisect', text)
                self.assertIn(gate, text)
        self.assertIn('commits only with current authority', agents)

    def test_guide_has_one_worked_example(self):
        self.assertEqual(self.doc.count('## Example'), 1)

    def test_loop_bounds_are_stated_in_skills_and_guide(self):
        self.assertIn('Default maximum: three authorized attempts', skill('iterate'))
        self.assertIn('A second indeterminate verdict', skill('judge'))
        self.assertIn('Default to at most three correction attempts', skill('cycle'))
        for bound in ['3 authorized correction attempts', 'second indeterminate', 'named deciding prerequisite']:
            self.assertIn(bound, self.doc)

    def test_task_authoring_returns_to_caller_without_chaining(self):
        text = skill('task-authoring')
        self.assertIn('STOP and return to the caller', text)
        self.assertEqual(set(SKILL_REF.findall(text)), set())
        for phase in PHASES:
            with self.subTest(phase=phase):
                self.assertIn('Load `agentic-development:task-authoring`', skill(phase))

    def test_skills_call_no_forge_cli_and_guide_says_so(self):
        forge = re.compile(r'`(gh|glab)\s|\b(gh|glab) (pr|mr|issue|release|api)\b')
        for path in (ROOT / 'skills').rglob('*.md'):
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(forge.search(path.read_text()))
        self.assertIn('Skills never call `gh` or `glab`', self.doc)

    def test_guide_names_gated_tool_calls(self):
        for command in ['bd prime', 'bd where', 'bd dep add', 'bd init', 'bd hooks',
                        'candidate_identity.py', 'git ls-files --stage', 'node "$CREATOR" full-eval', 'observe.py']:
            self.assertIn(command, self.doc)


if __name__ == '__main__':
    unittest.main()
