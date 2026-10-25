"""RPI context-first source contracts; not executed agent behavior."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class ResearchProductContext(unittest.TestCase):
    def test_research_activates_for_clear_and_familiar_changes(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        description = text.split('description:', 1)[1].split('---', 1)[0]
        for term in ('product context', 'before planning', 'every new development', 'clear or familiar'):
            self.assertIn(term, description)
        router = text.split('## Select the action from the intent', 1)[1].split('## Requirements', 1)[0]
        self.assertIn('Start any new development objective', router)
        self.assertIn('verify coverage and freshness', router)
        self.assertNotIn('Understand an unfamiliar feature, architecture or technical risk', router)

    def test_product_baseline_precedes_technical_exploration(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        workflow = text.split('## Workflow', 1)[1].split('## Conditional reuse decision', 1)[0]
        self.assertLess(workflow.index('product purpose'), workflow.index('Retrieve likely entry points'))
        for term in ('users', 'current behavior', 'constraints', 'sources', 'assumptions'):
            self.assertIn(term, workflow)
        self.assertIn('Product context and requested outcome', (ROOT / 'skills/research/references/requirements-output.md').read_text())

    def test_cycle_and_plan_require_context_before_planning(self):
        cycle = (ROOT / 'skills/cycle/SKILL.md').read_text()
        row = next(line for line in cycle.splitlines() if line.startswith('| 1 |'))
        self.assertIn('Every new development objective', row)
        self.assertIn('product context', row)
        self.assertIn('Research precedes Plan', cycle)
        plan = (ROOT / 'skills/plan/SKILL.md').read_text()
        self.assertIn('verify research coverage and freshness', plan)
        self.assertIn('A clear request is not a substitute for research', plan)

class ResearchModes(unittest.TestCase):
    def test_modes_answer_where_how_and_existing_examples(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        for mode in ('find_files', 'analyze_code', 'find_patterns'):
            self.assertIn(mode, text)
        self.assertIn('intent labels, not required tool names', text)
        self.assertIn('references/state-of-the-art.md', text)

    def test_freshness_search_is_conditional_and_source_grounded(self):
        path = ROOT / 'skills/research/references/state-of-the-art.md'
        self.assertTrue(path.is_file())
        text = path.read_text()
        for rule in ('three months', 'publication', 'access date', 'primary sources', 'unavailable', 'decision-critical', 'not installation permission'):
            self.assertIn(rule, text)

if __name__ == '__main__':
    unittest.main()
