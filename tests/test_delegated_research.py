"""Delegation and durable pointers source contracts, not host execution proof."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class DelegatedResearch(unittest.TestCase):
    def test_deeper_modes_require_delegation_without_silent_fallback(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        self.assertIn('Delegate deeper selected investigations', text)
        self.assertIn('The coordinator may directly verify', text)
        self.assertIn('references/delegated-investigation.md', text)
        self.assertIn('explicit permission for direct investigation', text)

    def test_worker_contract_retains_proof_and_task_reading_pointers(self):
        p = ROOT / 'skills/research/references/delegated-investigation.md'
        self.assertTrue(p.is_file())
        text = p.read_text()
        for required in ('reading_references:', 'source_identity:', 'findings:', 'evidence:', 'unknowns:', 'execution:', 'read_order:', 'reason:', 'coordinator', 'partial', 'Do not mutate Beads', 'not an independent acceptance review'):
            self.assertIn(required, text)

    def test_offline_capture_retains_provenance_and_permission_boundaries(self):
        p = ROOT / 'skills/research/references/knowledge-pointers.md'
        self.assertTrue(p.is_file())
        text = p.read_text()
        for required in ('original_url', 'publication_date', 'access_date', 'sha256', 'derived summary', 'copyright', 'read back', 'offline', 'stale', 'not task truth', 'no automatic refresh'):
            self.assertIn(required, text)
        for phase in ('research', 'plan'):
            self.assertIn('reading references', (ROOT / 'skills' / phase / 'references/requirements-output.md').read_text())

class OrderedChecklist(unittest.TestCase):
    def test_dispatch_checks_precede_final_output_read(self):
        text = (ROOT / 'skills/research/SKILL.md').read_text()
        block = text.split('## Workflow', 1)[1]
        import re
        checks = re.findall(r'^(\d+)\. \[ \] (.*)$', block, re.M)
        self.assertEqual([int(number) for number, _ in checks], list(range(1, 7)))
        delivery = block.split('5. [ ]', 1)[1].split('6. [ ]', 1)[0]
        self.assertIn('references/common-output.md', delivery)
        self.assertLess(block.index('completion status'), block.index('references/common-output.md'))
        self.assertLess(block.index('find_files'), block.index('analyze_code'))
        for term in ('worker invocation', 'completion status', 'in parallel', 'state_of_the_art', 'waiver'):
            self.assertIn(term, block)
        self.assertIn('   - [ ]', block)

if __name__ == '__main__':
    unittest.main()
