#!/usr/bin/env python3
"""Summarize Goose hook payloads without enforcing workflow policy.

The public interface is one JSON value on stdin and one ``goose-observer``
diagnostic line on stderr. Stdout stays empty and handled inputs return exit 0.
Only fixed metadata and identifier fingerprints are emitted; commands, paths,
reasons and assistant text are never copied into diagnostics. The observer does
not read files, persist records, access the network or launch child processes.

Stop diagnostics describe heading structure, not content correctness, feasibility
or acceptance. The input cap bounds parsing; output bounds follow from the fixed
record fields and are exercised by the public-interface tests.
"""
import hashlib
import json
import re
import sys
from typing import Literal, TypedDict


ReportFormat = Literal["canonical", "legacy", "mixed", "undetermined"]
ReportShape = Literal[
    "complete", "partial", "duplicate", "out-of-order", "malformed", "mixed", "undetermined"
]


class ReportStructure(TypedDict):
    """Fixed Stop metadata; section numbers refer only to legacy headings."""

    checkpoint_sections: list[int]
    handoff_check: Literal["structure-only"]
    report_format: ReportFormat
    report_shape: ReportShape


class ObservationRecord(TypedDict, total=False):
    """Allowlisted diagnostic fields; optional fields depend on the input event.

    ``host_*`` fields describe an existing runtime decision, never a decision
    emitted by this observer. Null fingerprints indicate missing/nonstring IDs.
    Types document the output contract; they do not validate untrusted input.
    """

    mode: Literal["observation-only"]
    status: Literal["ignored", "observed"]
    code: Literal["unsupported-payload", "payload-too-large", "invalid-payload"]
    event: str
    session_ref: str | None
    tool: str
    call_ref: str | None
    host_decision: Literal["allow", "deny", "unknown"]
    host_cause: Literal["policy_denial", "hook_failure", "unknown"]
    policy_evaluated: bool | None
    checkpoint_sections: list[int]
    handoff_check: Literal["structure-only", "unavailable"]
    report_format: ReportFormat
    report_shape: ReportShape


MAX_INPUT: int = 1048576
EVENTS: set[str] = {"SessionStart", "SessionEnd", "Stop", "AfterFileEdit", "AfterShellExecution",
          "PostToolUseFailure", "PreToolUseResult"}
TOOLS: set[str] = {"shell", "write", "edit", "tree", "read_image"}
# Explicit compatibility aliases only; never strip arbitrary extension namespaces.
TOOL_ALIASES: dict[str, str] = {"developer__" + name: name for name in ("shell", "write", "edit")}


def fingerprint(value: object) -> str | None:
    """Return a stable SHA-256 digest for a string identifier, otherwise None.

    Fingerprints support correlation without emitting raw IDs. They are neither
    encryption nor guaranteed anonymization of predictable identifiers.
    """
    return hashlib.sha256(value.encode()).hexdigest() if isinstance(value, str) else None


def report_structure(message: str) -> ReportStructure:
    """Classify recognized report headings outside backtick/tilde fenced examples.

    Canonical reports require five unique ordered headings and a recognized phase
    in ``current goal``; legacy reports require six numbered headings. Classification
    precedence is mixed formats, malformed goal, duplicates, ordering, completeness.
    Ordinary prose or fenced examples alone are undetermined, not invalid: compact
    responses may be legitimate. Empty sections can still be structurally complete.

    This is a narrow line scanner, not a full Markdown parser or semantic review.
    Return fixed enums and legacy section numbers only; never return message text.
    """
    canonical: list[int] = []
    legacy: list[int] = []
    malformed_goal = False
    fence_char: str | None = None
    fence_size = 0
    labels = {"## roadmap position": 2, "## modified files": 3,
              "## closed tasks": 4, "## explanation": 5}
    report_format: ReportFormat
    shape: ReportShape
    for line in message.splitlines():
        fence = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line)
        if fence_char is not None:
            if (fence and fence[1][0] == fence_char and len(fence[1]) >= fence_size
                    and not fence[2].strip()):
                fence_char = None
            continue
        if fence and (fence[1][0] == "~" or "`" not in fence[2]):
            fence_char, fence_size = fence[1][0], len(fence[1])
            continue
        heading = line.rstrip()
        if re.fullmatch(r"## current goal \{step: (cycle|research|plan|implement|test|judge|iterate)\}", heading):
            canonical.append(1)
        elif re.match(r"## current goal(?:\s|\{|$)", heading):
            canonical.append(1)
            malformed_goal = True
        elif heading in labels:
            canonical.append(labels[heading])
        numbered = re.match(r"## ([1-6])[.] ", line)
        if numbered:
            legacy.append(int(numbered[1]))
    if canonical and legacy:
        report_format, shape = "mixed", "mixed"
    elif canonical or legacy:
        report_format = "canonical" if canonical else "legacy"
        sections = canonical or legacy
        required = list(range(1, 6 if canonical else 7))
        if malformed_goal:
            shape = "malformed"
        elif len(sections) != len(set(sections)):
            shape = "duplicate"
        elif sections != sorted(sections):
            shape = "out-of-order"
        else:
            shape = "complete" if sections == required else "partial"
    else:
        report_format, shape = "undetermined", "undetermined"
    return {"checkpoint_sections": sorted(set(legacy)),
            "handoff_check": "structure-only", "report_format": report_format,
            "report_shape": shape}


def summarize(payload: object) -> ObservationRecord:
    """Reduce an untrusted decoded JSON value to allowlisted diagnostic metadata.

    Reject nonobjects and unsupported events. Optional fields are checked at runtime;
    unknown tool names are reduced to ``other``. PreToolUseResult records an existing
    host decision; Stop inspects headings only when its assistant message is text.
    Raw identifiers, tool arguments/results, prompts, paths and reasons are omitted.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("event"), str) or payload["event"] not in EVENTS:
        return {"mode": "observation-only", "status": "ignored", "code": "unsupported-payload"}
    event = payload["event"]
    record: ObservationRecord = {"mode": "observation-only", "status": "observed", "event": event,
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
            record.update(report_structure(message))
        else:
            record["handoff_check"] = "unavailable"
    # Deliberately omit raw identifiers, tool input/output, prompts, paths and reasons.
    return record


def main() -> int:
    """Read bounded stdin JSON and emit one metadata-only stderr diagnostic.

    Read one byte beyond the 1 MiB cap to identify oversized input. Invalid UTF-8,
    malformed/deep JSON and unsupported payloads become ignored diagnostics. Keep
    stdout empty: it is the host decision channel, not a logging destination.
    Return 0 for handled inputs; this function never emits a policy denial.
    """
    record: ObservationRecord
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
