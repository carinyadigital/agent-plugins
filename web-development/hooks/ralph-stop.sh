#!/bin/bash

# Ralph loop stop hook (Cursor).
# When the agent finishes a turn, decide whether to feed the loop prompt back
# for another iteration or let the session end.
#
# Cursor stop hook API:
#   Input:  { "status": "completed"|"aborted"|"error", "loop_count": N, ...common }
#   Output: { "followup_message": "<text>" } to continue, or exit 0 with no output to stop
#
# State files (seeded by the ralph skill):
#   .ralph/loop.md   active loop file: YAML frontmatter + prompt body
#   .ralph/done      flag written by ralph-capture.sh when the completion promise is seen
#   .ralph/stall     stall-guard tracking (hash + consecutive-unchanged count)

set -euo pipefail

HOOK_INPUT=$(cat)

PROJECT_DIR="${CURSOR_PROJECT_DIR:-.}"
RALPH_DIR="$PROJECT_DIR/.ralph"
LOOP_FILE="$RALPH_DIR/loop.md"
DONE_FLAG="$RALPH_DIR/done"
STALL_FILE="$RALPH_DIR/stall"

STALL_LIMIT=3

cleanup() {
  rm -f "$LOOP_FILE" "$DONE_FLAG" "$STALL_FILE"
}

# No active loop. Let the session end.
if [[ ! -f "$LOOP_FILE" ]]; then
  exit 0
fi

# Parse loop file frontmatter
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$LOOP_FILE")
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
MAX_ITERATIONS=$(echo "$FRONTMATTER" | grep '^max_iterations:' | sed 's/max_iterations: *//')
COMPLETION_PROMISE=$(echo "$FRONTMATTER" | grep '^completion_promise:' | sed 's/completion_promise: *//' | sed 's/^"\(.*\)"$/\1/')
STATE_FILE=$(echo "$FRONTMATTER" | grep '^state_file:' | sed 's/state_file: *//' | sed 's/^"\(.*\)"$/\1/' || true)

if [[ ! "$ITERATION" =~ ^[0-9]+$ ]]; then
  echo "Ralph loop: loop file corrupted (iteration: '$ITERATION'). Stopping." >&2
  cleanup
  exit 0
fi

if [[ ! "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "Ralph loop: loop file corrupted (max_iterations: '$MAX_ITERATIONS'). Stopping." >&2
  cleanup
  exit 0
fi

# Completion promise detected by the afterAgentResponse hook
if [[ -f "$DONE_FLAG" ]]; then
  echo "Ralph loop: completion promise fulfilled at iteration $ITERATION." >&2
  cleanup
  exit 0
fi

# Max iterations reached
if [[ $MAX_ITERATIONS -gt 0 ]] && [[ $ITERATION -ge $MAX_ITERATIONS ]]; then
  echo "Ralph loop: max iterations ($MAX_ITERATIONS) reached. Stopping. Run '/ralph status' to inspect progress." >&2
  cleanup
  exit 0
fi

# Stall guard: if a state file is declared and it has not changed for
# STALL_LIMIT consecutive iterations, the loop is spinning without progress.
if [[ -n "${STATE_FILE:-}" ]] && [[ "$STATE_FILE" != "null" ]]; then
  STATE_PATH="$PROJECT_DIR/$STATE_FILE"
  if [[ -f "$STATE_PATH" ]]; then
    CURRENT_HASH=$(cksum "$STATE_PATH" | awk '{print $1}')
    PREV_HASH=""
    PREV_COUNT=0
    if [[ -f "$STALL_FILE" ]]; then
      PREV_HASH=$(awk '{print $1}' "$STALL_FILE")
      PREV_COUNT=$(awk '{print $2}' "$STALL_FILE")
      [[ "$PREV_COUNT" =~ ^[0-9]+$ ]] || PREV_COUNT=0
    fi
    if [[ "$CURRENT_HASH" == "$PREV_HASH" ]]; then
      COUNT=$((PREV_COUNT + 1))
    else
      COUNT=1
    fi
    if [[ $COUNT -ge $STALL_LIMIT ]]; then
      echo "Ralph loop: no progress in $STALL_LIMIT consecutive iterations (state file unchanged: $STATE_FILE). Stopping so a human can inspect. Run '/ralph status' for details." >&2
      cleanup
      exit 0
    fi
    echo "$CURRENT_HASH $COUNT" > "$STALL_FILE"
  fi
fi

# Extract prompt text (everything after the closing --- of the frontmatter)
PROMPT_TEXT=$(awk '/^---$/{i++; next} i>=2' "$LOOP_FILE")

if [[ -z "$PROMPT_TEXT" ]]; then
  echo "Ralph loop: no prompt text found in loop file. Stopping." >&2
  cleanup
  exit 0
fi

# Increment iteration atomically
NEXT_ITERATION=$((ITERATION + 1))
TEMP_FILE="${LOOP_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$LOOP_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$LOOP_FILE"

# Build the followup message: iteration context + original prompt
if [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  HEADER="[Ralph loop iteration $NEXT_ITERATION. To complete: output <promise>$COMPLETION_PROMISE</promise> ONLY when genuinely true.]"
else
  HEADER="[Ralph loop iteration $NEXT_ITERATION.]"
fi

FOLLOWUP="$HEADER

$PROMPT_TEXT"

jq -n --arg msg "$FOLLOWUP" '{"followup_message": $msg}'

exit 0
