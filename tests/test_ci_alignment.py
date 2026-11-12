"""CI source contracts plus real shell failure propagation; not hosted-run proof."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CIAlignment(unittest.TestCase):
    def test_reusable_exact_source_and_failure_logs(self):
        text = (ROOT / '.github/workflows/source-checks.yml').read_text()
        for token in ('workflow_call:', 'source_sha:',
                      'inputs.source_sha || github.event.pull_request.head.sha || github.sha',
                      'set -euo pipefail', 'tee "$RUNNER_TEMP/ci-logs/',
                      'if: always()', 'actions/upload-artifact@',
                      'retention-days: 14'):
            self.assertIn(token, text)
        # Exercise the actual declared shell policy, not a mocked tool result.
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(['bash', '-c',
                f'set -euo pipefail\n(printf "diagnostic\\n"; exit 17) | tee "{tmp}/log"'],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 17)
            self.assertEqual(Path(tmp, 'log').read_text(), 'diagnostic\n')

