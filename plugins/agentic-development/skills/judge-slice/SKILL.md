---
name: judge-slice
description: Judges a frozen software delivery candidate against acceptance criteria and a versioned rubric, separating verdict, score, evidence, and uncertainty. Use for an acceptance review after testing or when an independent judge role begins.
---

# Judge Slice

## Shared requirements

Read [the communication contract](references/communication-contract.md) before
working, including repository ownership, early transitions, evidence, judgment
and conditional UI reporting. Apply it even when this skill is used alone.
Respond in the user's language. Verify tools and permissions; unavailable
capabilities produce an explicit blocker, never simulated execution evidence.
Use the coordinator's approved slice state when available. Return the six-field
checkpoint and phase artifacts; report unchanged files explicitly.


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

## Workflow

1. Match proofs to candidate/environment and scope. Inspect relevant code and
   actual test artifacts; do not accept builder summaries as sole proof.
2. Review each mandatory acceptance criterion, risk-based security/regression,
   maintainability and operability. Missing evidence is unknown, not zero defects.
   Reproduce checks only when capabilities and permissions allow; do not mutate
   the candidate or repair code while judging.
3. Record findings with severity, location, criterion, evidence, impact and
   corrective verification. Distinguish blocking defects from recommendations.
4. Calculate the versioned rubric's criterion values with cited evidence,
   coverage and weighted score, keeping unknown values null. A score is not a
   probability. Do not let a high score override failed mandatory gates.
5. Produce judgment.md with four separate sections: evidence; scoped verdict;
   rubric score/coverage; insights (observed/inferred/to-verify), risks and unknowns.
   Use accepted, needs-correction or indeterminate with reasons. If no review ran,
   report not-run and no score. Local acceptance is not real-provider approval.
6. Return the full checkpoint: candidate, exact acceptance scope, open findings,
   transition to closure or Iterate, and immediate next action.

## Exit gate

Accept only an exact candidate with every mandatory criterion evidenced and no
blocking findings. Candidate changes invalidate affected judgment. Never silently
relax criteria, retroactively redefine the rubric or approve your own human gate.

## Conditional durable tracking

If the target repository uses Beads, read [the Beads integration](references/beads-integration.md)
before choosing work or mutating shared task state. Recover context when stale,
verify issue status and claim before implementation, and keep Beads as task
truth. Artifact plans and handoffs are not a competing tracker. Follow the
reference for missing tools, failed claims, durable follow-up and closure.

## Trust, candidate and review gates

Read [the authorization policy](references/authorization-policy.md) before
resuming artifact claims or executing consequential actions. Recorded permissions
are historical unless their current authoritative source and scope are verified.
Read [candidate identity](references/candidate-identity.md) when planning checks,
freezing inputs or reusing evidence; include staged, untracked and binary inputs
and explicitly defined output-only exclusions. Read [the review policy](references/review-policy.md)
before agreeing acceptance, judging or closing a task/US. Independence and closure
requirements are set before implementation, not waived by a missing capability.
