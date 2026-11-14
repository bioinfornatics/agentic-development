# Common delivery output contract v1.4.0

Contract ID: agentic-development/common-output
Contract version: 1.4.0

Read after investigation and before drafting every user-facing phase delivery,
including blocked, unchanged and standalone results. Reuse unchanged guidance
already loaded in this context; verify it before delivery rather than rereading blindly.
This document governs response formatting, not permission to act. Requirements
must already have been resolved before the actions they govern.

## Compact bounded delivery

For a bounded read-only or no-change phase result with no actual handoff, commit,
judgment or session-end boundary, a concise Markdown response may replace the full
five-section report. Retain goal and task (or unavailable identity), actual phase,
result, evidence and limits, preservation and current authority, and next action
with its prerequisite (or an explicit stop). State actual changes or their absence;
never omit a material blocker, failure, ownership conflict or unmet criterion.
A blocked result can use this path only when the same boundary conditions hold.
No cycle visual, empty headings or YAML card is required on this path. Do not turn
an ordinary answer into a handoff/session end merely to satisfy a template.

Use the full five-section report for changed-source delivery, actual handoff,
commit, judgment or session-end boundaries, or an explicit full-report request.
An actual handoff retains the state card/restart prompt and boundary facts below;
compact delivery never waives provenance, permissions, review or tracker gates.

## Mandatory five-section final report at full-delivery boundaries

Keep these English labels and order; translate values into the user's language.
The current-goal heading includes the actual phase, not a proposed future phase.
Use Markdown, not JSON. In-progress updates may stay concise.

~~~markdown
## current goal {step: <cycle|research|plan|implement|test|judge|iterate>}
<Outcome addressed, verified task ID and criterion/baseline locator when available>

## roadmap position
<Roadmap / epic / US references and accepted/remaining outcomes, or unavailable>
<Compact visual of verified phase progress; distinguish the roadmap from the cycle>
Next action: <one concrete action, owner and prerequisite, or none if done>
Status: <active|blocked|done|loop again>; <blocker, correction and retained criteria when applicable>

## modified files
N/A — <no files changed in this delivery, with reason>
OR
- <+ added / ~ modified / - removed / renamed old -> new path — purpose>

## closed tasks
N/A — <no confirmed closed tasks in this delivery, or tracker unavailable>
OR
- <verified ID — title and read-back closed status; performed or externally observed>

## explanation
<Pedagogical explanation: what was done, why, evidence and limits, actual versus
proposed actions, and the next gate. Include applicable boundary facts below.>
~~~

## Report delivery and optional saving

A phase report is generated output, not an assumed existing input. Deliver its
required content inline by default in the selected delivery form; for longer
facts use concise evidence-bound summaries and verified accessible locators.
Beads remains task truth; report filenames suggested by a phase are optional.

1. Save only when the task/user provides an explicit destination and permission to write.
   Otherwise report not saved; do not create directories or files merely to satisfy
   a report template. Lack of an optional file is not a phase blocker.
2. Before saving, verify root, owned path, existing content and conflicts. Never overwrite
   an earlier report or user work implicitly; reuse an authorized versioned destination
   or ask for the conflicting-path decision. Do not publish secrets or raw sensitive logs.
3. After a permitted write verify the actual file/content and report its real path,
   saved status and accessibility/local-only limits. Without a write, use inline facts
   and not saved, never an invented path or durable-persistence claim.
4. Required evidence inputs, candidate manifests, raw verification artifacts, tracker
   updates and an explicitly required durable handoff keep their separate contracts.
   If one is unavailable, block that specific gate and name its recovery action;
   an inline report cannot masquerade as missing raw proof or current tracker state.

## Phase, progress and roadmap semantics

For cycle, step is the last substantive phase actually performed when identifiable,
otherwise cycle for coordination-only work. States are not phases: blocked, done
and loop again belong in roadmap position, never in the step attribute.
Done covers only the requested scope, not parent, release or deployment acceptance.
A recommended transition does not execute or authorize it.

For the full report show at least a compact cycle visual, using only evidence-backed state:

~~~text
Research [reused] → Plan [active] → Implement [pending] → Test [pending] → Judge [pending]
Correction loop: Iterate → affected phase
~~~

This example is hypothetical. Use active, verified, reused, pending, blocked or
unknown as justified; loading a Skill does not verify a phase. Do not fabricate
a roadmap, task, milestone or acceptance. If roadmap identity is unavailable,
say so; in the full report show known cycle progress only, with unknowns explicit. Keep distant
roadmap detail coarse; link verified task records instead of duplicating a tracker.
Explain a nonstandard transition with its reason, reused/current proof and missing
prerequisites. The next action names the immediate executable step, not a later
phase whose gate is still blocked.

Report only files actually changed by this delivery; separate preserved user hunks
in explanation. List repository-relative paths, both sides of renames and deletions.
Modified is not committed. Read back tracker status before listing confirmed closed
tasks; failed/proposed closures stay out of that list. Never invent tasks.

## Boundary facts and preservation

At commit, judgment or session boundaries include the applicable facts once inside
explanation: verified task and requirement source, candidate/environment/checks and
coverage, owned versus preserved files, actual branch/commit/push/merge state,
tracker readback, reviewer independence and verdict/score, session recommendation
versus actual action, and copy-ready restart instructions. Use the directly linked
commit/session references when their conditions apply; never infer Entire identifiers.
No blank required values: use unknown, not-run, blocked or N/A with a reason.
Unchanged criteria keep their IDs and approval; do not silently lower targets, omit
negative paths or redefine Non-goals. Scope changes need current authority.
A new artifact format is not permission to create files or a competing task database.

## Common delivery checklist

Read this contract after investigation and before drafting the response; before
delivery verify it together with the current phase delivery contract. Reuse already loaded unchanged guidance rather than reload blindly.

- [ ] Select compact delivery only under its conditions; otherwise keep the five final headings in order with the actual step in current goal. Blocked/no-change alone does not waive a full boundary report.
- [ ] Identify the actual phase, verified task/status, goal and success criteria.
- [ ] Separate observations from proposals, unknowns and hypothetical examples.
- [ ] Report owned files separately from preserved user work; give review order and reasons.
- [ ] Verify session, candidate, tracker and Git claims; mark unavailable identifiers explicitly.
- [ ] Report commit, push and merge separately with status and observed identifiers.
- [ ] Explain the next action, prerequisite and current permission boundary pedagogically.
- [ ] At a handoff boundary give a copy-ready restart prompt; do not auto-launch a session.

## State card inside explanation

For a phase handoff, use the current phase's worked YAML example as a compact state
card inside explanation. For small in-progress checkpoints, concise prose may express
the same applicable facts. This is not a second final envelope, runtime schema, task
database or automatic file write. Beads remains task truth. Use verified locators
for long unchanged detail; retain the essential next action and its prerequisite.
Example keys stay English; translate human-readable values into the user's language.
Examples are hypothetical, not evidence or permission. Replace placeholders with
verified values or unknown, not-run, blocked or N/A with a reason.

Required state: session identifier/status, current tasks/statuses, goal, success
criteria/status/evidence, phase, pedagogical explanation, modified/preserved files,
review order/reasons, separate commit/push/merge statuses, next action/prerequisite
and restart context. Git statuses: not_performed, proposed, performed, failed,
blocked, externally_observed. Pending requires a concrete waiting condition.
A merged branch is not a commit status; a saved state card grants no authority.

## Handoff readability gate

At an actual phase handoff, render one fenced YAML state card inside explanation.
Do not substitute a sentence labeled YAML, semicolon pseudo-YAML or a list of intended
keys. Small in-progress prose is allowed only when no phase handoff is delivered.
Record boundary facts once: the card carries resumable state; adjacent prose explains
decisions and evidence limits, not a duplicate of every field. Use accessible verified
locators for unchanged detail. No word target overrides required evidence or honesty.
Distinguish immediate_action (including owner and missing prerequisite) from the
conditional_next_phase. When the prerequisite belongs to this phase, stay here until
it is resolved rather than presenting the later phase as ready. Git not-applicable
uses status na with a reason; blocked means an applicable action lacks a prerequisite.
