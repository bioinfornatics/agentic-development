# Specification template

Use this template when an epic or user story needs a written specification that
several tasks and sessions will rely on. It synthesizes settled research and
decisions; it is not an interview and does not approve scope. Write it in the
project's glossary terms and respect existing decision records.

Keep file paths and code snippets out of the specification: they age quickly.
Exact paths belong to near-term tasks. When an earlier experiment fixed a shape
that prose would blur, such as a status transition table or a payload schema,
quote only that shape and name the experiment as its source.

## Sections

~~~md
## Problem
What the user cannot do today, from the user's perspective.

## Solution
What changes for the user, from the user's perspective.

## Goals and Non-goals
Explicit outcomes in scope and the closest tempting exclusions.

## User stories
Numbered, covering every actor and situation in scope:
1. As a <actor>, I want <capability>, so that <benefit>. Criteria: FR-1, FR-2.

## Acceptance criteria
| ID / story | Given | When | Then | Check / seam |
Include error, boundary and refusal paths; NFRs need an approved metric, target,
unit, workload, environment and method, or stay unresolved.

## Implementation decisions
Modules and interfaces to build or change, contracts, schema changes and
architectural choices, with the reason when it is not obvious. Choices that are hard
to reverse, surprising without context and a real trade-off become decision-record
candidates.

## Testing decisions
Agreed public seams (prefer existing and the highest that observes the guarantee),
what each catches and misses, independent oracles, required evidence level and
similar existing tests to follow.

## Out of scope
Deferred or rejected work, with the owner of any follow-up.

## Open questions
`NEEDS CLARIFICATION: <question>` for each unsettled decision and who decides it.
~~~

## Readiness

The specification is ready to decompose when every user story maps to at least
one criterion, every criterion names a check or an explicit capability gap, and
no open question blocks the next task. Decompose it into tracer-bullet tasks with
the Plan workflow; the specification is the parent outcome each task links to.
