#!/usr/bin/env python3
"""
Shim: plugin-check.py → validate_plugins.py (scoped mode).

Prefer:
  python3 scripts/validate_plugins.py [PLUGIN_DIR ...]

This wrapper preserves the old entry point for local habits and older docs.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_plugins import PluginChecker, main, print_usage  # noqa: E402

__all__ = ["PluginChecker", "main", "print_usage"]


if __name__ == "__main__":
    if "--help" in sys.argv:
        print(
            "Fast, single-plugin structural check (shim → validate_plugins.py).\n\n"
            "Usage: python3 scripts/plugin-check.py [PLUGIN_DIR ...] [options]\n"
            "Prefer: python3 scripts/validate_plugins.py [PLUGIN_DIR ...]\n"
        )
        print_usage()
        raise SystemExit(0)
    raise SystemExit(main())
