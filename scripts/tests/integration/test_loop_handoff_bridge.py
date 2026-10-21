"""Disposable Git/fake-bd protocol evidence, not host isolation or live Beads CAS."""
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('bridge', ROOT/'scripts/loop_handoff_bridge.py')
bridge = importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)

class BridgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name);self.repo = self.root/'repo';self.repo.mkdir()
        self.tracker = self.root/'tracker';(self.tracker/'.beads').mkdir(parents=True)
        self.git('init', '-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid');self.git('config','core.hooksPath','/dev/null')
        (self.repo/'code.txt').write_text('base');self.git('add','code.txt');self.git('commit','-qm','base')
        (self.repo/'evidence.txt').write_text('raw fixture evidence')
        self.db = self.tracker/'fixture.json';self.db.write_text(json.dumps({'id':'issue','status':'in_progress','metadata':{'unrelated':{'preserve':True}}}))
        self.bd = self.root/'fake-bd'
        self.bd.write_text('#!/usr/bin/python3'+chr(10)+
            'import json,sys,pathlib'+chr(10)+
            'p=pathlib.Path.cwd()/"fixture.json";x=json.loads(p.read_text())'+chr(10)+
            'if sys.argv[1]=="update":'+chr(10)+
            ' key,value=sys.argv[4].split("=",1);x["metadata"][key]=json.loads(value);p.write_text(json.dumps(x))'+chr(10)+
            'else:print(json.dumps([x]))'+chr(10))
        self.bd.chmod(0o755)
    def git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.repo,text=True).strip()
    def request(self, kind='checkpoint', seq=0, previous=None, session='builder'):
        candidate = bridge.snapshot(self.repo,['evidence.txt'])
        return {'issue_id':'issue','run_id':'run','slice_id':'slice','session_id':session,
                'event_id':'event-'+str(seq),'seq':seq,'previous':previous,'kind':kind,'phase':'test',
                'candidate_sha256':bridge.digest(candidate),'output_only':['evidence.txt'],
                'evidence':[{'path':'evidence.txt','sha256':hashlib.sha256((self.repo/'evidence.txt').read_bytes()).hexdigest()}]}
    def invoke(self,r):return bridge.process(self.repo,self.tracker,r,str(self.bd))
    def state(self):return json.loads(self.db.read_text())['metadata'][bridge.KEY]
    def handoff(self):
        first=self.invoke(self.request());r=self.request('handoff',1,first['event_sha256'])
        r.update(outcome='tests passed locally',remaining='host gate open',next_session_name='fresh verifier',restart_prompt='Inspect source, tasks, permissions and raw proof; no closure.')
        return self.invoke(r)
    def test_persistence_replay_and_preservation(self):
        r=self.request();a=self.invoke(r);b=self.invoke(r)
        self.assertTrue(a['written']);self.assertFalse(b['written']);self.assertFalse(a['authority'])
        data=json.loads(self.db.read_text());self.assertEqual(data['metadata']['unrelated'],{'preserve':True});self.assertEqual(data['status'],'in_progress')
        changed=dict(r,phase='judge')
        with self.assertRaises(ValueError):self.invoke(changed)
    def test_explicit_handoff_resume_and_sequence(self):
        end=self.handoff();r=self.request('resume',2,end['event_sha256'],'verifier')
        self.assertTrue(self.invoke(r)['written']);self.assertEqual(self.state()['events'][-1]['session_id'],'verifier')
        with self.assertRaises(ValueError):self.invoke(self.request('checkpoint',8,end['event_sha256'],'verifier'))
        self.assertEqual(len(self.state()['events']),3)
    def test_resume_rejects_every_historical_session(self):
        end=self.handoff();resumed=self.invoke(self.request('resume',2,end['event_sha256'],'verifier'))
        r=self.request('handoff',3,resumed['event_sha256'],'verifier')
        r.update(outcome='reviewed',remaining='host gate open',next_session_name='new context',restart_prompt='Inspect latest raw proof and authority.')
        ended=self.invoke(r)
        for reused in ['builder','verifier']:
            with self.assertRaises(ValueError):self.invoke(self.request('resume',4,ended['event_sha256'],reused))
        self.assertEqual(len(self.state()['events']),4)
        self.assertTrue(self.invoke(self.request('resume',4,ended['event_sha256'],'fresh-session'))['written'])

    def test_interruption_and_missing_handoff(self):
        first=self.invoke(self.request())
        with self.assertRaises(ValueError):self.invoke(self.request('resume',1,first['event_sha256'],'verifier'))
        with self.assertRaises(ValueError):self.invoke(self.request('checkpoint',1,first['event_sha256'],'other'))
        with self.assertRaises(ValueError):self.invoke(self.request('handoff',1,first['event_sha256']))
    def test_candidate_evidence_scope_and_root_drift(self):
        end=self.handoff();r=self.request('resume',2,end['event_sha256'],'verifier')
        (self.repo/'ignored.bin').write_bytes(bytes([0,255]))
        with self.assertRaises(ValueError):self.invoke(r)
        refreshed=self.request('resume',2,end['event_sha256'],'verifier')
        with self.assertRaises(ValueError):self.invoke(refreshed)
        (self.repo/'ignored.bin').unlink();(self.repo/'evidence.txt').write_text('changed')
        with self.assertRaises(ValueError):self.invoke(r)
        with self.assertRaises(ValueError):self.invoke(self.request('resume',2,end['event_sha256'],'verifier'))
        with self.assertRaises(ValueError):bridge.snapshot(self.repo,['code.txt'])
        sub=self.repo/'nested';sub.mkdir()
        with self.assertRaises(ValueError):bridge.process(sub,self.tracker,r,str(self.bd))
    def test_links_binary_modes_and_unsafe_evidence(self):
        (self.repo/'binary').write_bytes(bytes([0,255]));(self.repo/'link').symlink_to('/outside/not-read')
        snap=bridge.snapshot(self.repo,['evidence.txt']);entry=next(x for x in snap['files'] if x['path']=='link')
        self.assertEqual(entry['kind'],'symlink');self.assertEqual(entry['target'],'/outside/not-read')
        with self.assertRaises(ValueError):bridge.evidence(self.repo,[{'path':'link','sha256':entry['sha256']}])
        with self.assertRaises(ValueError):bridge.snapshot(self.repo,['nested/../code.txt'])
        before=bridge.digest(snap);(self.repo/'binary').chmod(0o755);self.assertNotEqual(before,bridge.digest(bridge.snapshot(self.repo,['evidence.txt'])))
    def test_actual_commit_receipt_and_rebind(self):
        (self.repo/'code.txt').write_text('candidate');first=self.invoke(self.request())
        self.git('add','code.txt');self.git('commit','-qm','actual fixture change')
        r=self.request('commit',1,first['event_sha256']);r['observed_commit']={'hash':self.git('rev-parse','HEAD'),'parent':self.git('rev-parse','HEAD^'),'message':self.git('show','-s','--format=%B','HEAD'),'files':self.git('diff-tree','--no-commit-id','--name-status','-r','HEAD').splitlines()}
        wrong=copy.deepcopy(r);wrong['observed_commit']['message']='invented'
        with self.assertRaises(ValueError):self.invoke(wrong)
        self.assertTrue(self.invoke(r)['written']);self.assertEqual(self.state()['events'][-1]['commit']['message'],'actual fixture change')
        self.assertFalse(self.invoke(r)['written'])
        (self.repo/'unexpected').write_text('drift')
        with self.assertRaises(ValueError):self.invoke(r)
    def test_evidence_parent_alias_into_excluded_state_rejected(self):
        (self.repo/'.beads').mkdir();(self.repo/'.beads/proof').write_text('proof')
        (self.repo/'alias').symlink_to('.beads',target_is_directory=True)
        r=self.request();r['evidence']=[{'path':'alias/proof','sha256':hashlib.sha256(b'proof').hexdigest()}]
        with self.assertRaises(ValueError):self.invoke(r)
        self.assertNotIn(bridge.KEY,json.loads(self.db.read_text())['metadata'])

    def test_failed_write_and_readback_not_success(self):
        from unittest.mock import patch
        original=bridge.call
        def drop_write(args,cwd):
            return '' if args[1]=='update' else original(args,cwd)
        with patch.object(bridge,'call',side_effect=drop_write):
            with self.assertRaises(ValueError):self.invoke(self.request())
        self.assertNotIn(bridge.KEY,json.loads(self.db.read_text())['metadata'])

    def test_corrupted_chain_and_wrong_tracker(self):
        first=self.invoke(self.request());data=json.loads(self.db.read_text());data['metadata'][bridge.KEY]['events'][0]['phase']='invented';self.db.write_text(json.dumps(data))
        with self.assertRaises(ValueError):self.invoke(self.request('checkpoint',1,first['event_sha256']))
        with self.assertRaises(ValueError):bridge.process(self.repo,self.root,self.request(),str(self.bd))

if __name__=='__main__':unittest.main()
