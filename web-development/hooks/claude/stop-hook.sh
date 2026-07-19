#!/usr/bin/env bash
#
# Ralph loop Stop hook (Claude Code).
#
# Blocks session exit while a loop is active and feeds the loop prompt back as
# the next turn's input.
#
# Claude Code Stop hook API:
#   Input:  { "transcript_path": "...", "session_id": "...",
#             "stop_hook_active": true|false, ... }
#   Output: { "decision": "block", "reason": "<prompt>", "systemMessage": "..." }
#           to continue, or exit 0 with no stdout to allow the stop.
#
# All decision logic lives in hooks/lib/ralph-common.sh so the Claude and
# Cursor hooks cannot drift apart. They previously duplicated ~120 lines and
# had already diverged: only the Cursor script used its project-dir variable.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB="$HERE/../lib/ralph-common.sh"

if [[ ! -f "$LIB" ]]; then
  printf 'Ralph loop: shared library missing at %s. Allowing stop.\n' "$LIB" >&2
  exit 0
fi

# shellcheck source=../lib/ralph-common.sh
. "$LIB"

HOOK_INPUT="$(cat 2>/dev/null || true)"

# Session identity, used by ralph_evaluate for session isolation.
RALPH_SESSION_ID="$(printf '%s' "$HOOK_INPUT" | jq -r '.session_id // ""' 2>/dev/null || true)"
export RALPH_SESSION_ID

TRANSCRIPT_PATH="$(printf '%s' "$HOOK_INPUT" | jq -r '.transcript_path // ""' 2>/dev/null || true)"
STOP_HOOK_ACTIVE="$(printf '%s' "$HOOK_INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || true)"

# stop_hook_active tells us this stop was itself caused by a previous block.
# We intentionally continue: that is exactly the Ralph technique. Runaway
# protection comes from max_iterations, the hard ceiling, and the stall guard,
# all enforced in ralph_evaluate. Read here so the contract is explicit.
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
  : # continuing a hook-driven turn; guards are enforced in ralph_evaluate
fi

LAST_TEXT="$(ralph_last_assistant_text "$TRANSCRIPT_PATH")"

ralph_evaluate claude "$LAST_TEXT"

if [[ "$RALPH_DECISION" != "continue" ]]; then
  [[ -n "$RALPH_REASON" ]] && ralph_log "$RALPH_REASON"
  exit 0
fi

SYSTEM_MSG="$(ralph_system_message "$RALPH_NEXT_ITER" "$RALPH_PROMISE")"

if ! jq -n \
  --arg prompt "$RALPH_PROMPT" \
  --arg msg "$SYSTEM_MSG" \
  '{ "decision": "block", "reason": $prompt, "systemMessage": $msg }' 2>/dev/null; then
  # If jq cannot render the payload the loop must stop rather than emit
  # malformed JSON, which the agent would treat as a hook failure anyway.
  ralph_log "failed to render hook JSON. Stopping."
  ralph_clear_active "$RALPH_BASE"
  exit 0
fi

exit 0
