"""Approved cycle routing/report source checks; not agent execution proof."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')

def workflow_steps(text):
    import re
    workflow = text.split('## Workflow', 1)[1]
    matches = list(re.finditer(r'^(\d+)\. \[ \] \*\*(.*?)\*\*$', workflow, re.M))
    return [(int(match[1]), match[2], workflow[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(workflow)])
            for i, match in enumerate(matches)]

class CycleDisclosure(unittest.TestCase):
    def test_activation_includes_single_phase_development(self):
        description = (ROOT / 'skills/cycle/SKILL.md').read_text().split('description:', 1)[1].split('---', 1)[0]
        for intent in ('software development', 'fixing bugs', 'testing', 'reviewing', 'single-phase'):
            self.assertIn(intent, description)

    def test_one_ordered_intent_router_and_explained_deviations(self):
        text = (ROOT / 'skills/cycle/SKILL.md').read_text()
        self.assertEqual(text.count('| Order | Intent / condition | Skill | Required output / exit gate |'), 1)
        self.assertNotIn('## Phase routing and gates', text)
        for order, phase in enumerate(NAMES[1:6], 1):
            self.assertIn(f'| {order} |', text)
            self.assertIn('agentic-development:' + phase, text)
        for rule in ('nonstandard transition', 'mandatory prerequisite', 'first incomplete or invalidated', 'single-phase request'):
            self.assertIn(rule, text)

    def test_output_is_late_and_requirements_are_early(self):
        for name in NAMES:
            with self.subTest(skill=name):
                entry = (ROOT / 'skills' / name / 'SKILL.md').read_text()
                self.assertNotIn('Before starting work, read', entry)
                self.assertIn('references/requirements-baseline.md', entry)
                block = workflow_steps(entry)[-2][2]
                self.assertRegex(block, r'After investigation and (?:immediately )?before drafting')
                self.assertIn('references/common-output.md', block)
                self.assertIn('references/requirements-output.md', block)
                output = (ROOT / 'skills' / name / 'references/common-output.md').read_text()
                self.assertNotIn('## Requirements baseline', output)
                self.assertIn('## current goal {step:', output)
                self.assertIn('## roadmap position', output)
                for old in ('## step\n', '## next step\n', '## next goal\n'):
                    self.assertNotIn(old, output)
                self.assertIn('States are not phases', output)
                self.assertIn('unavailable', output)
                baseline = (ROOT / 'skills' / name / 'references/requirements-baseline.md').read_text()
                for rule in ('Before implementation', 'Given/When/Then', 'Do not invent targets'):
                    self.assertIn(rule, baseline)

class ReferenceConcision(unittest.TestCase):
    def test_output_references_have_one_late_trigger(self):
        for name in NAMES:
            text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
            block = workflow_steps(text)[-2][2]
            for ref in ('references/common-output.md', 'references/requirements-output.md'):
                self.assertEqual(text.count(ref), 1, (name, ref))
                self.assertIn(ref, block)
            self.assertRegex(block, r'After investigation and (?:immediately )?before drafting')

    def test_each_skill_link_has_a_local_read_condition(self):
        import re
        for name in NAMES:
            with self.subTest(skill=name):
                text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
                blocks = text.split(chr(10) + chr(10))
                refs = []
                for block in blocks:
                    links = re.findall(r'\]\((references/[^)]+)\)', block)
                    if links:
                        self.assertRegex(block, r'(?i)(before|when|if|after|for a new|only for)')
                        refs.extend(links)
                self.assertEqual(len(refs), len(set(refs)))

class UnifiedWorkflow(unittest.TestCase):
    def test_every_skill_has_one_complete_ordered_workflow(self):
        for name in NAMES:
            with self.subTest(skill=name):
                text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
                self.assertEqual(text.count('## Workflow'), 1)
                self.assertEqual([line for line in text.splitlines() if line.startswith('## ')],
                                 ['## Select the action from the intent', '## Workflow'])
                self.assertNotIn('](references/', text.split('## Workflow', 1)[0])
                steps = workflow_steps(text)
                self.assertGreaterEqual(len(steps), 5)
                self.assertEqual([number for number, _, _ in steps], list(range(1, len(steps) + 1)))
                self.assertEqual(steps[-1][1], 'Execute the handoff or stop')
                self.assertIn('draft', steps[-2][1])
                for token in ('For a phase-only request', 'proposed handoff, then stop', 'current scope/permissions', 'specific missing input'):
                    self.assertIn(token, steps[-1][2])
                for ref in ('references/common-output.md', 'references/requirements-output.md'):
                    self.assertEqual(text.count(ref), 1)
                    self.assertIn(ref, steps[-2][2])
                    self.assertNotIn(ref, ''.join(body for _, _, body in steps[:-2]))

class DeliveryDraftOrder(unittest.TestCase):
    def test_handoff_is_drafted_after_output_guidance(self):
        for name in NAMES:
            with self.subTest(skill=name):
                text = (ROOT / 'skills' / name / 'SKILL.md').read_text()
                delivery = workflow_steps(text)[-2][2]
                self.assertIn('After reading delivery guidance, draft', delivery)
                self.assertLess(delivery.index('references/requirements-output.md'),
                                delivery.index('After reading delivery guidance, draft'))
                self.assertIn('fenced YAML state card and copy-ready restart prompt', delivery)
                self.assertNotIn('Return the full checkpoint:', ''.join(body for _, _, body in workflow_steps(text)[:-2]))

class ResearchWorkflowLoading(unittest.TestCase):
    def test_references_are_loaded_inside_the_governing_subphase(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        workflow = text.split('## Workflow', 1)[1].split('5. [ ]', 1)[0]
        stages = ('1. [ ] **Frame the objective and verify authority**',
                  '2. [ ] **Select and dispatch bounded investigations**',
                  '3. [ ] **Explore and verify the selected questions**',
                  '4. [ ] **Integrate evidence and prepare the decision**')
        positions = [workflow.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        for index, refs in enumerate((
                ('requirements-baseline', 'authorization-policy', 'beads-integration', 'review-policy'),
                ('delegated-investigation',),
                ('candidate-identity', 'state-of-the-art', 'reuse-decision'),
                ('knowledge-pointers', 'communication-contract'))):
            block = workflow.split(stages[index], 1)[1]
            if index + 1 < len(stages):
                block = block.split(stages[index + 1], 1)[0]
            for ref in refs:
                self.assertIn('references/' + ref + '.md', block)
        preamble = text.split('## Workflow', 1)[0]
        self.assertNotIn('](references/', preamble)

if __name__ == '__main__':
    unittest.main()
