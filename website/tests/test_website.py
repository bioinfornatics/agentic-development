"""Builder behavior at staging/subprocess seams; browser checks are separate."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('website_builder', ROOT / 'website/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class DocumentationBuilder(unittest.TestCase):
    def test_staging_is_allowlisted_and_does_not_edit_canonical_sources(self):
        original = (ROOT / 'docs/getting-started.md').read_bytes()
        with tempfile.TemporaryDirectory() as temp:
            stage = Path(temp) / 'en'
            config = builder.stage_language(ROOT, stage, stage / 'output', 'en',
                                            'http://localhost:8000/agentic-development/')
            self.assertEqual({p.name for p in (stage / 'docs').iterdir()},
                             {'index.md', 'getting-started.md', 'cycle.md',
                              'integrations.md', 'contributing.md'})
            data = tomllib.loads(config.read_text())['project']
            self.assertEqual(data['theme']['language'], 'en')
            self.assertEqual(data['site_url'], 'http://localhost:8000/agentic-development/en/')
            self.assertEqual(data['extra']['alternate'][1]['link'],
                             'http://localhost:8000/agentic-development/fr/')
            contribution = (stage / 'docs/contributing.md').read_text()
            self.assertIn('/blob/main/AGENTS.md', contribution)
            self.assertIn('/blob/main/skills/cycle/references/', contribution)
        self.assertEqual((ROOT / 'docs/getting-started.md').read_bytes(), original)

    def test_french_links_to_equivalent_source_and_local_guides(self):
        with tempfile.TemporaryDirectory() as temp:
            stage = Path(temp) / 'fr'
            builder.stage_language(ROOT, stage, stage / 'output', 'fr',
                                   'http://localhost:8000/agentic-development/')
            text = (stage / 'docs/getting-started.md').read_text()
            self.assertIn('http://localhost:8000/agentic-development/en/getting-started/', text)
            self.assertIn('](cycle.md)', text)
            self.assertNotIn('/en/cycle/', text)
            self.assertIn('anglais', (stage / 'docs/index.md').read_text())

    def test_output_guards_preserve_sources_and_user_files(self):
        for output in [ROOT, ROOT.parent, ROOT / 'docs/generated', ROOT / 'website/site',
                       ROOT / 'scripts/site', ROOT / '.claude/site', ROOT / '.vscode/site']:
            with self.subTest(path=output), self.assertRaises(ValueError):
                builder.validate_output(output)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'existing'; path.mkdir()
            (path / 'user.txt').write_text('preserve')
            with self.assertRaises(ValueError): builder.validate_output(path)
            self.assertEqual((path / 'user.txt').read_text(), 'preserve')

    def test_invalid_urls_rejected(self):
        for url in ['relative/', 'file:///tmp/', 'https://user:pass@example.org/',
                    'http://localhost/path', 'http://localhost/?x=1', 'http://localhost/#fragment']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                builder.validate_url(url, base=True)

    def test_wrong_package_version_rejected(self):
        probe = subprocess.CompletedProcess([], 0, stdout='Zensical version: 9.9.9', stderr='')
        with patch.object(builder.shutil, 'which', return_value=None),              patch.object(builder.subprocess, 'run', return_value=probe):
            with self.assertRaises(RuntimeError): builder.zensical_command()

    def test_build_is_strict_and_failure_leaves_output_unpublished(self):
        commands = []
        def fail(command, **kwargs):
            commands.append(command)
            raise subprocess.CalledProcessError(1, command)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'site'
            with patch.object(builder, 'zensical_command', return_value=['zensical']),                  patch.object(builder.subprocess, 'run', side_effect=fail):
                with self.assertRaises(subprocess.CalledProcessError):
                    builder.build(output, 'http://localhost:8000/agentic-development/')
            self.assertFalse(output.exists())
            self.assertIn('--strict', commands[0])

    def test_preview_instructions_do_not_serve_repository(self):
        text = (ROOT / 'website/README.md').read_text()
        self.assertNotIn('--directory .', text)
        self.assertIn('--directory /tmp/agentic-preview', text)


if __name__ == '__main__':
    unittest.main()


class DefaultLanguageLanding(unittest.TestCase):
    def test_root_opens_english_with_accessible_language_fallback(self):
        page = builder.landing_page()
        self.assertIn('http-equiv="refresh"', page)
        self.assertIn('url=en/', page)
        self.assertIn('href="en/"', page)
        self.assertIn('href="fr/"', page)
        self.assertNotIn('localhost', page)
        self.assertIn('<html lang="en">', page)
