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
python3 -B tests/probe_goose_distribution.py /absolute/new/product
```

The probe requires Goose 1.47.0, checks the exact seven Skills with
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
