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

    def test_ci3_source_triggers_and_bilingual_verification(self):
        trigger = self.text.split('permissions:', 1)[0]
        for event in ('push', 'pull_request'):
            block = trigger.split('  ' + event + ':', 1)[1].split('\n  pull_request:', 1)[0].split('\n  workflow_dispatch:', 1)[0]
            self.assertIn('branches: [main, develop]', block)
        verify = self.text.split('      - name: Verify source contracts', 1)[1].split('      - name:', 1)[0]
        self.assertIn('python -m unittest discover -s website/tests -v', verify)
        self.assertIn('Build both locales', self.text)
        self.assertIn('python website/build.py --output .site', self.text)

    def test_ci3_develop_push_cannot_request_publication(self):
        # Source contract only: not a GitHub expression evaluator or hosted CI run.
        intent = "(github.event_name == 'push' && github.ref == 'refs/heads/main') || (github.event_name == 'workflow_dispatch' && inputs.publish)"
        for name in ('Check publication prerequisites', 'Read existing Pages configuration'):
            block = self.text.split('      - name: ' + name, 1)[1].split('      - name:', 1)[0]
            self.assertIn('if: ' + intent, block)
        resolve = self.text.split('      - name: Resolve site and source URLs', 1)[1].split('      - name:', 1)[0]
        self.assertIn('PUBLISH: ${{ ' + intent + ' }}', resolve)
        deploy = self.text.split('  deploy:', 1)[1]
        self.assertIn('(' + intent + ') &&', deploy)
        for guard in ("vars.PAGES_DEPLOY_ENABLED == 'true'",
                      'vars.PAGES_REPOSITORY == github.repository',
                      "github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"):
            self.assertIn(guard, deploy)
        self.assertNotIn('pull_request_target', self.text)
        self.assertIn('group: documentation-pages-', self.text)
