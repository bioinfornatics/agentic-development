"""Source contracts and executable fixture readiness, not a Skill evaluation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / 'skills/iterate/evals/behavior-v2-inputs'
SUITE = ROOT / 'skills/iterate/evals/behavior-v2.json'
spec = importlib.util.spec_from_file_location('iterate_oracle', INPUTS / 'oracle.py')
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class IterateBehaviorV2(unittest.TestCase):
    def test_neutral_execute_intents_and_closed_subset(self):
        suite = json.loads(SUITE.read_text())
        self.assertEqual([c['id'] for c in suite['evals']], [1, 2, 3])
        allowed = {'id', 'name', 'subject', 'language', 'target', 'coverage_tags',
                   'prompt', 'assertions', 'expected_output', 'files'}
        for case in suite['evals']:
            self.assertLessEqual(set(case), allowed)
            self.assertTrue(case['assertions'])
            for leak in ('evals/', 'purpose-inputs', 'Implement', 'task_state.py', 'PASS'):
                self.assertNotIn(leak, case['prompt'])
            for path in case['files']:
                declared = ROOT / 'skills/iterate' / path
                self.assertTrue(declared.is_dir())
                self.assertTrue(declared.resolve().is_relative_to(INPUTS))
                self.assertFalse(any(p.is_symlink() for p in declared.rglob('*')))
        self.assertIn('fix Stop', suite['evals'][0]['prompt'])
        self.assertIn('verify', suite['evals'][1]['prompt'])
        self.assertIn('existing task authority', suite['evals'][2]['prompt'])
        correction = ' '.join(suite['evals'][0]['assertions'])
        self.assertIn('before any production edit', correction)
        self.assertIn('BEFORE', (ROOT / 'skills/iterate/SKILL.md').read_text())
        self.assertIn('before corrective execution or Implement dispatch', correction)
        self.assertIn('Baseline', correction)
        self.assertIn('inconclusive', correction)

    def test_independent_initial_bytes_and_public_red_green_readiness(self):
        initial = json.loads((INPUTS / 'initial-state.json').read_text())
        for case, expected in [('correction', 1), ('proof-only', 0), ('exhausted', 1)]:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as folder:
                project = Path(folder) / 'project'
                shutil.copytree(INPUTS / case, project)
                for file, digest in initial[case]['files'].items():
                    self.assertEqual(hashlib.sha256((project / file).read_bytes()).hexdigest(), digest)
                result = subprocess.run([sys.executable, '-B', 'test_controller.py'], cwd=project,
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, expected, result.stderr)
                if expected:
                    self.assertIn('0 != 1', result.stderr)
                    self.assertIn('test_active_stop_once', result.stderr)
                if case == 'correction':
                    state = subprocess.run([sys.executable, '-B', 'task_state.py', 'start'], cwd=project,
                                           capture_output=True, text=True, timeout=10)
                    self.assertEqual(state.returncode, 0)
                    self.assertEqual(json.loads((project / 'task.json').read_text())['attempts_started'], 2)
                    # Readiness probe only: the future agent has not executed this repair.
                    source = (project / 'controller.py').read_text()
                    (project / 'controller.py').write_text(source.replace(
                        '        if self.active:\n', '        if self.active:\n            self.transport.cancel()\n'))
                    green = subprocess.run([sys.executable, '-B', 'test_controller.py'], cwd=project,
                                           capture_output=True, text=True, timeout=10)
                    self.assertEqual(green.returncode, 0, green.stderr)
                check = oracle.inspect(case, project)
                self.assertEqual(check['final_state'], 'pass', check)
                self.assertEqual(check['action_order_and_restraint'], 'inconclusive')
                if case != 'exhausted':
                    self.assertEqual(check['behavior']['completion'], {
                        'passed': sorted('independent_public_tests.Cancellation.' + name for name in (
                            'test_active_stop_once', 'test_idle_stop', 'test_completed_stop')),
                        'run': 3, 'failures': 0, 'errors': 0, 'skipped': 0, 'successful': True})

    def test_exhausted_and_proof_state_cannot_start_or_reset(self):
        for case in ('proof-only', 'exhausted'):
            with tempfile.TemporaryDirectory() as folder:
                project = Path(folder) / 'project'
                shutil.copytree(INPUTS / case, project)
                before = (project / 'task.json').read_bytes()
                result = subprocess.run([sys.executable, '-B', 'task_state.py', 'start'], cwd=project,
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 2)
                self.assertEqual((project / 'task.json').read_bytes(), before)

    def test_oracle_reports_missing_or_symlink_controller_without_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / 'project'
            shutil.copytree(INPUTS / 'proof-only', project)
            (project / 'controller.py').unlink()
            missing = oracle.inspect('proof-only', project)
            self.assertEqual(missing['final_state'], 'fail')
            self.assertIsNone(missing['behavior'])
            (project / 'controller.py').symlink_to(INPUTS / 'proof-only/controller.py')
            linked = oracle.inspect('proof-only', project)
            self.assertEqual(linked['final_state'], 'fail')
            self.assertIsNone(linked['behavior'])

    def test_oracle_rejects_import_exit_without_public_test_completion(self):
        # F1: successful process termination is not successful test execution.
        for source in ('raise SystemExit(0)\n', 'import os; os._exit(0)\n',
                       'print("OK")\nraise SystemExit(0)\n'):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as folder:
                project = Path(folder) / 'project'
                shutil.copytree(INPUTS / 'correction', project)
                task = json.loads((project / 'task.json').read_text())
                task['attempts_started'] = 2
                (project / 'task.json').write_text(json.dumps(task))
                (project / 'controller.py').write_text(source)
                result = oracle.inspect('correction', project)
                self.assertEqual(result['final_state'], 'fail', result)
                self.assertIn('independent public behavior check failed', result['failures'])
                self.assertEqual(result['action_order_and_restraint'], 'inconclusive')

    def test_oracle_detects_preservation_and_false_green(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / 'project'
            shutil.copytree(INPUTS / 'correction', project)
            (project / 'test_controller.py').write_text('print("PASS")\n')
            (project / 'view.py').write_text('changed\n')
            result = oracle.inspect('correction', project)
            self.assertEqual(result['final_state'], 'fail')
            self.assertIn('preserved bytes changed: view.py', result['failures'])
            self.assertIn('preserved bytes changed: test_controller.py', result['failures'])
            self.assertIn('independent public behavior check failed', result['failures'])


if __name__ == '__main__':
    unittest.main()
