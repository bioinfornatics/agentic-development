---
name: iterate
description: Coordinates bounded corrective development. Use for judge findings, failed verification, missing proof, repeated failures or newly discovered scope risks.
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
required by that action, reuse unchanged guidance already loaded in this context, and verify
the result before taking the next action. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

## Workflow

Read each reference when its local condition applies, before the governed action
even if needed earlier than its numbered stage. Reuse unchanged loaded guidance.
These stages do not authorize additional phases or side effects.

1. [ ] **Recover scope and current authority**

   Read [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria or verification, and before implementation.
   Reuse verified Goals/Non-goals, FR/GWT and applicable quantified NFRs; do not
   invent targets. Investigation needs a bounded question, not a completed plan.

   Read [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions. Recorded permissions
   are historical unless their current authoritative source and scope are verified.

   If the repository uses Beads, read [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Use fresh `bd prime` guidance;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   Read [the communication contract](references/communication-contract.md) before preparing
   the first checkpoint or a Git/session transition, for ownership, transition, evidence
   and conditional UI reporting safeguards. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   Use the coordinator's verified slice state when available; do not fabricate execution or acceptance.

2. [ ] **Bind evidence and classify the gap**

   Read [candidate identity](references/candidate-identity.md) before planning checks,
   freezing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions. Read [the review policy](references/review-policy.md)
   before agreeing acceptance, judging or closing a task/US. Independence and closure
   requirements are set before implementation, not waived by a missing capability.
   For exact-candidate proof, use the contained [capture/validate/compare CLI](scripts/candidate_identity.py) with the [scope example](references/candidate-scope.example.json); consult the [manifest schema](references/candidate-identity.schema.json) and [manifest example](references/candidate-identity.example.json) when preparing or validating its JSON. Follow the candidate procedure above; equality is not acceptance.

   Read the available judgment or failed-check evidence, current candidate and
   verified task scope. Consult the roadmap when it exists; a missing roadmap or
   not-run Judge does not prevent diagnosis of an evidenced failed check. Verify
   the diff has not drifted. Preserve accepted outcomes and initial user work.

   Classify each open item as implementation defect, missing proof/capability,
   research gap or scope/acceptance decision. Link it to evidence and criterion.

3. [ ] **Check capability and remaining budget**

   Before starting a correction, check required capabilities and remaining budget.
   If a required capability is unavailable, stop and report the blocker, preserved
   state and prerequisite. A capability-only stop is not a correction attempt:
   do not increment the round counter. Preserve unchanged, still-current proofs;
   invalidate only evidence whose inputs changed or whose freshness failed.
   Do not fabricate a test or waive its gate because a capability is missing.

   An attempt begins only with authorized corrective execution, not diagnosis, planning or waiting. Default maximum: three authorized attempts unless the user explicitly approves another bound. Zero-budget diagnosis/waiting remains allowed and consumes zero attempts; it never resets the counter. Stop corrective execution on exhaustion or repeated no-progress.

4. [ ] **Define the smallest corrective task before dispatch**

   Prioritize blocking findings and define the smallest corrective task, its
   owned scope and expected verification before dispatch. Never delete tests or
   weaken criteria to manufacture a pass. Scope expansion and destructive changes
   require current authorization. Missing proof alone does not justify a code repair.
   For an implementation defect, require a symptom-specific red reproduction before
   repair; a missing public seam, fixture or access is a prerequisite, not repair proof.

   Reuse a matching tracker task rather than one per hunk; link its US/spec and
   precise corrective check. Changed scope/domain assumptions require Research/Plan,
   not speculative functionality or unrelated rewrites.

5. [ ] **Verify available outcomes and preserve restart state**

   Record diagnosis, waiting and corrections actually performed, not merely proposed, and actual counter before/after. If delegated, verify actual invocation/completion status, source/candidate identity and result locators; incomplete results remain provisional.

   For returned repairs, re-run the original symptom and relevant regressions, remove temporary instrumentation and verify candidate freshness. Invalidate only proofs/judgment affected by changed inputs or freshness failures; preserve current candidate-bound evidence with explicit justification. Acceptance never transfers to changed code; prepare the frozen candidate for Judge.

   Collect iteration.md facts in approved tracker/artifacts or inline if persistence is unavailable: classification, actions/results, retained/invalidated proof, counter and limits. Keep unmet real validation open; this phase grants no closure permission. Related repairs stay in the branch/session unless an actual transition trigger applies; objective change or Judge role may justify fresh context, never an implicit commit. Preserve dirty/staged/untracked state and exact resume conditions. Prepare immediate action, owner and prerequisite separately from conditional later phases.

6. [ ] **Read delivery guidance and draft the phase response**

   After investigation and immediately before drafting any user-facing phase response (including blocked or unchanged results), read [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and five-section report. Before drafting a proposed, performed, failed or externally observed commit report, read [the commit report](references/commit-report.md). Before drafting a planned session end, explicit wrap-up or recommended context transition report, read [the session report](references/session-report.md). Reuse unchanged guidance already loaded; combine overlapping reports without duplication.

   After reading delivery guidance, draft the actual handoff fenced YAML state card and copy-ready restart prompt; distinguish proposed from performed actions.

7. [ ] **Execute the handoff or stop**

   Execute the next phase only when it belongs to the user's requested workflow and
   current scope/permissions cover its actions. For a phase-only request, return the
   phase result and proposed handoff, then stop; do not expand the request by loading
   or executing a new phase. If continuing is authorized, apply the routes below.

   Immediately before executing or dispatching an authorized correction, recheck capability, current permission, red-before-repair and remaining budget. For phase-only requests return the proposal without starting an attempt. Increment and record the before/after counter in permitted state BEFORE dispatch; stop if required recording is unavailable. Diagnosis, planning and waiting never increment it. Never start after exhaustion or repeated no-progress.

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

   On return verify outcomes through the evidence steps before any new dispatch. No automatic extra attempt, closure, push, merge or production promotion.
