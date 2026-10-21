import importlib.util
from unittest.mock import patch
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GATE = ROOT / '.agents/plugins/loop-gate/scripts/gate-reviewed.sh'
GUARD = ROOT / '.agents/plugins/prevent-catastrophe/scripts/guard-shell.sh'

class HookConvergenceTest(unittest.TestCase):
    def invoke(self, handler, value, env=None):
        raw = json.dumps(value) if isinstance(value, dict) else value
        return subprocess.run(['/bin/sh', str(handler)], input=raw, text=True,
                              capture_output=True, env=env, timeout=15)

    def blocked(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['decision'], 'block')

    def test_guard_allow_deny_and_malformed(self):
        self.assertEqual(self.invoke(GUARD, {'tool_input': {'command': 'printf ok'}}).stdout, '')
        for text in ['sudo true', 'rm -rf /', 'rm -rf '+chr(39)+'/'+chr(39), 'git -C /tmp reset --hard', 'git clean --force -d', 'git reset --hard', 'wipefs /dev/dummy']:
            self.blocked(self.invoke(GUARD, {'tool_input': {'command': text}}))
        self.blocked(self.invoke(GUARD, '{'))

    def test_gate_nonmatching_allow(self):
        for command in ['printf ok', 'bd show closed', 'bd update one --status open --notes closed', 'bd update one --notes closed', 'bd update one --notes --status=closed']:
            self.assertEqual(self.invoke(GATE, {'tool_input': {'command': command}}).stdout, '', command)

    def test_gate_missing_cwd_and_malformed(self):
        self.blocked(self.invoke(GATE, {'tool_input': {'command': 'bd close dummy'}}))
        self.blocked(self.invoke(GATE, '{'))

    def test_gate_complex_closure_denied(self):
        for text in ['bd close one && bd close two', 'env bd close one', 'bd close one; true', 'bd update one --status=closed; true', 'bd update one --status closed; true', 'bd update one -sclosed', 'bd update one -s closed', 'bd --db /tmp/fixture close one', 'bd show one; bd close one', 'bd show one; bd update one --status=closed', 'bd update one --notes ";" --status=closed', 'bd update one --notes "|" --status closed', 'bd show one'+chr(10)+'bd close one']:
            self.blocked(self.invoke(GATE, {'tool_input': {'command': text}}))

    def test_receipt_consistency_not_authorization(self):
        spec=importlib.util.spec_from_file_location('receipt_consistency',GATE.with_suffix('.py'))
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        def consistency(payload, env):
            try:
                with patch.dict(os.environ,env,clear=True):
                    for issue in module.closure_ids(payload['tool_input']['command']):
                        if 'working_dir' not in payload:raise ValueError('no cwd')
                        receipt=json.loads(env['FIXTURE_RECEIPT']) if issue=='one' else None
                        module.check_receipt(Path(payload['working_dir']),issue,receipt)
                return subprocess.CompletedProcess([],0,'','')
            except Exception:
                return subprocess.CompletedProcess([],0,json.dumps({'decision':'block'}),'')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); repo = root / 'repo'; repo.mkdir()
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (repo / 'code.txt').write_text('candidate')
            subprocess.run(['git', 'add', 'code.txt'], cwd=repo, check=True)
            subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                            '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'fixture'], cwd=repo, check=True)
            (repo / 'evidence.txt').write_text('fixture checks pass')
            manifest = {'files': [{'path': 'code.txt', 'mode': oct((repo/'code.txt').stat().st_mode & 0o777),
                                   'sha256': hashlib.sha256((repo/'code.txt').read_bytes()).hexdigest()}],
                        'output_only': ['manifest.json', 'evidence.txt']}
            (repo / 'manifest.json').write_text(json.dumps(manifest))
            receipt = {'schema': 'loop-acceptance-v1', 'issue_id': 'one', 'verdict': 'accepted',
                       'builder_session': 'builder-fixture', 'verifier_session': 'verifier-fixture',
                       'independence': {'builder_participation': False, 'inherited_builder_conclusions': False,
                                        'raw_evidence_access': True, 'candidate_write_access': False},
                       'head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
                       'index_sha256': hashlib.sha256(subprocess.check_output(['git','ls-files','--stage'],cwd=repo)).hexdigest(),
                       'manifest_path': 'manifest.json', 'manifest_sha256': hashlib.sha256((repo/'manifest.json').read_bytes()).hexdigest(),
                       'criteria': [{'id':'AC-1','status':'proven'}],
                       'evidence': [{'path':'evidence.txt','sha256':hashlib.sha256((repo/'evidence.txt').read_bytes()).hexdigest()}]}
            bin_dir=root/'bin';bin_dir.mkdir(); bd=bin_dir/'bd'
            bd.write_text('#!/usr/bin/env python3'+chr(10)+'import json,os,sys'+chr(10)+
                          'r=json.loads(os.environ["FIXTURE_RECEIPT"]); print(json.dumps([{"id":sys.argv[2],"labels":["env:reviewed"],"metadata":{"loop_acceptance":r if sys.argv[2]=="one" else None}}]))'+chr(10))
            bd.chmod(0o755)
            env=dict(os.environ,PATH=str(bin_dir)+os.pathsep+os.environ['PATH'],FIXTURE_RECEIPT=json.dumps(receipt))
            registry = root / 'trust.json'
            digest = hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            policy={'receipt_sha256':digest,'repo_root':str(repo),'required_criteria':['AC-1'], 'output_only':['manifest.json','evidence.txt']}
            registry.write_text(json.dumps({'schema':'loop-trusted-acceptance-v1','receipts':{'one':policy}}))
            registry.chmod(0o600)
            env['GOOSE_LOOP_ACCEPTANCE_TRUST_FILE']=str(registry)
            payload={'tool_input':{'command':'bd close one'},'working_dir':str(repo)}
            self.assertEqual(consistency(payload,env).stdout,'')
            no_trust=dict(env);no_trust.pop('GOOSE_LOOP_ACCEPTANCE_TRUST_FILE')
            self.blocked(consistency(payload,no_trust))
            forged=dict(receipt,verifier_session='invented')
            self.blocked(consistency(payload,dict(env,FIXTURE_RECEIPT=json.dumps(forged))))
            def pin(modified, policy_change=None):
                new_policy=dict(policy)
                new_policy['receipt_sha256']=hashlib.sha256(json.dumps(modified,sort_keys=True,separators=(',',':')).encode()).hexdigest()
                if policy_change:new_policy.update(policy_change)
                registry.write_text(json.dumps({'schema':'loop-trusted-acceptance-v1','receipts':{'one':new_policy}}))
                return dict(env,FIXTURE_RECEIPT=json.dumps(modified))
            missing_criterion=dict(receipt,criteria=[{'id':'invented','status':'proven'}])
            self.blocked(consistency(payload,pin(missing_criterion)))
            self.blocked(consistency(payload,pin(receipt,{'repo_root':str(root)})))
            self.blocked(consistency(payload,pin(receipt,{'output_only':['manifest.json']})))
            # Even a trusted policy cannot hide tracked source under output_only.
            bad_manifest=dict(manifest,output_only=manifest['output_only']+['code.txt'])
            (repo/'manifest.json').write_text(json.dumps(bad_manifest))
            changed=dict(receipt,manifest_sha256=hashlib.sha256((repo/'manifest.json').read_bytes()).hexdigest())
            self.blocked(consistency(payload,pin(changed,{'output_only':bad_manifest['output_only']})))
            (repo/'manifest.json').write_text(json.dumps(manifest))
            pin(receipt)
            # Same-user repinning passes consistency, but never unlocks the hook.
            forged_env=pin(forged)
            self.assertEqual(consistency(payload,forged_env).stdout,'')
            self.blocked(self.invoke(GATE,payload,forged_env))
            pin(receipt)
            slash=chr(92)
            for command in ['bd cl'+slash+'ose one', "b'd' close one", 'bd update one --status=cl'+slash+'osed']:
                self.blocked(consistency({'tool_input':{'command':command}},env))

            self.blocked(consistency(dict(payload,tool_input={'command':'bd close one two'}),env))
            missing=dict(env,FIXTURE_RECEIPT='null')
            self.blocked(consistency(payload,missing))
            (repo/'untracked.txt').write_text('drift')
            self.blocked(consistency(payload,env))
            (repo/'untracked.txt').unlink()
            (repo/'code.txt').write_text('changed')
            self.blocked(consistency(payload,env))

    def test_missing_python_explicit_denial(self):
        with tempfile.TemporaryDirectory() as temp:
            # Keep dirname utility, deliberately omit Python.
            target=Path(temp)/'dirname';target.symlink_to('/usr/bin/dirname')
            env=dict(os.environ,PATH=temp)
            for handler in [GATE,GUARD]:
                result=self.invoke(handler,{'tool_input':{'command':'bd close one'}},env)
                self.assertEqual(result.returncode,2)
                self.assertNotEqual(result.stderr,'')

if __name__ == '__main__':
    unittest.main()
