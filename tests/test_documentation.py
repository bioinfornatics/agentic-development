"""Current documentation structure checks, not pedagogical usability proof."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class DocumentationLayout(unittest.TestCase):
    def test_user_docs_are_small_and_separate_from_receipts(self):
        docs = ROOT / 'docs'
        self.assertEqual({p.name for p in docs.iterdir()},
                         {'AGENTS.md', 'getting-started.md', 'cycle.md', 'integrations.md', 'contributing.md'})
        for p in docs.iterdir():
            text = p.read_text()
            self.assertNotIn('agentic-devlopment-', text)
            self.assertNotIn('docs/agentic/', text)
            self.assertLessEqual(len(text.splitlines()), 100)

    def test_entrypoint_is_navigation_not_execution_history(self):
        text = (ROOT / 'README.md').read_text()
        self.assertLessEqual(len(text.splitlines()), 60)
        self.assertNotIn('agentic-devlopment-', text)
        self.assertNotIn('.json', text)
        for name in ['getting-started', 'cycle', 'integrations', 'contributing']:
            self.assertIn('docs/' + name + '.md', text)

    def test_readme_explains_optional_workflow_tools(self):
        text = (ROOT / 'README.md').read_text()
        self.assertIn('## Dependencies and optional tools', text)
        for tool in ['GitHub CLI', 'Beads', 'Entire']:
            self.assertIn(tool, text)
        self.assertEqual(text.count(', optional |'), 3)
        self.assertIn('not replace task tracking or acceptance', text)
        self.assertIn('observed session/checkpoint IDs', text)

    def test_repository_language_policy_requires_explicit_exceptions(self):
        policy = (ROOT / 'AGENTS.md').read_text()
        self.assertIn('All repository and distributed content defaults to English', policy)
        self.assertIn('Only an explicit user request', policy)
        self.assertIn('conversation language does not authorize', policy)
        docs_policy = (ROOT / 'docs/AGENTS.md').read_text()
        self.assertIn('English is the canonical documentation language', docs_policy)
        self.assertNotIn('user guides may be French', docs_policy)

    def test_current_guides_have_english_entrypoints(self):
        expected = {'README.md': '# Agentic Development',
                    'docs/getting-started.md': '# Getting started',
                    'docs/cycle.md': '# Steering the development cycle',
                    'docs/integrations.md': '# Connecting tasks, commits and sessions',
                    'docs/contributing.md': '# Contributing to the method'}
        for name, heading in expected.items():
            with self.subTest(path=name):
                self.assertEqual((ROOT / name).read_text().splitlines()[0], heading)

    def test_new_run_outputs_do_not_pollute_user_docs(self):
        text = (ROOT / 'skills/cycle/SKILL.md').read_text()
        self.assertNotIn('docs/agentic/slices/<slice-id>/', text)
        self.assertIn('evidence/runs/<slice-id>/', text)

    def test_current_doc_links_resolve(self):
        for p in [ROOT / 'README.md', *list((ROOT / 'docs').glob('*.md'))]:
            for part in p.read_text().split('](')[1:]:
                target = part.split(')', 1)[0].split('#', 1)[0]
                if not target or '://' in target:
                    continue
                self.assertTrue((p.parent / target).exists(), (p, target))
