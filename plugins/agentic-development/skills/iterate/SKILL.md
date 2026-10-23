---
name: iterate
description: Turns judge findings or failed verification into bounded corrective development while preserving accepted outcomes and invalidating stale proofs. Use for addressing rejected or indeterminate slices, repeated failures, or newly discovered scope risks.
---

# Iterate Slice

## Shared requirements

Read [the communication contract](references/communication-contract.md) before
working, including repository ownership, early transitions, evidence, judgment
and conditional UI reporting. Apply it even when this skill is used alone.
Respond in the user's language. Verify tools and permissions; unavailable
capabilities produce an explicit blocker, never simulated execution evidence.
Use the coordinator's approved slice state when available. Return the six-field
checkpoint and phase artifacts; report unchanged files explicitly.


## Workflow

1. Read judgment, evidence, current candidate and approved roadmap. Verify the
   diff has not drifted. Preserve accepted outcomes and initial user work.
2. Classify each open item as implementation defect, missing proof/capability,
   research gap or scope/acceptance decision. Link it to evidence and criterion.
3. Route defects to Implement then Test, missing proof to Test, new uncertainty
   to Research/Plan, and unresolved scope to a user decision. Stay in the same
   branch/session for related test repairs unless an actual transition trigger
   applies. Do not create a branch for every task.
4. Prioritize blocking findings, define the smallest correction and expected
   verification. Never delete tests or weaken criteria to manufacture a pass.
   Scope expansion and destructive changes require appropriate authorization.
5. Increment the round counter, invalidate affected proofs/judgment and preserve
   unaffected candidate-bound evidence with explicit justification. Re-test the
   repaired paths and relevant regressions, then return to Judge on a new frozen
   candidate. Acceptance never transfers automatically to changed code.
6. Update iteration.md and roadmap remaining work; emit the common checkpoint.
   If the correction budget (default three rounds) is exhausted, failures repeat,
   or required capability is unavailable, stop and present blocker, options,
   preserved artifacts and a decision or prerequisite.

## Session and completion boundaries

Objective change or judge role may justify a fresh context, but never implies a
commit. Include dirty/staged/untracked state and exact resume conditions in the
handoff. Close only after the scoped acceptance gate passes; leave unmet real
validation work open. No automatic push, merge or production promotion.

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
