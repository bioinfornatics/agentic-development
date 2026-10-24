---
name: test
description: Verifies an exact software candidate against acceptance criteria with reproducible evidence and explicit mock, installed-package, and real-environment limits. Use for testing implementation, regression repairs, or changes that invalidate earlier checks.
---

# Test

## Select the action from the intent

Resolve the criteria, candidate, required environments and check permissions. Inventory tools before executing; an unavailable required environment leaves its criterion open, not silently skipped.

| Intent / condition | Execute | Required result |
|---|---|---|
| Verify an implementation or regression repair | Bind criteria to the candidate, run available checks and record actual results | Reproducible criterion-to-check evidence, failures and coverage limits |
| Reuse previous proof after a change | Compare the proof's inputs/environment with current ones; rerun affected checks | Justified retained proof and new evidence for changed inputs |
| Verify an installed package, real provider or rendered UI | Use the exact required artifact/environment and inspect actual behavior | Environment-specific observations, or explicit missing capability; mock proof is not substituted |

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

1. Freeze candidate identity and the acceptance/check matrix before running
   acceptance-bound checks. Preliminary near-change checks may use the limited-
   provenance path in candidate-identity.md; they must be rerun against a frozen
   candidate before acceptance or reuse, not retroactively promoted.
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

## Conditional reporting details

Read [the commit report](references/commit-report.md) only for a proposed,
performed, failed or externally observed commit. Read
[the session report](references/session-report.md) only for planned session end,
explicit wrap-up or recommended context transition. The common communication
contract remains mandatory; do not reload identical content already present in
the current context. Combine overlapping reports without dropping required fields.

## Verification output contract

Produce the phase artifact with the canonical headings in
[the requirements and output contract](references/requirements-output.md).
Include exact cwd, versions/fixtures relevant
to reproducibility, exit codes and timestamps; unknown data stays unknown.
A deterministic check should fail on the requested symptom, not merely prove
that a command did not crash. Use public behavior seams and independent expected
values. For nondeterminism record seed, repetition budget and observed failure rate;
never describe a flaky run as deterministic or a synthetic fixture as real usage.

Run near-change checks and risk-relevant regressions. Use new observations only
for their candidate/environment; separate old valid evidence explicitly. Report
missing tools/credentials as blocked or not-run, never skip silently. Output formatting
checks do not establish functional quality. Do not write acceptance or repair the
candidate as part of verification; return defects to the authorized correction phase.

## Execute the handoff or stop

Execute the next phase only when it belongs to the user's requested workflow and
current scope/permissions cover its actions. For a phase-only request, return the
phase result and proposed handoff, then stop; do not expand the request by loading
or executing a new phase. If continuing is authorized, apply the routes below.

After recording available verification, Load `agentic-development:judge`
with candidate identity, criteria/check matrix, actual results and missing evidence.
For a confirmed repair need, Load `agentic-development:iterate` with the
failing criterion and replay command; do not silently edit the tested candidate.
An unavailable mandatory check stays open and is handed off as a prerequisite.

Use the host's available Skill-loading mechanism; these identifiers are not shell
commands. If loading is unavailable, read the selected bundled SKILL.md and its
required contained references, and report direct reading rather than activation.
Pass a copy-ready handoff if execution cannot continue in this context. State the
specific missing input, permission or capability, who can supply it when known,
and the next executable action. Do not merely say "blocked" or "continue later".

End every phase delivery with the mandatory seven-field final report from
[the requirements and output contract](references/requirements-output.md), including
blocked or unchanged results. Keep the ordered fields and explain the next gate.
