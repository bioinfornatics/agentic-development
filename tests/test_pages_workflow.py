"""Static Pages safety contracts, not remote execution evidence."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
class PagesWorkflow(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / '.github/workflows/pages.yml').read_text()
    def test_automatic_triggers_and_manual_build_default(self):
        trigger = self.text.split('permissions:', 1)[0]
        self.assertIn('workflow_dispatch:', trigger)
        self.assertIn('push:', trigger)
        self.assertIn('pull_request:', trigger)
        self.assertIn('default: false', trigger)
    def test_explicit_deployment_guards(self):
        deploy = self.text.split('  deploy:', 1)[1]
        for token in ('inputs.publish', "vars.PAGES_DEPLOY_ENABLED == 'true'",
                      'vars.PAGES_REPOSITORY == github.repository',
                      'github.event.repository.default_branch', 'needs: build',
                      'pages: write', 'id-token: write', 'name: github-pages'):
            self.assertIn(token, deploy)
        build = self.text.split('  build:', 1)[1].split('  deploy:', 1)[0]
        self.assertNotIn('pages: write', build)
        self.assertIn('pages: read', build)
        self.assertIn('persist-credentials: false', build)
        self.assertIn('enablement: false', build)
    def test_pinned_actions_generated_artifact_and_quoted_urls(self):
        uses = re.findall(r'uses: ([^ ]+)', self.text)
        self.assertEqual(len(uses), 5)
        for action in uses: self.assertRegex(action, r'^actions/[a-z-]+@[0-9a-f]{40}$')
        for token in ('path: .site', 'python website/build.py',
                      '--base-url "$SITE_URL"', '--repo-url "$REPO_URL"'):
            self.assertIn(token, self.text)
    def test_publication_still_requires_separate_authorization(self):
        text = (ROOT / 'website/README.md').read_text()
        for token in ('PAGES_REPOSITORY', 'PAGES_DEPLOY_ENABLED', 'workflow_dispatch',
                      'separately authorized'):
            self.assertIn(token, text)

    def test_publication_intent_excludes_pr_and_includes_main_push(self):
        intent = "github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && inputs.publish)"
        self.assertEqual(self.text.count(intent), 4)
        self.assertIn('branches: [main]', self.text)
        self.assertNotIn('pull_request_target', self.text)
        self.assertIn('group: documentation-pages-', self.text)
