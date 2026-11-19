"""Static source evidence plus a CLI fixture for FR-1 (agentic-devlopment-31k).

FR-1: given an authorized commit after focused checks, when Test compares the
candidate, the Skills state an exact rebind procedure (what is compared, what is
excluded) so the outcome is deterministic. The source checks read instruction
text only; the fixture runs the bundled capture CLI and Git in a temporary
repository. Neither executes an agent workflow or proves agent compliance.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')
CLI = ROOT / 'skills/implement/scripts/candidate_identity.py'
PREVIOUS_VERSION = (1, 3, 0)


def flat(path):
    return ' '.join(path.read_text().split())


def rebind_projection(manifest):
    """Independent oracle for the documented rule: drop candidate_id and git."""
    return {k: v for k, v in manifest.items() if k not in ('candidate_id', 'git')}


class CommitRebindSource(unittest.TestCase):
    def setUp(self):
        self.paths = [ROOT / 'skills' / n / 'references/candidate-identity.md' for n in NAMES]
        self.text = flat(self.paths[0])

    def test_seven_candidate_identity_copies_are_byte_identical(self):
        self.assertEqual(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in self.paths}), 1)

    def test_contract_version_bumped_minor_with_title(self):
        raw = self.paths[0].read_text()
        major, minor, patch = PREVIOUS_VERSION
        version = f'{major}.{minor + 1}.0'
        self.assertIn('Contract version: ' + version, raw)
        self.assertIn('# Candidate identity v' + version, raw)

    def test_fr1_rebind_states_compared_and_excluded_fields(self):
        for rule in ('## C. Rebind evidence across a commit',
                     'capture again after the commit with the same root and scope',
                     'excluding only candidate_id and git (HEAD and index)',
                     'Otherwise rerun the affected checks',
                     'git diff --quiet HEAD --',
                     'consumes Git state'):
            self.assertIn(rule, self.text)

    def test_fr1_undefined_rebind_wording_removed(self):
        implement = flat(ROOT / 'skills/implement/SKILL.md')
        self.assertNotIn('rebind documented equality', implement)
        self.assertNotIn('documented content/environment equality', self.text)

    def test_fr1_implement_freezes_post_commit_candidate(self):
        implement = flat(ROOT / 'skills/implement/SKILL.md')
        step5 = implement.split('5. [ ]', 1)[1].split('6. [ ]', 1)[0]
        for rule in ('After a performed commit, capture the handoff candidate again',
                     'freeze its new candidate_id',
                     'commit rebind in candidate identity'):
            self.assertIn(rule, step5)


class CommitRebindFixture(unittest.TestCase):
    """Commit of identical content: candidate_id changes, rebind projection holds."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.root = self.base / 'root'
        (self.root / 'src').mkdir(parents=True)
        (self.root / 'src/a.txt').write_text('base\n')
        self.scope = self.base / 'scope.json'
        self.scope.write_text(json.dumps({'include': ['src'], 'exclude': [],
            'environment': {'python': 'fixture'}, 'criteria': 'FR-1-fixture'}))
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('add', '.')
        self.git('commit', '-qm', 'baseline')

    def git(self, *args, check=True):
        return subprocess.run(['git', '-C', str(self.root), *args], capture_output=True,
                              text=True, check=check)

    def capture(self, name):
        out = subprocess.run([sys.executable, '-B', str(CLI), 'capture', '--root',
                              str(self.root), '--scope', str(self.scope)],
                             capture_output=True, text=True, check=True).stdout
        (self.base / name).write_text(out)
        return json.loads(out)

    def compare(self):
        return subprocess.run([sys.executable, '-B', str(CLI), 'compare',
                               str(self.base / 'before.json'), str(self.base / 'after.json')],
                              capture_output=True, text=True).returncode

    def test_identical_content_commit_rebinds_but_compare_differs(self):
        (self.root / 'src/a.txt').write_text('changed\n')
        before = self.capture('before.json')       # unstaged change, as after checks
        self.git('add', 'src/a.txt')
        staged_tree = self.git('write-tree').stdout.strip()
        self.git('commit', '-qm', 'change')
        after = self.capture('after.json')
        self.assertEqual(self.compare(), 1)        # HEAD/index moved: DIFFERENT
        self.assertEqual(rebind_projection(before), rebind_projection(after))
        self.assertEqual(self.git('rev-parse', 'HEAD^{tree}').stdout.strip(), staged_tree)
        self.assertEqual(self.git('diff', '--quiet', 'HEAD', '--', 'src', check=False).returncode, 0)
        self.assertEqual(self.documented_rebind(), 0)

    def documented_rebind(self):
        """Run the documented section C command verbatim against the fixture manifests."""
        text = (ROOT / 'skills/implement/references/candidate-identity.md').read_text()
        section = text.split('## C. Rebind evidence across a commit', 1)[1]
        command = section.split('~~~sh\n', 1)[1].split('~~~', 1)[0]
        return subprocess.run(['bash', '-c', command], capture_output=True, text=True,
                              env={**os.environ, 'EVIDENCE_DIR': str(self.base)}).returncode

    def test_content_change_after_commit_breaks_rebind(self):
        before = self.capture('before.json')
        (self.root / 'src/a.txt').write_text('edited later\n')
        after = self.capture('after.json')
        self.assertNotEqual(rebind_projection(before), rebind_projection(after))
        self.assertEqual(self.documented_rebind(), 1)
        self.assertEqual(self.git('diff', '--quiet', 'HEAD', '--', 'src', check=False).returncode, 1)


if __name__ == '__main__':
    unittest.main()
