"""Coordinator runner: observed completion, NOT authenticated candidate attestation."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest


def identities(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from identities(test)
        else:
            yield test.id()


class CompletionResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.completed = []

    def stopTest(self, test):
        self.completed.append(test.id())
        super().stopTest(test)


def main():
    mode, oracle, project, outcome = sys.argv[1:]
    sys.path.insert(0, project)
    loader = unittest.TestLoader()
    if mode == "oracle":
        # The frozen oracle expects its project path as the first argument.
        sys.argv = [oracle, project]
        spec = importlib.util.spec_from_file_location("criteria_test", oracle)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite = loader.loadTestsFromModule(module)
    else:
        suite = loader.discover(project)
    planned = list(identities(suite))
    result = unittest.TextTestRunner(verbosity=2, resultclass=CompletionResult).run(suite)
    report = {"complete": True, "planned": planned, "completed": result.completed,
              "tests_run": result.testsRun, "failures": len(result.failures),
              "errors": len(result.errors), "skipped": len(result.skipped),
              "expected_failures": len(result.expectedFailures),
              "unexpected_successes": len(result.unexpectedSuccesses)}
    # Parent-owned disposable path, outside candidate cwd. Same-interpreter code
    # can still discover/forge this report: no hostile-code guarantee is made.
    with Path(outcome).open("x") as stream:
        json.dump(report, stream)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
