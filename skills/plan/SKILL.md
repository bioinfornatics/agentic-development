---
name: plan
description: Defines software roadmaps, user stories and executable task graphs with criteria, dependencies and verification gates. Use for planning from established research or creating and updating project tickets.
---

# Plan

## Select the action from the intent

Before planning, verify research coverage and freshness for the product purpose,
user outcome, current behavior and constraints relevant to the objective.
A clear request is not a substitute for research. If this baseline is absent or
a decision-critical gap remains, return the targeted prerequisite to Research;
for a phase-only request report that prerequisite rather than execute another
phase without permission. Reuse verified context and carry nonblocking assumptions
explicitly. Then resolve planning level, tracker and current write permissions.

| Intent / condition | Execute | Required result |
|---|---|---|
| Create or refine a roadmap | Define outcomes, success evidence, ordering and major dependencies; detail only the near-term frontier | Proposed or currently approved roadmap, with approval status and next outcome |
| Structure an epic or user story | Define capability or observable user behavior, Goals/Non-goals and requirement-derived criteria | Epic/US scope, relevant error paths, measurable NFRs and verification matrix |
| Turn research or a US into executable tasks | Decompose by independently reviewable result, assign exclusive ownership and prerequisite edges | Ready task graph with inputs, outputs, permissions, checks and task-ID-only restart context |
| Create or update tickets in the agreed tracker | Inspect existing issues, reuse matching work and perform only authorized writes; read back each changed issue | Actual IDs, verified fields/edges and next ready task; failed writes remain failed |

Use the workflow below for the selected planning level. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

## Workflow

A phase report is the result of this Skill, not a file to find before execution.
Collect its facts during work; deliver them inline by default at the delivery step.
Save a report only with an explicit destination and permission to write, following
the common output contract loaded at that step. Required evidence inputs and tracker
updates retain their own gates; an inline response does not replace task truth.

Apply contracts before their governed actions, even before the nominal step
containing the link when its condition arises earlier. Load a reference only when its
applicable content is absent, incomplete or outdated in the active context; reuse
identical available content from another Skill's contained copy. The same ID/version
with different content is a conflict, not proof of identity: resolve it before the
affected action. A previous read or loaded marker does not prove availability.
After compaction, a new session or worker, recover required unavailable instructions;
on workspace changes revalidate applicability. Reusing authorization guidance never renews
a previous permission. This is an agent instruction, not a runtime cache.

1. [ ] **Verify planning inputs and authority**

   Read the objective and cited research context; verify coverage and freshness
   before planning. Missing decision-critical context routes to Research, not
   speculative implementation. Verify approval status and inspect root, branch,
   dirty files and dependencies; do not invent roadmap approval or accepted outcomes.

   Apply [the communication contract](references/communication-contract.md) when preparing
   the first checkpoint or a Git/session transition, for ownership, transition, evidence
   and conditional UI reporting safeguards. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   Use the coordinator's verified slice state when available; do not fabricate execution or acceptance.

   Before creating or repairing task descriptions or acceptance criteria, apply
   [ticket authoring](references/ticket-authoring.md); verify readable purpose,
   criteria, ordered inputs and restart context without duplicating execution history.

   If the repository uses Beads, apply [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Use fresh `bd prime` guidance;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   Apply [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions; verify current
   permission for the intended action, not historical approval.

2. [ ] **Define the requested outcome and scope**

   Apply [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria or checks. Resolve the approved task baseline;
   retain Goals/Non-goals, FR/GWT and relevant NFRs; keep missing requirements explicit.

   Plan at the requested level: roadmap outcomes, epic capability, user story
   behavior or independently reviewable tasks. Define in/out scope, observable
   criteria and milestones; detail the ready frontier, not all distant work.
   Separate mock/local acceptance from installed-package,
   real-provider or production requirements. Keep open criteria visible.

3. [ ] **Set verification and review gates**

   Apply [candidate identity](references/candidate-identity.md) when planning checks,
   freezing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions.
   For exact-candidate proof, use the contained [capture/validate/compare CLI](scripts/candidate_identity.py) with the [scope example](references/candidate-scope.example.json); consult the [manifest schema](references/candidate-identity.schema.json) and [manifest example](references/candidate-identity.example.json) when preparing or validating its JSON. Follow the candidate procedure above; equality is not acceptance.

   Apply [the review policy](references/review-policy.md)
   before agreeing acceptance, judging or closing a task/US. Independence and closure
   requirements are set before implementation, not waived by a missing capability.

   Apply [the default judgment rubric](references/judgment-rubric.md) before agreeing
   acceptance unless an explicitly approved replacement is supplied. Record its
   version and the review-policy independence/closure decision in the plan.

   Select weighted or predefined small-task review mode before implementation; retain
   any user-required numeric score. Map each criterion to a test or observation and required capability. Include
   negative paths, cancellation/error states, regressions and risk-based security.
   Agree rubric identity/version, required independence and closure authority
   before implementation. Use proportional checks for a narrow task without
   claiming broader US or release acceptance.

4. [ ] **Build the ready task frontier**

   Plan from verifiable roadmap outcomes to an epic capability, user-story behavior,
   then coherent tasks. US is a convention, not an assumed tracker type. Detail the
   next executable frontier; retain distant needs, risks and major dependencies.
   A task is small when its result can be reviewed and resumed independently, not
   because it edits few files. Do not split by function/file or phase mechanically.

   For each task record: Goal; Parent outcome/specification; Scope and exclusions;
   Inputs and expected output; Observable acceptance/error paths; Blocking dependencies;
   Verification and public seams; Ownership and permissions; Durable context and restart.
   Research tasks instead state the question and evidence-producing deliverable.
   Distinguish parent hierarchy from dependency direction; bd dep add A B means A
   waits on B when Beads applies. A fresh session with only the task ID must be able
   to recover what, why, boundaries and checks. Fill gaps before declaring ready.

   Agree meaningful behavior seams before tests; reuse an already authorized seam
   without repetitive confirmation. Record what each seam catches and misses.

   For the near-term implementation frontier, break work into coherent tasks with
   exact target paths, exclusive ownership, prerequisites and expected outputs.
   For distant roadmap outcomes, record needs, risks and dependencies instead;
   do not invent file paths, numeric targets, owners or approval. Multiple tasks/commits may share one
   branch. If an independent review slice needs a different branch, announce
   current branch fit, proposed base/name and permission before any Git action.

   For UI work describe objects and CRUD (or N/A), changed zones using +/~/-/=,
   an ASCII sketch and the real visual verification planned. A drawing is not
   a rendered proof. Resolve product/UX choices rather than invent approval.

5. [ ] **Prepare and verify the planning report**

   Collect planning report facts: checks, candidate identity strategy, permissions,
   unresolved decisions, rollback considerations and iteration stop budget. Deliver
   them inline by default; save only at an explicitly authorized destination.

   Create or update issues only when requested/authorized in the agreed tracker.
   Inspect existing issues first, reuse matching work, verify supported fields and
   write goals, exclusions, criteria, dependencies, ownership and restart context.
   Include Research's verified task-specific reading references: files or authorized
   local web captures, entrypoints/sections, reasons, order, source identity and
   freshness/accessibility limits. Do not copy full research into tickets or invent
   saved resources; record local-only pointers honestly.
   Distinguish parent hierarchy from prerequisites. After each write, read back
   the issue and verify fields/edges; report actual IDs and errors. If writes are
   not authorized, return proposed tickets without claiming they were created.

   Verify actual delegated planning completion, source identity and result locator
   before integration. Reconcile conflicts and retain unresolved decisions and missing
   proof. Failed or missing worker results remain provisional. Collect source-linked
   phase facts; source-only checks remain static, not acceptance.

   A previously authorized, unambiguous plan can proceed without a new ritual
   approval. Ask for actual scope/safety trade-offs or permissions not granted.
   Do not start code changes under unresolved blocking assumptions. Retain proposed commit boundaries and the plan-time independent review policy
   for the response drafted in the next step.

6. [ ] **Verify readiness and draft the phase response**

   - Verify the cited product-context baseline, requested planning level, scope and approval status; expose decision-critical gaps and carry nonblocking assumptions explicitly.
   - Check the planning artifact's criteria, verification matrix, review policy and next executable frontier; when tasks or tickets are in scope, verify inputs, outputs, dependencies, ownership, permissions and restart context. Read back actual tracker writes when applicable; distinguish proposed tickets from created ones.
   - Prepare the immediate next action and blockers; collect verified reading pointers and permissions for any proposed handoff; format them after the output-contract application below.
   - After investigation and before drafting any user-facing phase response (including blocked or unchanged results), apply [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and five-section report.

   Apply [the commit report](references/commit-report.md) only for a proposed,
   performed, failed or externally observed commit. Apply
   [the session report](references/session-report.md) only for planned session end,
   explicit wrap-up or recommended context transition. The common communication
   contract governs these checkpoints; combine overlapping reports without duplication.

   After reading delivery guidance, draft the response and, at an actual handoff,
   the fenced YAML state card and copy-ready restart prompt.

7. [ ] **Execute the handoff or stop**

   Execute the next phase only when it belongs to the user's requested workflow and
   current scope/permissions cover its actions. For a phase-only request, return the
   phase result and proposed handoff, then stop; do not expand the request by loading
   or executing a new phase. If continuing is authorized, apply the routes below.

   When a task is ready and implementation is authorized, Load `agentic-development:implement`
   with its verified ID/context, scope, criteria, public seams, owned paths, checks and
   review policy. For an unresolved technical prerequisite, Load
   `agentic-development:research` with the specific question. For roadmap-only
   work, return the planning artifact and next ready task; do not start implementation.

   Use the host's available Skill-loading mechanism; these identifiers are not shell
   commands. If loading is unavailable, read the selected bundled SKILL.md and its
   required contained references, and report direct reading rather than activation.
   Pass a copy-ready handoff if execution cannot continue in this context. State the
   specific missing input, permission or capability, who can supply it when known,
   and the next executable action. Do not merely say "blocked" or "continue later".
