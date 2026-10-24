#!/usr/bin/env python3
"""Best-effort, metadata-only Goose hook diagnostics; no policy or durable writes."""
import hashlib
import json
import re
import sys

MAX_INPUT = 1048576
EVENTS = {"SessionStart", "SessionEnd", "Stop", "AfterFileEdit", "AfterShellExecution",
          "PostToolUseFailure", "PreToolUseResult"}
TOOLS = {"shell", "write", "edit", "tree", "read_image"}
# Explicit compatibility aliases only; never strip arbitrary extension namespaces.
TOOL_ALIASES = {"developer__" + name: name for name in ("shell", "write", "edit")}


def fingerprint(value):
    return hashlib.sha256(value.encode()).hexdigest() if isinstance(value, str) else None


def summarize(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("event"), str) or payload["event"] not in EVENTS:
        return {"mode": "observation-only", "status": "ignored", "code": "unsupported-payload"}
    event = payload["event"]
    record = {"mode": "observation-only", "status": "observed", "event": event,
              "session_ref": fingerprint(payload.get("session_id"))}
    if "tool_name" in payload:
        tool = payload["tool_name"]
        canonical = TOOL_ALIASES.get(tool, tool) if isinstance(tool, str) else None
        record["tool"] = canonical if canonical in TOOLS else "other"
    if "tool_call_id" in payload:
        record["call_ref"] = fingerprint(payload.get("tool_call_id"))
    if event == "PreToolUseResult":
        decision = payload.get("decision")
        record["host_decision"] = decision if decision in ("allow", "deny") else "unknown"
        cause = payload.get("cause")
        record["host_cause"] = cause if cause in ("policy_denial", "hook_failure") else "unknown"
        evaluated = payload.get("policy_evaluated")
        record["policy_evaluated"] = evaluated if isinstance(evaluated, bool) else None
    if event == "Stop":
        message = payload.get("last_assistant_message")
        if isinstance(message, str):
            sections = sorted({int(x) for x in re.findall(r"(?m)^## ([1-6])[.] ", message)})
            record["checkpoint_sections"] = sections
            record["handoff_check"] = "structure-only"
        else:
            record["handoff_check"] = "unavailable"
    # Deliberately omit raw identifiers, tool input/output, prompts, paths and reasons.
    return record


def main():
    raw = sys.stdin.buffer.read(MAX_INPUT + 1)
    if len(raw) > MAX_INPUT:
        record = {"mode": "observation-only", "status": "ignored", "code": "payload-too-large"}
    else:
        try:
            record = summarize(json.loads(raw.decode("utf-8")))
        except (UnicodeError, ValueError, TypeError, RecursionError):
            record = {"mode": "observation-only", "status": "ignored", "code": "invalid-payload"}
    # stdout is Goose's decision channel. This observer never writes to it.
    sys.stderr.write("goose-observer " + json.dumps(record, sort_keys=True, separators=(",", ":")) + chr(10))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
