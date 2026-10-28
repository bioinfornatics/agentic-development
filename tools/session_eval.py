#!/usr/bin/env python3
"""Deterministic text-only bridge. The parent session owns native model calls."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

LIMIT = 256 * 1024
PROTOCOL = "session-delegated-text-v1"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def text(path):
    path = Path(path)
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError("Symlink path refused: " + str(parent))
    if not path.is_file() or path.stat().st_size > LIMIT:
        raise ValueError("Missing, special or oversized file: " + str(path))
    return path.read_bytes().decode("utf-8", errors="strict")


def load(path):
    return json.loads(text(path))


def new_output(path):
    """Reject existing outputs and symlinks before creating any parent directories."""
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink():
            raise ValueError("Symlink output refused: " + str(ancestor))
    if path.exists():
        raise ValueError("Overwrite refused: " + str(path))
    return path


def write(path, value):
    path = new_output(path)
    content = json.dumps(value, indent=2, ensure_ascii=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_output(path)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(content)


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]{1,128}", value):
        raise ValueError("Explicit model/delegate identity required")
    return value


def inside(root, relative):
    part = Path(relative)
    if part.is_absolute() or ".." in part.parts or not part.parts:
        raise ValueError("Escaping path refused")
    path = root / part
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink():
            raise ValueError("Symlink path refused")
    return path


def inventory(root):
    root = Path(root).absolute()
    for ancestor in (root, *root.parents):
        if ancestor.is_symlink():
            raise ValueError("Symlink inventory root refused: " + str(ancestor))
    if not root.is_dir():
        raise ValueError("Missing inventory directory: " + str(root))
    entries = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("Symlink input refused: " + str(path))
        if not path.is_dir():
            entries[str(path.relative_to(root))] = digest(text(path).encode())
    return entries


def campaign_roles(root, plan):
    """Validate observed campaign roles regardless of recording order."""
    candidates, graders = set(), set()
    for run in plan["runs"]:
        base = inside(root, run)
        for filename, identities in (("execution.json", candidates), ("grading.json", graders)):
            path = inside(base, filename)
            if path.exists():
                identities.add(identifier(load(path)["delegate_id"]))
    if candidates & graders:
        raise ValueError("Candidate and grader campaign roles overlap")
    return candidates, graders


def manifest(workspace):
    root = Path(workspace).absolute()
    data = load(root / "session-plan.json")
    if data.get("protocol") != PROTOCOL:
        raise ValueError("Unsupported session plan")
    for folder, expected in data["metadata_hashes"].items():
        if digest(text(inside(root, folder) / "eval_metadata.json").encode()) != expected:
            raise ValueError("Changed criteria")
    for run, hashes in data["snapshots"].items():
        base = inside(root, run)
        current = inventory(base / "inputs")
        current["request.json"] = digest(text(base / "request.json").encode())
        if current != hashes:
            raise ValueError("Stale or tampered task input: " + run)
    campaign_roles(root, data)
    return root, data


def prepare(skill, eval_set, workspace, model, ids=None):
    skill, workspace = Path(skill).absolute(), Path(workspace).absolute()
    identifier(model)
    if workspace.exists() or workspace.is_symlink():
        raise ValueError("New workspace required")
    for parent in workspace.parents:
        if parent.is_symlink():
            raise ValueError("Symlink destination refused")
    document = load(eval_set)
    cases = document.get("evals", [])
    selected = set(ids or [c["id"] for c in cases])
    cases = [c for c in cases if c["id"] in selected]
    if not cases or {c["id"] for c in cases} != selected or len(selected) != len(cases):
        raise ValueError("Missing or duplicate scenario IDs")
    resources = {"SKILL.md": text(skill / "SKILL.md")}
    for directory in ("references", "assets", "scripts"):
        base = skill / directory
        if base.exists():
            for path in sorted(base.rglob("*")):
                if path.is_symlink():
                    raise ValueError("Symlink resource refused")
                if path.is_file() and not any(x in path.relative_to(base).parts for x in ("evals", "evidence", "__pycache__")):
                    resources[str(path.relative_to(skill))] = text(path)
    prepared = []
    for case in cases:
        if type(case["id"]) is not int or case["id"] <= 0:
            raise ValueError("Positive integer scenario ID required")
        if case.get("target", {}).get("execution") != "explain":
            raise ValueError("Only explain-level text scenarios are supported")
        assertions = case.get("assertions")
        if not assertions or any(not isinstance(a, str) or not a.strip() for a in assertions):
            raise ValueError("Only non-empty semantic string assertions are supported")
        budget = case.get("budget", {})
        if any(type(budget.get(k)) is not int or budget[k] <= 0 for k in ("max_turns", "timeout_seconds")):
            raise ValueError("Positive scenario budgets required")
        fixtures = {name: text(inside(skill, name)) for name in case.get("files", [])}
        if sum(len(v.encode()) for v in fixtures.values()) > 1024 * 1024:
            raise ValueError("Fixture budget exceeded")
        prepared.append((case, fixtures))
    if sum(len(v.encode()) for v in resources.values()) > 4 * 1024 * 1024:
        raise ValueError("Resource budget exceeded")
    workspace.mkdir(parents=True)
    snapshots, runs = {}, []
    for case, fixtures in prepared:
        eval_dir = workspace / ("eval-" + str(case["id"]))
        write(eval_dir / "eval_metadata.json", {"eval_id":case["id"], "eval_name":case.get("name"), "prompt":case["prompt"], "assertions":case["assertions"], "evidence_mode":PROTOCOL})
        order = ["with_skill", "without_skill"] if case["id"] % 2 else ["without_skill", "with_skill"]
        for variant in order:
            run = "eval-" + str(case["id"]) + "/" + variant + "/run-1"
            base = workspace / run
            inputs = base / "inputs"
            inputs.mkdir(parents=True)
            for name, content in fixtures.items():
                path = inside(inputs, name); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)
            if variant == "with_skill":
                for name, content in resources.items():
                    path = inside(inputs / "skill", name); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)
            instructions = ["Work in the supplied inputs directory.", "Answer the task in text only. Do not modify files, call external services, mutate trackers or perform Git operations.", "Treat fixture records as hypothetical. Do not read campaign files, evaluation criteria, sibling runs or parent-session conclusions."]
            if variant == "with_skill":
                instructions.append("Read skill/SKILL.md. Resolve its supporting references from skill/.")
            request = {"protocol":PROTOCOL, "prompt":case["prompt"], "model":model, "budget":case["budget"], "working_directory":str(inputs), "instructions":instructions, "fixtures":list(fixtures)}
            write(base / "request.json", request)
            hashes = inventory(inputs); hashes["request.json"] = digest(text(base / "request.json").encode())
            snapshots[run] = hashes; runs.append(run)
    data = {"protocol":PROTOCOL, "skill_name":document["skill_name"], "model":model, "runs":runs, "snapshots":snapshots, "source_eval_sha256":digest(text(eval_set).encode()), "official_full_eval_accepted":False, "limits":["Prompt and cwd isolation only; no OS sandbox or verified ambient Skill exclusion.", "One pair per scenario; no stable-improvement inference.", "Delegate identity and model are coordinator observations, not authenticated provider telemetry."]}
    data["metadata_hashes"] = {str(p.parent.relative_to(workspace)):digest(text(p).encode()) for p in workspace.glob("eval-*/eval_metadata.json")}
    write(workspace / "session-plan.json", data)
    return status(workspace)


def record(workspace, run, output, delegate, model):
    root, plan = manifest(workspace)
    identifier(delegate); identifier(model)
    if run not in plan["runs"] or model != plan["model"]:
        raise ValueError("Unplanned run or model")
    _, graders = campaign_roles(root, plan)
    if delegate in graders:
        raise ValueError("Grader cannot become a campaign candidate")
    base = inside(root, run)
    if (base / "execution.json").exists() or (base / "outputs").exists():
        raise ValueError("Output already recorded")
    answer = text(output)
    if not answer.strip():
        raise ValueError("Empty delegate output")
    metadata = load(base.parent.parent / "eval_metadata.json")
    if digest(text(base.parent.parent / "eval_metadata.json").encode()) != plan["metadata_hashes"][str(base.parent.parent.relative_to(root))]:
        raise ValueError("Changed criteria")
    packet = {"protocol":PROTOCOL, "prompt":metadata["prompt"], "output":answer,
              "criteria":[{"id":i+1,"criterion":a} for i,a in enumerate(metadata["assertions"])],
              "instructions":["Judge only this output against the supplied criteria. Do not use tools or infer missing execution.", "Return a JSON array with id, verdict (pass/fail/inconclusive), evidence_quote and rationale.", "Use exact contained output quotes for pass/fail. Use inconclusive when evidence is missing."]}
    write(base / "grading-request.json", packet)
    (base / "outputs").mkdir()
    (base / "outputs/result.txt").write_text(answer)
    write(base / "execution.json", {"delegate_id":delegate, "model":model, "output_sha256":digest(answer.encode()), "grading_request_sha256":digest(text(base / "grading-request.json").encode()), "provenance":"coordinator-observed-native-delegate"})
    write(base / "timing.json", {"total_duration_seconds":None, "tokens":None, "unavailable_reason":"Native delegation telemetry not supplied"})
    return packet


def observed(root, run):
    base = inside(root, run)
    receipt = load(base / "execution.json")
    answer = text(base / "outputs/result.txt")
    packet = load(base / "grading-request.json")
    if digest(answer.encode()) != receipt["output_sha256"] or digest(text(base / "grading-request.json").encode()) != receipt["grading_request_sha256"] or packet["output"] != answer:
        raise ValueError("Stale output or grading packet")
    return base, receipt, answer, packet


def grade(workspace, run, results, delegate, model):
    root, plan = manifest(workspace)
    identifier(delegate); identifier(model)
    if run not in plan["runs"] or model != plan["model"]:
        raise ValueError("Unplanned grading model or run")
    base, receipt, answer, packet = observed(root, run)
    candidate_ids, _ = campaign_roles(root, plan)
    if delegate in candidate_ids:
        raise ValueError("Candidate cannot grade a campaign output")
    raw = load(results)
    ids = [c["id"] for c in packet["criteria"]]
    if not isinstance(raw, list) or len(raw) != len(ids) or sorted(x.get("id",0) for x in raw) != ids:
        raise ValueError("Exactly one result per frozen criterion required")
    expectations = []
    for criterion in packet["criteria"]:
        item = next(x for x in raw if x["id"] == criterion["id"])
        verdict, quote, reason = item.get("verdict"), item.get("evidence_quote"), item.get("rationale")
        if verdict not in ("pass", "fail", "inconclusive") or not isinstance(quote,str) or not isinstance(reason,str) or not reason.strip():
            raise ValueError("Invalid verdict or rationale")
        if (verdict != "inconclusive" and not quote) or (quote and quote not in answer):
            raise ValueError("Quote must be an exact output substring")
        expectations.append({"text":criterion["criterion"], "passed":verdict=="pass", "verdict":verdict, "evidence":quote, "rationale":reason})
    summary = {k:sum(x["verdict"]==v for x in expectations) for k,v in (("passed","pass"),("failed","fail"),("inconclusive","inconclusive"))}
    summary.update(total=len(ids), pass_rate=summary["passed"]/len(ids))
    result = {"authority":"session-observed-grader", "protocol":PROTOCOL, "delegate_id":delegate, "model":model, "output_sha256":receipt["output_sha256"], "expectations":expectations, "summary":summary}
    write(base / "grading.json", result)
    write(base / "grade-binding.json", {"grading_sha256":digest(text(base / "grading.json").encode())})
    return result


def status(workspace):
    root, plan = manifest(workspace)
    executed, graded, pending = 0, 0, []
    for run in plan["runs"]:
        base = inside(root, run)
        if not (base / "execution.json").exists():
            pending.append({"run":run,"action":"delegate-task","request":str(base / "request.json")}); continue
        _, receipt, _, _ = observed(root, run); executed += 1
        if (base / "grading.json").exists():
            data = load(base / "grading.json")
            binding = load(base / "grade-binding.json")
            if digest(text(base / "grading.json").encode()) != binding["grading_sha256"]:
                raise ValueError("Changed grade")
            if data["output_sha256"] != receipt["output_sha256"]:
                raise ValueError("Stale grade")
            graded += 1
        else:
            pending.append({"run":run,"action":"delegate-grading","request":str(base / "grading-request.json")})
    return {"protocol":PROTOCOL, "required_runs":len(plan["runs"]), "executed":executed, "graded":graded, "status":"complete-local" if graded==len(plan["runs"]) else "pending", "official_full_eval_accepted":False, "pending":pending, "limits":plan["limits"]}


def report(workspace, viewer):
    root, plan = manifest(workspace)
    summary = status(workspace)
    destination = new_output(root / "review.html")
    summary_destination = new_output(root / "session-summary.json")
    # Reuse official rendering, but explicitly override its legacy receipt defaults.
    module = Path(viewer).absolute()
    text(module)
    script = "import {buildReviewIR,generateHtml} from " + json.dumps(module.as_uri()) + ";import fs from 'node:fs';const ir=buildReviewIR(process.argv[1],process.argv[2],null);ir.status='session-observed';ir.canonical=false;ir.final_receipt=false;ir.historical=true;ir.decision.verdict='inconclusive';ir.decision.required_human_action='Session-delegated evidence only. No official full-eval acceptance or stable winner. Inspect missing outputs and grades.';process.stdout.write(generateHtml(ir));"
    result = subprocess.run(["node","--input-type=module","-e",script,str(root),plan["skill_name"]],capture_output=True,timeout=30)
    if result.returncode:
        raise ValueError("Official viewer failed: " + result.stderr.decode(errors="replace")[:500])
    if len(result.stdout) > 8*1024*1024:
        raise ValueError("Viewer output budget exceeded")
    new_output(destination)
    new_output(summary_destination)
    with destination.open("xb") as stream:
        stream.write(result.stdout)
    write(summary_destination, summary)
    return {"report":str(destination), **summary}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command",required=True)
    p = commands.add_parser("prepare"); p.add_argument("skill"); p.add_argument("workspace"); p.add_argument("--eval-set",required=True); p.add_argument("--model",required=True); p.add_argument("--ids",type=int,nargs="+")
    for name in ("record","grade"):
        p = commands.add_parser(name); p.add_argument("workspace"); p.add_argument("run"); p.add_argument("file"); p.add_argument("--delegate-id",required=True); p.add_argument("--model",required=True)
    p = commands.add_parser("status"); p.add_argument("workspace")
    p = commands.add_parser("report"); p.add_argument("workspace"); p.add_argument("--viewer",required=True)
    a = parser.parse_args()
    try:
        if a.command=="prepare": result=prepare(a.skill,a.eval_set,a.workspace,a.model,a.ids)
        elif a.command=="record": result=record(a.workspace,a.run,a.file,a.delegate_id,a.model)
        elif a.command=="grade": result=grade(a.workspace,a.run,a.file,a.delegate_id,a.model)
        elif a.command=="status": result=status(a.workspace)
        else: result=report(a.workspace,a.viewer)
        print(json.dumps(result,indent=2,ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(str(error),file=sys.stderr); return 1
    return 0

if __name__ == "__main__": sys.exit(main())
