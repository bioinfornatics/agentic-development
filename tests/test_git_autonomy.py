"""Static source evidence for the standing Git autonomy grant (agentic-devlopment-8ma.1).

Expected rules derive from the task acceptance criteria AC1-AC6, not from the
implementation text. These checks read Skill sources and docs only; they do not
execute Git, an agent workflow or a host integration.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')


def flat(text):
    return ' '.join(text.split())


def read(rel):
    return (ROOT / rel).read_text()


def section(text, heading):
    return text.split(heading, 1)[1].split('\n## ', 1)[0]


class AuthorizationPolicyGrant(unittest.TestCase):
    def setUp(self):
        blobs = [(ROOT / 'skills' / p / 'references/authorization-policy.md').read_bytes()
                 for p in PHASES]
        self.blobs = blobs
        self.text = blobs[0].decode()
        self.grant = flat(section(self.text, '## Standing Git autonomy grant'))

    def test_ac6_copies_identical_and_version_bumped(self):
        self.assertEqual(len(set(self.blobs)), 1)
        self.assertIn('Contract version: 1.1.0', self.text)
        self.assertIn('v1.1.0', self.text.splitlines()[0])

    def test_ac1_level_0_is_the_default(self):
        for rule in ('Level 0', 'default', 'propose', 'no push'):
            self.assertIn(rule, self.grant)

    def test_ac2_grant_fields_and_level_1_commit_preconditions(self):
        for field in ('level', 'repository', 'scope', 'expiry', 'source'):
            self.assertIn(field, self.grant)
        for rule in ('Level 1', 'one commit per closed task', 'Test evidence',
                     'Judge `accepted`', 'closure readback', 'exact owned paths/hunks',
                     'identity', 'task ID', 'commit report'):
            self.assertIn(rule, self.grant)

    def test_ac3_level_2_fast_forward_push_of_covered_branch_only(self):
        for rule in ('Level 2', 'fast-forward', 'non-protected', 'branch pattern'):
            self.assertIn(rule, self.grant)
        for stop in ('divergence', 'rejection', 'hook failure', 'no upstream', 'stop'):
            self.assertIn(stop, self.grant)

    def test_ac4_grant_never_covers_protected_or_publication_actions(self):
        never = self.grant.split('never covers', 1)[1]
        for excluded in ('`develop`', '`main`', 'default', 'release', 'force-push',
                         'tags', 'merges', 'publication', 'pull requests'):
            self.assertIn(excluded, never)

    def test_ac5_artifact_grants_are_historical_and_revocable(self):
        for rule in ('historical', 'restart prompt', 'revoke', 'narrow'):
            self.assertIn(rule, self.grant)
        self.assertNotRegex(self.grant, r'\bgh\b|\bglab\b')


class SkillsHonorGrant(unittest.TestCase):
    def test_beads_bridge_performs_commit_only_under_verified_grant(self):
        blobs = [(ROOT / 'skills' / p / 'references/beads-integration.md').read_bytes()
                 for p in PHASES]
        self.assertEqual(len(set(blobs)), 1)
        text = flat(section(blobs[0].decode(), '## Post-closure commit evaluation'))
        for rule in ('standing Git autonomy grant', 'Level 1', 'Level 2', 'Never auto-push'):
            self.assertIn(rule, text)

    def test_implement_commit_paragraph_references_grant(self):
        text = flat(read('skills/implement/SKILL.md'))
        self.assertIn('standing Git autonomy grant', text)
        self.assertIn('Never auto-push', text)

    def test_cycle_keeps_pre_judge_no_commit_and_finalizes_under_grant(self):
        text = flat(read('skills/cycle/SKILL.md'))
        self.assertIn('Do not auto-commit before accepted closure', text)
        self.assertIn('standing Git autonomy grant', text)


class NoContradictingPushWording(unittest.TestCase):
    PATTERN = re.compile(r'(No automatic push|Do not push automatically|no automatic push)([^.]*)\.')

    def test_absolute_no_push_wording_names_the_level_2_exception(self):
        paths = list((ROOT / 'skills').rglob('*.md')) + list((ROOT / 'docs').rglob('*.md'))
        paths += [ROOT / 'AGENTS.md', ROOT / 'README.md', ROOT / 'CONTRIBUTING.md']
        for path in paths:
            for match in self.PATTERN.finditer(flat(path.read_text())):
                with self.subTest(path=str(path.relative_to(ROOT))):
                    self.assertIn('Level 2', match.group(0))
                    self.assertIn('verified', match.group(0))

    def test_grant_scope_excludes_merges_and_worktrees(self):
        text = flat(read('skills/cycle/references/authorization-policy.md'))
        self.assertIn('only the commit and push actions defined below', text)
        self.assertIn('never covers', text)
        self.assertIn('worktree', text.split('never covers', 1)[1])


class FlowDocsAndInstructions(unittest.TestCase):
    def test_skill_flow_documents_grant_levels(self):
        doc = flat(read('docs/skill-flow.md'))
        for rule in ('standing Git autonomy grant', 'Level 1', 'Level 2',
                     'fast-forward', 'never `develop` or `main`'):
            self.assertIn(rule, doc)
        self.assertNotIn('nothing pushes automatically', doc)

    def test_agents_md_states_grant_boundary(self):
        text = flat(read('AGENTS.md'))
        self.assertIn('standing Git autonomy grant', text)
        self.assertRegex(text, r'never (covers|cover) `?develop`?')


if __name__ == '__main__':
    unittest.main()
