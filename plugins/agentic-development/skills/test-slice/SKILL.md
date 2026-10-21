---
name: test-slice
description: Verifies an exact software candidate against acceptance criteria with reproducible evidence and explicit mock, installed-package, and real-environment limits. Use for testing implementation, regression repairs, or changes that invalidate earlier checks.
---

# Test Slice

## Shared requirements

Read [the communication contract](references/communication-contract.md) before
working, including repository ownership, early transitions, evidence, judgment
and conditional UI reporting. Apply it even when this skill is used alone.
Respond in the user's language. Verify tools and permissions; unavailable
capabilities produce an explicit blocker, never simulated execution evidence.
Use the coordinator's approved slice state when available. Return the six-field
checkpoint and phase artifacts; report unchanged files explicitly.


## Workflow

1. Freeze candidate identity and the acceptance/check matrix before running.
   Read the project test instructions and verify commands, environment, tooling
   and side effects. Isolate data; production tests need explicit authorization.
2. Map mandatory criteria to checks: unit, integration, negative paths,
   regression, build/install and real-provider behavior as required by scope.
   Do not invent a command or assume a tool exists; inspect project scripts.
3. Execute available relevant checks. Capture command, exit result, timestamp,
   environment, candidate, mock/real mode and sanitized output artifact in
   evidence.md. Record PASS, FAIL, NOT RUN, BLOCKED or UNKNOWN distinctly.
4. For UI changes test the functional journey and, when possible, capture and
   inspect actual rendering with viewport/state and evidence path. ASCII and
   source review alone are inferred, not visual observation. Missing browser
   leaves visual acceptance open. A passing automation test need not prove
   full visual correctness.
5. For installed-package or real-provider criteria use the exact candidate
   artifact/environment. Mock tests cannot substitute. Explicitly distinguish
   missing credentials/capability from a failing executed test.
6. Return failures, repro steps, evidence coverage and unknowns to Judge. If a
   code repair is needed, hand back to Implement/Iterate rather than mutating
   the frozen candidate silently. Invalidate affected evidence after a change.

## Gate

Test reports evidence, not acceptance on behalf of Judge. Announce the judge
context transition and preserve the possibly uncommitted candidate, artifacts
and replay commands. Missing mandatory evidence cannot become an implicit pass.

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
