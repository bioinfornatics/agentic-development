"""Public stdin/stderr behavior tests; not an LLM or installed-hook acceptance suite."""
import json
import re
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
HANDLER = ROOT / "scripts/observe.py"


def invoke(value):
    data = value if isinstance(value, bytes) else json.dumps(value).encode()
    return subprocess.run(["python3", str(HANDLER)], input=data, capture_output=True)


class GooseObserverBehavior(unittest.TestCase):
    def read_record(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"")
        self.assertLessEqual(len(result.stderr), 2048)
        return json.loads(result.stderr.decode().split(" ", 1)[1])

    def test_minimal_session_start(self):
        record = self.read_record(invoke({"event": "SessionStart", "session_id": "session-fixture"}))
        self.assertEqual(record["event"], "SessionStart")
        self.assertEqual(record["mode"], "observation-only")
        self.assertEqual(len(record["session_ref"]), 64)

    def test_sensitive_payload_is_not_echoed(self):
        secret = "PRIVATE-fixture-key-123"
        result = invoke({"event": "PostToolUseFailure", "session_id": secret,
                         "tool_name": "shell", "tool_call_id": "call1",
                         "tool_input": {"command": "echo " + secret},
                         "message": secret, "reason": secret, "working_dir": secret})
        record = self.read_record(result)
        self.assertNotIn(secret.encode(), result.stdout + result.stderr)
        self.assertEqual(record["tool"], "shell")
        self.assertEqual(len(record["call_ref"]), 64)

    def test_stop_reports_structure_not_acceptance(self):
        text = "## 1. Scope\n## 2. Result\n## 3. Changes\n## 4. Verdict\n## 5. Transition\n## 6. Restart"
        record = self.read_record(invoke({"event": "Stop", "last_assistant_message": text}))
        self.assertEqual(record["checkpoint_sections"], [1, 2, 3, 4, 5, 6])
        self.assertEqual(record["handoff_check"], "structure-only")
        self.assertNotIn("accepted", json.dumps(record))

    def test_stop_recognizes_canonical_five_section_report(self):
        # Expected headings come from the user baseline/common-output, not the parser.
        text = ("## current goal {step: implement}\nRepair the observer.\n"
                "## roadmap position\nBounded task.\n"
                "## modified files\nObserver and tests.\n"
                "## closed tasks\nNone.\n"
                "## explanation\nStructure is not acceptance.")
        record = self.read_record(invoke({"event": "Stop", "last_assistant_message": text}))
        self.assertEqual(record.get("report_format"), "canonical")
        self.assertEqual(record.get("report_shape"), "complete")
        self.assertEqual(record["handoff_check"], "structure-only")
        self.assertEqual(record["checkpoint_sections"], [])
        self.assertNotIn("accepted", record)

    def test_stop_shape_boundaries_and_fenced_examples(self):
        headings = ["## current goal {step: test}", "## roadmap position",
                    "## modified files", "## closed tasks", "## explanation"]
        canonical = "\n".join(headings)
        legacy = "\n".join("## " + str(i) + ". Fixture" for i in range(1, 7))
        cases = [
            ("complete", "canonical", canonical),
            ("complete", "canonical", canonical.replace("\n", "\r\n")),
            ("partial", "canonical", "\n".join(headings[:-1])),
            ("duplicate", "canonical", canonical + "\n" + headings[2]),
            ("out-of-order", "canonical", "\n".join([headings[1], headings[0]] + headings[2:])),
            ("mixed", "mixed", canonical + "\n## 1. Legacy"),
            ("complete", "legacy", legacy),
            ("partial", "legacy", "## 2. Fixture"),
            ("duplicate", "legacy", legacy + "\n## 1. Fixture"),
            ("out-of-order", "legacy", "## 2. Fixture\n## 1. Fixture"),
            ("undetermined", "undetermined", "Done; no changes. Next action: stop."),
            ("undetermined", "undetermined", ""),
            ("undetermined", "undetermined", "## arbitrary PRIVATE-heading"),
        ]
        for phase in ("", "done", "IMPLEMENT", "<phase>", "private-sensitive-phase"):
            cases.append(("malformed", "canonical", canonical.replace("step: test", "step: " + phase)))
        cases.append(("malformed", "canonical", canonical.replace(" {step: test}", "")))
        for opening, closing in (("```markdown", "```"), ("~~~markdown", "~~~~"),
                                 ("   ````markdown", "   ````")):
            example = opening + "\n" + canonical + "\n" + legacy + "\n" + closing
            cases.append(("undetermined", "undetermined", example))
            cases.append(("complete", "canonical", example + "\n" + canonical))
        cases.extend([
            ("undetermined", "undetermined", "````\n```\n" + canonical),
            ("undetermined", "undetermined", "~~~\n```\n" + canonical),
            ("undetermined", "undetermined", "```\n" + canonical),
        ])
        for shape, report_format, text in cases:
            with self.subTest(shape=shape, report_format=report_format, text=text[:45]):
                result = invoke({"event": "Stop", "last_assistant_message": text})
                record = self.read_record(result)
                self.assertEqual(record["report_shape"], shape)
                self.assertEqual(record["report_format"], report_format)
                self.assertEqual(record["handoff_check"], "structure-only")
                self.assertNotIn("PRIVATE-heading", result.stderr.decode())
                self.assertNotIn("private-sensitive-phase", result.stderr.decode())
                self.assertNotIn("valid", record)
                self.assertNotIn("accepted", record)

    def test_stop_all_canonical_phases(self):
        for phase in ("cycle", "research", "plan", "implement", "test", "judge", "iterate"):
            text = ("## current goal {step: " + phase + "}\n## roadmap position\n"
                    "## modified files\n## closed tasks\n## explanation")
            record = self.read_record(invoke({"event": "Stop", "last_assistant_message": text}))
            self.assertEqual(record["report_shape"], "complete")

    def test_stop_missing_or_nonstring_message_is_unavailable(self):
        for payload in ({"event": "Stop"}, *({"event": "Stop", "last_assistant_message": value}
                                            for value in (None, [], {}, 42, False))):
            record = self.read_record(invoke(payload))
            self.assertEqual(record["handoff_check"], "unavailable")
            self.assertNotIn("report_shape", record)
            self.assertNotIn("report_format", record)

    def test_stop_sensitive_and_maximum_input_remain_bounded(self):
        secret = "PRIVATE-key-and-/sensitive/path"
        payload = {"event": "Stop", "last_assistant_message":
                   "## current goal {step: " + secret + "}\n## " + secret + "\n" + secret}
        result = invoke(payload)
        self.assertEqual(self.read_record(result)["report_shape"], "malformed")
        self.assertNotIn(secret.encode(), result.stdout + result.stderr)
        # Exactly 1 MiB of valid input is accepted; one byte more is ignored.
        prefix = b'{"event":"Stop","last_assistant_message":"'
        suffix = b'"}'
        raw = prefix + b'x' * (1048576 - len(prefix) - len(suffix)) + suffix
        self.assertEqual(self.read_record(invoke(raw))["report_shape"], "undetermined")
        self.assertEqual(self.read_record(invoke(raw + b' '))["code"], "payload-too-large")

    def test_no_message_and_unknown_optional_fields(self):
        record = self.read_record(invoke({"event": "Stop", "extra": [1, 2]}))
        self.assertEqual(record["handoff_check"], "unavailable")

    def test_bad_or_oversized_payload_is_safe(self):
        for raw in (b"not json", b"[]", b"{}", b"x" * (1048576 + 1), b"\xff"):
            with self.subTest(raw=raw[:12]):
                record = self.read_record(invoke(raw))
                self.assertEqual(record["status"], "ignored")

    def test_unknown_event_is_not_interpreted(self):
        record = self.read_record(invoke({"event": "SubagentStart", "message": "private"}))
        self.assertEqual(record["status"], "ignored")

    def test_host_decision_observation_is_not_a_policy_decision(self):
        record = self.read_record(invoke({"event": "PreToolUseResult", "decision": "deny",
                                         "cause": "policy_denial", "policy_evaluated": True,
                                         "reason": "private", "tool_name": "shell"}))
        self.assertEqual(record["host_decision"], "deny")
        self.assertNotIn("decision", record)
        self.assertNotIn("reason", record)

    def test_wrong_optional_field_types_are_ignored_without_failure(self):
        for value in ([], {}, 42, False):
            record = self.read_record(invoke({"event": "PostToolUseFailure", "tool_name": value}))
            self.assertEqual(record["tool"], "other")
        record = self.read_record(invoke({"event": [], "message": "private"}))
        self.assertEqual(record["status"], "ignored")

    def test_deep_json_and_zero_input_never_echo_payload(self):
        for raw in (b"", b"[" * 1500 + b"0" + b"]" * 1500):
            record = self.read_record(invoke(raw))
            self.assertEqual(record["status"], "ignored")

    def test_one_plugin_with_root_hooks_and_no_adapter(self):
        self.assertFalse((ROOT / "adapters").exists())
        self.assertTrue((ROOT / "hooks/hooks.json").is_file())
        self.assertTrue((ROOT / "scripts/observe.py").is_file())
        manifest = json.loads((ROOT / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "agentic-development")

    def test_exact_developer_tool_aliases_match_and_normalize(self):
        hooks = json.loads((ROOT / "hooks/hooks.json").read_text())["hooks"]
        for event in ("PreToolUseResult", "PostToolUseFailure"):
            for canonical in ("shell", "write", "edit"):
                for name in (canonical, "developer__" + canonical):
                    with self.subTest(event=event, name=name):
                        self.assertTrue(any(re.search(rule["matcher"], name) for rule in hooks[event]))
                        record = self.read_record(invoke({"event": event, "tool_name": name,
                                                         "decision": "allow"}))
                        self.assertEqual(record["tool"], canonical)

    def test_other_namespaces_and_lookalikes_stay_out_of_scope(self):
        hooks = json.loads((ROOT / "hooks/hooks.json").read_text())["hooks"]
        for name in ("remote__shell", "other__write", "developer__shell_exec",
                     "developer__developer__edit", "prefixshell", "shell_suffix", "tree"):
            for event in ("PreToolUseResult", "PostToolUseFailure"):
                with self.subTest(event=event, name=name):
                    self.assertFalse(any(re.search(rule["matcher"], name) for rule in hooks[event]))
        for name in ("remote__shell", "developer__shell_exec", "developer__developer__edit"):
            record = self.read_record(invoke({"event": "PostToolUseFailure", "tool_name": name}))
            self.assertEqual(record["tool"], "other")

    def test_hook_guide_discloses_current_verification_limits(self):
        text = (ROOT / "hooks/README.md").read_text()
        self.assertEqual(text.splitlines()[0], "# Plugin Goose hooks")
        self.assertIn("mandatory five-section final report", text)
        self.assertIn("historical observation is not verification", text)
        self.assertIn("do not turn that failed validator", text)

    def test_hook_configuration_is_observation_only(self):
        root = ROOT
        hooks = json.loads((root / "hooks/hooks.json").read_text())["hooks"]
        self.assertNotIn("PreToolUse", hooks)
        self.assertEqual(set(hooks), {"SessionStart", "SessionEnd", "Stop", "AfterFileEdit",
                                    "AfterShellExecution", "PostToolUseFailure", "PreToolUseResult"})
        for rules in hooks.values():
            for rule in rules:
                for action in rule["hooks"]:
                    self.assertEqual(action["timeout"], 3)
                    self.assertEqual(action["type"], "command")
                    self.assertNotIn("on_failure", action)


if __name__ == "__main__":
    unittest.main()
