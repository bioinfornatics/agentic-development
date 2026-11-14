---
name: task-authoring
description: Authors readable, restartable task tickets from established scope. Use when creating a ticket or repairing its description or acceptance criteria, not for routine reads, claims, progress updates or closure.
---

# Task authoring

## Intent and outcome

Create or repair a ticket from an existing goal, scope and criteria; return an
actual tracker ID with verified readback, or a clearly labeled proposal when
writing is unavailable. This is an optional bounded capability, not an eighth
development phase. Routine reads, claims, progress updates and closure return
to the caller without authoring.

## Procedure

1. Verify supplied goal, scope, criteria, native tracker context and current
   authority. Before any write, apply the contained
   [authorization limits](references/authorization-policy.md).
   Inspect matching work and its native fields/history; reuse a matching ticket
   rather than create competing work. Consume established decisions, do not invent
   missing targets, requirements or approvals. Name decision-blocking gaps.
2. Before drafting or repairing, apply contained
   [ticket guidance](references/ticket-authoring.md) for readable purpose,
   observable criteria, ordered inputs and executable restart context. Reuse
   identical guidance already available and current; do not mechanically reread.
   Preserve criterion IDs, native owner/status/relationships and execution history;
   scope changes need current permission, not merely a wording repair.
   Check the ticket guidance's readability/readiness gate before writing;
   unresolved mandatory facts remain gaps, not invented readiness.
3. Use the chosen tracker's available supported create/repair operation only within
   current authority. If Beads is used, before native operations apply the contained
   [Beads authoring bridge](references/beads-integration.md); other trackers do not
   require Beads commands. Missing write capability or permission yields a proposal,
   never a counterfeit created ID. Failed writes remain errors, not success.
4. After an actual write, read back the ID, purpose, criteria, ordered inputs,
   restart and applicable native fields/links; verify preserved history and report
   discrepancies. Return the actual ID/readback and changed fields, or the proposal
   and exact missing input, authority or capability. STOP and return to the caller.
   Do not recursively load Cycle, Research or Plan, claim or close work, approve a
   closed task, or infer implementation/acceptance authority. No phase report,
   score, candidate manifest, full test suite or evaluation campaign is required
   for routine ticket authoring; the caller retains its own phase obligations.
