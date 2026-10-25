---
name: judge
description: Judges a frozen software delivery candidate against acceptance criteria and a versioned rubric, separating verdict, score, evidence, and uncertainty. Use for an acceptance review after testing or when an independent judge role begins.
---

# Judge

## Select the action from the intent

Resolve approved scope, frozen candidate, evidence index, review mode and independence policy. Identify the reviewer and validate provenance before deriving a verdict.

| Intent / condition | Execute | Required result |
|---|---|---|
| Review a tested candidate for acceptance | Verify scope, candidate, evidence and required independence; review every mandatory criterion | Scoped verdict, actionable findings and uncertainties |
| Review requirement fidelity and repository standards | Assess requested behavior separately from documented quality standards | Separate requirement and standards findings with sources and corrective checks |
| Score a candidate | Apply the review mode and rubric agreed before implementation | Evidence-derived weighted score/coverage, or N/A in predefined small-task mode |
| Evidence or required independence is missing | Record the exact gap; use indeterminate unless a known defect already requires correction | Specific prerequisite, not self-approval or an invented pass |

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

Read [the judgment rubric](references/judgment-rubric.md) before judging unless
an explicitly approved replacement rubric is supplied. Record its version.

## Prerequisites and independence

Require approved acceptance scope, frozen candidate identity, diff/ownership
ledger, evidence index and known limitations. Recommend an independent context
before judgment; announce the transition and prepare a handoff without an
automatic commit. Identify reviewer/context and all independence dimensions from review-policy.md.
Require the plan-time independence decision; default US acceptance requires
independent review. A new session alone is insufficient. If reviewing your own work in the
same context, disclose limited self-review; never claim independence. If required
independence is unavailable, the verdict is indeterminate unless a known blocker
already justifies needs-correction.

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

1. Match proofs to candidate/environment and scope. Inspect relevant code and
   actual test artifacts; do not accept builder summaries as sole proof.
2. Review each mandatory acceptance criterion, risk-based security/regression,
   maintainability and operability. Missing evidence is unknown, not zero defects.
   Reproduce checks only when capabilities and permissions allow; do not mutate
   the candidate or repair code while judging.
3. Record findings with severity, location, criterion, evidence, impact and
   corrective verification. Distinguish blocking defects from recommendations.
4. Apply the plan-time review mode in the versioned rubric. In weighted mode,
   calculate criterion values, coverage and score from evidence, keeping unknowns
   null. In small-task mode report score not-applicable, without numeric grading.
   Neither mode can override a failed mandatory gate or waive independence.
5. Produce judgment.md using the canonical artifact headings in the requirements
   and output contract. Keep evidence, scoped verdict, rubric mode/score and
   insights (observed/inferred/to-verify), risks and unknowns separate.
   Use accepted, needs-correction or indeterminate with reasons. If no review ran,
   report not-run and no score. Local acceptance is not real-provider approval.
6. Return the full checkpoint: candidate, exact acceptance scope, open findings,
   transition to closure or Iterate, and immediate next action.

## Conditional finding verification

For code review or specialist findings, read [finding verification](references/finding-verification.md)
before publishing claims. Check surrounding context and reachable failure paths,
separate observed from inferred evidence, justify severity by impact and consolidate
duplicates. Keep mandatory defects and missing-evidence gates; a filter against
unsupported findings is not permission to suppress a required acceptance failure.

## Exit gate

Accept only an exact candidate with every mandatory criterion evidenced and no
blocking findings. Candidate changes invalidate affected judgment. Never silently
relax criteria, retroactively redefine the rubric or approve your own human gate.

## Conditional reporting details

Read [the commit report](references/commit-report.md) only for a proposed,
performed, failed or externally observed commit. Read
[the session report](references/session-report.md) only for planned session end,
explicit wrap-up or recommended context transition. The common communication
contract remains mandatory; do not reload identical content already present in
the current context. Combine overlapping reports without dropping required fields.

## Separate review axes and actionable findings

Identify the requirement/specification and documented standards for the exact
candidate. Report requirement fidelity (missing, incorrect or unauthorized behavior)
separately from repository standards/maintainability. A passing standards review
cannot compensate for implementing the wrong behavior. Missing specification or
standard sources are disclosed, not invented. A pinned Git comparison is useful
but must include relevant staged, dirty and untracked inputs in candidate identity.

Treat code smells as labeled heuristics, not hard violations; project standards
take precedence over generic taste. Do not repeat automated checks as unsupported
manual findings. Use parallel read-only reviewers only when capabilities and
independence requirements are satisfied; different sessions/models alone are not proof.

Within judgment.md, include Requirement findings and Standards findings under the
evidence section. Each finding needs criterion/source, location, observation,
impact and minimal corrective check. Preserve the existing evidence/verdict/score/
insights separation; no invented numeric score or acceptance from builder assertions.

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

For needs-correction, Load `agentic-development:iterate` with the scoped
verdict, evidence-linked findings and minimal corrective checks. For indeterminate,
return the specific evidence/independence prerequisite, not a speculative correction.
For accepted, return the exact accepted scope to the coordinator or user; perform no
implicit issue closure, commit, merge or release.

Use the host's available Skill-loading mechanism; these identifiers are not shell
commands. If loading is unavailable, read the selected bundled SKILL.md and its
required contained references, and report direct reading rather than activation.
Pass a copy-ready handoff if execution cannot continue in this context. State the
specific missing input, permission or capability, who can supply it when known,
and the next executable action. Do not merely say "blocked" or "continue later".

End every phase delivery with the mandatory seven-field final report from
[the common requirements and output contract](references/common-output.md), including
blocked or unchanged results. Keep the ordered fields and explain the next gate.
