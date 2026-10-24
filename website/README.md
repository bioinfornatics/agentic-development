# Zensical documentation website

English guides in ../docs/ and the English home are canonical. The builder stages
an explicit allowlist in temporary directories; generated copies are disposable,
never edited sources. French mirrors all five English pages, with matching section
structure and navigation order, French guide links and a discreet English source
link on every page. Missing translations or route mismatches stop staging.
The site root opens the themed English home by default, with language fallback links.
The header shows the active flag and language name. Its native disclosure offers
both named languages and retains the current page when switching. Enter/Space open
it; Tab follows links, arrow keys move between choices, and Escape dismisses it.
Links and disclosure also work without JavaScript. The pinned theme selector is
replaced after building; unexpected upstream markup stops the build rather than
silently removing the selector. Only the contained CSS/JavaScript assets are read.
No translation plugin is assumed. Zensical's search interface is currently English,
including in the French edition. Structural checks cannot prove translation fidelity.

## Build and preview

From the repository root, with an authorized isolated dependency environment:

Use a dedicated preview root so the project Pages prefix resolves correctly:

    uv run --isolated --no-project --with-requirements website/requirements.txt python website/build.py --output /tmp/agentic-preview/agentic-development --base-url http://localhost:8000/agentic-development/
    python3 -m http.server 8000 --bind 127.0.0.1 --directory /tmp/agentic-preview

Open http://localhost:8000/agentic-development/. Serve only generated output,
not the repository (which includes internal instructions and local task data).
Existing nonempty outputs are refused, including earlier builds. Choose a fresh
output path; inspect old generated artifacts before removing them yourself.

## Verify local bilingual journeys

Run the standard-library suite from the repository root:

    python3 -m unittest discover -s website/tests -v

For a generated preview already served on loopback, with Playwright and Chromium
already available, run the opt-in browser probe using a fresh evidence directory:

    python3 website/tests/browser_probe.py --base-url http://localhost:8000/agentic-development/ --evidence-dir /tmp/agentic-browser-evidence

It checks ten equivalent-page switches, keyboard opening/navigation/dismissal,
mobile widths 320/390/768, root redirect, no-JavaScript switching and observed
HTTP/page errors. It records screenshots and a result summary. It does not install
anything, prove screen-reader accessibility or certify every browser. Translation
structure checks are not a substitute for independent semantic review.

## Scope and configuration

Two independent Zensical builds set theme.language to en/fr and generate separate
search indexes. The builder uses supported language/alternate configuration,
not MkDocs translation plugins. Version is pinned in requirements.txt; transitive
dependencies are not fully locked. No global install or automatic install occurs.

Use --base-url https://OWNER.github.io/REPOSITORY/ for a project site.
Use --repo-url https://github.com/OWNER/REPOSITORY for source links. The default
repository URL is bioinfornatics/agentic-development, the delivered upstream destination; this local checkout has no configured remote.
Confirm the destination again before publication. Source links use main; local uncommitted
source content may not exist remotely. Relative guide links become local site
links; optional non-guide references become GitHub source links, not public copies.

Only the two homes and four guides in each language are published. AGENTS.md, Skill fixtures, evidence and task data are never copied.
This documentation builder does not install the agent plugin or activate Goose hooks.

The workflow is in .github/workflows/pages.yml. PRs run tests and builds only;
pushes to main automatically build and publish after repository guards pass.
This workflow is adapted from the delivered integration repository. It has not
executed from this standalone candidate; no publication is performed by preparation.
Browser verification remains separate from a successful build.

## Prepare GitHub Pages (separate remote authorization)

1. Confirm the repository/default branch: bioinfornatics/agentic-development, main.
2. Review and commit/push intended source only when separately authorized.
3. In Settings → Pages, select GitHub Actions as the build source.
4. Restrict the github-pages environment to the default branch and require
   reviewer approval where available for the repository/plan.
5. Set PAGES_REPOSITORY to exact OWNER/REPOSITORY and PAGES_DEPLOY_ENABLED to true
   only after reviewing public content and explicitly authorizing hosting.
6. Run workflow_dispatch with publish false first and inspect the artifact.
7. After explicit publication approval, dispatch on the default branch with
   publish true; verify the resulting public URL and both locales.

Pushes to main request publication automatically. PRs never publish and have no
Pages/OIDC write permissions. Manual publish defaults to false. Publication fails
unless both variables match the guards and the default branch is used. To pause
automatic publication, set PAGES_DEPLOY_ENABLED to false; main builds fail closed.
PR runs are isolated per ref; publication runs serialize on the main ref.
configure-pages reads metadata with enablement false, without enabling Pages.
Build permissions are read-only; only deployment has Pages/OIDC writes.
Leave site_url empty for publication to use existing Pages metadata including
custom domains. A manual override must match the actual hosting URL; it does not
configure a domain. Build-only fallback handles standard project/user Pages URLs.
Source links derive from github.repository, not a fixed site assumption.
Top-level actions use observed upstream SHAs; transitive action/package references
are not fully locked. Never upload or serve the repository itself.

## Upstream references

- [Language configuration](https://github.com/zensical/docs/blob/master/docs/setup/language.md)
- [Search behavior](https://github.com/zensical/docs/blob/master/docs/setup/search.md)
- [Build CLI](https://github.com/zensical/docs/blob/master/docs/usage/build.md)

## Integration boundary

Standalone source 0.5.0 uses the seven short Skill names and the current
seven-field final report, conditional commit evaluation and correction policy.
English guides in ../docs/ remain canonical; the builder does not create duplicate
English guide sources. This checkout has no configured remote. The delivered
integration website supplied the pinned builder and selector, not its older core
procedures or harness topology. No harness, runtime or hook activation is imported.
Exactly one Pages workflow is prepared; the old manual-only workflow is preserved
outside the repository, not kept as a second deployer. Publication needs separate
current authority and verification in the actual destination repository.
