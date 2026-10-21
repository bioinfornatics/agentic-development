# Controlled Beads initialization v1.1.0

## When to use

Use only when Beads is explicitly selected for this repository and the workspace
is not initialized. Loading drive-cycle is not setup approval. The coordinator
owns setup; phase workers report missing prerequisites. An existing or partial
workspace must be diagnosed and preserved, never reset to change setup options.

## Preconditions

1. Confirm repository root, current permission and existing local instructions,
   .beads/, branch/status, host integration files and Git hooks configuration.
   Capture pre-existing files/hunks and active hook path before any mutation.
2. Verify bd availability/version, bd where and bd init --help. Failed lookup is
   not proof of absence. Missing bd is a dependency, not installation approval.
   In a non-Git folder establish separate authority for any required Git mutation.
3. Check --non-interactive, --agents-profile minimal, --skip-agents and --skip-hooks
   in the installed CLI. Meanings below were verified using bd 1.1.2 help; consult
   local help for other versions. Do not treat noninteractive defaults as an
   approved project policy or authority to commit/sync.
4. Choose the smallest justified profile below and announce generated files,
   hook effects, preservation/coexistence risks and required authorization.
   Inspect executable hooks and chained handlers before approval. Existing hooks
   are not inherently safe because installed; do not blindly execute/remove them.

## Setup profiles

Recommended when project agent integrations are wanted but Git hooks have not
been reviewed or approved:

    bd init --non-interactive --agents-profile minimal --skip-hooks

The minimal profile supplies a pointer to bd prime rather than a full duplicate
CLI reference. Review actual AGENTS.md, CLAUDE.md, local Beads Skill and generated
Claude/Codex integration changes; keep project policy separate from operational
Skill guidance. These are integration instructions, not a custom plugin agent.

When both agent integration and Git hook installation/coexistence are explicitly
approved after inspection, use:

    bd init --non-interactive --agents-profile minimal

Keep Beads-generated hooks separate from this plugin's behavioral communication
contract. Context hooks can refresh Beads guidance for their supported host;
Git hooks run chained handlers and may add identity trailers, depending on the
installed implementation. They do not guarantee our structured commit/session
reports. Host-specific hooks are not automatically portable to another host.
Inspect timeout/error behavior and effects of chained handlers; a successful Git
operation does not prove every hook check completed. No hook bypass or automatic
remote sync is authorized by choosing this profile.

When existing/manual agent guidance and integrations must not be generated, use
the deliberately minimal storage-only profile:

    bd init --non-interactive --skip-agents --skip-hooks

In the checked CLI, --skip-agents suppresses AGENTS.md and Claude/Codex setup
creation; --skip-hooks skips Git hook installation, not all host hooks or all Git
configuration mutations. None of these profiles guarantees zero incidental Git
or file mutation. Obtain permission for effects beyond the allowed scope.

Do not add --force, --reinit-local, --from-jsonl, remote-discard options or retries.
Do not reinitialize to remove duplicate instruction blocks or add hooks later.

## Existing workspace and optional later hooks

Preserve current agent guidance and hooks unless an explicit change is approved.
Read the local Beads Skill for operational workflow, use current prime/help,
and remove redundancy only through a separate scoped edit with ownership checks.
Never delete generated setup just because the plugin also contains Skill rules.

If Git hooks need later installation, inspect bd hooks list, active hooksPath,
existing hook content and bd hooks install --help. In the verified CLI,
bd hooks install --beads selects .beads/hooks/ and --chain chains existing hooks.
Choose path/coexistence deliberately and verify actual configuration; do not
blindly change hooksPath, overwrite shared hooks or use --force. Hook installation
is a separate approved mutation, not a side effect of reading this reference.

## Verification and handoff

Check actual exit output, then bd where and bd prime. Compare instruction,
configuration, hooks and working-tree state with the baseline. Report generated
and changed files, integrations installed/skipped, effects on existing handlers,
and errors or partial state. Pause on unintended changes; do not discard user
work or retry initialization blindly. Verify that new integrations do not weaken
current Git/remote permissions or duplicate conflicting project policy.

Read the local Beads Skill when available; otherwise use the plugin's contained
integration fallback and current CLI help. Storage-only setup does not supply
host guidance: propose any missing pointers as separate approved changes.
No commit, push, Dolt sync or cleanup is authorized by initialization. An already
initialized repository reuses its workspace; no init command is run just to
apply a different profile. A proposed profile is not a claim it was executed.
