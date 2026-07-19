#!/usr/bin/env bash
#
# Ralph loop afterAgentResponse hook (Cursor).
#
# Scans the agent's response for the configured completion promise. On a match
# it writes the `done` sentinel, which the stop hook reads to end the loop.
#
# Input:  { "text": "<assistant response text>" }
# Output: none (fire and forget)
#
# Cursor gets a dedicated response hook, so promise detection here is exact.
# The Claude hook has no equivalent event and falls back to scanning the
# transcript, which is why the `done` sentinel is the primary signal on both
# agents: the loop's `done` step writes it directly.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB="$HERE/../lib/ralph-common.sh"

if [[ ! -f "$LIB" ]]; then
  exit 0
fi

# shellcheck source=../lib/ralph-common.sh
. "$LIB"

HOOK_INPUT="$(cat 2>/dev/null || true)"

BASE="$(ralph_base_dir cursor)"
LOOP_FILE="$BASE/active.md"

# No active loop, nothing to detect.
[[ -f "$LOOP_FILE" ]] || exit 0

FM="$(ralph_frontmatter "$LOOP_FILE")" || FM=""
[[ -n "$FM" ]] || exit 0

PROMISE="$(ralph_field "$FM" completion_promise)"
ralph_promise_is_set "$PROMISE" || exit 0

RESPONSE_TEXT="$(printf '%s' "$HOOK_INPUT" | jq -r '.text // empty' 2>/dev/null || true)"
[[ -n "$RESPONSE_TEXT" ]] || exit 0

if ralph_promise_matches "$RESPONSE_TEXT" "$PROMISE"; then
  : > "$BASE/done" 2>/dev/null || true
fi

exit 0
