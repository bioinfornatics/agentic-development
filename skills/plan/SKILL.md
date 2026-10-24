---
name: plan
description: Creates or refines software roadmaps, epics, user stories and executable task graphs with acceptance criteria, dependencies, ownership and verification gates. Use for planning outcomes, turning research into authorized implementation work, or creating and updating project tickets.
---

# Plan

## Select the action from the intent

Resolve the requested planning level, outcome source, existing research, tracker and current write permissions. If a critical assumption cannot be planned safely, route it to Research; otherwise record it and continue the authorized planning work.

| Intent / condition | Execute | Required result |
|---|---|---|
| Create or refine a roadmap | Define outcomes, success evidence, ordering and major dependencies; detail only the near-term frontier | Proposed or currently approved roadmap, with approval status and next outcome |
| Structure an epic or user story | Define capability or observable user behavior, Goals/Non-goals and requirement-derived criteria | Epic/US scope, relevant error paths, measurable NFRs and verification matrix |
| Turn research or a US into executable tasks | Decompose by independently reviewable result, assign exclusive ownership and prerequisite edges | Ready task graph with inputs, outputs, permissions, checks and task-ID-only restart context |
| Create or update tickets in the agreed tracker | Inspect existing issues, reuse matching work and perform only authorized writes; read back each changed issue | Actual IDs, verified fields/edges and next ready task; failed writes remain failed |

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

Read [the default judgment rubric](references/judgment-rubric.md) before agreeing
acceptance unless an explicitly approved replacement is supplied. Record its
version and the review-policy independence/closure decision in the plan.

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

1. Read the objective and any available research; verify approval status and inspect
   root, branch, dirty files and dependencies. Do not invent roadmap approval or accepted outcomes.
2. Plan at the requested level: roadmap outcomes, epic capability, user story
   behavior or independently reviewable tasks. Define in/out scope, observable
   criteria and milestones; detail the ready frontier, not all distant work.
   Separate mock/local acceptance from installed-package,
   real-provider or production requirements. Keep open criteria visible.
3. Select weighted or predefined small-task review mode before implementation; retain
   any user-required numeric score. Map each criterion to a test or observation and required capability. Include
   negative paths, cancellation/error states, regressions and risk-based security.
   Agree rubric identity/version, required independence and closure authority
   before implementation. Use proportional checks for a narrow task without
   claiming broader US or release acceptance.
4. For the near-term implementation frontier, break work into coherent tasks with
   exact target paths, exclusive ownership, prerequisites and expected outputs.
   For distant roadmap outcomes, record needs, risks and dependencies instead;
   do not invent file paths, numeric targets, owners or approval. Multiple tasks/commits may share one
   branch. If an independent review slice needs a different branch, announce
   current branch fit, proposed base/name and permission before any Git action.
5. For UI work describe objects and CRUD (or N/A), changed zones using +/~/-/=,
   an ASCII sketch and the real visual verification planned. A drawing is not
   a rendered proof. Resolve product/UX choices rather than invent approval.
6. Produce plan.md with checks, candidate identity strategy, permissions,
   unresolved decisions, rollback considerations and iteration stop budget in the
   authorized workspace, or return its content inline when persistence is unavailable.
7. Create or update issues only when requested/authorized in the agreed tracker.
   Inspect existing issues first, reuse matching work, verify supported fields and
   write goals, exclusions, criteria, dependencies, ownership and restart context.
   Distinguish parent hierarchy from prerequisites. After each write, read back
   the issue and verify fields/edges; report actual IDs and errors. If writes are
   not authorized, return proposed tickets without claiming they were created.

## Gate and handoff

A previously authorized, unambiguous plan can proceed without a new ritual
approval. Ask for actual scope/safety trade-offs or permissions not granted.
Do not start code changes under unresolved blocking assumptions. Return the
common checkpoint, proposed commit boundaries and the plan-time independent
review policy; use the routing below for the actual next phase.

## Conditional reporting details

Read [the commit report](references/commit-report.md) only for a proposed,
performed, failed or externally observed commit. Read
[the session report](references/session-report.md) only for planned session end,
explicit wrap-up or recommended context transition. The common communication
contract remains mandatory; do not reload identical content already present in
the current context. Combine overlapping reports without dropping required fields.

## Task graph and readiness contract

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

Produce the phase artifact with the canonical headings in
[the requirements and output contract](references/requirements-output.md).
Agree meaningful behavior seams before tests; reuse an already authorized seam
without repetitive confirmation. Record what each seam catches and misses.

## Before delivery or handoff

- [ ] Verify [the common output checklist](references/common-output.md): seven headings,
  verified tasks/goals/criteria, actual files, truthful Git/session status and next action.
- [ ] Verify [this phase's delivery checklist](references/requirements-output.md) and
  include its specific evidence, remaining criteria and recommended review order.
- [ ] At a handoff boundary include the worked state card inside explanation and a
  copy-ready restart prompt; distinguish recommendations from performed actions.
- [ ] Keep missing proof/independence open; report source-only checks as static.

## Execute the handoff or stop

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

End every phase delivery with the mandatory seven-field final report from
[the common requirements and output contract](references/common-output.md), including
blocked or unchanged results. Keep the ordered fields and explain the next gate.
