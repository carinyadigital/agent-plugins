#!/usr/bin/env python3
"""Unit tests for scripts/validate.py orchestrator and validate_lib frontmatter."""
from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE_PATH = ROOT / "scripts" / "validate.py"
VALIDATE_LIB_PATH = ROOT / "scripts" / "validate_lib.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    # Ensure scripts/ is importable for validate.py's sibling imports
    scripts_dir = str(path.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec.loader.exec_module(module)
    return module


validate = load_module("agency_validate", VALIDATE_PATH)
validate_lib = load_module("agency_validate_lib", VALIDATE_LIB_PATH)


class ParseFrontmatterTests(unittest.TestCase):
    def test_parses_scalar_fields(self) -> None:
        text = "---\nname: example\ndescription: An example skill.\n---\n\n## When to use\n"
        frontmatter, body, errors = validate_lib.parse_frontmatter(text)
        self.assertEqual(errors, [])
        self.assertIsNotNone(frontmatter)
        assert frontmatter is not None
        self.assertEqual(frontmatter["name"], "example")
        self.assertEqual(frontmatter["description"], "An example skill.")
        self.assertIn("## When to use", body)

    def test_reports_missing_delimiters(self) -> None:
        frontmatter, _, errors = validate_lib.parse_frontmatter("# No frontmatter\n")
        self.assertIsNone(frontmatter)
        self.assertTrue(any("missing YAML frontmatter" in err for err in errors))

    def test_parses_allowed_tools_list(self) -> None:
        text = (
            "---\n"
            "name: tools\ndescription: Tool list.\n"
            "allowed-tools:\n"
            "  - Read\n"
            "  - Write\n"
            "---\n"
        )
        frontmatter, _, errors = validate_lib.parse_frontmatter(text)
        self.assertEqual(errors, [])
        assert frontmatter is not None
        self.assertEqual(frontmatter["allowed-tools"], ["Read", "Write"])


class StripScalarTests(unittest.TestCase):
    def test_strips_quoted_strings(self) -> None:
        self.assertEqual(validate_lib.strip_scalar('"hello"'), "hello")
        self.assertEqual(validate_lib.strip_scalar("'world'"), "world")

    def test_preserves_block_indicators(self) -> None:
        self.assertEqual(validate_lib.strip_scalar("|"), "|")
        self.assertEqual(validate_lib.strip_scalar(">"), ">")


class MainTests(unittest.TestCase):
    def test_help_exits_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATE_PATH), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("validate.py", result.stdout)

    def test_repo_validation_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATE_PATH)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=result.stderr or result.stdout,
        )

    def test_json_format_emits_parseable_report(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            exit_code = validate.main(["--format", "json"])
        self.assertEqual(exit_code, 0)
        report = json.loads(buffer.getvalue())
        self.assertEqual(report["version"], 1)
        self.assertIn("summary", report)
        self.assertIn("check_results", report)
        self.assertEqual(report["summary"]["errors"], 0)


if __name__ == "__main__":
    unittest.main()
