# Candidate identity v1.1.0

Read when planning a verification strategy, freezing a candidate, reviewing
proofs or resuming evidence. A Git diff hash alone is never a sufficient identity
when relevant inputs can be staged, untracked, ignored, binary or external.

## Preliminary checks versus acceptance-bound evidence

For a near-change smoke check that does not support acceptance or proof reuse,
record the command, relevant input paths, environment, observed exit/result and
known provenance limits. A preliminary result may be PASS for that check while
its candidate provenance remains limited; do not claim a frozen candidate,
independent acceptance, installed behavior or release readiness from it.
Do not block useful preliminary checks merely because no full manifest exists.

Before promoting a result into exact-candidate acceptance or reusing it as proof,
freeze the scope and full identity below and rerun the relevant checks on that
candidate. A later manifest must not retroactively relabel preliminary evidence.
The acceptance identity may cover a narrow agreed slice, but must include every
input relevant to that slice. Missing inputs still block its acceptance.

## Freeze scope before acceptance-bound execution

Define and record the verification scope: code, tests, configuration, lockfiles,
build inputs, relevant local instruction/policy files and any fixtures consumed.
Inventory the full working tree, staged state and untracked files. Explicitly
account for ignored/generated files used by checks rather than relying on Git's
tracked set. Keep sensitive environment inputs redacted; record environment,
provider/package/tool versions and non-secret configuration identity separately.
Unavailable relevant inputs mean provenance is incomplete, not a complete hash.

Use a deterministic UTF-8 JSON content manifest with format_version 1. Each entry
has repository-relative forward-slash path, kind (file or symlink), mode,
sha256 of raw file bytes or UTF-8 symlink target and, for symlinks, target.
Sort entries by path, reject duplicates and ambiguous paths, preserve case,
record deletion as absence relative to the baseline. Include tracked, staged,
unstaged, untracked and relevant ignored content. Hash binary bytes, not a text
diff. This is the working-tree content actually verified, not staged content.
If a check consumes the index instead, freeze that index projection explicitly.

Record root, scope rules, exclusions with reasons, HEAD (or no-head/non-Git),
index projection and working-tree content separately. In Git, identify staged
content by sorted path/mode/blob records from the index, including conflicts.
The candidate ID covers the content manifest, scope/exclusion rules and HEAD/index
identity using canonical JSON (sorted keys, compact separators, UTF-8). State the
canonicalization and hash algorithm. Reject an unresolved merge index as a
verification-ready candidate. A non-Git candidate uses the same content manifest
with Git fields not-applicable; do not initialize Git for identity capture.

## Exclusions and reports

Record a narrow approved output-only set for evidence.md, judgment.md, logs,
state and restart artifacts. These files do not change tested content identity
when checks never consume them. Do not exclude the entire slice directory if it
also contains tests, fixtures or executable inputs. Never exclude a file merely
because it is untracked, ignored, contains user work, or lives under docs/.
Freeze exclusions before checks; a new exclusion changes candidate identity.

When a report, generated artifact or build input is consumed by a check, include
its input snapshot before that check. Verify the output artifact's own digest
separately after creation. If a check mutates candidate inputs, mark pre-check
and post-check identities and rerun on a stable candidate or disclose that the
proof does not match the final candidate. Reports must link to input candidate
and output artifact hashes; avoid a self-referential manifest hashing itself.

## Freshness and commit boundary

Compare both manifest identity and relevant environment/criteria before reuse.
Any relevant content, staged state, scope or environment change invalidates
related evidence and verdict. Adding, deleting or renaming an untracked input
counts. A status listing without content hashes is an inventory, not a proof.
For unaffected evidence explain why its defined input scope remains identical.

Writing an output-only report does not invalidate input proofs; changing a
verified input does. Report changes are separately versioned for audit integrity.
Do not automatically commit generated reports. Stage only explicitly authorized
owned changes; explain whether reports are included. Never silently include
user hunks. After a commit creates a new HEAD/index identity, retain the original
verification input ID; do not rewrite it as if tests ran on the new commit. Rebind
only with documented equality of tested content and environment, or rerun. If
staged content differs from the tested working tree, that commit is a different
candidate and cannot inherit the verdict automatically.

## Capability limits

No utility is shipped for this contract. Use verified available tools to build
and compare the manifest; do not claim execution from the specification alone.
If complete identity cannot be captured, report provenance BLOCKED/UNKNOWN and
keep required exact-candidate acceptance open. Do not display secrets or raw
sensitive input content in the manifest; follow project data-handling rules.
