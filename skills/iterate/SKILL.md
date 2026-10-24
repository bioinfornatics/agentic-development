---
name: iterate
description: Turns judge findings or failed verification into bounded corrective development while preserving accepted outcomes and invalidating stale proofs. Use for addressing rejected or indeterminate slices, repeated failures, or newly discovered scope risks.
---

# Iterate

## Select the action from the intent

Resolve the findings, candidate, retained proof, current permissions and correction counter. Classify the gap before selecting a corrective action; diagnosis and waiting do not consume attempts.

| Intent / condition | Execute | Required result |
|---|---|---|
| Correct an evidenced implementation defect | Check current scope, reproduction, capability and budget; route the smallest authorized correction to Implement | Corrective task with symptom-specific verification and attempt counter |
| Supply missing proof without changing behavior | Route available checks to Test; wait on unavailable capability without consuming a correction round | New proof or precise prerequisite, with valid prior evidence retained |
| Resolve a research gap or changed requirement | Route uncertainty to Research, changed scope/criteria to Plan and unresolved authorization to the user | Decision-grounded next task; no speculative repair |
| Budget is exhausted or repeated attempts make no progress | Stop corrective execution and preserve the candidate, evidence and restart context | Blocker, bounded options and required decision; no extra attempt |

Execute the selected action through the workflow below. Read only the references
required by that action, reuse guidance already loaded in this context, and verify
the result before taking the next action. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

## Structured requirements and output format

Read [the requirements and output contract](references/requirements-output.md)
for Goals/Non-goals, functional Given/When/Then criteria, relevant quantified NFRs
and the mandatory seven-field final report with phase-specific evidence and notifications.
Produce this phase's artifact using the contract's headings; map every result to
its verified criterion ID/target and mark unresolved or N/A fields explicitly.
Do not invent metrics, Git results, session launches or acceptance to fill a field.

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

1. Read the available judgment or failed-check evidence, current candidate and
   verified task scope. Consult the roadmap when it exists; a missing roadmap or
   not-run Judge does not prevent diagnosis of an evidenced failed check. Verify
   the diff has not drifted. Preserve accepted outcomes and initial user work.
2. Classify each open item as implementation defect, missing proof/capability,
   research gap or scope/acceptance decision. Link it to evidence and criterion.
3. Before starting a correction, check required capabilities and remaining budget.
   If a required capability is unavailable, stop and report the blocker, preserved
   state and prerequisite. A capability-only stop is not a correction attempt:
   do not increment the round counter. Preserve unchanged, still-current proofs;
   invalidate only evidence whose inputs changed or whose freshness failed.
   Do not fabricate a test or waive its gate because a capability is missing.
4. Prioritize blocking findings and define the smallest corrective task, its
   owned scope and expected verification before dispatch. Never delete tests or
   weaken criteria to manufacture a pass. Scope expansion and destructive changes
   require current authorization. Missing proof alone does not justify a code repair.
5. Recheck capability, permission and remaining budget for the selected action.
   For a phase-only request, return the proposed handoff without starting an attempt.
   Increment the round counter only when an authorized correction attempt begins,
   immediately before executing or dispatching that correction, not during diagnosis,
   planning or waiting. Record the before/after counter in the permitted state.
   Never start a correction after its budget is exhausted.
6. Load Implement then Test for implementation defects, Test for missing proof,
   Research for unknown causes, or Plan for changed scope/criteria; request unresolved
   user decisions instead of dispatching unauthorized work. Stay in the same
   branch/session for related repairs unless an actual transition trigger applies.
   Invalidate only proofs/judgment affected by changed inputs or freshness failures;
   preserve other current candidate-bound evidence with explicit justification.
   Re-test repaired paths and relevant regressions, then return the frozen candidate
   to Judge. Acceptance never transfers automatically to changed code.
7. Record the outcome or capability-only stop in iteration.md and the agreed
   tracker/artifacts; emit the common checkpoint. If the correction budget
   (default three rounds) is exhausted or failures repeat, stop and present
   blocker, options, preserved artifacts and a decision or prerequisite.
   Never start a correction after its budget is exhausted.

## Session and completion boundaries

Objective change or judge role may justify a fresh context, but never implies a
commit. Include dirty/staged/untracked state and exact resume conditions in the
handoff. Close only after the scoped acceptance gate passes; leave unmet real
validation work open. No automatic push, merge or production promotion.

## Conditional reporting details

Read [the commit report](references/commit-report.md) only for a proposed,
performed, failed or externally observed commit. Read
[the session report](references/session-report.md) only for planned session end,
explicit wrap-up or recommended context transition. The common communication
contract remains mandatory; do not reload identical content already present in
the current context. Combine overlapping reports without dropping required fields.

## Corrective task and output contract

Turn each blocking finding into the smallest evidence-producing correction or
prerequisite. Reuse a matching tracker task rather than create a task per hunk;
record its relation to the US/spec and the precise check that can disprove success.
If a diagnosis changes scope or a domain assumption, return to Research/Plan.
Do not add speculative functionality or rewrite unrelated accepted outcomes.

Produce the phase artifact with the canonical headings in
[the requirements and output contract](references/requirements-output.md).
Record the counter before/after: waiting or diagnosis is not an attempt, while an
authorized correction consumes one. Preserve still-current proof; invalidate actual
input/freshness drift only. Re-run the original symptom and relevant regressions,
remove temporary instrumentation and return the changed frozen candidate to Judge.

## Execute the handoff or stop

Execute the next phase only when it belongs to the user's requested workflow and
current scope/permissions cover its actions. For a phase-only request, return the
phase result and proposed handoff, then stop; do not expand the request by loading
or executing a new phase. If continuing is authorized, apply the routes below.

For an authorized implementation correction, Load `agentic-development:implement`
with its task, reproduction, owned paths and remaining budget, then route the changed
candidate through Test and Judge. For proof-only work, Load
`agentic-development:test` with the missing criterion and unchanged candidate.
Load `agentic-development:research` for unknown causes, or
`agentic-development:plan` for changed scope/criteria; request the real
permission or scope decision rather than inventing it.

Use the host's available Skill-loading mechanism; these identifiers are not shell
commands. If loading is unavailable, read the selected bundled SKILL.md and its
required contained references, and report direct reading rather than activation.
Pass a copy-ready handoff if execution cannot continue in this context. State the
specific missing input, permission or capability, who can supply it when known,
and the next executable action. Do not merely say "blocked" or "continue later".

End every phase delivery with the mandatory seven-field final report from
[the requirements and output contract](references/requirements-output.md), including
blocked or unchanged results. Keep the ordered fields and explain the next gate.
