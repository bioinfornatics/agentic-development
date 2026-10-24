"""Source integration boundaries, not runtime acceptance."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[2]

class IntegrationScope(unittest.TestCase):
    def test_guides_reference_only_bundled_skill_names(self):
        for path in [*(ROOT / 'docs').glob('*.md'),
                     *(ROOT / 'website/i18n').rglob('*.md'), ROOT / 'website/index.md']:
            for name in re.findall('agentic-development:([a-z-]+)', path.read_text()):
                self.assertTrue((ROOT / 'skills' / name / 'SKILL.md').is_file(),
                                (path, name))

    def test_relative_markdown_links_exist(self):
        for path in (ROOT / 'website').rglob('*.md'):
            for part in path.read_text().split('](')[1:]:
                target = part.split(')',1)[0].split('#',1)[0]
                if not target or '://' in target: continue
                self.assertTrue((path.parent / target).exists(), (path,target))

    def test_site_declares_standalone_source_boundary(self):
        text = (ROOT / 'website/README.md').read_text()
        self.assertIn('Standalone source 0.5.0', text)
        self.assertIn('no configured remote', text)

    def test_only_one_pages_deployment_workflow(self):
        workflows = [p for p in (ROOT / '.github/workflows').glob('*.yml')
                     if 'actions/deploy-pages@' in p.read_text()]
        self.assertEqual([p.name for p in workflows], ['pages.yml'])

    def test_cycle_follows_current_reporting_policy(self):
        text = (ROOT / 'docs/cycle.md').read_text()
        for field in ('step','modified files','next step','current goal','next goal','closed tasks','explanation'):
            self.assertIn('**' + field + '**', text)
        self.assertIn('three authorized attempts',text)
