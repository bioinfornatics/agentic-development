# Specification template

Use this template when an epic or user story will be delivered by several tasks or
across sessions, so that every worker reads the same agreed behavior. Drafting it
approves nothing; it only writes down what is already settled.

- Source: every statement traces to Research evidence or a user decision. A point
  that is not settled goes to Open questions instead of being guessed.
- Vocabulary: use the project's glossary terms and the decisions already recorded.
- Durability: the specification describes behavior and decisions, not file paths or
  code, because it must stay true while a refactor moves and renames the code under
  it. Concrete paths belong in near-term task tickets. A data or state structure
  that was itself decided is recorded under Decisions.

## Sections

~~~md
## Context
Current behavior from the user's perspective, who it affects and the evidence for it
(research note, ticket, observed defect). One short paragraph.

## Goals
Outcomes this work must deliver, each observable by a user, operator or caller.

## Non-goals
The nearest tempting extensions left out, and deferred work with its follow-up owner.

## Stories
One line per actor and situation in scope, each pointing to its criteria:
S1. A warehouse operator needs to cancel a pick list before dispatch, to avoid
    shipping a withdrawn order. -> FR-1, FR-2

## Criteria
| ID | Story | Given | When | Then | Check and seam |
Behavioral criteria only; each ID is referenced by at least one story.

## Errors and boundaries
Refusals, invalid input, limits, empty and maximum cases, concurrency, cancellation
and partial failure, each as its own criterion ID with Given/When/Then.

## Quality targets
NFRs with metric, target, unit, workload or window, environment and measurement
method. A target nobody approved stays unresolved; N/A needs a stated reason.

## Decisions
Each choice with the alternatives considered and why this one won: components affected,
named by responsibility, contracts, data shapes, interfaces, dependencies, deployment
shape. A choice that is costly to undo,
whose rationale the code will not show, and that followed a real comparison of
alternatives is a decision-record candidate.

## Test approach
Agreed seams, starting from the outermost existing public one that can observe each
guarantee; which failures each seam detects and which it cannot; independent oracles; required
evidence level; the outer acceptance check per story; existing checks to imitate.

## Open questions
`NEEDS CLARIFICATION: <question>` with the person who decides and what it blocks.
~~~

## Readiness

The specification is ready to decompose when every user story maps to at least
one criterion, every criterion names a check or an explicit capability gap, and
no open question blocks the next task. Decompose it into tracer-bullet tasks with
the Plan workflow; the specification is the parent outcome each task links to.
