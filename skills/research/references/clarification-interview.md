# Clarification interview

Use this procedure when a decision-critical requirement, scope boundary or
trade-off is unresolved after reading the available evidence. Skip it when the
evidence already answers the question or the gap does not change the next decision,
unless the user explicitly asks for grill mode below.

## Procedure

1. Sort each gap into a fact or a decision. A fact has an answer somewhere you
   can read: code, documentation, tracker or history. Find it, cite where it came
   from, and do not turn it into a question; the user is asked for decisions only.
2. Map how the open decisions depend on each other. A decision is ready once
   everything it relies on is settled; only ready decisions are asked.
3. Put each ready decision in its own numbered question, at most three per turn
   (grill mode below lifts this bound). Attach the answer you propose and why, so
   the user can simply agree with it or overrule it.
4. Record each answer where it belongs: Goal or Non-goal, FR with Given/When/Then,
   NFR target, assumption, or ADR candidate for a hard-to-reverse choice.
5. After every reply, check which decisions have become ready and continue. Anything
   still unresolved is written as `NEEDS CLARIFICATION: <question>`; planning is not
   ready while such a marker blocks it.
6. Stop when no decision-blocking marker remains, or when the user defers a
   decision. A deferred blocking decision stays a Plan blocker with its owner.

## Grill mode

Grill mode is the same procedure run to exhaustion. Use it only when the user asks
to grill or stress-test a plan, design or idea; ordinary research keeps the
default. Only these settings differ:

| Setting | Default | Grill mode |
|---|---|---|
| Questions per message | At most three ready decisions | One message: present all decisions that are ready under step 2, each with its proposed answer |
| Fact not yet found | Look it up before asking | Delegate the lookup to a separate worker when the host offers one and keep asking the ready decisions meanwhile |
| End | No decision-blocking marker remains | No open decision remains and the user confirms the recorded decisions are complete; nothing is acted on before then |

Readiness is still recomputed after every reply, so a question whose answer
depends on another one in the same message waits. A blocking decision the user
defers keeps its `NEEDS CLARIFICATION` marker and owner in both modes.
Conflicting or vague domain terms and hard-to-reverse choices go through the
domain-modeling route of the calling phase.

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
