# Clarification interview

Use this procedure when a decision-critical requirement, scope boundary or
trade-off is unresolved after reading the available evidence. Skip it when the
evidence already answers the question or the gap does not change the next decision.

## Procedure

1. Separate facts from decisions. Look up facts yourself in code, documentation,
   tracker or history; never ask the user for a fact you can verify.
2. List the open decisions and their dependencies. Ask only decisions whose
   prerequisites are already settled.
3. Ask one decision per question, at most three per turn, numbered. For each,
   give your recommended answer and the reason, phrased so that "yes" accepts it.
4. Record each answer where it belongs: Goal or Non-goal, FR with Given/When/Then,
   NFR target, assumption, or ADR candidate for a hard-to-reverse choice.
5. Recompute which decisions became ready and repeat. Mark anything still open as
   `NEEDS CLARIFICATION: <question>`; planning is not ready while a marker blocks it.
6. Stop when no decision-blocking marker remains, or when the user defers a
   decision. A deferred blocking decision stays a Plan blocker with its owner.

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
requests: research remains mandatory, interrogation does not.
