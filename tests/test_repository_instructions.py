"""Static repository onboarding contracts; not agent effectiveness evidence."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RepositoryInstructions(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / 'AGENTS.md').read_text()

    def test_product_and_scannable_map(self):
        self.assertLessEqual(len(self.text.splitlines()), 120)
        for item in ['## Product', '## Repository map', '## Branch and distribution contract',
                     '## Task truth and restart', '## Permissions and preservation', '## Verification']:
            self.assertIn(item, self.text)
        self.assertIn('scope drift', self.text)
        self.assertIn('not an enforcement', self.text)
        self.assertIn('tools/production.py', self.text)

    def test_generated_main_is_not_a_source_merge(self):
        for item in ['Never merge develop into main', 'previous main as sole parent',
                     'generated-only PR', 'squash', 'Never force-push',
                     'exact source SHA', 'README.md', 'release_ready=false']:
            self.assertIn(item, self.text)
        self.assertIn('feature/*', self.text)

    def test_beads_and_permissions_remain_mandatory(self):
        for item in ['Beads is mandatory', 'claim', 'readback', 'blocker',
                     'task ID alone', 'Do not initialize', 'Dolt sync',
                     'current scoped authority', 'No self-approval', 'three authorized attempts',
                     'Given/When/Then', 'NFR', 'English', 'Entire', 'seven-field']:
            self.assertIn(item, self.text)
        self.assertNotIn('currently 0.5.0', self.text)
        self.assertNotIn('See .beads/README.md', self.text)

    def test_direct_policy_links_exist(self):
        required = ['CONTRIBUTING.md', 'skills/cycle/SKILL.md',
                    'skills/cycle/references/authorization-policy.md',
                    'skills/cycle/references/beads-integration.md',
                    'skills/cycle/references/candidate-identity.md',
                    'skills/cycle/references/review-policy.md',
                    'skills/cycle/references/common-output.md']
        links = re.findall(r'\]\(([^)]+)\)', self.text)
        for target in required:
            self.assertIn(target, links)
        for target in links:
            if '://' not in target:
                self.assertTrue((ROOT / target.split('#')[0]).exists(), target)

    def test_canonical_instruction_symlink_is_preserved(self):
        link = ROOT / 'CLAUDE.md'
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.readlink(), Path('AGENTS.md'))

    def test_stale_migration_claim_is_removed(self):
        text = (ROOT / 'CONTRIBUTING.md').read_text()
        self.assertNotIn('not yet', text)
        self.assertIn('main contains a generated installation projection', text)
        self.assertIn('No license grant', text)
