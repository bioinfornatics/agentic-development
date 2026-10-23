#!/usr/bin/env python3
"""Build a local bilingual prototype, without installing or deploying anything.

Run: python website/build.py --output .site --base-url
     http://localhost:8000/agentic-development/
Install requirements separately in an isolated environment when authorized.
Existing nonempty outputs are refused (including earlier builds): choose a new
output or remove an old generated artifact yourself after inspecting it. No user
files are cleaned. Only the explicit page allowlist is staged; no recursive copy.
Zensical 0.0.71 requires site_dir under its config root: each temporary project
has separate docs/ and output/ directories. Finished locales are moved into a
second temporary publication root before the final rename.

The default repository URL matches the confirmed integration repository.
Override --repo-url when targeting a different repository. Source links use
that repository's main branch. English documentation remains canonical.
"""
from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = "http://localhost:8000/agentic-development/"
DEFAULT_REPO_URL = "https://github.com/bioinfornatics/agentic-development"
ENGLISH_PAGES = {
    "website/index.md": "index.md",
    "website/guides/getting-started.md": "getting-started.md",
    "website/guides/cycle.md": "cycle.md",
    "website/guides/integrations.md": "integrations.md",
    "website/guides/contributing.md": "contributing.md",
}
FRENCH_PAGES = {
    "website/i18n/fr/index.md": "index.md",
    "website/i18n/fr/getting-started.md": "getting-started.md",
}


def validate_url(value: str, *, base: bool = False) -> str:
    """Require an absolute HTTP(S) URL; base URLs must end in a slash."""
    parsed = urlsplit(value)
    if (parsed.scheme not in {"http", "https"} or not parsed.hostname
            or parsed.username is not None or parsed.password is not None
            or parsed.query or parsed.fragment or "?" in value or "#" in value
            or any(char.isspace() or ord(char) < 32 for char in value)
            or "\\" in value or (base and not value.endswith("/"))):
        raise ValueError("URL must be absolute HTTP(S), without credentials, query or fragment"
                         + (", and end with /" if base else ""))
    try:
        parsed.port
    except ValueError as exc:
        raise ValueError("Invalid URL port") from exc
    return value if base else value.rstrip("/")


def validate_output(output: Path) -> Path:
    """Reject source trees, repository ancestors, symlinks and nonempty targets."""
    raw = Path(output).absolute()
    if raw.is_symlink():
        raise ValueError("Output cannot be a symlink")
    resolved = raw.resolve()
    if resolved == Path(resolved.anchor) or ROOT == resolved or ROOT.is_relative_to(resolved):
        raise ValueError("Output cannot be a filesystem or repository root/ancestor")
    for name in ("docs", "skills", "hooks", "tests", "website", "scripts", "integration", ".git", ".beads", ".agents", ".claude", ".codex", ".vscode"):
        if resolved.is_relative_to(ROOT / name):
            raise ValueError(f"Output cannot be inside {name}/")
    if resolved.exists() and (not resolved.is_dir() or any(resolved.iterdir())):
        raise ValueError("Output already exists and is not an empty directory; choose a new path")
    return resolved


def page_url(base_url: str, language: str, page: str) -> str:
    return base_url + language + "/" + ("" if page == "index.md" else page[:-3] + "/")


def rewrite_links(text: str, source: Path, root: Path, pages: dict[str, str],
                  language: str, base_url: str, repo_url: str) -> str:
    """Rewrite inline/reference destinations, preserving code fences and URL suffixes."""
    current = {str((root / key).resolve()): val for key, val in pages.items()}
    english = {str((root / key).resolve()): val for key, val in ENGLISH_PAGES.items()}
    french = {str((root / key).resolve()): val for key, val in FRENCH_PAGES.items()}

    def destination(url: str) -> str:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
            return url
        target = (source.parent / unquote(parsed.path)).resolve()
        key = str(target)
        if key in current:
            path = current[key]
        elif key in english:
            path = page_url(base_url, "en", english[key])
        elif key in french:
            path = page_url(base_url, "fr", french[key])
        else:
            try:
                relative = target.relative_to(root).as_posix()
            except ValueError as exc:
                raise ValueError(f"Relative link leaves repository: {source}: {url}") from exc
            kind = "tree" if target.is_dir() else "blob"
            path = repo_url + "/" + kind + "/main/" + quote(relative, safe="/")
        return urlunsplit(("", "", path, parsed.query, parsed.fragment))

    def inline(match: re.Match[str]) -> str:
        url = match.group(2)
        angled = url.startswith("<")
        replaced = destination(url[1:-1] if angled else url)
        return match.group(1) + ("<" + replaced + ">" if angled else replaced)

    result = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            result.append(line)
            continue
        if fence is None:
            line = re.sub(r"(\]\(\s*)(<[^>]+>|[^\s)]+)", inline, line)
            line = re.sub(r"(^\s{0,3}\[[^\]]+\]:\s*)(<[^>]+>|\S+)", inline, line)
        result.append(line)
    return "".join(result)


def stage_language(root: Path, stage: Path, site_dir: Path, language: str,
                   base_url: str, repo_url: str = DEFAULT_REPO_URL) -> Path:
    """Public staging seam: write only selected Markdown and a documented TOML config."""
    if language not in {"en", "fr"}:
        raise ValueError("Language must be en or fr")
    base_url = validate_url(base_url, base=True)
    repo_url = validate_url(repo_url)
    root = root.resolve()
    docs_dir = stage.resolve() / "docs"
    docs_dir.mkdir(parents=True, exist_ok=False)
    pages = ENGLISH_PAGES if language == "en" else FRENCH_PAGES
    for relative, target in pages.items():
        source = root / relative
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            raise ValueError(f"Allowlisted source cannot escape the repository: {relative}")
        text = rewrite_links(source.read_text(encoding="utf-8"), source, root,
                             pages, language, base_url, repo_url)
        if target == "getting-started.md":
            other = "fr" if language == "en" else "en"
            label = "Lire cette page en français" if language == "en" else "Read the English source"
            text += f"\n\n[{label}]({page_url(base_url, other, target)})\n"
        if language == "fr" and target == "index.md":
            text += ("\n\nLes guides non traduits restent disponibles en anglais : "
                     f"[English documentation]({page_url(base_url, 'en', 'index.md')}).\n")
        (docs_dir / target).write_text(text, encoding="utf-8")
    nav = [("Home", "index.md"), ("Getting started", "getting-started.md"),
           ("Cycle", "cycle.md"), ("Integrations", "integrations.md"),
           ("Contributing", "contributing.md")]
    if language == "fr":
        nav = [("Accueil", "index.md"), ("Bien démarrer", "getting-started.md")]
    q = lambda value: json.dumps(str(value), ensure_ascii=False)
    config = stage / "zensical.toml"
    config.write_text(
        "# Generated temporary config; search uses Zensical defaults.\n[project]\n"
        + 'site_name = "Agentic Development"\n'
        + f"site_url = {q(base_url + language + '/')}\n"
        + f"docs_dir = {q(docs_dir.relative_to(stage.resolve()))}\nsite_dir = {q(site_dir.resolve().relative_to(stage.resolve()) if site_dir.resolve().is_relative_to(stage.resolve()) else site_dir.resolve())}\n"
        + "nav = [" + ", ".join("{ " + q(title) + " = " + q(page) + " }" for title, page in nav) + "]\n"
        + f"\n[project.theme]\nlanguage = {q(language)}\n"
        + "\n[project.extra]\nalternate = [\n"
        + f'  {{ name = "English", link = {q(base_url + "en/")}, lang = "en" }},\n'
        + f'  {{ name = "Français", link = {q(base_url + "fr/")}, lang = "fr" }}\n]\n',
        encoding="utf-8",
    )
    return config


def zensical_command() -> list[str]:
    """Use the active interpreter, or a PATH executable that passes --version."""
    candidates = [[sys.executable, "-m", "zensical"]]
    executable = shutil.which("zensical")
    if executable:
        candidates.append([executable])
    for command in candidates:
        try:
            probe = subprocess.run(command + ["--version"], capture_output=True, text=True)
        except OSError:
            continue
        if probe.returncode == 0 and probe.stdout.strip() == "0.0.71":
            return command
    raise RuntimeError("Required Zensical 0.0.71 is unavailable. Install website/requirements.txt separately "
                       "in an authorized isolated environment; no automatic install is performed.")


def build(output: Path, base_url: str, repo_url: str = DEFAULT_REPO_URL) -> Path:
    """Build both locales before atomically publishing into a new/empty directory."""
    base_url = validate_url(base_url, base=True)
    repo_url = validate_url(repo_url)
    output = validate_output(output)
    command = zensical_command()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="agentic-stage-") as staging, \
         tempfile.TemporaryDirectory(prefix=".agentic-artifact-", dir=output.parent) as artifacts:
        artifact = Path(artifacts) / "site"
        artifact.mkdir()
        for language in ("en", "fr"):
            stage = Path(staging) / language
            locale_output = stage / "output"
            config = stage_language(ROOT, stage, locale_output, language, base_url, repo_url)
            subprocess.run(command + ["build", "--strict", "--config-file", str(config)], cwd=stage, check=True)
            if not (locale_output / "index.html").is_file():
                raise RuntimeError(f"Zensical did not produce {language}/index.html")
            shutil.move(str(locale_output), artifact / language)
        links = " ".join(f'<a href="{html.escape(base_url + lang + "/", quote=True)}" lang="{lang}">{label}</a>'
                         for lang, label in (("en", "English"), ("fr", "Français")))
        (artifact / "index.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
                                            '<title>Agentic Development</title><body><h1>Agentic Development</h1>'
                                            + links + '</body></html>\n', encoding="utf-8")
        # Recheck immediately before rename; rename itself refuses a nonempty target.
        validate_output(output)
        os.rename(artifact, output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", type=Path, default=Path(".site"))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    args = parser.parse_args()
    try:
        print(f"Built {build(args.output, args.base_url, args.repo_url)}")
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
