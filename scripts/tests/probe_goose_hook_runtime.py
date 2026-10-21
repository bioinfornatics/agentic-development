"""Actual Goose hook protocol probes with a localhost simulated provider, not LLM acceptance."""
import argparse,json,os,threading,tempfile,subprocess,hashlib,time
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    calls=0
    def log_message(self,*args):pass
    def do_POST(self):
        n=int(self.headers.get('Content-Length',0));body=json.loads(self.rfile.read(n));Handler.calls+=1
        tools=body.get('tools',[])
        name=next((x['function']['name'] for x in tools if x['function']['name'] in ('shell','developer__shell')),None)
        if Handler.calls==1 and name:
            message={'role':'assistant','content':None,'tool_calls':[{'id':'fixture-call','type':'function','function':{'name':name,'arguments':json.dumps({'command':'printf runtime-probe > marker.txt'})}}]};finish='tool_calls'
        else:message={'role':'assistant','content':'fixture finished'};finish='stop'
        result={'id':'chatcmpl-fixture','object':'chat.completion','created':0,'model':'gpt-4o','choices':[{'index':0,'message':message,'finish_reason':finish}],'usage':{'prompt_tokens':1,'completion_tokens':1,'total_tokens':2}}
        if body.get('stream'):
            delta = dict(message);delta.pop('role',None)
            if 'tool_calls' in delta:
                delta['tool_calls'][0]['index']=0
            chunk={'id':'chatcmpl-fixture','object':'chat.completion.chunk','created':0,'model':'gpt-4o','choices':[{'index':0,'delta':delta,'finish_reason':None}]}
            final={'id':'chatcmpl-fixture','object':'chat.completion.chunk','created':0,'model':'gpt-4o','choices':[{'index':0,'delta':{},'finish_reason':finish}]}
            data=('data: '+json.dumps(chunk)+chr(10)*2+'data: '+json.dumps(final)+chr(10)*2+'data: [DONE]'+chr(10)*2).encode()
            self.send_response(200);self.send_header('Content-Type','text/event-stream');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
        data=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)

server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--goose-cli',required=True)
parser.add_argument('--layout',choices=['root','creator-extension'],default='root')
parser.add_argument('--omit-on-failure',action='store_true')
parser.add_argument('--cases',nargs='+',choices=['allow','block','exit2','timeout-allow','timeout-block','missing-command-allow','missing-command-block','spawn-allow','spawn-block'],default=['allow','block','exit2','timeout-allow','timeout-block','missing-command-allow','missing-command-block','spawn-allow','spawn-block'])
args=parser.parse_args()
binary=Path(args.goose_cli).resolve(strict=True)
binary_hash=hashlib.sha256(binary.read_bytes()).hexdigest()
version=subprocess.check_output([str(binary),'--version'],text=True).strip()
records=[]
for failure in args.cases:
    Handler.calls=0
    root=Path(tempfile.mkdtemp(prefix='goose-hook-runtime-'));home=root/'home';home.mkdir();work=root/'work';work.mkdir();runtime=root/'runtime'
    plugin=work/'.agents/plugins/runtime-fixture'
    hook_rel='hooks/hooks.json' if args.layout=='root' else 'extensions/io.github.bioinfornatics.agent-plugins.goose/hooks.json'
    hook_path=plugin/hook_rel;hook_path.parent.mkdir(parents=True)
    manifest={'name':'runtime-fixture','version':'0.0.1','description':'Isolated runtime fixture'}
    if args.layout=='creator-extension':
        manifest['extensions']={'io.github.bioinfornatics.agent-plugins.goose':{'version':1,'hooks':hook_rel}}
    (plugin/'plugin.json').write_text(json.dumps(manifest))
    mode='allow' if failure=='allow' or failure.endswith('-allow') else 'block'
    script=plugin/'fail.sh'
    action='exit 2' if failure=='exit2' else ('exec /bin/sleep 4' if failure.startswith('timeout-') else 'exit 1')
    script.write_text('#!/bin/sh'+chr(10)+'cat >/dev/null'+chr(10)+'printf invoked >> "'+str(root/'hook-invoked')+'"'+chr(10)+action+chr(10));script.chmod(0o755)
    hook_command=str(plugin/'does-not-exist') if failure.startswith('missing-command-') else str(script)
    config={'type':'command','command':hook_command,'timeout':1 if failure.startswith('timeout-') else 5}
    if not args.omit_on_failure:config['on_failure']=mode
    hook_path.write_text(json.dumps({'hooks':{'PreToolUse':[{'matcher':'^(shell|developer__shell)$','hooks':[config]}]}}))
    env=dict(os.environ,HOME=str(home),GOOSE_PATH_ROOT=str(runtime),XDG_CONFIG_HOME=str(home/'.config'),XDG_DATA_HOME=str(home/'.local/share'),XDG_STATE_HOME=str(home/'.local/state'),GOOSE_PROVIDER='openai',GOOSE_MODEL='gpt-4o',GOOSE_PROVIDER__TYPE='openai',GOOSE_PROVIDER__HOST='http://127.0.0.1:'+str(server.server_port),GOOSE_PROVIDER__API_KEY='fixture-not-a-secret',OPENAI_API_KEY='fixture-not-a-secret',OPENAI_HOST='http://127.0.0.1:'+str(server.server_port),GOOSE_DISABLE_SESSION_NAMING='true')
    if failure.startswith('spawn-'):
        # Hooks spawn bare sh; developer shell uses explicit /bin/bash. No global PATH mutation.
        empty_path=root/'empty-path';empty_path.mkdir();env['PATH']=str(empty_path);env['GOOSE_SHELL']='/bin/bash'
    started=time.monotonic()
    command=[str(binary),'run','--no-profile','--with-builtin','developer','--provider','openai','--model','gpt-4o','--max-turns','3','--no-session','--text','Execute the fixture shell command, then finish.']
    try:
        p=subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,timeout=45)
        (root/'stdout.log').write_text(p.stdout);(root/'stderr.log').write_text(p.stderr)
        output=p.stdout+p.stderr
        marker=(work/'marker.txt').exists();invoked=(root/'hook-invoked').exists()
        expected=mode=='allow' and failure!='exit2'
        denial='Tool call blocked' in output or 'Tool call denied by policy hook' in output
        diagnostics=[];log_hashes=[]
        for log in sorted(runtime.glob('state/logs/cli/**/*.log')):
            raw=log.read_bytes();log_hashes.append({'path':str(log),'sha256':hashlib.sha256(raw).hexdigest()})
            for line in raw.decode().splitlines():
                try:
                    event=json.loads(line)
                    if event.get('target')=='goose::hooks':diagnostics.append(event.get('fields',{}))
                except ValueError:pass
        diagnostic_text=json.dumps(diagnostics)
        failure_observed=('timed out after 1s' in diagnostic_text) if failure.startswith('timeout-') else (('spawning hook' in diagnostic_text and 'os error 2' in diagnostic_text) if failure.startswith('spawn-') else (('status 127' in diagnostic_text) if failure.startswith('missing-command-') else True))
        # A spawn failure cannot invoke its handler. It must have a diagnostic or remain UNKNOWN.
        passed=Handler.calls>=2 and marker==expected and (expected or denial) and (invoked or failure.startswith(('spawn-','missing-command-'))) and failure_observed
        records.append({'probe_case':failure,'binary':str(binary),'binary_sha256':binary_hash,'version':version,'layout':args.layout,'on_failure':None if args.omit_on_failure else mode,'root':str(root),'exit':p.returncode,'elapsed_seconds':round(time.monotonic()-started,3),'hook_invoked':invoked,'marker_created':marker,'expected_marker':expected,'denial_observed':denial,'failure_observed':failure_observed,'mock_requests':Handler.calls,'hook_diagnostics':diagnostics,'runtime_log_hashes':log_hashes,'assertions_status':'PASS' if passed else 'FAIL_OR_INDETERMINATE','stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest(),'output_tail':output[-2400:]})
    except subprocess.TimeoutExpired:records.append({'probe_case':failure,'binary':args.goose_cli,'on_failure':('allow' if failure=='allow' else 'block'),'root':str(root),'result':'timeout'})
server.shutdown()
Path(args.output).write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
