"""Static convergence checks; not deployment or translation quality proof."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
class WebsiteConvergence(unittest.TestCase):
    def test_complete_french_mirror(self):
        self.assertEqual({p.name for p in (ROOT / "website/i18n/fr").glob("*.md")}, {"index.md","getting-started.md","cycle.md","integrations.md","contributing.md"})
    def test_single_automatic_pages_workflow(self):
        paths=[p for p in (ROOT / ".github/workflows").glob("*.yml") if "actions/deploy-pages@" in p.read_text()]
        self.assertEqual([p.name for p in paths],["pages.yml"])
        self.assertIn("push:",paths[0].read_text())
    def test_local_canonical_reporting_preserved(self):
        text=(ROOT / "website/i18n/fr/cycle.md").read_text()
        for field in ("current goal {step: …}", "roadmap position", "modified files", "closed tasks", "explanation"):
            self.assertIn("**"+field+"**",text)
        self.assertNotIn("Le bilan suit six",text)
