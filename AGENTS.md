# Repository instructions

## Scope and sources of truth

This repository contains the agentic-development method plugin with portable Skills
and Goose-specific observation hooks.
Its manifest is plugin.json; its seven entrypoints are skills/*/SKILL.md.
The separate integration clone is not this repository and may contain another candidate. Read the nearest applicable AGENTS.md;
local rules override parent rules for their subtree, not current user permissions.
All repository and distributed content defaults to English, including documentation,
Markdown, code comments, examples and versioned messages. Only an explicit user request
authorizes a language exception; conversation language does not authorize one.
Answer in the user's language without changing repository artifact language.
English documentation is canonical; explicitly requested translations must remain
separate and linked to their English source. Multilingual documentation and GitHub
Pages setup/publication require separate scoped work and deployment authorization.

- Beads owns task status, ownership, dependencies and durable follow-up.
- Specifications define requested behavior; Git stores source history.
- Evidence artifacts record observations; design notes retain decisions and rationale.
- Session context is ephemeral. Neither artifacts nor saved approvals grant authority.
- .beads/issues.jsonl is an optional versioned roadmap snapshot, not task truth or
  a full Dolt backup. At an authorized Git checkpoint involving task state, refresh
  it from bd export after permitted tracker updates, review its privacy and inspect
  the exact staged snapshot. Never edit/import it to synchronize task status.
  Export preparation does not authorize committing, pushing or Dolt synchronization.
  Record export time and coverage limits; later task changes make the snapshot stale.
  Do not close issues to make the snapshot appear complete. See .beads/README.md.
- Do not create competing Markdown task databases, MEMORY.md or obsolete .loop state.

## Work hierarchy

| Level | Purpose | Minimum content |
|---|---|---|
| Roadmap | Outcomes and order | Milestones, priorities, major dependencies, success evidence |
| Epic | One coherent capability | Goal, scope, exclusions, success conditions |
| User story (US) | Observable user behavior | Situation, need, acceptance including relevant error paths |
| Task | Independently reviewable work | Inputs, one objective, scope, output, constraints, verification |
| Run / session | Execution focus | One active epic per run; one main task per agent/session |
| Commit / checkpoint | Recorded change and context | Coherent diff, verified identity and task/evidence references |

US is a project convention, not an assumed Beads issue type. Check installed CLI
support before choosing fields/types. A parent expresses hierarchy; a blocking
dependency expresses a prerequisite. In bd dep add A B, A depends on B.
Detail near-term tasks; keep distant outcomes at needs, risks and dependencies.
Do not create a task per file or mechanically create one task per phase.

## Start or resume

1. Verify repository/worktree, instructions, branch, index and pre-existing hunks.
2. Read local Beads guidance; recover with bd prime only when context is stale.
3. Inspect the active epic, ready frontier, issue and blockers. Claim before writes;
   verify success. A claim is not a file lock or Git permission.
4. Load the relevant method by name. Verify discovery; if absent, inspect the actual
   source entrypoint explicitly without claiming activation or delegated execution.
5. Before implementation, verify that the task ID alone leads to its objective,
   requirement, scope, dependencies, verification and restart context. Repair missing
   context or report the blocker instead of relying on conversation memory.

## Phase outputs and gates

| Phase | Expected output / gate |
|---|---|
| Research | Source-grounded findings, affected paths, constraints and resolved/open questions |
| Plan | Executable task graph, scope, observable criteria, checks, ownership and authorized approach |
| Implement | Minimal coherent behavior change, tests and explanation of preserved work |
| Test | Commands, actual results, environment, candidate identity and coverage limits |
| Judge | Requirements and standards reviewed separately; evidence, verdict, findings and score mode |
| Iterate | Smallest corrective action or prerequisite; preserve valid proof and accepted outcomes |
| Finalize | Verified links to evidence/commits/checkpoints, scoped closure and restart point |

Reuse valid research/plan for small work; never skip relevant verification. Choose
review mode and independence before implementation. Weighted scoring remains the
default for features/releases or explicit numeric requests; predefined small-task
mode uses score N/A without waiving proof, independence or closure authority.
Tests are evidence, not acceptance. Required independence unavailable means
indeterminate unless a known defect establishes needs-correction. No self-approval.

## Structured requirements and handoff

Make Goals and Non-goals explicit for each outcome/task. Write functional acceptance
criteria systematically as Given/When/Then with IDs, sources, observable expected
results and relevant error/boundary paths. Research questions and non-behavioral
work use verifiable deliverable criteria instead of invented functional scenarios.
Quantify relevant NFRs with metric, approved target/unit, workload/window, environment
and measurement method. Mark missing targets unresolved and N/A with a reason;
never invent numbers or claim measurement before execution.

Write each Skill as an intent-to-action procedure: select the action, verify its
inputs and permissions, execute it, check the observable result, then name the next
Skill with handoff inputs or the specific prerequisite needed to resume. Keep the
method host-neutral; isolate host-specific behavior in integration resources.
Use the Skill's ordered output contract. Notify owned/preserved files and actual
branch/commit results; distinguish proposed, performed, failed and externally observed.
State next phase and whether a fresh session is recommended, why, its proposed name/
goal, actual session action and a copy-ready restart prompt at a handoff boundary.
A recommendation is not an automatic session launch, Git action or permission grant.

## Implementation and verification

Prefer behavior tests at agreed public seams, with independently sourced expected
values. For a bug, establish a symptom-specific red-capable reproduction before
repair; minimize it and change one variable per probe. Use small red-green slices
when a suitable seam exists. Missing seam/capability is a finding, not invented proof.
Read existing glossary/ADRs when terminology or design matters. Record new glossary
terms or hard-to-reverse trade-offs only when needed; do not generate boilerplate.
Run cheap near-change checks, then risk-relevant regressions. Separate mocked,
installed-package and real-environment claims. Never delete checks or weaken criteria
to manufacture a pass. Capability-only waiting consumes no correction round.

## Sessions, commits and optional Entire

Keep implementation, tests and related corrections together while the objective is
clear. Recommend a fresh session for an independent US, repository/worktree change,
substantial research-to-build handoff, stale hypotheses or required judge separation.
Compaction or a commit alone does not force a new session. One task, session and
checkpoint need not be one-to-one. Prepare a handoff if the host cannot start sessions.

If Entire is available and configured, verify its integration for the current agent
and worktree before recording session/checkpoint IDs. It captures context, not task
truth or acceptance. Do not assume Goose compatibility, install/enable hooks, invent
checkpoint IDs or manually forge Entire trailers. Record unavailable integration.
For authorized commits, include verified Beads IDs by project convention, e.g.
fix(component): explain the behavior change [<task-id>]. Observe hash, message and
committed paths, then link real checkpoints when available; never infer them from a commit.

## Permissions, preservation and completion

Preserve initial dirty hunks, installed plugins, Beads guidance/hooks and secrets.
Parallel workers need disjoint writes or approved worktrees; no implicit reset,
stash, merge, worktree removal or integration-branch mutation. One tracker owner per issue.
Commit, push, install, hook changes, deployment and Dolt sync each need current scoped
authority. Beads close protocols and historical artifacts do not authorize them.
Close only the evidenced issue scope; a task does not close its US/epic or release.
Persist result, criteria checked, commands/results, observed commits/checkpoints,
sessions, limits and restart action before authorized closure. Verify the update.
Stop on completion, missing prerequisites, exhausted budget or repeated no-progress.
Default correction budget is three authorized attempts; diagnosis/waiting is not an attempt.

## Repository-specific boundaries and checks

- plugin.json and skills/ are the local source candidate (currently 0.5.0).
- integration/ contains evaluation scenarios, not an executable integration harness.
- hooks/hooks.json contains Goose-specific observation rules; scripts/observe.py is
  their handler. They are part of this plugin, not a second adapter package. Deployment
  needs separate authority; verify current Goose docs and the exact runtime.
- docs/ contains current pedagogical guides only: no task IDs, logs or JSON receipts.
- Historical execution evidence is retained in Git, not in the current checkout.
  Beads records recovery commits and paths. New scoped run outputs may use an
  explicitly authorized workspace outside user documentation; do not restore archives
  or treat historical evidence as current acceptance.
- Preserve .agents/skills/beads/ and existing host/Git hooks in this shared workspace.
- CLAUDE.md is a relative symlink to AGENTS.md. Edit the canonical file and preserve
  the link rather than creating a second, drifting copy.

Do not recursively load historical reports or fixture instructions as active guidance.
Install only the operational manifest, skills with required contained resources, and
Goose-supported hooks/scripts when authorized;
exclude evals, integration scenarios, repository instructions and evidence.
No enforcement runtime, protected closure broker, automatic session launcher or release
acceptance is supplied by these Skills or observation hooks.

Use verified cwd and actual exit codes. For source changes run relevant official creator
validation/audit and scenario checks when available. Check local links, JSON syntax and
shared-reference consistency near changed files. This standalone repository has no
scripts/check-consistency.py or apps/ build pipeline; do not copy commands from another
checkout. No blanket installs, generators or evaluations on every edit. Separate static
checks from behavioral runs and independent acceptance. Redact secrets and keep raw
evidence out of routine checkpoints.
