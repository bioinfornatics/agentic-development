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
EDGE = re.compile(r'^\s*(\w+)\s*-(?:-|\.-)>\|[^|]*\|\s*(\w+(?:\s*&\s*\w+)*)', re.M)
COMMAND = re.compile(r'`((?:bd|git|node|python3)\b[^`]*|[\w.-]+\.py)`')

# Handoff routes named in each phase's final "Execute the handoff or stop" step.
HANDOFF_ROUTES = {
    'cycle': set(),
    'research': {'plan'},
    'plan': {'implement', 'research'},
    'implement': {'test', 'iterate'},
    'test': {'judge', 'iterate'},
    'judge': {'iterate'},
    'iterate': {'implement', 'test', 'research', 'plan'},
}
# Edges the guide must draw: handoffs, cycle dispatch, loops and exits.
DOC_EDGES = {(s, t) for s, targets in HANDOFF_ROUTES.items() for t in targets} | {
    ('cycle', p) for p in PHASES[1:]} | {
    ('research', 'research'), ('implement', 'implement'), ('judge', 'test'),
    ('judge', 'finalize'), ('plan', 'halt'), ('judge', 'halt'), ('iterate', 'halt')}
# Edges outside the Load routes, each tied to the Skill sentence that grounds it.
EDGE_SOURCES = {
    ('research', 'research'): ('research', 'execute the next bounded probe within permission'),
    ('implement', 'implement'): ('implement', 'observe red, implement green, then refactor'),
    ('judge', 'test'): ('judge', 'route missing checks to Test only when authorized'),
    ('judge', 'halt'): ('judge', 'A second indeterminate verdict on the same candidate'),
    ('judge', 'finalize'): ('cycle', 'After accepted judgment, persist results'),
    ('plan', 'halt'): ('plan', 'For roadmap-only work, return the planning artifact'),
    ('iterate', 'halt'): ('iterate', 'Stop corrective execution on exhaustion or repeated no-progress'),
}


def skill(name):
    return (ROOT / 'skills' / name / 'SKILL.md').read_text()


def flat(text):
    return ' '.join(text.split())


def normalized_sources():
    files = [*(ROOT / 'skills').rglob('*.md'), *(ROOT / 'skills').rglob('*.py'), ROOT / 'hooks/hooks.json']
    text = ' '.join(path.read_text() for path in files)
    return flat(re.sub(r'[(),]', ' ', text.replace('"', '')))


def doc_edges(doc):
    return {(s, t.strip()) for s, ts in EDGE.findall(doc) for t in ts.split('&')}


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
                self.assertIn(flat(command.replace('"', '')), sources)

    def test_entire_is_described_as_observed_links_not_a_command(self):
        self.assertIn('record observed session/checkpoint links', flat(skill('cycle')))
        self.assertIn('observed session/checkpoint links', self.doc)
        self.assertNotIn('Entire status', self.doc)

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
