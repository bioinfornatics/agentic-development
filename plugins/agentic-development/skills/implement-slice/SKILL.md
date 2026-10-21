---
name: implement-slice
description: Supports scoped software implementation with coherent diffs, preserved pre-existing changes, and UI reporting. Use for implementing an approved or otherwise authorized delivery plan and its acceptance criteria.
---

# Implement Slice

## Shared requirements

Read [the communication contract](references/communication-contract.md) before
working, including repository ownership, early transitions, evidence, judgment
and conditional UI reporting. Apply it even when this skill is used alone.
Respond in the user's language. Verify tools and permissions; unavailable
capabilities produce an explicit blocker, never simulated execution evidence.
Use the coordinator's approved slice state when available. Return the six-field
checkpoint and phase artifacts; report unchanged files explicitly.


## Workflow

1. Read the approved plan, acceptance criteria, local instructions and ownership
   ledger. Reinspect branch/status/diff and compare pre-existing hunks. Block
   conflicting ownership; do not overwrite another contributor's work.
2. Confirm branch fit and announce impending branch action if needed. Check
   action-specific Git authorization before creation/switch. Non-Git work can
   proceed on authorized files with branch marked not applicable.
3. Make the smallest coherent change within approved scope. Preserve external
   contracts, avoid unrelated cleanup and never include secrets. Parallelize
   only disjoint writable files; return conflicting changes to the coordinator.
4. After each coherent change batch inspect the actual diff, update changes.md
   with owned paths/hunks and reasons, and emit the short checkpoint. Run cheap
   available checks near changes; record commands and actual outputs.
5. For UI/journey changes provide ASCII with CRUD and +/~/-/=, functional/visual
   differences and explicit observed/tested/inferred/not-run status. Record any
   capture independently of the drawing. Do not infer browser quality from code.
6. Hand the exact candidate and relevant checks to Test. Recommend a commit only
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
