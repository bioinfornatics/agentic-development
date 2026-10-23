"""Static selector contracts; keyboard/rendered checks run in a browser separately."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('selector_builder', ROOT / 'website/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class LanguageSelector(unittest.TestCase):
    def test_active_label_and_equivalent_named_choices(self):
        for language, label in [('en', 'English'), ('fr', 'Français')]:
            for route in ['index.md', 'cycle.md', 'getting-started.md', 'integrations.md', 'contributing.md']:
                markup = builder.language_selector('https://example.org/prefix/', language, route)
                self.assertIn('<details class="language-selector">', markup)
                self.assertIn('<summary', markup)
                self.assertIn(label, markup.split('</summary>')[0])
                self.assertIn('🇬🇧', markup)
                self.assertIn('🇫🇷', markup)
                for other in ('en', 'fr'):
                    self.assertIn('href="'+builder.page_url('https://example.org/prefix/',other,route)+'"',markup)
                    self.assertIn('hreflang="'+other+'"',markup)
                self.assertIn('aria-current="page"', markup)

    def test_unknown_locale_or_page_is_rejected(self):
        for language, page in [('de','index.md'),('en','missing.md')]:
            with self.assertRaises(ValueError):
                builder.language_selector('https://example.org/',language,page)

    def test_render_hook_fails_on_upstream_markup_drift(self):
        with self.assertRaisesRegex(ValueError, 'selector'):
            builder.replace_language_selector('<html>changed theme</html>', 'https://example.org/', 'en','index.md')

    def test_successful_replacement_preserves_header_and_injects_assets_once(self):
        native = ('<header>before<div class="md-header__option"><div class="md-select">'
                  '<button>language</button><div><ul><li>choice</li></ul></div></div></div>'
                  'after</header>')
        html = '<html><head></head><body>'+native+'</body></html>'
        actual = builder.replace_language_selector(html, 'https://example.org/project/', 'fr', 'cycle.md')
        self.assertIn('<header>before<details', actual)
        self.assertIn('</details>after</header>', actual)
        self.assertEqual(actual.count('<style>'), 1)
        self.assertEqual(actual.count('<script>'), 1)
        self.assertEqual(actual.count('<details class="language-selector">'), 1)
        self.assertNotIn('class="md-select"', actual)
