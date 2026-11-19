"""Static source evidence: repeated phase paragraphs stay byte-identical.

These checks read the seven phase SKILL.md sources only. They prove that each
shared paragraph family has one normalized wording across the phases that carry
it, and that documented phase-specific companions remain present. They do not
execute an agent workflow or prove agent behavior.

Each family is extracted as the Markdown block (blank-line paragraph or list
item) that starts with the family's opening phrase; whitespace is normalized and
a leading list marker is ignored.

Documented exceptions (phase-specific text kept OUTSIDE the shared block, in a
separate companion paragraph or list item, because it is semantically bound to
one phase):
- cycle: delivery-mechanism/asset-map routing after the task-authoring block
  (coordinator readiness gate) and the UI checkpoint example (cycle-only asset).
- research: allowed probe effects and the no-production-edit limit (research
  probes); bounded question with no completed plan (investigation precedes
  planning); provenance-path selection for source-only observations and
  preliminary checks.
- test: a check needs a named criterion or risk, not a complete test plan.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')

# family -> (opening phrase, rule fragments the canonical union must retain)
FAMILIES = {
    'task-authoring routing': (
        'Before creating or repairing task descriptions',
        ('verify current scope and write authority',
         "using the host's available Skill-loading mechanism (not a shell command)",
         'do not load both routes normally',
         'report direct reading, not activation',
         'do not load task-authoring',
         'Resume this caller after verified ticket readback')),
    'beads': (
        'If the repository uses Beads',
        ('before choosing work or mutating task state',
         'Run `bd prime` only when Beads context is missing or stale',
         'without inferring Git authority')),
    'authorization': (
        'Apply [the authorization policy]',
        ('before resuming artifact claims or executing consequential actions',
         'not historical approval')),
    'requirements baseline': (
        'Apply [the requirements baseline]',
        ('scope, criteria, checks or verification',
         'before running checks',
         'Resolve the approved task baseline',
         'quantified NFRs without inventing targets',
         'keep missing requirements explicit')),
    'review policy': (
        'Apply [the review policy]',
        ('setting or reporting acceptance/review requirements',
         'before implementation',
         'proposing or agreeing acceptance, judging or closing a task/US',
         'set at plan time, before implementation',
         'a missing capability does not waive them')),
    'communication contract': (
        'Apply [the communication contract]',
        ('before the first mutation',
         'before preparing the first checkpoint or a Git/session transition',
         'not an up-front load of response templates',
         'standalone use too',
         "Respond in the user's language",
         'never simulated execution evidence',
         'do not fabricate execution or acceptance')),
    'candidate identity': (
        'Apply [candidate identity]',
        ('before planning checks, freezing or comparing inputs or reusing evidence',
         'staged, untracked and binary inputs',
         'output-only exclusions',
         'equality is not acceptance')),
    'phase report': (
        'A phase report is the result',
        ('not a file to find before execution',
         'does not replace task truth')),
    'next phase': (
        'Execute the next phase only when',
        ('For a phase-only request',)),
    'skill-loading fallback': (
        "Use the host's available Skill-loading mechanism",
        ('not shell commands', 'report direct reading rather than activation')),
}

CLI_SENTENCE = re.compile(r'For exact-candidate proof, .*?equality is not acceptance\.')

# phase -> fragments of documented phase-specific companions (exceptions)
COMPANIONS = {
    'cycle': ('Require explicit delivery mechanisms and asset maps',
              'For a UI checkpoint apply [the checkpoint example]'),
    'research': ('Research does not authorize production edits',
                 'Side-effecting probes require scoped authority and an isolated environment',
                 'Investigation needs no completed plan',
                 'Select the provenance path',
                 "before accepting a worker's evidence as reusable"),
    'test': ('A check needs a named criterion or risk, not a complete test plan',),
}


def blocks(text):
    """Split Markdown into normalized paragraphs and list items."""
    out, cur = [], []
    for line in text.splitlines():
        stripped = line.strip()
        starts_item = re.match(r'^(?:[-*] |\d+\. |\|)', stripped)
        if not stripped or (starts_item and cur):
            if cur:
                out.append(' '.join(cur))
                cur = []
            if not stripped:
                continue
        cur.append(stripped)
    if cur:
        out.append(' '.join(cur))
    return [re.sub(r'^(?:[-*] )', '', ' '.join(b.split())) for b in out]


def source(phase):
    return (ROOT / 'skills' / phase / 'SKILL.md').read_text(encoding='utf-8')


class SharedParagraphIdentity(unittest.TestCase):
    def test_each_family_is_identical_across_phases(self):
        for family, (opening, _) in FAMILIES.items():
            with self.subTest(family=family):
                variants = {}
                for phase in PHASES:
                    found = [b for b in blocks(source(phase)) if b.startswith(opening)]
                    self.assertEqual(len(found), 1, (family, phase, found))
                    variants.setdefault(found[0], []).append(phase)
                self.assertEqual(len(variants), 1, (family, variants))

    def test_canonical_union_retains_every_rule(self):
        for family, (opening, rules) in FAMILIES.items():
            text = next(b for b in blocks(source('cycle')) if b.startswith(opening))
            for rule in rules:
                with self.subTest(family=family, rule=rule):
                    self.assertIn(rule, text)

    def test_candidate_cli_sentence_is_identical_and_inside_candidate_block(self):
        sentences = set()
        for phase in PHASES:
            block = next(b for b in blocks(source(phase))
                         if b.startswith(FAMILIES['candidate identity'][0]))
            found = CLI_SENTENCE.findall(block)
            self.assertEqual(len(found), 1, phase)
            self.assertEqual(len(CLI_SENTENCE.findall(' '.join(source(phase).split()))), 1, phase)
            sentences.add(found[0])
        self.assertEqual(len(sentences), 1, sentences)

    def test_documented_phase_specific_companions_remain(self):
        for phase, fragments in COMPANIONS.items():
            text = ' '.join(source(phase).split())
            for fragment in fragments:
                with self.subTest(phase=phase, fragment=fragment):
                    self.assertTrue(fragment in text, (phase, fragment))


if __name__ == '__main__':
    unittest.main()
