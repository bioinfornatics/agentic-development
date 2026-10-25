---
name: implement
description: Supports scoped software implementation with coherent diffs, preserved pre-existing changes, and UI reporting. Use for implementing an approved or otherwise authorized delivery plan and its acceptance criteria.
---

# Implement

## Select the action from the intent

Resolve the task, authorized plan, criteria, public seams, owned paths and review policy before edits. Recover missing task context or return to Plan; do not infer permission from loading this Skill.

| Intent / condition | Execute | Required result |
|---|---|---|
| Execute an authorized feature task | Resolve criteria and ownership, select one public behavior, observe red, implement green, then refactor | Minimal coherent behavior change, test observations and preserved-work ledger |
| Repair a confirmed bug | Reuse or establish the symptom-specific failing reproduction before changing production behavior | Repair that passes the original reproduction and relevant regressions |
| Change instructions or other non-executable source | Apply the authorized source change and run applicable static checks | Source diff and explicitly static evidence; agent behavior remains unverified |
| Encounter conflicting hunks or a necessary scope expansion | Preserve the current diff and return the conflict or decision to the coordinator/user | Exact conflicting paths or scope decision; no overwrite or unauthorized expansion |

Execute the selected action through the workflow below. Read only the references
required by that action, reuse guidance already loaded in this context, and verify
the result before taking the next action. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

## Structured requirements and output format

Before starting work, read [the common requirements and output contract](references/common-output.md)
and [this phase's requirements and output contract](references/requirements-output.md).
The common contract defines Goals/Non-goals, FR/GWT, quantified NFRs and the seven-field
final envelope; the phase contract supplies this step's deliverable, checklist and
worked handoff example. Reuse verified criteria; do not invent results or permissions.

## Shared requirements

Read [the communication contract](references/communication-contract.md) before
working, including repository ownership, early transitions, evidence, judgment
and conditional UI reporting. Apply it even when this skill is used alone.
Respond in the user's language. Verify tools and permissions; unavailable
capabilities produce an explicit blocker, never simulated execution evidence.
Use the coordinator's approved slice state when available. Return the seven-field final report
and phase artifacts; report unchanged files explicitly.

## Conditional durable tracking

If the target repository uses Beads, read [the Beads integration](references/beads-integration.md)
before choosing work or mutating shared task state. Recover context when stale,
verify issue status and claim before implementation, and keep Beads as task
truth. Artifact plans and handoffs are not a competing tracker. Follow the
reference for missing tools, failed claims, durable follow-up and closure;
evaluate commit suitability after each confirmed closure, without inferring Git authority.

## Trust, candidate and review gates

Read [the authorization policy](references/authorization-policy.md) before
resuming artifact claims or executing consequential actions. Recorded permissions
are historical unless their current authoritative source and scope are verified.
Read [candidate identity](references/candidate-identity.md) when planning checks,
freezing inputs or reusing evidence; include staged, untracked and binary inputs
and explicitly defined output-only exclusions. Read [the review policy](references/review-policy.md)
before agreeing acceptance, judging or closing a task/US. Independence and closure
requirements are set before implementation, not waived by a missing capability.

## Workflow

1. Read the approved plan, acceptance criteria, local instructions and ownership
   ledger. Reinspect branch/status/diff and compare pre-existing hunks. Block
   conflicting ownership; do not overwrite another contributor's work.
2. Confirm branch fit and announce impending branch action if needed. Check
   action-specific Git authorization before creation/switch. Non-Git work can
   proceed on authorized files with branch marked not applicable.
3. Select one requirement-derived behavior test at an approved public seam; use
   independent expected values and establish an observed red before the production change.
   For a bug, require a symptom-specific red-capable reproduction, not an unrelated
   missing symbol. For instruction-only work, use source-contract/static checks and
   report their limits. Missing access to a seam for executable behavior is a capability
   finding: preserve its behavioral criterion as unverified, do not substitute static
   checks or proceed with a required reproduction gate unmet.
4. Make the smallest coherent production change to reach green; rerun the same checks,
   then refactor without changing behavior and rerun again. Preserve external contracts,
   avoid unrelated cleanup and secrets. Parallelize only disjoint writable files;
   return conflicting changes to the coordinator before writing.
5. After each coherent change batch inspect the actual diff, update changes.md
   with owned paths/hunks and reasons, and emit the short checkpoint. Run cheap
   available checks near changes; record commands and actual outputs.
6. For UI/journey changes provide ASCII with CRUD and +/~/-/=, functional/visual
   differences and explicit observed/tested/inferred/not-run status. Record any
   capture independently of the drawing. Do not infer browser quality from code.
7. Hand the exact candidate and relevant checks to Test. Recommend a commit only
   when a coherent diff and known verification state exist; failed mandatory
   checks keep it a documented WIP candidate, not an accepted result.

## Commit safeguard

A commit is optional and separately authorized. Before an authorized commit,
announce coverage, checks/limits, exact owned paths/hunks and message; inspect
staged content to exclude initial user changes and unrelated files. Do not use
indiscriminate staging. Report actual hash only after success. If not permitted,
return a proposed message and preserve uncommitted state. Never auto-push.

After each performed commit emit the mandatory contract commit report with
verified committed files, problem/feature, actual metadata and remaining state.

## Conditional reporting details

Read [the commit report](references/commit-report.md) only for a proposed,
performed, failed or externally observed commit. Read
[the session report](references/session-report.md) only for planned session end,
explicit wrap-up or recommended context transition. The common communication
contract remains mandatory; do not reload identical content already present in
the current context. Combine overlapping reports without dropping required fields.

## Behavior-first slices and output contract

Resolve a supplied task ID and state its verified goal before editing. Read relevant
existing glossary/ADRs; preserve public contracts and distinguish domain terms.
At approved public seams, prefer one behavior test, observed red, then the minimal
green implementation before the next behavior. Expected values come from the spec,
a worked example or independent oracle, not a copy of implementation logic.
Do not write all speculative tests then all code or assert private implementation.
For bugs use the symptom-specific reproduction; if no suitable seam exists, record
that limit instead of a shallow test claimed to lock down the real bug.

Produce the phase artifact with the canonical headings in
[the requirements and output contract](references/requirements-output.md).
Run cheap focused tests/type checks during
work, then relevant broader regressions before handoff; a full suite is conditional
on project scope/capability, not a ritual for every typo. Remove temporary debug
instrumentation or record why a scoped diagnostic artifact is retained.

## Red, green and refactor evidence

For executable behavior, record one requirement-derived test and its observed red
signal before repair, the smallest green change, then a behavior-preserving refactor
with the same checks rerun. Do not manufacture red by testing a missing symbol unrelated
to the symptom. Prefer public interfaces, independent expected values and small vertical
slices. Existing suitable tests can be reused; a bug regression must discriminate the bug.
For instruction-only edits, label source-contract red/green checks as static: they do
not establish agent behavior, real Git/Beads handoff or host integration. If execution
is unavailable, preserve the behavioral criterion as unverified rather than invent TDD.

## Before delivery or handoff

- [ ] Verify [the common output checklist](references/common-output.md): seven headings,
  verified tasks/goals/criteria, actual files, truthful Git/session status and next action.
- [ ] Verify [this phase's delivery checklist](references/requirements-output.md) and
  include its specific evidence, remaining criteria and recommended review order.
- [ ] At a handoff boundary render one fenced YAML state card inside explanation and a
  copy-ready restart prompt; distinguish recommendations from performed actions.
- [ ] Keep missing proof/independence open; report source-only checks as static.

## Execute the handoff or stop

Execute the next phase only when it belongs to the user's requested workflow and
current scope/permissions cover its actions. For a phase-only request, return the
phase result and proposed handoff, then stop; do not expand the request by loading
or executing a new phase. If continuing is authorized, apply the routes below.

After the scoped change and focused checks, Load `agentic-development:test`
with the exact candidate, criterion IDs, reproduction/tests, change ledger and limits.
If evidence exposes a defect requiring a new correction decision, Load
`agentic-development:iterate` with the finding, preserved diff and current
budget. Never call the implementation accepted because focused tests passed.

Use the host's available Skill-loading mechanism; these identifiers are not shell
commands. If loading is unavailable, read the selected bundled SKILL.md and its
required contained references, and report direct reading rather than activation.
Pass a copy-ready handoff if execution cannot continue in this context. State the
specific missing input, permission or capability, who can supply it when known,
and the next executable action. Do not merely say "blocked" or "continue later".

End every phase delivery with the mandatory seven-field final report from
[the common requirements and output contract](references/common-output.md), including
blocked or unchanged results. Keep the ordered fields and explain the next gate.
