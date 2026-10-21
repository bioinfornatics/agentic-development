import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('projection', ROOT / 'scripts/project-phase-core.py')
projection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(projection)

class PhaseCoreConvergenceTest(unittest.TestCase):
    def test_operational_projection(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'core'
            receipt = projection.project(target)
            self.assertEqual(len(receipt['files']), 49)
            self.assertEqual(len(list(target.glob('skills/*/SKILL.md'))), 7)
            self.assertFalse(any('evals' in p.parts for p in target.rglob('*')))
            self.assertFalse((target / '.beads').exists())
            for entry in receipt['files']:
                self.assertEqual((target / entry['path']).read_bytes(),
                                 (ROOT / 'plugins/agentic-development' / entry['path']).read_bytes())
            with self.assertRaises(ValueError):
                projection.project(target)

    def test_inventory_covers_base(self):
        inventory = json.loads((ROOT / 'docs/convergence/inventory.json').read_text())
        paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only',
                                         inventory['historicalBase']], cwd=ROOT, text=True).splitlines()
        self.assertEqual(set(paths), {entry['path'] for entry in inventory['entries']})
        for entry in inventory['entries']:
            if entry['action'] == 'remove':
                self.assertFalse((ROOT / entry['path']).exists())

    def test_recipes_use_active_database(self):
        for recipe in (ROOT / '.goose/recipes').glob('*.yaml'):
            text = recipe.read_text()
            self.assertNotIn('.beads/issues.jsonl', text)
            self.assertIn('bd list --json', text)

    def test_manifest_contains_core(self):
        data = json.loads((ROOT / 'harness/source-manifest.json').read_text())
        core = next(x for x in data['components'] if x['id'] == 'plugin:agentic-development')
        self.assertEqual(core['packagePolicy'], 'operational-skill-tree')
        self.assertEqual(core['sourcePath'], 'plugins/agentic-development')

if __name__ == '__main__':
    unittest.main()
