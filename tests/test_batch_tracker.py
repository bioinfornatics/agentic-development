"""Static source evidence for batch tracker mechanics in the Beads bridge.

These checks read the seven phase copies of references/beads-integration.md.
They do not execute bd, an agent workflow or a host integration.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')
PREVIOUS_VERSION = (1, 2, 0)
EXPECTED_VERSION = '1.3.0'


def copies():
    return [(ROOT / 'skills' / name / 'references/beads-integration.md') for name in NAMES]


class BatchTrackerBridge(unittest.TestCase):
    def setUp(self):
        paths = copies()
        self.blobs = [p.read_bytes() for p in paths]
        self.text = self.blobs[0].decode()
        self.flat = ' '.join(self.text.split())

    def test_seven_copies_are_byte_identical(self):
        self.assertEqual(len(set(self.blobs)), 1)

    def test_contract_version_bumped_minor(self):
        match = re.search(r'Contract version: ([0-9]+)\.([0-9]+)\.([0-9]+)', self.text)
        self.assertIsNotNone(match)
        version = tuple(int(x) for x in match.groups())
        self.assertGreater(version, PREVIOUS_VERSION)
        self.assertIn('Contract version: ' + EXPECTED_VERSION, self.text)
        title = self.text.splitlines()[0]
        self.assertNotIn('1.2.0', title)
        if re.search(r'v[0-9]+\.[0-9]+\.[0-9]+', title):
            self.assertIn('v' + EXPECTED_VERSION, title)

    def test_fr5_closure_requires_test_evidence_judge_accepted_and_authority(self):
        for rule in ('Test evidence', 'Judge `accepted`', 'exact candidate',
                     'current closure authority', 'stays open',
                     'named blocker', 'restart action'):
            self.assertIn(rule, self.flat)

    def test_fr8_discovered_work_is_open_follow_up_outside_batch(self):
        self.assertIn('bd create ... --deps discovered-from:<id>', self.flat)
        for rule in ('open follow-up', 'never claim', 'active batch'):
            self.assertIn(rule, self.flat)

    def test_d4_blocked_task_is_released_and_batch_continues(self):
        self.assertIn('bd update <id> --status open --assignee ""', self.flat)
        for rule in ('native dependency', 'named blocker', 'restart action',
                     'other batch tasks continue'):
            self.assertIn(rule, self.flat)

    def test_batch_wip_and_ready_queries(self):
        self.assertIn('bd list --status in_progress --parent <epic>', self.flat)
        self.assertIn('bd ready --parent <epic>', self.flat)

    def test_existing_bridge_identity_and_fields_kept(self):
        for rule in ('Contract ID: agentic-development/beads-integration',
                     'acceptance field', 'description', 'notes', 'readback'):
            self.assertIn(rule, self.text)


if __name__ == '__main__':
    unittest.main()
