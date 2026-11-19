# Root-cause investigation

Use this procedure when a defect is observed or reported but its cause is
unknown, including an unknown-cause gap routed from Iterate. It produces a
confirmed cause and a red-capable reproduction; it does not repair code.

## Procedure

1. Reproduce the symptom through the closest public seam. Record the command,
   inputs, environment and observed versus expected result. If it does not
   reproduce, record what was tried and return the missing input as the next probe.
2. Minimize the reproduction: remove inputs, steps and configuration until the
   failure disappears; keep the smallest failing case.
3. List at most three ranked hypotheses. For each, name the observation that
   would refute it.
4. Test one variable at a time, cheapest refutation first. Use logs, a debugger,
   `git bisect` in a separate authorized worktree or clean checkout (never in a tree
   with work to preserve), or a temporary probe outside the candidate. Never change several factors in one probe.
5. Confirm the cause only when a probe turns the failure on and off predictably.
   A plausible reading of the code is a hypothesis, not a confirmed cause.
6. Return the confirmed cause, the minimal reproduction usable as a failing test,
   affected seams and the refuted hypotheses.

## Escalation

After three refuted hypotheses on the same symptom, stop probing. Return the
questioned design assumption with options and the decision owner; route it to
Plan only when a scope or design change is authorized. Iterate owns the fix-attempt
budget; this procedure makes no fix attempts.
