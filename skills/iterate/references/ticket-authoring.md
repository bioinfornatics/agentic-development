# Readable and restartable task tickets v1.2.0

Contract ID: agentic-development/ticket-authoring
Contract version: 1.2.0

Apply before creating or repairing task descriptions or acceptance criteria in any
agreed tracker; apply the Beads bridge when relevant. This is authoring guidance,
not an enforcement engine or permission to mutate tickets.

## Author and verify

1. Inspect existing work, parent outcome, requirement sources, owner and blockers.
   Reuse matching tickets. Write a title with a verb and specific outcome, not
   "Improvements" or an implementation detail that hides the user/problem result.
2. Put Why first: observed problem, affected user, impact and desired value. Use
   short sections/bullets, one idea per paragraph; separate facts from assumptions.
   Explain the situation and what the reader will be able to do or understand
   afterward, before naming architecture, storage or fixtures. Use plain language;
   explain necessary domain terms. A commit or prior decision is context, not the problem.
   Do not paste operational preambles, transcripts or circular justification.
   Do not invent an end user for technical/non-behavioral work: identify the
   affected maintainer/system, concrete difficulty and verifiable deliverable.
3. Bound one independently reviewable result. Split when outcomes need different
   prerequisites or acceptance decisions, not by file or phase mechanically.
   Technical detail comes after the problem, expected outcome, limits, success
   criteria and open decisions. How describes the approach; acceptance criteria describe results, not
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
   Keep product decisions visible in their own section, not hidden in technical
   vocabulary or presented as settled implementation details. State which work
   can proceed and which depends on the answer; do not invent command names,
   output formats or unavailable functionality to make a ticket look ready.
7. Store current specification in the description, canonical criteria in the
   acceptance field when available (otherwise in the description), results in
   notes/comments, and status/owner/prerequisite edges in native fields. Never
   maintain divergent criteria copies. Dated notes contain criterion IDs, candidate,
   checks/results, limits and next action; use locators, not full logs or secrets.
   Do not copy general work instructions (authorization, review, Git or session
   procedure) into every ticket. Reference the applicable shared policy instead;
   retain only task-specific restrictions, review/evidence needs and exceptions.
   Keep the first restart action specific to this task, not a generic work checklist.
   Verify current facts against accessible sources before reusing technical starting
   points; mark stale or unverified facts and their readiness impact. Removing a
   promised feature or choosing a new storage contract is a scope change, not a wording repair.
   Preserve history; explain supersession in a dated note. Do not change criterion IDs,
   thresholds, scope, status or ownership merely to reformat; substantive changes
   need current scoped authority. Do not bulk-rewrite unrelated tickets or close parents.
8. Read back the rendered ticket and fields after authorized writes. Use the
   readiness checklist below. Readiness does not establish acceptance or closure.

## Description template

Preserve the required facts; combine headings for small tasks. Omit non-applicable
optional detail with a reason; do not leave unexplained placeholders. The product
questions come first; technical detail is a short second layer, not another work
protocol. Use native fields for owner, status, parent and prerequisite edges; when
unavailable, add a compact task-specific ownership/dependencies section below.

~~~markdown
## Why
<Who encounters what problem, in which situation, with what consequence/value?>
<Requirement source; observed facts versus assumptions>

## Expected outcome
<What the reader can do or understand afterward; one reviewable result>
<For non-behavioral work: concrete deliverable and who/what benefits>

## Scope and non-goals
- In: <covered outcomes and relevant environment>
- Out: <excluded behavior, including adjacent features not yet delivered>

## Acceptance criteria
<Canonical acceptance field pointer, or criteria here if no separate field>
<Observable situations/results; stable IDs, sources, errors and boundaries>

## Open decisions
<Decision / owner / readiness impact / next resolution action, or none>
<Which work depends on this answer? Unknown decision owners stay explicit.>

## Technical starting point
<Short verified approach, relevant paths/constraints and parent/specification locator>
<Proposal versus existing facts; task-specific restrictions or shared-policy pointer>

## Reading references
1. <required/supporting; root-relative file or canonical URL; section/symbol;
   reason; source identity/version, freshness/accessibility; inspected or unread>

## Verification
<Criterion ID -> check/seam and independent expected result>
<Task-specific review and evidence level: source, mock, installed or real; gaps>

## Restart
<First task-specific executable action, required input/prerequisite and expected result>
<Current observations and remaining work: canonical notes locator, not copied history>
~~~

If criteria live in a separate acceptance field, read the description and that field
as one ticket; do not duplicate or hide them behind a technical report. Necessary
execution metadata remains recoverable through native fields and resolvable references,
not repeated policy text in the product explanation.

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

Hypothetical ticket, not execution evidence. This example keeps one result narrow;
inline output and missing-destination behavior would need separate criteria if in scope.

~~~markdown
Title: Preserve the previous report when its destination already exists

## Why
A user saving a new report to an occupied destination could lose an earlier report
without choosing to replace it.

## Expected outcome
The user receives an explicit conflict message and keeps the earlier report intact.

## Scope and non-goals
In: saving to an existing report destination without overwrite approval.
Out: approved replacement, renaming, inline output and missing destinations.

## Acceptance criteria
### REPORT-1 — Preserve existing content
Source: This hypothetical task's no-implicit-overwrite requirement.
Given: The requested destination already contains an earlier report.
When: The user requests saving a new report without explicit overwrite permission.
Then: The earlier report's bytes remain unchanged.
Check: Compare the original bytes after the attempt; execution not-run.

### REPORT-2 — Explain the conflict
Source: This hypothetical task's explicit-conflict-message requirement.
Given: The requested destination already contains an earlier report.
When: The user requests saving a new report without explicit overwrite permission.
Then: The response identifies the occupied destination as the reason saving was refused.
Check: Inspect the response for that destination and reason; execution not-run.

## Open decisions
Exact conflict-message wording -> owner unknown -> decide before message-specific
assertions; REPORT-1 does not depend on that wording.

## Technical starting point
Locate the existing report-saving entrypoint; its path is not yet verified.
A conflict check is a proposed approach, not the acceptance criterion.

## Restart
Locate the saving entrypoint and a conflict-reproduction seam before implementation.
Native fields: owner unknown; no verified parent or prerequisite issue IDs.
~~~

"Add a conflict-check function" belongs in technical detail, not in Then. Do not
turn an uncertain approach into a product promise or mix future scoring/replacement
capabilities into a read-only/preservation result.

## Readiness checklist

- [ ] With only the ticket and its resolvable references, a new reader can explain
      the problem, expected change, how success is observed and what remains to decide
      without technical vocabulary or generic work instructions obscuring them.
- [ ] Limits precede technical detail; the task-specific starting point is short,
      current or explicitly unverified, and identifies where to start.
- [ ] Title/outcome and task size are coherent; bug facts/reproduction are separated
      from hypotheses when applicable.
- [ ] Criterion IDs/sources map to independent checks; relevant errors/boundaries
      and approved NFR definitions are present, without implementation-only acceptance.
- [ ] Required inputs resolve; owner, parent/prerequisite direction, permissions
      and blocking decisions are explicit. Missing mandatory facts block readiness.
- [ ] Readback confirms fields/links, preserved history and unchanged criteria;
      first restart action is executable or names its exact prerequisite.
