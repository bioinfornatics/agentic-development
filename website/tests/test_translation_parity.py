"""Translation structure contracts; semantic fidelity requires human review."""
import importlib.util
from pathlib import Path
import re
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('parity_builder', ROOT / 'website/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
EXPECTED = ['index.md', 'getting-started.md', 'cycle.md', 'integrations.md', 'contributing.md']

class TranslationParity(unittest.TestCase):
    def test_complete_routes_and_matching_navigation(self):
        self.assertEqual(list(builder.ENGLISH_PAGES.values()), EXPECTED)
        self.assertEqual(list(builder.FRENCH_PAGES.values()), EXPECTED)
        with tempfile.TemporaryDirectory() as temp:
            targets = []
            for language in ('en', 'fr'):
                stage = Path(temp) / language
                config = builder.stage_language(ROOT, stage, stage / 'output', language,
                                                'https://example.org/project/')
                project = tomllib.loads(config.read_text())['project']
                targets.append([next(iter(entry.values())) for entry in project['nav']])
                self.assertEqual(sorted(p.name for p in (stage / 'docs').iterdir()), sorted(EXPECTED))
            self.assertEqual(targets, [EXPECTED, EXPECTED])

    def test_matching_heading_structure_and_skill_identifiers(self):
        self.assertEqual(list(builder.FRENCH_PAGES.values()), EXPECTED)
        for english, french in zip(builder.ENGLISH_PAGES, builder.FRENCH_PAGES):
            en = (ROOT / english).read_text()
            fr = (ROOT / french).read_text()
            with self.subTest(page=english):
                headings = lambda text: [line.split(' ', 1)[0] for line in text.splitlines() if line.startswith('#')]
                self.assertEqual(headings(en), headings(fr))
                names = lambda text: re.findall('agentic-development:[a-z-]+', text)
                self.assertEqual(names(en), names(fr))

    def test_each_french_page_has_one_canonical_source_and_local_guide_links(self):
        with tempfile.TemporaryDirectory() as temp:
            stage = Path(temp) / 'fr'
            builder.stage_language(ROOT, stage, stage / 'output', 'fr', 'https://example.org/project/')
            for target in EXPECTED:
                text = (stage / 'docs' / target).read_text()
                canonical = builder.page_url('https://example.org/project/', 'en', target)
                self.assertEqual(text.count(canonical), 1, target)
                self.assertIn('Source canonique', text)
                for link in re.findall(r'][(]([^ )]+)', text):
                    if '/en/' in link:
                        self.assertEqual(link, canonical, (target, link))
                self.assertNotIn('guides non traduits', text)

    def test_missing_translation_and_route_mismatch_fail_before_staging(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = dict(builder.FRENCH_PAGES)
            missing.pop(next(iter(missing)))
            with patch.object(builder, 'FRENCH_PAGES', missing):
                with self.assertRaisesRegex(ValueError, 'parity'):
                    builder.stage_language(ROOT, Path(temp) / 'fr', Path(temp) / 'fr/output', 'fr',
                                           'https://example.org/project/')
            missing_file = dict(builder.FRENCH_PAGES)
            first = next(iter(missing_file))
            missing_file['website/i18n/fr/missing.md'] = missing_file.pop(first)
            with patch.object(builder, 'FRENCH_PAGES', missing_file):
                with self.assertRaises((ValueError, FileNotFoundError)):
                    builder.stage_language(ROOT, Path(temp) / 'missing', Path(temp) / 'missing/output', 'fr',
                                           'https://example.org/project/')

    def test_homes_do_not_claim_partial_translation_or_local_only_publication(self):
        en = (ROOT / 'website/index.md').read_text()
        fr = (ROOT / 'website/i18n/fr/index.md').read_text()
        for token in ('local Zensical prototype', 'currently includes', 'only Getting started'):
            self.assertNotIn(token, en)
        for token in ('Traduction partielle', 'prototype local', "aucune publication GitHub Pages", 'Seul le guide'):
            self.assertNotIn(token, fr)

    def test_canonical_source_url_is_html_escaped(self):
        from html import escape
        base = 'https://example.org/"><script>alert(1)</script>/'
        with tempfile.TemporaryDirectory() as temp:
            stage = Path(temp) / 'fr'
            builder.stage_language(ROOT, stage, stage / 'output', 'fr', base)
            text = (stage / 'docs/cycle.md').read_text()
            self.assertIn('href="' + escape(builder.page_url(base, 'en', 'cycle.md'), quote=True) + '"', text)
            self.assertNotIn('<script>', text)
