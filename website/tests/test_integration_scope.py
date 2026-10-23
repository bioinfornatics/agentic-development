"""Source integration boundaries, not runtime acceptance."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[2]

class IntegrationScope(unittest.TestCase):
    def test_guides_reference_only_bundled_skill_names(self):
        for path in [*(ROOT / 'website/guides').glob('*.md'),
                     *(ROOT / 'website/i18n').rglob('*.md'), ROOT / 'website/index.md']:
            for name in re.findall('agentic-development:([a-z-]+)', path.read_text()):
                self.assertTrue((ROOT / 'plugins/agentic-development/skills' / name / 'SKILL.md').is_file(),
                                (path, name))

    def test_relative_markdown_links_exist(self):
        for path in (ROOT / 'website').rglob('*.md'):
            for part in path.read_text().split('](')[1:]:
                target = part.split(')',1)[0].split('#',1)[0]
                if not target or '://' in target: continue
                self.assertTrue((path.parent / target).exists(), (path,target))

    def test_site_does_not_claim_runtime_upgrade(self):
        text = (ROOT / 'website/README.md').read_text()
        self.assertIn('0.4.2 unchanged', text)
        self.assertIn('legacy harness/evaluation public URLs are not preserved', text)

    def test_only_one_pages_deployment_workflow(self):
        workflows = [p for p in (ROOT / '.github/workflows').glob('*.yml')
                     if 'actions/deploy-pages@' in p.read_text()]
        self.assertEqual([p.name for p in workflows], ['pages.yml'])

    def test_cycle_follows_bundled_reporting_scoring_and_round_policy(self):
        text = (ROOT / 'website/guides/cycle.md').read_text()
        for token in ('Objective and roadmap position', 'rubric v1.0.1',
                      'weighted scoring', 'three correction rounds'):
            self.assertIn(token, text)
        self.assertNotIn('three authorized attempts', text)
        self.assertNotIn('do not consume an attempt', text)
