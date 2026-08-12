#!/usr/bin/env bash
# Worked example: a hook reading a plugin's own .local.md settings file.
#
# Hooks run as plain scripts, not through the agent's YAML-aware Read tool, so this
# extracts the frontmatter block by hand and greps individual `key: value` lines —
# the technique the plugin-settings skill's own body describes.
#
# Usage: read_setting <file> <key> <default>

set -euo pipefail

read_setting() {
  local file="$1" key="$2" default="$3"
  local value

  if [[ ! -f "${file}" ]]; then
    printf '%s' "${default}"
    return 0
  fi

  # Extract only the block between the first pair of '---' lines.
  value="$(awk '/^---$/{c++; next} c==1' "${file}" \
    | grep -E "^${key}:[[:space:]]*" \
    | head -n1 \
    | sed -E "s/^${key}:[[:space:]]*//" \
    | sed -E 's/^"(.*)"$/\1/; s/^'"'"'(.*)'"'"'$/\1/' || true)"

  if [[ -z "${value}" ]]; then
    printf '%s' "${default}"
  else
    printf '%s' "${value}"
  fi
}

settings_file=".claude/code-review-helper.local.md"

enabled="$(read_setting "${settings_file}" "enabled" "true")"
strictness="$(read_setting "${settings_file}" "strictness" "standard")"

if [[ "${enabled}" != "true" ]]; then
  # A kill switch a user can flip without editing hooks.json — see the main skill
  # body's note that hook-consumed settings changes may need a session restart.
  exit 0
fi

echo "code-review-helper: running with strictness=${strictness}"
# ... rest of the hook's actual logic goes here ...
