# Readable and restartable task tickets v1.1.0

Contract ID: agentic-development/ticket-authoring
Contract version: 1.1.0

Apply before creating or repairing task descriptions or acceptance criteria in any
agreed tracker; apply the Beads bridge when relevant. This is authoring guidance,
not an enforcement engine or permission to mutate tickets.

## Author and verify

1. Inspect existing work, parent outcome, requirement sources, owner and blockers.
   Reuse matching tickets. Write a title with a verb and specific outcome, not
   "Improvements" or an implementation detail that hides the user/problem result.
2. Put Why first: observed problem, affected user, impact and desired value. Use
   short sections/bullets, one idea per paragraph; separate facts from assumptions.
   Do not paste operational preambles, transcripts or circular justification.
3. Bound one independently reviewable result. Split when outcomes need different
   prerequisites or acceptance decisions, not by file or phase mechanically.
   How describes the approach; acceptance criteria describe results, not
   implementation steps such as "edit three files". Detail only the ready frontier;
   do not invent paths, owners, estimates, metrics or approvals.
4. For bugs, state current behavior, expected behavior, minimal reproduction and
   environment/version. A hypothesis is not an observed cause. If reproduction is
   unavailable, name the missing input and next probe, not a confirmed diagnosis.
5. Give each criterion a stable ID, source and check. Use explicit Given/When/Then
   with one observable outcome and relevant error/boundary cases. For non-behavioral
   tasks use a verifiable Deliverable/Check instead of fabricated user behavior.
   Define applicable NFR metric/approved target/unit/workload/environment/method.
6. Record blocking questions as Decision / owner / readiness impact, with the next
   resolution action. Mark unknown owners/inputs explicitly. Resolve decision-critical
   gaps before readiness; block the affected work, not unrelated permitted work.
7. Store current specification in the description, canonical criteria in the
   acceptance field when available (otherwise in the description), results in
   notes/comments, and status/owner/prerequisite edges in native fields. Never
   maintain divergent criteria copies. Dated notes contain criterion IDs, candidate,
   checks/results, limits and next action; use locators, not full logs or secrets.
   Preserve history; explain supersession in a dated note. Do not change criterion IDs,
   thresholds, scope, status or ownership merely to reformat; substantive changes
   need current scoped authority. Do not bulk-rewrite unrelated tickets or close parents.
8. Read back the rendered ticket and fields after authorized writes. Use the
   readiness checklist below. Readiness does not establish acceptance or closure.

## Description template

Preserve the required facts; combine headings for small tasks. Omit non-applicable
optional detail with a reason; do not leave unexplained placeholders.

~~~markdown
## Why
<Observed problem, affected user, impact/value; source or assumption>

## What
<One reviewable outcome/deliverable; parent/specification locator>

## How
<Bounded approach and constraints; proposal if unresolved>

## Scope and non-goals
- In: <owned outcomes/paths and environment>
- Out: <excluded behavior/operations and preserved work>

## Acceptance criteria
<Canonical acceptance field pointer, or criteria here if no separate field>

## Reading references
1. <required/supporting; root-relative file or canonical URL; section/symbol;
   reason; source identity/version, freshness/accessibility; inspected or unread>

## Verification
<Criterion ID -> check/seam and independent expected result>
<Required review and evidence level: source, mock, installed or real; gaps>

## Ownership and dependencies
<Owner, parent versus prerequisite IDs, current permission scope/prohibitions>
<Blocking decision -> resolution owner/action and readiness impact, or none>

## Restart
<First executable action, input/prerequisite, owner and expected result>
<Read task/notes/references; verify workspace, ownership, candidate and permissions>
~~~

Keep references small and ordered. Separate source, product/specification docs and
external references; explain each reading decision. Include canonical URLs for
local captures; mark ephemeral/local-only availability and source freshness.
Suggested unread references are not evidence. Do not auto-capture web content or
assume an installed package/current page matches a recorded source identity.

## Acceptance scenario template

~~~markdown
### <stable ID> — <behavior>
Source: <verified requirement/request>
Given: <state/data/preconditions>
When: <one action/event>
Then: <independently observable expected result>
Check: <test/observation and evidence level; not-run until observed>
~~~

For non-behavioral criteria use Deliverable and Check. Missing facts/proof remain
unresolved or N/A with reason, never passed.

## Filled example

Hypothetical criterion, not execution evidence; other required ticket fields still apply.

~~~markdown
Title: Preserve the previous report when its destination already exists
Why: A user must not lose an earlier report through an implicit overwrite.
What: Refuse an unapproved overwrite while keeping inline delivery available.
How: Check destination conflicts before saving; the implementation is not the criterion.
Acceptance: REPORT-1 in the acceptance field.

### REPORT-1 — Preserve existing content
Source: This hypothetical task's no-implicit-overwrite requirement.
Given: The requested destination already contains an earlier report.
When: The agent attempts to save without explicit overwrite permission.
Then: The earlier report's bytes remain unchanged.
Check: Compare the original bytes after the attempt; execution not-run.
~~~

"Add a conflict-check function" belongs in How, not in Then. Cover inline delivery
and missing-destination behavior in separate criteria when they are in scope.

## Readiness checklist

- [ ] With only the ticket and its resolvable references, a new reader can explain
      why the work matters, what is excluded, where to start and how success is observed.
- [ ] Title/outcome and task size are coherent; bug facts/reproduction are separated
      from hypotheses when applicable.
- [ ] Criterion IDs/sources map to independent checks; relevant errors/boundaries
      and approved NFR definitions are present, without implementation-only acceptance.
- [ ] Required inputs resolve; owner, parent/prerequisite direction, permissions
      and blocking decisions are explicit. Missing mandatory facts block readiness.
- [ ] Readback confirms fields/links, preserved history and unchanged criteria;
      first restart action is executable or names its exact prerequisite.
