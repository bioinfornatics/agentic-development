# Candidate identity v1.2.0

Use before planning checks, freezing a candidate or reusing evidence. Choose one path.

## A. Run a preliminary check

1. Record the command, relevant input paths, environment and observed exit/result.
2. Label provenance limited; no full manifest is required for a smoke check.
3. Before using this result for exact-candidate acceptance or proof reuse, follow B
   and rerun the checks. Never retroactively relabel the preliminary result.

## B. Bind checks to an exact candidate

1. Verify Python >=3.10; Git workspaces also require the Git CLI and their worktree
   root. Resolve this Skill's directory as `SKILL_DIR`; the shell cwd is not that directory.
2. Copy the bundled scope example to an authorized location outside the inputs.
   Replace include paths, criteria identity and non-secret environment values.
   Use sorted unique root-relative paths (directories recurse, including ignored
   and untracked files). Include code, tests, fixtures, configuration, lockfiles,
   consumed reports, applicable instructions and the verification tool itself.
   Review task dependencies: the tool cannot discover omitted inputs or secrets.
3. Keep exclusions narrow: each has a path and reason, approved before checks,
   and must be output-only, never consumed. Do not exclude user work merely because
   it is dirty/untracked. External inputs require an authorized local snapshot in
   scope or remain BLOCKED/UNKNOWN. Do not copy sensitive data without permission.
4. Set SKILL_DIR, PROJECT_ROOT and an authorized EVIDENCE_DIR outside the captured
   inputs. Prepare the scope file, then capture before execution:

~~~sh
cp "$SKILL_DIR/references/candidate-scope.example.json" "$EVIDENCE_DIR/scope.json"
# Edit scope.json with verified paths, environment and criteria before capture.
python3 -B "$SKILL_DIR/scripts/candidate_identity.py" capture \
  --root "$PROJECT_ROOT" --scope "$EVIDENCE_DIR/scope.json" > "$EVIDENCE_DIR/before.json"
~~~

5. Require exit 0 and a manifest with candidate_id. Record commands, actual results,
   environment and approved criteria against that ID; execute the scoped checks.
6. Capture again with the same root/scope and compare:

~~~sh
python3 -B "$SKILL_DIR/scripts/candidate_identity.py" capture \
  --root "$PROJECT_ROOT" --scope "$EVIDENCE_DIR/scope.json" > "$EVIDENCE_DIR/after.json"
python3 -B "$SKILL_DIR/scripts/candidate_identity.py" compare \
  "$EVIDENCE_DIR/before.json" "$EVIDENCE_DIR/after.json"
~~~

7. Exit 0 / SAME: inputs match, not acceptance. Exit 1 / DIFFERENT: inspect changes
   and rerun affected checks on a stable candidate. Exit 2: stop exact-candidate
   claims, record provenance BLOCKED/UNKNOWN and the missing input/capability.
   Validate a saved manifest with `validate "$EVIDENCE_DIR/before.json"` after the script path.
8. Link reports to input candidate_id and hash output artifacts separately. Do not
   hash a manifest into itself or commit reports automatically. After a commit,
   retain the precommit ID: HEAD/index changes require documented content/environment
   equality or reruns, never an invented claim that tests ran on the new commit.

## Format and limits

The bundled schema defines format_version 1; the example is illustrative, not proof.
SHA-256 covers every field except candidate_id, serialized with sorted JSON keys,
compact separators, UTF-8, no ASCII escaping or non-finite numbers. Arrays are sorted
by path; entries hash raw bytes or UTF-8 symlink targets and record permission modes.
Root, scope/reasons, criteria/environment, HEAD and full staged path/mode/blob index
are included. The verified projection is the working tree, not staged content.
Deletion is absence relative to the previous manifest; missing explicit scope blocks.
Non-Git uses git: null; no Git initialization occurs. The CLI validates the bundled
schema's supported keywords plus semantic rules/digest; it is not a general validator.
Unresolved indexes, submodules, special files, nested Git roots and external/broken
symlinks block. Symlink file targets must also be in scope; directory links block.
Capture is not an atomic filesystem snapshot: stop concurrent writers, compare before/
after, and disclose remaining race limits. Equality does not prove completeness,
unchanged external services, authentic evidence, reviewer independence or acceptance.
