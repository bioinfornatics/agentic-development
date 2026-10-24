"""Real Goose process, scripted localhost provider; no LLM or global installation."""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import time


def probe(binary, source, output, fault=None):
    version = subprocess.check_output([str(binary), "--version"], text=True).strip()
    root = Path(tempfile.mkdtemp(prefix="goose-observer-probe-"))
    work = root / "work"
    home = root / "home"
    work.mkdir()
    home.mkdir()
    plugin = work / ".agents/plugins/agentic-development"
    plugin.mkdir(parents=True)
    shutil.copy2(source / "plugin.json", plugin / "plugin.json")
    for name in ("skills", "hooks", "scripts"):
        shutil.copytree(source / name, plugin / name)
    observed = root / "observations.jsonl"
    config = json.loads((plugin / "hooks/hooks.json").read_text())
    # Probe-only stderr sink; same event/matcher/handler. No production log path.
    for rules in config["hooks"].values():
        for rule in rules:
            for action in rule["hooks"]:
                action["command"] += ' 2>> "' + str(observed) + '"'
    (plugin / "hooks/hooks.json").write_text(json.dumps(config))
    if fault:
        # Add a failing observation action, never a policy or changed handler.
        command = "sleep 2" if fault == "timeout" else "command-that-does-not-exist-observer-fixture"
        config["hooks"]["AfterShellExecution"][0]["hooks"].append({
            "type": "command", "command": command, "timeout": 1})
        (plugin / "hooks/hooks.json").write_text(json.dumps(config))
    actions = [
        ("write", {"path": "fixture.txt", "content": "first"}),
        ("edit", {"path": "fixture.txt", "before": "first", "after": "second"}),
        ("shell", {"command": "printf shell-fixture > shell-marker.txt"}),
        ("edit", {"path": "fixture.txt", "before": "absent-original", "after": "never"}),
        ("tree", {"path": ".", "depth": 1}),
    ]
    state = {"requests": 0, "offered": [], "missing_tools": []}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            index = state["requests"]
            state["requests"] += 1
            if index < len(actions):
                name, arguments = actions[index]
                tools = [x["function"]["name"] for x in body.get("tools", [])]
                if name not in tools:
                    state["missing_tools"].append(name)
                state["offered"].append(name)
                message = {"role": "assistant", "content": None, "tool_calls": [{
                    "id": "scripted-call-" + str(index), "type": "function",
                    "function": {"name": name, "arguments": json.dumps(arguments)}}]}
                finish = "tool_calls"
            else:
                text = chr(10).join("## " + str(i) + ". Fixture section" for i in range(1, 7))
                message = {"role": "assistant", "content": text}
                finish = "stop"
            if body.get("stream"):
                delta = dict(message)
                delta.pop("role", None)
                if "tool_calls" in delta:
                    delta["tool_calls"][0]["index"] = 0
                chunks = [{"id": "fixture", "object": "chat.completion.chunk", "created": 0,
                           "model": "gpt-4o", "choices": [{"index": 0, "delta": delta,
                           "finish_reason": None}]},
                          {"id": "fixture", "object": "chat.completion.chunk", "created": 0,
                           "model": "gpt-4o", "choices": [{"index": 0, "delta": {},
                           "finish_reason": finish}]}]
                data = ("".join("data: " + json.dumps(x) + chr(10) * 2 for x in chunks)
                        + "data: [DONE]" + chr(10) * 2).encode()
                kind = "text/event-stream"
            else:
                data = json.dumps({"id": "fixture", "object": "chat.completion", "created": 0,
                    "model": "gpt-4o", "choices": [{"index": 0, "message": message,
                    "finish_reason": finish}], "usage": {"prompt_tokens": 1,
                    "completion_tokens": 1, "total_tokens": 2}}).encode()
                kind = "application/json"
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    env = dict(os.environ, HOME=str(home), GOOSE_PATH_ROOT=str(root / "runtime"),
               XDG_CONFIG_HOME=str(home / ".config"), XDG_DATA_HOME=str(home / ".local/share"),
               XDG_STATE_HOME=str(home / ".local/state"), GOOSE_PROVIDER="openai",
               GOOSE_MODEL="gpt-4o", OPENAI_API_KEY="fixture-not-a-secret",
               OPENAI_HOST="http://127.0.0.1:" + str(server.server_port),
               GOOSE_DISABLE_SESSION_NAMING="true")
    command = [str(binary), "run", "--no-profile", "--with-builtin", "developer",
               "--provider", "openai", "--model", "gpt-4o", "--max-turns", "8",
               "--no-session", "--text", "Execute isolated fixture tool calls then finish."]
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=work, env=env, capture_output=True,
                                text=True, timeout=60)
    finally:
        server.shutdown()
        server.server_close()
    (root / "stdout.log").write_text(result.stdout)
    (root / "stderr.log").write_text(result.stderr)
    records = []
    if observed.exists():
        for line in observed.read_text().splitlines():
            if line.startswith("goose-observer "):
                records.append(json.loads(line.split(" ", 1)[1]))
    counts = {event: sum(x.get("event") == event for x in records)
              for event in config["hooks"]}
    checks = {
        "goose_exit_zero": result.returncode == 0,
        "tools_advertised": not state["missing_tools"],
        "scripted_sequence_completed": state["requests"] >= 6,
        "file_edit_observed": counts["AfterFileEdit"] >= 1,
        "shell_execution_observed": counts["AfterShellExecution"] == 1,
        "failed_edit_observed": counts["PostToolUseFailure"] == 1,
        "session_start_observed": counts["SessionStart"] >= 1,
        "stop_structure_observed": any(x.get("event") == "Stop" and
            x.get("checkpoint_sections") == [1, 2, 3, 4, 5, 6] for x in records),
        "pretool_matching_only": counts["PreToolUseResult"] == 4,
        "tool_effects_retained": (work / "fixture.txt").exists() and
            (work / "fixture.txt").read_text() == "second" and
            (work / "shell-marker.txt").exists(),
        "session_end_observed": counts["SessionEnd"] >= 1,
    }
    diagnostics = []
    for log in (root / "runtime").glob("state/logs/cli/**/*.log"):
        for line in log.read_text().splitlines():
            try:
                event = json.loads(line)
                if event.get("target") == "goose::hooks":
                    diagnostics.append(event.get("fields", {}))
            except ValueError:
                pass
    if fault:
        diagnostic_text = json.dumps(diagnostics)
        checks["fault_observed"] = ("timed out after 1s" in diagnostic_text if fault == "timeout"
                                    else "exited with Some(127)" in diagnostic_text)
    receipt = {"binary": str(binary), "version": version,
               "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
               "source_handler_sha256": hashlib.sha256((source / "scripts/observe.py").read_bytes()).hexdigest(),
               "root": str(root), "command": command, "cwd": str(work),
               "exit": result.returncode, "elapsed_seconds": round(time.monotonic() - started, 3),
               "provider": "localhost scripted OpenAI-compatible fixture; zero real LLM calls",
               "isolation": "temporary HOME, GOOSE_PATH_ROOT, XDG dirs, project plugin only",
               "probe_config_delta": "stderr redirected to temporary observation sink; optional injected observer failure",
               "injected_fault": fault, "hook_diagnostics": diagnostics,
               "scripted_tools": state, "event_counts": counts, "observations": records,
               "checks": checks, "status": "PASS" if all(checks.values()) else "needs-investigation",
               "limits": ["runtime event wiring, not LLM behavior or release acceptance",
                          "SessionEnd checked only for this CLI no-session path",
                          "No global installation/config/hooks modified"]}
    Path(output).write_text(json.dumps(receipt, indent=2) + chr(10))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--goose-cli", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--fault", choices=["timeout", "missing-command"])
    args = parser.parse_args()
    receipt = probe(Path(args.goose_cli).resolve(strict=True),
                    Path(__file__).resolve().parents[1], args.output, args.fault)
    print(json.dumps({k: receipt[k] for k in ("version", "exit", "root", "event_counts", "checks", "status")}, indent=2))
    raise SystemExit(0 if receipt["status"] == "PASS" else 1)
