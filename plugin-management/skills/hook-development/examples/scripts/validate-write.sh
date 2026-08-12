#!/usr/bin/env bash
# PreToolUse hook: block Write/Edit tool calls that target common secret-file
# paths, and warn (without ever printing the value) if the new content looks
# like it contains a hardcoded credential.
#
# Reads the tool-call JSON payload on stdin, e.g.:
#   { "tool_input": { "file_path": "...", "content": "..." } }
#
# Blocking contract (Claude Code): exit 0 allows the call. Exit 2 blocks it —
# and the reason must be on stderr, not stdout; Claude Code ignores stdout
# when the exit code is 2. Any other non-zero exit (including 1) is a
# NON-BLOCKING error: the tool call proceeds regardless, so `exit 1` here
# would silently fail to enforce anything. See the "Hook allow/block
# contract" section of this skill's SKILL.md before changing this script —
# and verify against your Claude Code version's current hooks reference,
# since the exact JSON shape has changed across releases.

set -euo pipefail

payload="$(cat)"

deny() {
  echo "$1" >&2
  exit 2
}

# Every extraction below is guarded with `|| true`: under `set -e`+`pipefail`,
# a payload that doesn't match (or a missing `jq`) would otherwise abort the
# script before the `-z` allow-check runs, which defeats the "no match →
# allow" default this hook depends on.
if command -v jq >/dev/null 2>&1; then
  file_path="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
else
  # Fallback when jq isn't installed. This is a fragile, best-effort parse,
  # not a real JSON parser — [^"]* stops at the first embedded quote, so a
  # value containing an escaped `\"` will be truncated. Install jq for a
  # reliable extraction; see this skill's SKILL.md for why the grep
  # approach below can't be trusted as a control on its own.
  file_path="$(printf '%s' "$payload" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed -E 's/.*:[[:space:]]*"([^"]*)"/\1/' || true)"
fi

if [[ -z "${file_path}" ]]; then
  # Nothing to check — allow.
  exit 0
fi

# Reject path traversal before doing anything else with the path.
case "${file_path}" in
  *".."*)
    deny "Blocked: file path contains '..' (${file_path})"
    ;;
esac

# Block direct writes to known secret-file paths.
case "${file_path}" in
  *".env"|*".env."*|*"credentials.json"|*"id_rsa"|*".pem")
    deny "Blocked: writes to secret-bearing paths are not allowed via this tool (${file_path}). Edit this file manually if the change is intentional."
    ;;
esac

if command -v jq >/dev/null 2>&1; then
  content="$(printf '%s' "$payload" | jq -r '.tool_input.content // empty' 2>/dev/null || true)"
else
  # Same fragility caveat as file_path above — this will miss content that
  # contains an escaped quote before the credential pattern, which is most
  # real file content. Best-effort scan, not a control, without jq.
  content="$(printf '%s' "$payload" | grep -o '"content"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 || true)"
fi

# Heuristic, best-effort check for an obviously hardcoded AWS-style key —
# never print the matched value itself, only that the pattern was seen.
if printf '%s' "${content}" | grep -Eq 'AKIA[0-9A-Z]{16}'; then
  deny "Blocked: content being written to \"${file_path}\" looks like it contains an AWS access key (AKIA****). Move it to an environment variable instead."
fi

exit 0
