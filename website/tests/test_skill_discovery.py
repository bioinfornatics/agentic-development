"""Published instructions must resolve to the bundled Skill discovery contract."""
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {'cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate'}
class SkillDiscovery(unittest.TestCase):
    def test_exact_names_and_matching_frontmatter(self):
        skills = ROOT / 'plugins/agentic-development/skills'
        self.assertEqual({p.name for p in skills.iterdir() if p.is_dir()}, EXPECTED)
        for name in EXPECTED:
            text = (skills / name / 'SKILL.md').read_text()
            self.assertRegex(text, r'(?m)^name: ' + name + r'$')
    def test_both_locale_instructions_resolve_and_have_no_legacy_names(self):
        pages = [ROOT / 'website/index.md', *(ROOT / 'website/guides').glob('*.md'),
                 *(ROOT / 'website/i18n/fr').glob('*.md')]
        for page in pages:
            text = page.read_text()
            self.assertNotRegex(text, r'agentic-development:(?:drive-cycle|[a-z]+-slice)')
            for name in re.findall(r'agentic-development:([a-z-]+)', text):
                self.assertIn(name, EXPECTED, str(page))
                self.assertTrue((ROOT / 'plugins/agentic-development/skills' / name / 'SKILL.md').is_file())
    def test_contributor_source_links_exist(self):
        for page in (ROOT / 'website/guides/contributing.md', ROOT / 'website/i18n/fr/contributing.md'):
            for link in re.findall(r'\]\(([^ )]+)\)', page.read_text()):
                if 'plugins/agentic-development/skills/' in link:
                    self.assertTrue((page.parent / link).resolve().is_file(), link)
