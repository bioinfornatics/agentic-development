# Clarification interview

Use this procedure when a decision-critical requirement, scope boundary or
trade-off is unresolved after reading the available evidence. Skip it when the
evidence already answers the question or the gap does not change the next decision,
unless the user explicitly asks for grill mode below.

## Procedure

1. Separate facts from decisions. Look up facts yourself in code, documentation,
   tracker or history; never ask the user for a fact you can verify.
2. List the open decisions and their dependencies. Ask only decisions whose
   prerequisites are already settled.
3. Ask one decision per question, at most three per turn (grill mode below asks
   every ready decision), numbered. For each,
   give your recommended answer and the reason, phrased so that "yes" accepts it.
4. Record each answer where it belongs: Goal or Non-goal, FR with Given/When/Then,
   NFR target, assumption, or ADR candidate for a hard-to-reverse choice.
5. Recompute which decisions became ready and repeat. Mark anything still open as
   `NEEDS CLARIFICATION: <question>`; planning is not ready while a marker blocks it.
6. Stop when no decision-blocking marker remains, or when the user defers a
   decision. A deferred blocking decision stays a Plan blocker with its owner.

## Grill mode

Use grill mode only when the user asks to grill or stress-test a plan, design or
idea; ordinary research keeps the default procedure above.

- Keep the dependency list from step 2 current: an answer can settle decisions
  and reveal new ones. In each round present all decisions that are ready under
  step 2, numbered, each with a recommended answer; hold any decision that depends
  on another question of the same round for the next round.
- Send fact lookups to fresh-context workers when available and keep asking the
  ready decisions meanwhile; only decisions that need a pending fact wait for it.
- When domain terms conflict or stay vague, or a choice is hard to reverse, apply
  the domain-modeling route of the calling phase.
- Finish only when no open decision remains and the user confirms the shared
  understanding. Do not act on the result before that confirmation; a deferred
  blocking decision stays a `NEEDS CLARIFICATION` marker with its owner.

## Example

~~~text
1. Should expired sessions return 401 rather than redirecting to login?
   Recommended: yes. The API has no browser clients (src/api/README.md).
2. Is audit logging of failed logins in scope for this slice?
   Recommended: no. Keep it as a follow-up; the stated goal is token expiry only.
~~~

## Limits

An interview collects decisions; it does not approve a plan, grant write
permission or replace research evidence. Avoid interviewing on clear, evidenced
requests: research remains mandatory, interrogation does not. An explicit grill
request is the one exception: it walks every open decision, yet evidenced facts
are still verified, never asked.
