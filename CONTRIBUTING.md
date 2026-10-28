# Contributing and production promotion

## Branch contract

The source branch is named **develop** (formerly development).

```text
feature/* -> reviewed source PR -> develop
develop -> exact-source verification and independent approval
            -> generated installation projection -> main
```

**Feature PRs target develop. Never merge develop into main.** A
production PR contains only a generated installation tree based on previous main,
not a develop source merge. Squash that generated-only PR after verification;
never merge or delete develop as part of publication.

- develop owns editable instructions, tests, tools and build inputs.
- main is reserved for the generated, ready-to-install distribution.
- Production publication creates a generated-tree commit with previous main as its
  sole parent. With protected main, use a generated-only PR and a squash merge;
  the resulting commit has previous main as sole parent (a fast-forward update).
  Never force-push production or bypass required PR checks.
- Feature branches start from develop. Check the worktree and preserve existing
  changes; Git operations, installation and promotion require current authority.

## Source verification

Read [repository instructions](AGENTS.md) and [instruction authoring](docs/contributing.md).
Run `python3 -B -m unittest discover -s tests -v` from the source repository.
Use official component validation for changed Skills/hooks and risk-relevant tests.
Source CI checks the exact source SHA, not GitHub synthetic merge content.
Passing static checks does not prove agent behavior or installed-host compatibility.

## Production boundary

Generate only the manifest, self-contained Skills and their required resources,
user-facing prerequisite documentation, provenance, read-only verification workflows
and verified optional hook runtimes. Runtime metadata uses a distributor-owned
manifest extension; it does not install dependencies or promise portable execution.
Exclude tests, evaluations, research, tracker state, repository instructions and
build tools from the installation payload. Hash the projected paths, modes and bytes.

Current portable Skills are Markdown. The optional observer uses the Python standard
library; prepare any executable runtime before publication. End-user installation
must require no build or dependency download. Future runtimes must carry their
contained, locked dependency closure and explicit host prerequisites.

## Promotion gates

1. Merge an independently reviewed feature PR into develop.
2. Freeze a clean exact source SHA and the expected current main SHA.
3. Build the distribution deterministically, verify its inventory and contained
   runtimes, and test Git installation/update in an authorized isolated environment.
4. Obtain independent maintainer approval for that exact source and evidence.
5. Recheck approval, source SHA and current main immediately before a separately
   authorized generated-tree publication. Changed inputs or stale approval stop it.
6. Publish without force, then verify remote provenance and installation results.

Do not use GitHub Merge on a develop-to-main source request. Use squash
only for an exact verified generated-tree PR based on previous main. Source changes enter main only
through the generated projection. Approval and branch-protection enforcement are
separate repository settings; this policy and read-only CI do not configure them.

## Generate and verify a distribution candidate

From a clean committed develop source checkout, use a new destination outside
the repository:

```sh
python3 -B tools/production.py candidate /absolute/new/product
python3 -B tools/production.py verify /absolute/new/product
python3 -B tools/production.py smoke /absolute/new/product
```

The candidate binds the exact source commit/tree and rejects dirty or untracked
source and uncommitted operational resources. `project` remains a working-tree
preview. Both keep `release_ready=false`: integrity is not review or installation
approval. Verify candidate hashes after isolated Git install/update and before
publication. The opt-in real-host probe uses disposable HOME, XDG and Goose
roots and a local Git transport repository; it never replaces a live installation:

```sh
python3 -B tests/probe_goose_distribution.py /absolute/new/product --goose /absolute/path/to/goose
```

The probe requires Goose 1.56.0, checks the exact seven Skills with
`goose skills list` after installation and update, verifies installed payload
hashes and observer execution, and confirms that update removes an obsolete
fixture. Working-tree previews are diagnostic evidence, not committed-source
or release approval. This probe is not part of the automatic unit suite.

Production excludes creator eval sets, evaluation/conformance fixtures and
synthetic study inputs, including those nested under Skill resources. Unknown
nested `SKILL.md*` entrypoints fail closed; suffixes such as `.fixture` are not
a reliable discovery boundary. Operational references and user output templates
remain contained and available. These commands never publish or mutate branches.

## Distribution status and limits

- main contains a generated installation projection; develop remains its editable source.
- Resolve the published source SHA from main's distribution.json; do not assume it matches the latest develop.
- Source updates require a new verified projection and separately authorized promotion.
- Inventory integrity and branch names do not establish installation compatibility or release acceptance.
- The generator and read-only CI do not publish, approve, configure protection or bypass promotion gates.
- No license grant is present in source; do not invent one or copy another project's license.
- Preserve local tracker/evidence and source history; do not infer publication authority from prior runs.

## Evaluate the cycle coordinator with Skill Creator

Every Skill already has a canonical evals/evals.json source suite. The cycle
suite now includes five adapted integration cases with distinct immutable
hypothetical fixtures under skills/cycle/evals/files/. The original integration/
inventory is retained, but is not the direct Skill Creator input. These
explain-level cases assess proposed coordination and handoffs, not live
implementation, tracker operations or acceptance of all seven Skills.

Explanation assertions cover observable final-output properties. Actual read/order
and prerequisite requirements remain in canonical execution_assertions metadata;
they require instrumented execution evidence, not self-reports. Official normalized
sets may omit this metadata. Preserve it separately and never retrofit old grades
onto changed cases. For a real disposable cancellation fixture and independent
checker, see [the execution pilot](integration/execution-pilot/README.md). Its default
isolation gate is BLOCKED: copied directories and fresh sessions do not prove that
ambient Skills/hints or sibling/coordinator inputs are excluded. Preserve normal
authentication and verify host exclusion before any clean-baseline model campaign.

Pilot the installed agent-plugins Skill Creator CLI from the active session.
Use full-eval --execute and its Goose subprocess runner by default; keep native
delegation optional. Follow skills/cycle/references/session-evaluation.md.
Do not copy its runtime here or install dependencies as part of evaluation.
From the repository root:

~~~sh
skill-creator validate skills/cycle
skill-creator design-evals skills/cycle/evals/evals.json --skill-path skills/cycle --format json
skill-creator full-eval skills/cycle --workspace evidence/runs/<campaign>/iteration-1 --dry-run --format json
~~~

For a source installation, replace skill-creator with the installed launcher:
node /absolute/agent-plugins/skills/skill-creator/scripts/skill-creator.mjs.
That launcher requires Node.js 22 or newer; native packages use their executable.

Before live comparison, agree current/baseline snapshots, executor and independent
grader models, equivalent fixture/resource access, run profile and spending caps.
The suite's aggregate budget covers the standard profile's three paired
repetitions per scenario. It is schedule capacity, not authorization to spend.
Declared developer access enables fixture/reference reads; correct use still
requires evidence. These declarations are not an OS sandbox. Non-cycle suites
remain separate and are not automatically executed by this campaign.

For an old-versus-current comparison, use a separately frozen baseline Skill:

~~~sh
skill-creator full-eval skills/cycle --workspace evidence/runs/<campaign>/iteration-1 --execute --baseline old_skill --baseline-skill /absolute/frozen/cycle --model <executor-model> --grader review-a=<grader-model> --run-profile standard --format json
~~~

Confirm installed CLI help before execution. Keep both variants' fixture and
resource access equivalent. An older snapshot lacking the new fixtures requires
an isolated staging decision before dispatch. Do not inject grades into prompts.
After each output has bound independent blinded grading, aggregate and generate
the official viewer:

~~~sh
skill-creator aggregate evidence/runs/<campaign>/iteration-1 --skill-name cycle
skill-creator review evidence/runs/<campaign>/iteration-1 --skill-name cycle --benchmark evidence/runs/<campaign>/iteration-1/benchmark.json --static evidence/runs/<campaign>/iteration-1/review.html
~~~

Let official tools produce outputs, grades, benchmarks and receipts. Preserve
incomplete work and resume at its first incomplete phase. One exploratory pair
does not establish stable improvement; completed artifacts do not grant release
approval. Results remain local evidence; all evals/ directories stay excluded
from the installation projection. No model, Git publication or closure permission
is implied by these examples.

### Optional native session loop (no Goose subprocess)

Select this alternative explicitly; do not use it to relabel failed official runs.
Use tools/session_eval.py for explain-level text scenarios. The active session
performs native candidate and grader delegation; the script makes no model calls.
Follow skills/cycle/references/session-evaluation.md. Pass the explicit scenario
model and turn budget to each delegate. Observe completion before recording bytes.

~~~sh
python3 -B tools/session_eval.py prepare skills/cycle evidence/runs/<campaign>/session --eval-set skills/cycle/evals/evals.json --model <model> --ids 25
python3 -B tools/session_eval.py status evidence/runs/<campaign>/session
~~~

Delegate each request.json. Save returned responses outside frozen inputs.
Import them with record. Delegate each grading-request.json to a separate grader.
Import its array with grade. Run report with the installed generate_review.js.
This reuses official rendering functions, not full-eval receipt acceptance.
Session records are coordinator-observed. No authenticated usage, sandbox,
natural activation or ambient baseline exclusion is implied. Never relabel this
workspace as full-eval or sign an invented governed-import receipt.
