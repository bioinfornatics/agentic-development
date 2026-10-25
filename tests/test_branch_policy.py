"""Static branch-policy checks, not enforcement or installation evidence."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class BranchPolicy(unittest.TestCase):
    def test_contribution_flow_separates_source_and_product(self):
        text = (ROOT / "CONTRIBUTING.md").read_text()
        for term in ("develop", "Feature PRs target", "Never merge",
                     "sole parent", "fast-forward", "exact source SHA",
                     "independent", "isolated", "not yet", "no build"):
            self.assertIn(term, text)
        self.assertIn("../CONTRIBUTING.md", (ROOT / "docs/contributing.md").read_text())

    def test_source_ci_checks_exact_head_without_write_permissions(self):
        text = (ROOT / ".github/workflows/source-checks.yml").read_text()
        for term in ("branches: [develop]", "contents: read",
                     "github.event.pull_request.head.sha || github.sha",
                     "persist-credentials: false",
                     "python -B -m unittest discover -s tests -v"):
            self.assertIn(term, text)
        for term in ("pull_request_target", "contents: write", "secrets.",
                     "git push", "pip install", "npm install"):
            self.assertNotIn(term, text)
        for action in re.findall(r"uses: ([^ ]+)", text):
            self.assertRegex(action, r"^actions/[a-z-]+@[0-9a-f]{40}$")

class DevelopLinks(unittest.TestCase):
    def test_old_branch_is_not_a_ci_target(self):
        text = (ROOT / ".github/workflows/source-checks.yml").read_text()
        self.assertNotIn("development", text.lower())
        self.assertIn('run: test "$BASE_BRANCH" = develop', text)

    def test_generated_readme_targets_develop(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("/blob/develop/", text)
        self.assertNotIn("/blob/development/", text)
        self.assertIn("source branch is named **develop**", (ROOT / "CONTRIBUTING.md").read_text())

if __name__ == "__main__":
    unittest.main()
