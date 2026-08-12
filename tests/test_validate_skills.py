#!/usr/bin/env python3
"""Unit tests for scripts/validate_skills.py expansions."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE_SKILLS_PATH = ROOT / "scripts" / "validate_skills.py"


def load_validate_skills_module():
    scripts_dir = str(VALIDATE_SKILLS_PATH.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    module_name = "agency_validate_skills"
    spec = importlib.util.spec_from_file_location(module_name, VALIDATE_SKILLS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {VALIDATE_SKILLS_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


validate_skills = load_validate_skills_module()


class AgentContractTests(unittest.TestCase):
    def test_bare_bash_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            agent = Path(tmp) / "agents" / "demo.md"
            agent.parent.mkdir(parents=True)
            agent.write_text(
                "---\n"
                "name: demo\n"
                "description: Demo agent.\n"
                "model: inherit\n"
                "tools: Read, Bash\n"
                "metadata:\n"
                "  model_tier: fast\n"
                "  budget: 1\n"
                "---\n\nBody.\n",
                encoding="utf-8",
            )
            # Monkeypatch agent_paths by checking via SkillValidator against
            # a single file using the lib helpers directly.
            from validate_lib import has_bare_bash, normalize_tools, parse_frontmatter

            fm, _, errs = parse_frontmatter(agent.read_text(encoding="utf-8"))
            self.assertEqual(errs, [])
            assert fm is not None
            self.assertTrue(has_bare_bash(normalize_tools(fm.get("tools"))))

    def test_scoped_bash_ok(self) -> None:
        from validate_lib import has_bare_bash, normalize_tools

        self.assertFalse(
            has_bare_bash(normalize_tools("Read, Bash(git diff:*), Grep"))
        )


class OrphanSkillTests(unittest.TestCase):
    def test_orphan_detection_logic(self) -> None:
        # .../skills/<name>/SKILL.md is valid; other layouts are orphans.
        valid = Path("brand-creative/skills/setup/SKILL.md").parts
        orphan = Path("brand-creative/SKILL.md").parts
        self.assertEqual(valid[-3], "skills")
        self.assertNotEqual(orphan[-2] if len(orphan) >= 2 else None, "skills")
        self.assertTrue(
            len(valid) >= 3 and valid[-3] == "skills" and valid[-1] == "SKILL.md"
        )
        self.assertFalse(
            len(orphan) >= 3 and orphan[-3] == "skills" and orphan[-1] == "SKILL.md"
        )


class CliTests(unittest.TestCase):
    def test_help_exits_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATE_SKILLS_PATH), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("validate_skills.py", result.stdout)

    def test_repo_skills_pass(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATE_SKILLS_PATH), "--skip-drift"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
