#!/usr/bin/env bash
# SessionStart hook: if this plugin's per-project settings file exists (see the
# plugin-settings skill), surface a short summary so the agent has it in context
# from the very first turn instead of discovering it mid-task.
#
# SessionStart hooks are typically expected to print plain text (not JSON) that
# gets added to the session's initial context — check your host's current
# documentation for the exact expected output shape before relying on this.
#
# This hook itself is Claude-only (hooks/hooks.json isn't read by Cursor — see
# hook-development's portability note), so the hardcoded .claude/ path below is
# fine as written. If you ever port this settings-reading logic to run on
# another host directly, don't assume .claude/ is that host's convention too.

set -euo pipefail

settings_file=".claude/code-review-helper.local.md"

if [[ ! -f "${settings_file}" ]]; then
  # Nothing to add — a missing settings file is the normal case, not an error.
  exit 0
fi

strictness="$(awk '/^---$/{c++; next} c==1' "${settings_file}" \
  | grep -E '^strictness:[[:space:]]*' \
  | head -n1 \
  | sed -E 's/^strictness:[[:space:]]*//' || true)"

if [[ -n "${strictness}" ]]; then
  echo "code-review-helper: this project's settings file sets strictness=${strictness}."
fi
