"""Static source evidence for guided Beads persistence (epic agentic-devlopment-00q).

Expected rules derive from the acceptance criteria of agentic-devlopment-00q.1
(persistence checkpoints and Beads sync grant), not from the implementation
text. These checks read Skill sources and docs only; they do not execute bd,
Git, Dolt, an agent workflow or a host integration.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('cycle', 'research', 'plan', 'implement', 'test', 'judge', 'iterate')


def flat(text):
    return ' '.join(text.split())


def read(rel):
    return (ROOT / rel).read_text()


def section(text, heading):
    return text.split(heading, 1)[1].split('\n## ', 1)[0]


def copies(name):
    blobs = [(ROOT / 'skills' / p / 'references' / name).read_bytes() for p in PHASES]
    return blobs, blobs[0].decode()


class PersistenceCheckpoints(unittest.TestCase):
    def setUp(self):
        self.blobs, self.text = copies('beads-integration.md')
        self.section = flat(section(self.text, '## Persistence checkpoints'))

    def test_ac6_copies_identical_and_version_bumped(self):
        self.assertEqual(len(set(self.blobs)), 1)
        self.assertIn('Contract version: 1.5.0', self.text)
        self.assertIn('v1.5.0', self.text.splitlines()[0])

    def test_ac1_checkpoints_are_named(self):
        for moment in ('confirmed task or epic closure', 'handoff', 'session end'):
            self.assertIn(moment, self.section)

    def test_ac2_jsonl_snapshot_only_when_tracked_and_committed_alone(self):
        for rule in ('git ls-files .beads/issues.jsonl', 'bd export -o .beads/issues.jsonl',
                     'memories', 'private data', 'chore(beads): snapshot (<IDs>)',
                     'alone', 'never directly on `develop`', '`main`'):
            self.assertIn(rule, self.section)
        self.assertIn('not tracked', self.section)
        self.assertIn('never edit or import', self.section.lower())

    def test_ac3_dolt_push_only_with_remote_and_never_forced(self):
        for rule in ('bd dolt remote list', 'bd dolt push', 'epic closure', 'local-only'):
            self.assertIn(rule, self.section)
        self.assertIn('Never `--force`', self.section)
        for stop in ('rejection', 'divergence', 'stop'):
            self.assertIn(stop, self.section)

    def test_ac4_actions_need_the_beads_sync_grant_or_are_proposed(self):
        self.assertIn('Beads sync grant', self.section)
        self.assertIn('propose', self.section)

    def test_ac5_each_action_reports_its_outcome(self):
        self.assertIn('perform / propose / skip / blocked', self.section)

    def test_post_closure_section_points_to_checkpoints(self):
        post = flat(section(self.text, '## Post-closure commit evaluation'))
        self.assertIn('Persistence checkpoints', post)
        self.assertIn('Never auto-push', post)


class BeadsSyncGrant(unittest.TestCase):
    def setUp(self):
        self.blobs, self.text = copies('authorization-policy.md')
        self.grant = flat(section(self.text, '## Beads sync grant'))

    def test_ac6_copies_identical_and_version_bumped(self):
        self.assertEqual(len(set(self.blobs)), 1)
        self.assertIn('Contract version: 1.2.0', self.text)
        self.assertIn('v1.2.0', self.text.splitlines()[0])

    def test_ac4_grant_fields_and_separation_from_git_levels(self):
        for field in ('repository', 'scope', 'expiry', 'source'):
            self.assertIn(field, self.grant)
        self.assertIn('separate from', self.grant)
        self.assertIn('Level 1', self.grant)
        self.assertIn('Level 2', self.grant)
        for action in ('bd export', 'chore(beads)', 'bd dolt push'):
            self.assertIn(action, self.grant)

    def test_ac4_grant_never_covers_force_or_protected_branches(self):
        never = self.grant.split('never covers', 1)[1]
        for excluded in ('`develop`', '`main`', 'force', 'remote', 'import', 'initialization'):
            self.assertIn(excluded, never)

    def test_ac4_without_grant_actions_are_proposed(self):
        self.assertIn('propose', self.grant)
        self.assertIn('historical', self.grant)

    def test_git_grant_still_excludes_dolt_sync(self):
        git = flat(section(self.text, '## Standing Git autonomy grant'))
        self.assertIn('Dolt sync', git.split('never covers', 1)[1])


class CommunicationAndDocs(unittest.TestCase):
    def test_communication_contract_names_the_grant_exception(self):
        blobs, text = copies('communication-contract.md')
        self.assertEqual(len(set(blobs)), 1)
        self.assertNotIn('No automatic tracker installation or Dolt sync is authorized.', flat(text))
        self.assertIn('Beads sync grant', flat(text))

    def test_skill_flow_documents_persistence_gate(self):
        doc = flat(read('docs/skill-flow.md'))
        for rule in ('Beads sync grant', '`bd export -o .beads/issues.jsonl`',
                     '`bd dolt push`', 'chore(beads)', 'never `--force`'):
            self.assertIn(rule, doc)

    def test_integrations_guide_explains_when_to_persist(self):
        doc = flat(read('docs/integrations.md'))
        for rule in ('Beads sync grant', 'bd export', 'bd dolt push', 'chore(beads)'):
            self.assertIn(rule, doc)

    def test_agents_md_names_the_grant(self):
        self.assertIn('Beads sync grant', flat(read('AGENTS.md')))


BD_LINK = 'https://github.com/gastownhall/beads'


class BeadsAbsentNotice(unittest.TestCase):
    """agentic-devlopment-00q.2 AC1-AC4."""

    def setUp(self):
        self.cycle = flat(read('skills/cycle/SKILL.md'))

    def test_ac1_cycle_notices_absence_once_per_session_with_link(self):
        self.assertIn(BD_LINK, self.cycle)
        for rule in ('no Beads workspace', 'once per session',
                     'works better with Beads'):
            self.assertIn(rule, self.cycle)

    def test_ac2_notice_never_installs_and_does_not_block(self):
        notice = self.cycle.split('works better with Beads', 1)[1][:600]
        for rule in ('never install', 'initialize', 'does not block',
                     'another tracking approach'):
            self.assertIn(rule, notice)

    def test_ac3_no_notice_when_beads_is_present(self):
        self.assertIn('no notice when Beads is present', self.cycle)

    def test_ac4_readme_and_guide_carry_the_same_link(self):
        for rel in ('README.md', 'docs/integrations.md'):
            with self.subTest(path=rel):
                self.assertIn(BD_LINK, read(rel))

    def test_ac1_workspace_without_bd_stays_a_blocker(self):
        # Judge F1: a Beads workspace with bd missing is missing task access, not "no Beads".
        self.assertIn('no Beads workspace (Beads not adopted)', self.cycle)
        self.assertIn('report missing task access as a blocker', self.cycle)
        self.assertNotIn('If `bd` is not installed or the repository has no Beads workspace', self.cycle)


class CorrectionFindings(unittest.TestCase):
    """Judge findings F2-F6 on agentic-devlopment-00q.1."""

    def setUp(self):
        _, text = copies('beads-integration.md')
        self.section = flat(section(text, '## Persistence checkpoints'))

    def test_f2_current_per_action_authority_is_also_valid(self):
        self.assertIn('current per-action authority', self.section)
        _, comm = copies('communication-contract.md')
        self.assertIn('current scoped authority or a verified Beads sync grant', flat(comm))

    def test_f3_failed_export_or_commit_stops_without_bypass(self):
        self.assertIn('hook failure', self.section)
        self.assertIn('`--no-verify`', self.section)

    def test_f5_guide_limits_dolt_push_timing(self):
        doc = flat(read('docs/integrations.md'))
        self.assertIn('run `bd dolt push` at epic closure, handoff or session end', doc)

    def test_f6_protected_current_branch_reports_blocked(self):
        self.assertIn('on such a branch report blocked', self.section)

    def test_f4_agents_md_limits_grants_to_their_listed_actions(self):
        self.assertIn("only the grants' listed actions", flat(read('AGENTS.md')))


if __name__ == '__main__':
    unittest.main()
