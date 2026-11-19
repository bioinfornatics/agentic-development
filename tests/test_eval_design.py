"""Source contract: every Skill eval case declares a gradeable target, preconditions and capabilities.

Static source evidence only: it checks eval-set structure, not agent behavior.
The skill-creator design-evals run is used only when that runtime is available.
"""
import json
import os
import shutil
import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXECUTIONS = {'explain', 'dry-run', 'execute', 'resume'}
CAPABILITIES = {'filesystem', 'agent_runner', 'browser', 'network', 'tools'}
CREATOR = Path(os.environ.get(
    'SKILL_CREATOR',
    Path.home() / '.cache/agent-plugins-patch-proof/repo/skills/skill-creator/scripts/skill-creator.mjs'))


def eval_sets():
    return sorted((ROOT / 'skills').glob('*/evals/evals.json'))


class EvalDesign(unittest.TestCase):
    def test_every_case_declares_target_preconditions_and_capabilities(self):
        self.assertTrue(eval_sets())
        for path in eval_sets():
            for case in json.loads(path.read_text())['evals']:
                with self.subTest(skill=path.parts[-3], eval_id=case.get('id')):
                    target = case.get('target')
                    self.assertIsInstance(target, dict)
                    self.assertTrue(target.get('kind'))
                    self.assertTrue(target.get('path') or target.get('paths') or target.get('output'))
                    self.assertIn(target.get('execution'), EXECUTIONS)
                    self.assertTrue(case.get('preconditions'))
                    self.assertEqual(set(case.get('capabilities', {})), CAPABILITIES)

    @unittest.skipUnless(CREATOR.is_file() and shutil.which('node'), 'skill-creator runtime unavailable')
    def test_design_evals_reports_no_error(self):
        for path in eval_sets():
            skill = path.parents[1]
            with self.subTest(skill=skill.name):
                run = subprocess.run(['node', str(CREATOR), 'design-evals', str(path), '--skill-path', str(skill),
                                      '--format', 'json'], capture_output=True, text=True, timeout=120)
                status = json.loads(run.stdout).get('status')
                self.assertEqual(status, 'success', run.stdout[-600:])


if __name__ == '__main__':
    unittest.main()
