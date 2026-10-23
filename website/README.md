# Local Zensical documentation prototype

English guides in guides/ are canonical. The builder stages an explicit allowlist
in temporary directories; generated copies are disposable, never edited sources.
The French edition currently contains only Getting started and a language landing.
The header selector opens each edition's home. Getting started links its equivalent;
other French links explicitly lead to English. No translation plugin is assumed.
Zensical's search interface is currently English, including in the French edition.

## Build and preview

From the repository root, with an authorized isolated dependency environment:

Use a dedicated preview root so the project Pages prefix resolves correctly:

    uv run --isolated --no-project --with-requirements website/requirements.txt python website/build.py --output /tmp/agentic-preview/agentic-development --base-url http://localhost:8000/agentic-development/
    python3 -m http.server 8000 --bind 127.0.0.1 --directory /tmp/agentic-preview

Open http://localhost:8000/agentic-development/. Serve only generated output,
not the repository (which includes internal instructions and local task data).
Existing nonempty outputs are refused, including earlier builds. Choose a fresh
output path; inspect old generated artifacts before removing them yourself.

## Scope and configuration

Two independent Zensical builds set theme.language to en/fr and generate separate
search indexes. The builder uses supported language/alternate configuration,
not MkDocs translation plugins. Version is pinned in requirements.txt; transitive
dependencies are not fully locked. No global install or automatic install occurs.

Use --base-url https://OWNER.github.io/REPOSITORY/ for a future project site.
Use --repo-url https://github.com/OWNER/REPOSITORY for source links. The default
repository URL is bioinfornatics/agentic-development, matching this checkout
remote; confirm the destination again before publication. Source links use main; local uncommitted
source content may not exist remotely. Relative guide links become local site
links; optional non-guide references become GitHub source links, not public copies.

Only the four English guides, landing pages and French starter are
published. AGENTS.md, Skill fixtures, evidence and task data are never copied.
This prototype does not install the agent plugin or activate Goose hooks.

A manually gated workflow is prepared in .github/workflows/pages.yml.
It has not executed on GitHub. Pages settings, push and publication have not been
performed. Browser verification remains separate from a successful build.

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

No push-triggered deployment exists. Publish defaults to false. Publication fails
unless both variables match the guards and the default branch is used.
configure-pages reads metadata with enablement false, without enabling Pages.
Build permissions are read-only; only deployment has Pages/OIDC writes.
Leave site_url empty for publication to use existing Pages metadata including
custom domains. A manual override must match the actual hosting URL; it does not
configure a domain. Build-only fallback handles standard project/user Pages URLs.
Source links derive from github.repository, not the prototype assumption.
The workflow is prepared locally, not executed as a live deployment.
Top-level actions use observed upstream SHAs; transitive action/package references
are not fully locked. Never upload or serve the repository itself.

## Upstream references

- [Language configuration](https://github.com/zensical/docs/blob/master/docs/setup/language.md)
- [Search behavior](https://github.com/zensical/docs/blob/master/docs/setup/search.md)
- [Build CLI](https://github.com/zensical/docs/blob/master/docs/usage/build.md)

## Integration boundary

This branch preserves harness, apps and portable core 0.4.2 unchanged. Site guides
use its existing drive-cycle and *-slice identifiers. The standalone 0.5.0 core
and observation hooks are not ported. English guides in website/guides are canonical
for this site. Existing harness docs stay in Git, but are not included in the new
site; legacy harness/evaluation public URLs are not preserved by this slice.
The former push-triggered pages.yml is replaced, not kept alongside this workflow.
The integration checkout has a confirmed remote, bioinfornatics/agentic-development.
