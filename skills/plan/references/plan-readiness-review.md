# Plan readiness review

Use before declaring tickets ready and before approving the complete current plan
for execution. This is a decision review, not another phase or ticket-authoring
procedure. Reuse the caller's established scope, authoring guidance, research,
review policy and current permissions. Readiness is not acceptance.

## Contents

- [1. Challenge each individual ready ticket](#1-challenge-each-individual-ready-ticket)
- [2. Delegate the complete-plan logical challenge](#2-delegate-the-complete-plan-logical-challenge)
- [3. Stop with an executable frontier](#3-stop-with-an-executable-frontier)

## 1. Challenge each individual ready ticket

Read the actual ticket, canonical criteria, native fields and resolvable references.
Use the following open questions to explain the result; answer each paired closed
question **yes / no / unknown**, citing the relevant input. Yes passes that gate;
no fails it; unknown never passes. Mark an inactive question N/A with a scope-based
reason. Do not demand extra headings or copy this checklist into every ticket.

| Open inquiry | Closed readiness question |
|---|---|
| Why is this result useful to the actual user, maintainer or system, and what changes afterward? | Is one usable, independently reviewable outcome tied to a verified requirement rather than a file/phase activity? |
| What must already exist or be decided, and what evidence shows those prerequisites hold? | Are actual prerequisites, native blocking edges and textual assumptions consistent, with no critical unresolved input? |
| Which supported research premise justifies this approach, and what would invalidate it? | Are decision-material hypotheses supported or explicitly unresolved rather than asserted as facts? |
| How will a reader distinguish success from a plausible but incorrect result? | Do stable source-derived criteria have independent observable checks, including relevant errors/boundaries and approved applicable NFRs? |
| Which inspected inputs are needed first, what is created or modified, and what must stay untouched? | Are Read/Create/Modify/Preserve/Exclude paths or assets verified/proposed honestly, ownership conflicts resolved and adjacent work excluded? |
| What can a fresh worker do first using only this ID and its references? | Does the first restart action name an accessible input, operation, prerequisite and expected result within current permissions? |

For a critical feasibility claim, name the indispensable unproven operation,
evidence that would refute it and the smallest authorized deciding probe. Challenge
risky compositions, not just component availability: documentation is not execution.
Reuse applicable evidence for low-risk compatible work; no universal proof-of-concept
is required. An unproven indispensable operation leaves affected nodes pending.

Use exact documents/resources instead of invented code paths for non-code work.
Unknown critical input blocks the affected ticket only; retain the rest of the ready
frontier. Record each gap's decision owner (unknown if not established), impact and
smallest resolving action. Repair only authorized affected sections through the
caller's conditional task-authoring route; preserve criteria/history/native fields.

## 2. Delegate the complete-plan logical challenge

Before the plan is approved for execution, request a **separate read-only subagent**
review of the **complete current plan**, not a selected easy ticket. Supply objective,
Goals/Non-goals, requirement/criterion sources, research premises and unresolved gaps,
all current plan nodes (including coarse future work), native edges, relevant source
identity, permissions and an agreed bounded turn/time/output budget. Give reviewer
criteria, not expected answers or the builder's desired verdict/private reasoning.
The reviewer must not have participated in candidate construction; disclose inherited
context and exposure limits. No source, tracker, Git or candidate writes.

Ask the reviewer:
- What is the primary deliverable and its exit criteria? Does the selected ready
  frontier suffice, distinct from the roadmap and any user-requested backlog?
  Are planned tickets, verified claims and actual execution distinguished without
  treating backlog size or intended delegation as active work?
- What is the least viable ordering that delivers the requested usable outcome?
  Are outcomes covered without speculative capabilities or missing integration?
  Trace each material goal/criterion to contributing outcomes and independent
  verification; trace each planned outcome back to a goal/criterion or an explicit
  enabling rationale (including necessary housekeeping). A consistent graph is not
  goal sufficiency: a valid subset can still omit the requested usable outcome.
- For each material producer-to-consumer transition, does the output satisfy the
  next input/precondition in format, interface, state, environment and authority
  where relevant? Ordering alone is not compatibility. Identify a named bridge
  and its owner/verification or block the affected consumer with a deciding
  prerequisite; this is not a microtask per edge.
- Which implicit semantic dependencies are missing from native edges: a foundation
  contract before a consumer, architecture selection before its implementation,
  credential/bootstrap or security boundary before the operation relying on it?
  Check only relevant boundaries; do not dump a generic security checklist.
- Do native edges and described prerequisites agree? Are there cycles (including
  implicit cycles), reverse prerequisites, false parallelism or shared-file conflicts?
  For a concurrent group, are its inputs actually ready, outputs independently
  verifiable and writer paths exclusive? Who owns the verified join, and which
  dependent actions wait for required worker completion rather than partial returns?
- Which research gaps can change ordering, scope or observable criteria? Which nodes
  are actually ready now, which must wait, and what single resolving probe is needed?
- Is decomposition by independently usable result, not a microticket per file,
  phase or SOURCE marker? Keep distant work coarse; task count is not quality.

The goal-trace question checks, in both directions, the same criterion -> task ->
check trace that the Plan workflow delivers.

Return source-linked findings, blocking/nonblocking classification, affected node
IDs, missing or incorrect edges with rationale, a proposed least viable ordering,
ready frontier, research prerequisites and completion/provenance limits. The
coordinator verifies invocation, completion, source identity and result locator,
reconciles findings under existing permissions and retains unresolved contradictions.
A worker summary is not plan approval or independent acceptance of implementation.

If delegation is unavailable, name the exact prerequisite: coordinator/user supplies
a separate non-builder read-only reviewer with access to this complete plan and
criteria. Keep the global approval gate pending; no silent direct fallback or
self-acceptance. This blocks approval of the affected plan, not unrelated authorized
work. Run this challenge once before approval; rerun only when changes affect the
graph, criteria or material inputs, not for every minor wording edit.

## 3. Stop with an executable frontier

Finish when every applicable readiness question is answered (or inactive with a
reason), critical gaps have named impacts/owners/probes, and the global review is
complete or has its precise prerequisite. Report ready/blocked nodes and the next
executable action, not a speculative backlog or bulk ticket rewrite. Confirm tasks
exist only for the active epic and the next epic in line; other epics keep goal,
outcomes and rough scope with no child tasks unless the current request explicitly
asks for detail. Neither this
review nor task authoring grants execution authority. Use proportional checks;
no automatic exhaustive web research, full test suite or evaluation campaign, and
no performance or agent-effectiveness claim from source readiness.
