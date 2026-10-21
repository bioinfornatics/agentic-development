---
name: plan-slice
description: Plans a reviewable software delivery slice with acceptance criteria, file ownership, branch fit, verification gates, and explicit permissions. Use for turning research or an approved user story into an implementation plan.
---

# Plan Slice

## Shared requirements

Read [the communication contract](references/communication-contract.md) before
working, including repository ownership, early transitions, evidence, judgment
and conditional UI reporting. Apply it even when this skill is used alone.
Respond in the user's language. Verify tools and permissions; unavailable
capabilities produce an explicit blocker, never simulated execution evidence.
Use the coordinator's approved slice state when available. Return the six-field
checkpoint and phase artifacts; report unchanged files explicitly.


Read [the default judgment rubric](references/judgment-rubric.md) before agreeing
acceptance unless an explicitly approved replacement is supplied. Record its
version and the review-policy independence/closure decision in the plan.

## Workflow

1. Read approved objective and research; inspect root, branch, dirty files and
   dependencies. Do not invent roadmap approval or accepted outcomes.
2. Define one US or reviewable delivery slice, in/out scope, observable acceptance
   criteria and milestones. Separate mock/local acceptance from installed-package,
   real-provider or production requirements. Keep open criteria visible.
3. Map each criterion to a test or observation and required capability. Include
   negative paths, cancellation/error states, regressions and risk-based security.
   Agree rubric identity/version, required independence and closure authority
   before implementation. Use proportional checks for a narrow task without
   claiming broader US or release acceptance.
4. Break work into coherent tasks with exact target paths, exclusive ownership,
   prerequisites and expected outputs. Multiple tasks/commits may share one
   branch. If an independent review slice needs a different branch, announce
   current branch fit, proposed base/name and permission before any Git action.
5. For UI work describe objects and CRUD (or N/A), changed zones using +/~/-/=,
   an ASCII sketch and the real visual verification planned. A drawing is not
   a rendered proof. Resolve product/UX choices rather than invent approval.
6. Produce plan.md with checks, candidate identity strategy, permissions,
   unresolved decisions, rollback considerations and iteration stop budget.

## Gate and handoff

A previously authorized, unambiguous plan can proceed without a new ritual
approval. Ask for actual scope/safety trade-offs or permissions not granted.
Do not start code changes under unresolved blocking assumptions. Return the
common checkpoint, proposed commit boundaries and independent Judge handoff.

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
