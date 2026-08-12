#!/usr/bin/env bash
# PreToolUse hook: block Bash tool calls that match a small denylist of clearly
# dangerous command shapes, before they run.
#
# Reads the tool-call JSON payload on stdin, e.g.:
#   { "tool_input": { "command": "..." } }
#
# Blocking contract (Claude Code): exit 0 allows the call. Exit 2 blocks it —
# and the reason must be on stderr, not stdout; Claude Code ignores stdout
# when the exit code is 2. Any other non-zero exit (including 1) is a
# NON-BLOCKING error: the tool call proceeds regardless. See the "Hook
# allow/block contract" section of this skill's SKILL.md, and verify against
# your Claude Code version's current hooks reference before relying on this.

set -euo pipefail

payload="$(cat)"

deny() {
  echo "$1" >&2
  exit 2
}

# Guarded with `|| true`: under `set -e`+`pipefail`, a payload with no
# `command` field (or a missing `jq`) would otherwise abort the script before
# the `-z` allow-check runs.
if command -v jq >/dev/null 2>&1; then
  command="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
else
  # Fallback when jq isn't installed — a fragile, best-effort parse, not a
  # real JSON parser. `[^"]*` stops at the first embedded quote, so a command
  # string containing an escaped `\"` will be truncated before this pattern
  # sees it. Install jq for a reliable extraction.
  command="$(printf '%s' "$payload" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed -E 's/.*:[[:space:]]*"([^"]*)"/\1/' || true)"
fi

if [[ -z "${command}" ]]; then
  exit 0
fi

# Deny patterns worth a hard stop rather than a judgment call at the moment of
# execution — keep this list short and unambiguous; anything requiring nuance
# belongs in a prompt-type hook instead of a command hook like this one.
deny_patterns=(
  'rm[[:space:]]+-rf[[:space:]]+/'
  'git[[:space:]]+push[[:space:]]+.*--force'
  'DROP[[:space:]]+TABLE'
  ':\(\)\{[[:space:]]*:\|:&[[:space:]]*\};:'   # fork bomb shape
)

for pattern in "${deny_patterns[@]}"; do
  if [[ "${command}" =~ ${pattern} ]]; then
    deny "Blocked: command matches a denylisted pattern (${pattern}). If this is genuinely intended, run it manually outside this tool."
  fi
done

exit 0
