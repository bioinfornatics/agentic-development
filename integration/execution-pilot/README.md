# Disposable cancellation execution pilot

This opt-in stdlib tool prepares a real, runnable mini Python project and independently
checks its public cancellation behavior. It does **not** launch a model, run a Skill
workflow, record agent tool events, enforce every execution requirement, or accept a
product/release. Fixture prompts are evaluation inputs, not contributor instructions.
There are no installs, Git operations, tracker writes or network calls.

## Scope and frozen evidence

`tools/execution_eval.py prepare` stages identical `project/` bytes and `task.txt` in
`contexts/with_skill` and `contexts/without_skill`. Only the current selected Skill's
`SKILL.md` and contained `references/`, `assets/`, `scripts/` resources are added to
`with_skill/skill`. No source AGENTS, evals, sibling Skills, tracker, or source history
is staged. The baseline has no Skill or AGENTS instructions. Keep candidate cwd and
filesystem grants restricted to its own context; copying folders does not establish
those restrictions.

The project starts with a real cancellation defect: `cancel()` updates the flag but
continues delivering chunks. Its normal-exhaustion smoke test passes. `user-notes.txt`
is a byte-preserved snapshot of pre-existing local user edits (not a Git status claim).
Candidates may repair `streamer.py`, edit `test_streamer.py`, and add top-level
`test_*.py` regression tests. No other existing project bytes may change.

`manifest.json` freezes the exact working-tree inputs, including local source edits,
Skill/fixture/oracle/preparer hashes, task, and subset criteria. It does not assert a
clean source commit or authenticate provenance. Save the returned `manifest_sha256`
**outside candidate access**; `check` requires this independent binding. Do not obtain
it again from a potentially altered manifest to manufacture a match.

The independent oracle and full canonical `execution_assertions` inventory are under
`control/`, outside either candidate context. Canonical requirements remain in
`skills/*/evals/evals.json`; the manifest binds these source suite bytes and retains
all execution assertion IDs/content. This pilot checks only cancellation,
preservation, and absence of Git metadata, **not all 530 execution assertions** or
workflow read-order/tool authorization. The inventory may grow; no fixed count is
used as acceptance. Ordinary candidate tests are not the oracle.

## Prepare and check (no models)

Run from the verified source repository. Use an explicit **new** external path,
preferably under an operator-owned disposable temporary directory. Existing outputs,
symlink components/resources, and destinations inside the source are refused. Inputs
are validated before destination creation; failed/partial outputs are not reused.
No automatic cleanup or overwrite is performed.

```sh
python3 -B tools/execution_eval.py prepare "$PWD" "$PWD/skills/cycle" /absolute/new/external-pilot
# Save the returned manifest_sha256 in a coordinator-controlled location.
python3 -B tools/execution_eval.py check /absolute/new/external-pilot with_skill --manifest-sha256 <saved-hash>
python3 -B tools/execution_eval.py check /absolute/new/external-pilot without_skill --manifest-sha256 <saved-hash>
python3 -B -m unittest discover -s tests -p test_execution_eval.py -v
```

`prepare` returns JSON, `model_launches: 0`, and `isolation_status: BLOCKED`.
`check` returns the oracle and project-test exit codes/output, candidate hashes,
preservation violations, separate `behavior_status` and `isolation_status`, plus
machine `status: BLOCKED` until host verification is supplied. CLI exit 0 means
preparation or passing deterministic behavior checks only; exit 1 means behavior
failure; exit 2 means invalid/stale/unsafe inputs. Always inspect the JSON gate:
exit 0 does not imply isolation, acceptance, or a completed agent evaluation.

### Observed completion and trust limit

Exit 0 alone is never a test PASS. A frozen coordinator runner writes a structured
outcome to a parent-owned disposable path outside candidate cwd. The parent requires
completion of exactly the three expected cancellation-oracle test identities, matching
planned/completed identities and run count, and zero failures, errors, skips, expected
failures or unexpected successes. Local discovery similarly requires a completed,
nonempty run with matching planned/completed identities and zero adverse counts;
local identities are discovery-derived, not independent behavioral criteria.
Missing/malformed output, empty discovery, or premature `os._exit(0)` is FAIL, even
when stdout/stderr are empty and the process exits 0. The checker does not intercept
or bypass `os._exit` to pretend execution continued.

**This is observed completion, not authenticated attestation.** Candidate Python
shares the runner's interpreter and privileges: it can inspect or forge the structured
outcome or monkeypatch test machinery. A private parent path separates outcomes from
logs but does not establish a hostile-code guarantee. External host isolation claims
do not cure this same-interpreter limitation. PASS remains a limited deterministic
observation suitable for ordinary cooperative candidates, not adversarial acceptance.

Regression tests exercise the import-time exit-0 reproduction, empty local discovery,
local import/test-time premature termination, and parent rejection of incomplete
identities/counts or adverse result counts.

The focused test `test_public_cancel_red_then_green` executes the original oracle
and requires a post-cancel late-chunk assertion failure (RED), then changes only the
disposable copy to set `active = False` during cancellation and reruns the same
oracle (GREEN). This is a fixture/checker demonstration, **not an agent repair** or
proof of Skill effectiveness. Source fixtures remain buggy and unchanged for future
trials. Other tests cover paired equality, hidden criteria staging, canonical
retention, symlinks, overwrite refusal, manifest/oracle tampering, preserved-byte
violations, Git metadata, unchanged source, and CLI status.

## Isolation gate and safe execution boundary

**BLOCKED by default.** Before any actual paired candidate run, an external host
operator must verify ambient instruction exclusion and that the candidate cannot
read/write the source, tracker, sibling context, coordinator manifest/oracle, or
expected answers. Use equal tools, budget and project access for each candidate.
This preparation/checker does not configure or verify host grants, sandbox Python,
exclude inherited host hints, or provide a launcher. A fresh cwd is not a sandbox.

`check` executes candidate Python with inherited environment and a 15-second
subprocess timeout; candidate code can access anything the checker process can.
Read the candidate first and run verification only in a separately authorized,
verified environment when the candidate is untrusted. Timeouts are not process-tree
containment. Symlink checks protect ordinary operations, not concurrent hostile
path replacement. Hide `control/` through real host access controls, not its name.

An externally produced JSON attestation can be passed with `--isolation <file>`:

```json
{
  "manifest_sha256": "<saved-hash>",
  "verified_by": "<external host operator or evidence locator>",
  "ambient_instructions_excluded": true,
  "source_and_tracker_inaccessible": true,
  "sibling_context_inaccessible": true,
  "coordinator_criteria_inaccessible": true
}
```

All fields must be present and true, with a nonempty verifier and matching hash.
This records an **external claim**, not authenticated proof: resulting status is
`CHECKED_NOT_ACCEPTED` and isolation is `EXTERNALLY_REPORTED_VERIFIED`. Never create
an attestation merely to unblock a pilot. The unit test uses a labeled test double,
not a real host-verification record. No real attestation is supplied by this project.

## Observation and comparison limits

`tool_events` is an explicit unavailable placeholder with `events: null`, not a
counterfeit event log. Model token/cost/time fields remain null. Test subprocess
stdout/stderr and exit codes are actual deterministic observations, not model or
agent telemetry. No model ID, session ID, delegation success or independent reviewer
is invented. An independent expected-behavior oracle is not an independent Judge.

The no-commit check detects Git metadata and refuses extra files. No Git repository
is initialized, and the tool cannot prove that a candidate did not create/delete
history or commit elsewhere: external tool events are still needed for historical
permission enforcement. Preserved bytes are checked before/after tests; this cannot
prove no transient writes. Candidate outputs and host evidence must be frozen and
independently reviewed in a later authorized experiment. No causal A/B uplift,
workflow completion, official receipt, or release acceptance follows from GREEN.
