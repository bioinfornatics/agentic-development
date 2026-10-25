"""Source contracts only: no claim of actual harness deduplication."""
import hashlib
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
NAMES=('cycle','research','plan','implement','test','judge','iterate')
CONTRACTS=('requirements-baseline','authorization-policy','communication-contract','review-policy','judgment-rubric','common-output','candidate-identity','beads-integration','commit-report','session-report')

class ContextLoading(unittest.TestCase):
    def test_protocol_identical_and_recovers_unavailable_context(self):
        copies=[]
        for name in NAMES:
            text=(ROOT/'skills'/name/'SKILL.md').read_text()
            start=text.index('Apply contracts before their governed actions,')
            end=text.index('\n\n', start)
            protocol=text[start:end]
            copies.append(protocol)
            for rule in ('absent, incomplete or outdated', 'active context', 'another Skill', 'same ID/version', 'different content', 'loaded marker', 'compaction', 'worker', 'applicability', 'never renews'):
                self.assertIn(rule, protocol, name)
            self.assertIn('not a runtime cache',protocol,name)
        self.assertEqual(len(set(copies)),1)

    def test_contracts_have_identity_and_identical_copies(self):
        for contract in CONTRACTS:
            copies=[]
            consumers=('cycle','plan','judge') if contract=='judgment-rubric' else NAMES
            for name in consumers:
                p=ROOT/'skills'/name/'references'/(contract+'.md')
                text=p.read_text()
                self.assertIn('Contract ID: agentic-development/'+contract,text)
                self.assertRegex(text,r'Contract version: [0-9]+\.[0-9]+\.[0-9]+')
                copies.append(hashlib.sha256(p.read_bytes()).hexdigest())
            self.assertEqual(len(set(copies)),1,contract)

    def test_local_conditions_apply_instead_of_unconditional_read(self):
        for name in NAMES:
            text=(ROOT/'skills'/name/'SKILL.md').read_text()
            for contract in ('requirements-baseline','authorization-policy','communication-contract','candidate-identity','review-policy'):
                self.assertIn('references/'+contract+'.md',text,name)
            self.assertRegex(text,r'(?i)apply\s+\[',name)
            self.assertNotIn('Read [the requirements baseline]',text,name)
            self.assertNotIn('Read [the authorization policy]',text,name)

if __name__=='__main__': unittest.main()
