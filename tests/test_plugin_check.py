#!/usr/bin/env python3
"""Unit tests for scripts/plugin-check.py."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_CHECK_PATH = ROOT / "scripts" / "plugin-check.py"


def load_plugin_check_module():
    module_name = "agency_plugin_check"
    spec = importlib.util.spec_from_file_location(module_name, PLUGIN_CHECK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PLUGIN_CHECK_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


plugin_check = load_plugin_check_module()


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def make_plugin_manifests(plugin_dir: Path, **fields) -> None:
    manifest = {"name": plugin_dir.name, "version": "0.1.0", "description": "Test plugin."}
    manifest.update(fields)
    write_json(plugin_dir / ".claude-plugin" / "plugin.json", manifest)
    write_json(plugin_dir / ".cursor-plugin" / "plugin.json", manifest)


class WellFormedPluginTests(unittest.TestCase):
    def test_passes_with_no_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plugin_dir = Path(tmp) / "sample-plugin"
            make_plugin_manifests(plugin_dir, author={"name": "Test"})
            skill_dir = plugin_dir / "skills" / "do-thing"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: do-thing\ndescription: Does the thing.\n"
                "allowed-tools:\n  - Read\n---\n\n## When to use\n",
                encoding="utf-8",
            )

            checker = plugin_check.PluginChecker("pretty")
            checker.check_plugin(plugin_dir)

            errors = [i for i in checker.v.issues if i.severity == "error"]
            self.assertEqual(errors, [], msg=[e.message for e in errors])


class MissingFieldTests(unittest.TestCase):
    def test_missing_version_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plugin_dir = Path(tmp) / "broken-plugin"
            write_json(
                plugin_dir / ".claude-plugin" / "plugin.json",
                {"name": "broken-plugin", "description": "Missing version."},
            )
            write_json(
                plugin_dir / ".cursor-plugin" / "plugin.json",
                {"name": "broken-plugin", "description": "Missing version."},
            )

            checker = plugin_check.PluginChecker("pretty")
            checker.check_plugin(plugin_dir)

            codes = [i.code for i in checker.v.issues if i.severity == "error"]
            self.assertIn("PLUGIN_FIELD_MISSING", codes)


class McpShapeTests(unittest.TestCase):
    def test_practice_plugin_mcp_shape_needs_no_manifest_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plugin_dir = Path(tmp) / "some-practice"
            make_plugin_manifests(plugin_dir, author={"name": "Test"})
            write_json(
                plugin_dir / ".mcp.json",
                {"mcpServers": {"figma": {"type": "http", "url": "https://mcp.figma.com/mcp"}}},
            )

            checker = plugin_check.PluginChecker("pretty")
            checker.check_plugin(plugin_dir)

            errors = [i for i in checker.v.issues if i.severity == "error"]
            self.assertEqual(errors, [], msg=[e.message for e in errors])

    def test_legacy_mcp_shape_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plugin_dir = Path(tmp) / "some-practice"
            make_plugin_manifests(plugin_dir, author={"name": "Test"})
            write_json(
                plugin_dir / ".mcp.json",
                {"github": {"type": "http", "url": "https://api.githubcopilot.com/mcp/"}},
            )

            checker = plugin_check.PluginChecker("pretty")
            checker.check_plugin(plugin_dir)

            codes = [i.code for i in checker.v.issues if i.severity == "error"]
            self.assertIn("MCP_SHAPE_INVALID", codes)


class CliTests(unittest.TestCase):
    def test_help_exits_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, str(PLUGIN_CHECK_PATH), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("plugin-check.py", result.stdout)

    def test_repo_plugins_pass(self) -> None:
        # plugin-check is deliberately narrower than validate.py — it should
        # pass clean even while repo-wide validate.py has unrelated failures.
        result = subprocess.run(
            [sys.executable, str(PLUGIN_CHECK_PATH)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()