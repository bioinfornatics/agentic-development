"""Public probe version-gate regressions; mocked host, not installation evidence."""
import importlib.util
from pathlib import Path
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("distribution_probe", ROOT / "tests/probe_goose_distribution.py")
probe_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe_module)


class DistributionProbeVersionTests(unittest.TestCase):
    def run_until_install(self, version):
        calls = []
        production = SimpleNamespace(verify=lambda _: {}, smoke=lambda _: None)
        fake_spec = SimpleNamespace(loader=SimpleNamespace(exec_module=lambda _: None))

        def run(command, **kwargs):
            calls.append((command, kwargs))
            if command[1:] == ["--version"]:
                return subprocess.CompletedProcess(command, 0, " " + version + "\n", "")
            if command[1:3] == ["plugin", "install"]:
                raise RuntimeError("installation boundary reached")
            return subprocess.CompletedProcess(command, 0, "", "")

        with (
            patch.object(probe_module.importlib.util, "spec_from_file_location", return_value=fake_spec),
            patch.object(probe_module.importlib.util, "module_from_spec", return_value=production),
            patch.object(probe_module.shutil, "which", return_value="/verified/goose"),
            patch.object(probe_module.shutil, "copytree"),
            patch.object(probe_module.subprocess, "run", side_effect=run),
        ):
            try:
                probe_module.probe(ROOT, "/verified/goose")
            except (ValueError, RuntimeError) as error:
                return error, calls
        self.fail("Probe unexpectedly completed without installation")

    def test_selected_155_reaches_isolated_install(self):
        error, calls = self.run_until_install("1.55.0")
        self.assertEqual(str(error), "installation boundary reached")
        command, kwargs = calls[-1]
        self.assertEqual(command[:4], ["/verified/goose", "plugin", "install", "--auto-update"])
        self.assertTrue(command[4].startswith("file://"))
        env = kwargs["env"]
        home = Path(env["HOME"])
        self.assertEqual(Path(env["GOOSE_PATH_ROOT"]).parent, home.parent)
        self.assertEqual(env["GIT_CONFIG_NOSYSTEM"], "1")
        self.assertFalse(home.exists(), "Disposable root should be cleaned after failure")

    def test_unverified_versions_refused_before_git_or_install(self):
        for version in ("1.47.0", "1.56.0", "1.55.1", "", "goose 1.55.0"):
            with self.subTest(version=version):
                error, calls = self.run_until_install(version)
                self.assertIsInstance(error, ValueError)
                self.assertIn("requires verified Goose 1.55.0", str(error))
                self.assertEqual(len(calls), 1)

    def test_documented_runtime_and_explicit_executable(self):
        text = (ROOT / "CONTRIBUTING.md").read_text()
        self.assertIn("The probe requires Goose 1.55.0", text)
        self.assertIn("--goose /absolute/path/to/goose", text)


if __name__ == "__main__":
    unittest.main()
