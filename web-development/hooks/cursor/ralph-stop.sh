#!/usr/bin/env bash
#
# Ralph loop stop hook (Cursor).
#
# Cursor stop hook API:
#   Input:  { "status": "completed"|"aborted"|"error", "loop_count": N, ... }
#   Output: { "followup_message": "<text>" } to continue, or exit 0 with no
#           stdout to stop.
#
# Promise detection on Cursor is handled by ralph-capture.sh, which runs on
# afterAgentResponse and writes the `done` sentinel. This hook only reads that
# sentinel, so it never needs to parse a transcript.
#
# All decision logic lives in hooks/lib/ralph-common.sh, shared with the
# Claude hook.

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

STATUS="$(printf '%s' "$HOOK_INPUT" | jq -r '.status // "completed"' 2>/dev/null || true)"

# An aborted or errored turn means the user interrupted or the agent failed.
# Re-feeding the prompt would fight the user for control of the session.
if [[ "$STATUS" == "aborted" || "$STATUS" == "error" ]]; then
  ralph_log "turn ended with status '$STATUS'. Not continuing the loop."
  exit 0
fi

# A promise detected this turn by ralph-capture.sh is handled inside
# ralph_evaluate via the `done` sentinel, so no text is passed here.
ralph_evaluate cursor ""

if [[ "$RALPH_DECISION" != "continue" ]]; then
  [[ -n "$RALPH_REASON" ]] && ralph_log "$RALPH_REASON"
  exit 0
fi

HEADER="$(ralph_system_message "$RALPH_NEXT_ITER" "$RALPH_PROMISE")"
FOLLOWUP="[$HEADER]

$RALPH_PROMPT"

if ! jq -n --arg msg "$FOLLOWUP" '{ "followup_message": $msg }' 2>/dev/null; then
  ralph_log "failed to render hook JSON. Stopping."
  ralph_clear_active "$RALPH_BASE"
  exit 0
fi

exit 0
