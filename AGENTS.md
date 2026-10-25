# Repository instructions

## Product

- Goal: prevent scope drift, context loss and unsupported completion claims in AI-assisted software changes.
- Product: agentic-development, seven portable Skills: cycle, research, plan, implement, test, judge, iterate.
- Optional Goose hooks observe events/report structure; they are not an enforcement or acceptance engine.
- Non-goals: automatic authorization, protected task closure, session launching or release acceptance.
- Manifest/schema/version truth: plugin.json; do not repeat a hard-coded version here.

## Repository map

| Path / location | Role / boundary |
|---|---|
| plugin.json, skills/*/SKILL.md | Source manifest and seven Skill entrypoints; required resources stay contained. |
| hooks/hooks.json, scripts/observe.py | Goose-specific rules/handler in this plugin, not a second adapter. |
| tools/production.py | Deterministic projection CLI; stdlib observer packaged as scripts/observe.pyz. |
| tests/, integration/ | Source/handler checks and evaluation scenarios; integration/ is not an executable harness. |
| docs/ | Pedagogical guides only; no task IDs, execution logs or JSON receipts. |
| .beads/ | Local task truth; snapshots are not the database or a full Dolt backup. |
| evidence/ | Preserve existing local evidence; historical paths may require Git recovery via Beads references. |
| CLAUDE.md | Relative symlink to AGENTS.md; edit this canonical file, preserve the link. |
| Separate checkout / installed plugin | Different candidate; never assume it matches this source or mutate it implicitly. |

## Branch and distribution contract

~~~text
feature/* -> reviewed source PR -> develop
clean develop@SHA -> verified generated tree -> generated-only PR -> main (squash)
~~~

- develop owns editable source, tests, tools and build inputs; feature PRs target develop.
- main contains only the generated installation projection. Never merge develop into main.
- Publish with previous main as sole parent through a verified generated-only PR and squash merge.
- Never force-push main, bypass protection, or delete/merge develop as part of publication.
- Freeze exact source SHA/tree and expected main SHA; recheck evidence, independent approval and current scoped authority before publication.
- Include manifest, contained Skills/resources, canonical README.md, provenance, verification workflow and optional verified runtime.
- Exclude repository instructions, tracker/evidence, tests/evals, integration scenarios and build tools from the payload.
- Copy README.md unchanged from source; use documentation links that work on both branches.
- Skills need no build; observer requires Python >=3.10, standard library only, no install-time dependency download.
- distribution.json binds source and inventory, not authenticity/acceptance; release_ready=false is not release approval.
- Full workflow, installation probes and promotion gates: [CONTRIBUTING.md](CONTRIBUTING.md). No source license grant: never invent/copy one.

## Task truth and restart

- Beads is mandatory for this repository: status, owner, dependencies and durable follow-up live there.
- Specifications define behavior; Git records source; evidence records observations; prompts/session context are ephemeral.
- Flow: prompt -> verified task -> claim -> bounded work -> Beads result/evidence/next action -> restart prompt with task ID -> task readback.
- Verify repository/worktree, nearest AGENTS.md, branch, index and initial dirty hunks before work.
- Read local Beads guidance if present, otherwise [the contained integration contract](skills/cycle/references/beads-integration.md); verify installed CLI help.
- Use bd prime only for stale context; inspect bd where/context, ready/active work, task and blockers before writes.
- Missing task access, workspace identity mismatch or failed claim is a blocker, not permission to continue untracked.
- Do not initialize, import a snapshot or guess database identity to repair access; require scoped recovery authority and verify existing data.
- Verify claim and update results by readback; one tracker owner per issue; a claim is not a file lock or Git permission.
- The task ID alone must recover goal, requirement, scope, inputs, dependencies, checks, ownership and restart context.
- Repair missing task context; no competing Markdown task databases, MEMORY.md or obsolete .loop state.
- Hierarchy: roadmap -> epic -> US -> task; one active epic/run and one main task/agent. US is a convention, not an assumed CLI type.
- Parent means hierarchy; bd dep add A B means A depends on B. Detail the ready frontier, not a task per file or phase.
- .beads/issues.jsonl is only an optional snapshot: at authorized task-state checkpoints export after permitted updates, review privacy/staged bytes and record time/coverage.
- Never edit/import a snapshot to sync status or close tasks to complete it; export does not authorize Git publication or Dolt sync.

## Method and handoff

- Load the relevant Skill; if discovery fails, read its actual source entrypoint and report direct reading, not activation.
- Read the Skill's required references before work/delivery; [cycle](skills/cycle/SKILL.md) routes phases, not implicit permissions.
- Goals/Non-goals explicit; behavior criteria use IDs, sources and Given/When/Then including errors/boundaries.
- Research/non-behavioral tasks use verifiable deliverables. NFRs need approved metric/target/unit, workload/window, environment and method; missing targets unresolved, N/A justified.
- Skill procedure: intent -> verified inputs/permissions -> action -> observable result -> named next Skill with inputs, or exact prerequisite to resume.
- Keep Skills host-neutral; isolate host-specific details in integration resources; avoid duplicating full phase procedures here.
- Follow [common output](skills/cycle/references/common-output.md) and the current phase contract: five-section final report, owned/preserved paths, actual versus proposed actions.
- At handoff include a fenced YAML state card and copy-ready restart prompt; separate immediate_action from conditional_next_phase.
- Recommend a fresh session for independent objectives, repository changes, stale hypotheses, major research/build handoffs or judge separation; a commit/compaction alone does not require one.
- Keep related implementation/tests/corrections together; report proposed session name/goal and actual action. No automatic launch or new permission from handoffs.

## Permissions and preservation

- Commit, push, merge, install, hook changes, deployment, tracker closure and Dolt sync require current scoped authority.
- Historical approvals/artifacts are context, not permission; follow [authorization policy](skills/cycle/references/authorization-policy.md).
- Local subtree instructions override parent rules for their paths, never current user permissions.
- Preserve initial dirty hunks, .beads/, evidence/, installed plugins, secrets, and existing host/Git hooks; preserve local Beads Skill if present.
- Parallel writes need disjoint paths or approved worktrees; no implicit reset, stash, cleanup, worktree removal or integration-branch mutation.
- Before commits verify identity and exact staged paths/hunks; include verified task ID, observe hash/message/paths, link results in Beads and read back.
- Entire is optional context capture, not task truth/acceptance: verify agent/worktree integration; never assume Goose support or forge session IDs/checkpoints/trailers.
- Close only authorized evidenced issue scope, not its parent/US/release; persist criteria, commands/results, candidate, limits and restart action before closure, then verify.
- Evaluate commit suitability after confirmed closure; closure never grants Git authority. Stop on completion, missing prerequisites or repeated no-progress.
- Default correction budget: three authorized attempts; diagnosis/waiting does not consume an attempt.

## Verification

~~~sh
python3 -B -m unittest discover -s tests -v
python3 -B tests/payload_inventory.py .
~~~

- Run focused checks first, then risk-relevant regressions; relevant official creator validation/audit and scenario checks when available.
- Bugs need a symptom-specific red-capable reproduction before repair; prefer public behavior seams and independent expected values. Missing seam is a finding, not proof.
- Separate static/source, mocked, installed-package and real-environment evidence; passing checks do not establish agent effectiveness or acceptance.
- Freeze/verify exact candidate inputs per [candidate identity](skills/cycle/references/candidate-identity.md); reject stale evidence after changes.
- Select review mode/independence before implementation per [review policy](skills/cycle/references/review-policy.md); weighted scoring default, predefined small-task mode N/A.
- Tests are evidence, not acceptance. No self-approval; missing required independence means indeterminate unless a known defect establishes needs-correction.
- Never weaken tests/criteria to manufacture success; record terminology/ADRs only for needed terms or hard-to-reverse decisions.
- Check changed local links, JSON syntax and shared-reference consistency; use verified cwd/actual exit codes, redact secrets, keep raw evidence out of routine commits.
- Verify current official Goose docs and exact runtime before host/hook changes; source presence is not installation. No blanket installs/generators/evaluations.
- No scripts/check-consistency.py or apps/ pipeline in this standalone repository; do not copy another checkout's commands or recursively load fixture/history instructions.

## Language

- All repository and distributed content defaults to English: documentation, Markdown, code comments, examples and versioned messages.
- Only an explicit user request authorizes a language exception; conversation language does not authorize one. Respond in the user's language.
- English documentation is canonical; translations remain separate and linked. Multilingual docs and Pages setup/publication need separate scope and deployment authority.
