#!/usr/bin/env bash
# shellcheck shell=bash
#
# Ralph loop shared hook library.
#
# Sourced by the agent-specific stop hooks:
#   hooks/claude/stop-hook.sh
#   hooks/cursor/ralph-stop.sh
#   hooks/cursor/ralph-capture.sh
#
# DESIGN NOTE: this library deliberately does NOT use `set -e`.
#
# The previous implementation ran `set -euo pipefail` and then immediately
# executed unguarded pipelines such as:
#
#     RALPH_BASE=$(cat ".ralph-loop" 2>/dev/null | head -1 | tr -d '[:space:]')
#
# A missing file made `cat` return 1, `pipefail` propagated it, and `set -e`
# killed the hook before it printed anything. Both Claude Code and Cursor read
# a silent non-zero exit as "allow the stop", so the loop died with no
# diagnostic. Every function below therefore handles its own failures and
# returns a status the caller must check.

set -uo pipefail

# Hard ceiling applied even when max_iterations is 0 (unlimited). Prevents a
# genuinely runaway loop from burning an account overnight.
RALPH_HARD_CEILING="${RALPH_HARD_CEILING:-200}"

# Consecutive iterations with an unchanged state file before the loop stops.
RALPH_STALL_LIMIT="${RALPH_STALL_LIMIT:-3}"

# Raw transcript lines (all roles) scanned by ralph_last_assistant_text when
# looking for the current turn's boundary. Must exceed the largest realistic
# single turn's line count, or the boundary-finding degrades to "whole window".
RALPH_TRANSCRIPT_WINDOW="${RALPH_TRANSCRIPT_WINDOW:-500}"

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

# ralph_project_dir <agent>
#
# Resolve the project root. Each agent exports its own variable; fall back to
# the working directory only as a last resort.
ralph_project_dir() {
  local agent="${1:-}"
  case "$agent" in
    claude) printf '%s' "${CLAUDE_PROJECT_DIR:-$PWD}" ;;
    cursor) printf '%s' "${CURSOR_PROJECT_DIR:-$PWD}" ;;
    *)      printf '%s' "$PWD" ;;
  esac
}

# ralph_base_dir <agent>
#
# Resolve the loop base directory deterministically. There is no pointer file:
# each hook already knows which agent it belongs to, so discovery is not
# needed and the pointer file was pure fragility.
#
# Override with RALPH_BASE_DIR (used by the test harness).
ralph_base_dir() {
  local agent="${1:-}" project
  if [[ -n "${RALPH_BASE_DIR:-}" ]]; then
    printf '%s' "$RALPH_BASE_DIR"
    return 0
  fi
  project="$(ralph_project_dir "$agent")"
  case "$agent" in
    claude) printf '%s/.claude/loop' "$project" ;;
    cursor) printf '%s/.cursor/loop' "$project" ;;
    *)      printf '%s/.agent/loop' "$project" ;;
  esac
}

# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

# ralph_frontmatter <file>
#
# Emit ONLY the first YAML frontmatter block.
#
# The previous implementation used:
#     sed -n '/^---$/,/^---$/{ /^---$/d; p; }'
# sed ranges restart after each closing match, so a loop file with `---`
# separators in the prompt body (the shipped template had four) fed large
# slices of the body back as frontmatter. Verified: 108 lines captured where
# 4 were expected. Any body line beginning `iteration:` or `max_iterations:`
# then produced a multi-line value, failed numeric validation, and triggered
# the delete-the-loop-file path.
ralph_frontmatter() {
  local file="${1:-}"
  [[ -f "$file" ]] || return 1
  awk '
    NR == 1 && /^---[[:space:]]*$/ { inblock = 1; next }
    inblock && /^---[[:space:]]*$/ { exit }
    inblock { print }
  ' "$file" 2>/dev/null
}

# ralph_body <file>
#
# Emit everything after the first frontmatter block, preserving any `---`
# lines inside the body. The old `awk '/^---$/{i++; next} i>=2'` silently
# deleted every horizontal rule in the prompt.
ralph_body() {
  local file="${1:-}"
  [[ -f "$file" ]] || return 1
  awk '
    NR == 1 && /^---[[:space:]]*$/ { inblock = 1; next }
    inblock && !closed && /^---[[:space:]]*$/ { closed = 1; next }
    closed { print }
  ' "$file" 2>/dev/null
}

# ralph_field <frontmatter> <key>
#
# Read a scalar field. Uses grep -m1 so a duplicated key can never yield a
# multi-line value, trims whitespace, and strips one layer of surrounding
# single or double quotes. Always returns 0; a missing key yields an empty
# string, which the caller validates.
ralph_field() {
  local fm="${1:-}" key="${2:-}" line value
  line="$(printf '%s\n' "$fm" | grep -m1 "^${key}:" 2>/dev/null || true)"
  [[ -n "$line" ]] || { printf ''; return 0; }
  value="${line#"${key}":}"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  if [[ ${#value} -ge 2 ]]; then
    if [[ "${value:0:1}" == '"' && "${value: -1}" == '"' ]]; then
      value="${value:1:${#value}-2}"
    elif [[ "${value:0:1}" == "'" && "${value: -1}" == "'" ]]; then
      value="${value:1:${#value}-2}"
    fi
  fi
  printf '%s' "$value"
  return 0
}

# ralph_is_uint <value>
ralph_is_uint() {
  [[ "${1:-}" =~ ^[0-9]+$ ]]
}

# ralph_promise_is_set <value>
#
# Treats empty, "null" and "~" as unset so YAML nulls behave consistently.
ralph_promise_is_set() {
  local v="${1:-}"
  [[ -n "$v" && "$v" != "null" && "$v" != "~" ]]
}

# ---------------------------------------------------------------------------
# Promise detection
# ---------------------------------------------------------------------------

# ralph_extract_promise <text>
#
# Return the contents of a <promise>...</promise> tag, whitespace normalised,
# but ONLY when that tag is the entire last line of <text> (leading
# whitespace and trailing whitespace/blank lines are tolerated; anything else
# on that line, before or after the tag, disqualifies it). Empty when absent.
# perl is fenced so a failure cannot abort the hook.
#
# The tag must be the last line, not merely present, because a bare substring
# search matches the model MENTIONING its own stop condition:
#   "I will only output <promise>EPIC_DONE</promise> once every task is done."
#   "Reminder: only output `<promise>EPIC_DONE</promise>` when true."
# Anchoring to "alone, on the final line" rejects both — there is always more
# text on that line after the tag in the mention case — while still matching
# the real completion turn, which ends the message on the tag. A *closed*
# fenced quote is rejected too, for the same reason: its last line is the
# closing ``` fence, not the tag.
#
# An UNCLOSED fence needs its own check, because the tag genuinely is the
# last line in that case (there is no closing fence left to disqualify it):
#   "Reminder about the tag:
#   ```
#   <promise>EPIC_DONE</promise>"
# so count fence-marker lines (```) appearing before the matched tag; an odd
# count means the tag sits inside a fence that never closed, and is rejected.
ralph_extract_promise() {
  local text="${1:-}" out
  [[ -n "$text" ]] || { printf ''; return 0; }
  out="$(printf '%s' "$text" | perl -0777 -ne '
    if (/\A(.*?)(?:^|\n)[ \t]*<promise>(.*?)<\/promise>[ \t]*\n*\z/s) {
      my ($prefix, $p) = ($1, $2);
      my $fences = () = $prefix =~ /^[ \t]*```/mg;
      if ($fences % 2 == 0) {
        $p =~ s/^\s+|\s+$//g;
        $p =~ s/\s+/ /g;
        print $p;
      }
    }
  ' 2>/dev/null)" || out=""
  printf '%s' "$out"
  return 0
}

# ralph_promise_matches <text> <expected>
ralph_promise_matches() {
  local text="${1:-}" expected="${2:-}" found
  ralph_promise_is_set "$expected" || return 1
  found="$(ralph_extract_promise "$text")"
  [[ -n "$found" && "$found" = "$expected" ]]
}

# ralph_last_assistant_text <transcript>
#
# Extract the most recent assistant TEXT block from a Claude Code JSONL
# transcript, scoped to the CURRENT turn.
#
# Claude Code writes each content block (text, tool_use, thinking) as its own
# JSONL line, all tagged role=assistant. An earlier implementation took
# `tail -1` of the assistant lines and read text blocks from that single line,
# so any turn ending on a tool call, which is the normal case for a loop that
# delegates every step to a sub-agent, produced no text and the completion
# promise was never seen. The fix after that widened the scan to the last 100
# assistant lines with no turn boundary at all — which meant a stale promise
# left over from an earlier iteration (or an earlier, already-finished loop)
# could be found again by a *fresh* turn that happens to end on tool calls,
# stopping the loop at iteration 1 on a promise nobody made this run.
#
# Every Ralph continuation is a Stop-hook "block" whose `reason` Claude Code
# re-injects as a genuine new user turn: role=user, plain text — never a
# tool_result (those are also role=user, but their content is an array of
# tool_result blocks, never a bare string and never a "text"-type block).
# That is an unambiguous, always-present turn boundary, so scope the scan to
# assistant text after the LAST such real user turn. If none is found in the
# window (the very first turn of a session), boundary defaults to -1, i.e.
# scan the whole window — unchanged behaviour for that case.
#
# A plain-text user turn's `message.content` may be a bare JSON string (the
# simple shape) or an array containing a "text"-type block (used when other
# block types accompany it) — Claude Code has been observed to use either
# depending on context, so a boundary check that only recognised the array
# shape would silently never fire for the (also real) bare-string shape,
# degrading straight back to the pre-fix "scan the whole window" behaviour
# with no error or signal that the boundary was missed. Recognise both.
#
# RALPH_TRANSCRIPT_WINDOW bounds a raw tail over ALL roles (not assistant-only,
# since the boundary line itself may be outside an assistant-only tail), so it
# must comfortably exceed the largest realistic single turn's line count.
ralph_last_assistant_text() {
  local transcript="${1:-}" raw out
  [[ -n "$transcript" && -f "$transcript" ]] || { printf ''; return 0; }
  raw="$(tail -n "$RALPH_TRANSCRIPT_WINDOW" "$transcript" 2>/dev/null)" || raw=""
  [[ -n "$raw" ]] || { printf ''; return 0; }
  out="$(printf '%s\n' "$raw" | jq -rs '
    . as $all
    | ( [ range(0; ($all | length))
          | select($all[.].role == "user"
                   and (
                     (($all[.].message.content | type) == "string"
                       and ($all[.].message.content | length) > 0)
                     or ((([$all[.].message.content[]?.type]) // []) | index("text") != null)
                   ))
        ] | last // -1
      ) as $boundary
    | [ $all[($boundary + 1):][]
        | select(.role == "assistant")
        | .message.content[]?
        | select(.type == "text")
        | .text
      ] | last // ""
  ' 2>/dev/null)" || out=""
  printf '%s' "$out"
  return 0
}

# ---------------------------------------------------------------------------
# Stall guard
# ---------------------------------------------------------------------------

# ralph_check_stall <state_path> <stall_file>
#
# Returns 0 when the loop should STOP (state unchanged RALPH_STALL_LIMIT times
# in a row), 1 when it should continue. A missing or undeclared state file
# disables the guard.
ralph_check_stall() {
  local state_path="${1:-}" stall_file="${2:-}" current prev_hash prev_count count

  [[ -n "$state_path" && "$state_path" != "null" && -f "$state_path" ]] || return 1

  current="$(cksum "$state_path" 2>/dev/null | awk '{print $1}')" || current=""
  [[ -n "$current" ]] || return 1

  prev_hash=""
  prev_count=0
  if [[ -f "$stall_file" ]]; then
    prev_hash="$(awk '{print $1}' "$stall_file" 2>/dev/null)" || prev_hash=""
    prev_count="$(awk '{print $2}' "$stall_file" 2>/dev/null)" || prev_count=0
    ralph_is_uint "$prev_count" || prev_count=0
  fi

  if [[ "$current" == "$prev_hash" ]]; then
    count=$((prev_count + 1))
  else
    count=1
  fi

  printf '%s %s\n' "$current" "$count" > "$stall_file" 2>/dev/null || true

  [[ $count -ge $RALPH_STALL_LIMIT ]]
}

# ---------------------------------------------------------------------------
# Iteration bookkeeping
# ---------------------------------------------------------------------------

# ralph_bump_iteration <loop_file> <next>
#
# Rewrite `iteration:` in the FIRST frontmatter block only, atomically. The
# old `sed "s/^iteration: .*/..."` rewrote every matching line anywhere in the
# file, including inside the prompt body.
ralph_bump_iteration() {
  local loop_file="${1:-}" next="${2:-}" tmp
  [[ -f "$loop_file" ]] || return 1
  ralph_is_uint "$next" || return 1
  tmp="${loop_file}.tmp.$$"
  # NOTE: the awk variable must not be called `next`, which is an awk keyword.
  awk -v newiter="$next" '
    NR == 1 && /^---[[:space:]]*$/ { inblock = 1; print; next }
    inblock && /^---[[:space:]]*$/ { inblock = 0; print; next }
    inblock && /^iteration:[[:space:]]/ { print "iteration: " newiter; next }
    { print }
  ' "$loop_file" > "$tmp" 2>/dev/null || { rm -f "$tmp"; return 1; }
  [[ -s "$tmp" ]] || { rm -f "$tmp"; return 1; }
  mv "$tmp" "$loop_file" 2>/dev/null || { rm -f "$tmp"; return 1; }
  return 0
}

# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

# ralph_clear_active <base>
#
# End the loop: remove the active file and its transient flags. Run
# directories are never touched, they are the audit record.
ralph_clear_active() {
  local base="${1:-}"
  [[ -n "$base" ]] || return 0
  rm -f "$base/active.md" "$base/done" "$base/stall" 2>/dev/null || true
  return 0
}

# ralph_log <message...>
#
# Diagnostics to stderr. Never stdout: stdout is the hook's JSON channel and
# any stray byte there corrupts the agent's parse.
ralph_log() {
  printf 'Ralph loop: %s\n' "$*" >&2
}

# ---------------------------------------------------------------------------
# Shared stop-hook decision
# ---------------------------------------------------------------------------

# ralph_evaluate <agent> <last_assistant_text>
#
# Single source of truth for "should the loop continue?". Both agents call
# this and differ only in how they render the answer.
#
# Sets, on success:
#   RALPH_DECISION   continue | stop
#   RALPH_REASON     human-readable reason when stopping
#   RALPH_PROMPT     prompt body to feed back when continuing
#   RALPH_NEXT_ITER  iteration number of the next turn
#   RALPH_PROMISE    configured completion promise (may be empty)
#   RALPH_BASE       resolved base directory
ralph_evaluate() {
  local agent="${1:-}" last_text="${2:-}"
  local base loop_file fm iteration max_iter promise state_file session_id
  local project state_path next

  RALPH_DECISION="stop"
  RALPH_REASON=""
  RALPH_PROMPT=""
  RALPH_NEXT_ITER=""
  RALPH_PROMISE=""

  base="$(ralph_base_dir "$agent")"
  # shellcheck disable=SC2034  # out-parameter, read by callers per the contract above
  RALPH_BASE="$base"
  loop_file="$base/active.md"

  # No active loop. Allow the stop silently: this is the overwhelmingly
  # common case and must never emit noise.
  if [[ ! -f "$loop_file" ]]; then
    RALPH_REASON=""
    return 0
  fi

  fm="$(ralph_frontmatter "$loop_file")" || fm=""
  if [[ -z "$fm" ]]; then
    RALPH_REASON="active loop file has no frontmatter ($loop_file). Stopping."
    ralph_clear_active "$base"
    return 0
  fi

  iteration="$(ralph_field "$fm" iteration)"
  max_iter="$(ralph_field "$fm" max_iterations)"
  promise="$(ralph_field "$fm" completion_promise)"
  state_file="$(ralph_field "$fm" state_file)"
  session_id="$(ralph_field "$fm" session_id)"
  # shellcheck disable=SC2034  # out-parameter, read by callers per the contract above
  RALPH_PROMISE="$promise"

  if ! ralph_is_uint "$iteration"; then
    RALPH_REASON="active loop file corrupted (iteration: '$iteration'). Stopping. Re-seed with /ralph-loop:ralph-loop-setup."
    ralph_clear_active "$base"
    return 0
  fi

  if ! ralph_is_uint "$max_iter"; then
    RALPH_REASON="active loop file corrupted (max_iterations: '$max_iter'). Stopping. Re-seed with /ralph-loop:ralph-loop-setup."
    ralph_clear_active "$base"
    return 0
  fi

  # Session isolation. The loop file is project-scoped but the stop hook fires
  # in every session open in that project. Without this check a second window
  # gets conscripted into someone else's loop. An empty session_id means the
  # loop was seeded without one, so fall through for backwards compatibility.
  if [[ -n "$session_id" && -n "${RALPH_SESSION_ID:-}" && "$session_id" != "${RALPH_SESSION_ID}" ]]; then
    RALPH_REASON=""
    return 0
  fi

  # Completion sentinel. On Claude this file is never written — Claude Code
  # has no hook that can write it, so this branch only ever fires for Cursor,
  # whose Stop hook (ralph-stop.sh) always calls ralph_evaluate with an empty
  # last_text and relies entirely on ralph-capture.sh (afterAgentResponse)
  # having written this file already. Checked first only so the (always
  # empty on Claude) $last_text scan below never runs needlessly for Cursor.
  if [[ -f "$base/done" ]]; then
    RALPH_REASON="completion promise fulfilled at iteration $iteration."
    ralph_clear_active "$base"
    return 0
  fi

  if ralph_promise_matches "$last_text" "$promise"; then
    RALPH_REASON="completion promise '$promise' fulfilled at iteration $iteration."
    ralph_clear_active "$base"
    return 0
  fi

  if [[ $max_iter -gt 0 ]] && [[ $iteration -ge $max_iter ]]; then
    RALPH_REASON="max iterations ($max_iter) reached. Run /ralph-loop:ralph-loop status to inspect progress."
    ralph_clear_active "$base"
    return 0
  fi

  # Hard ceiling. Applies even to unlimited loops (max_iterations: 0).
  if [[ $iteration -ge $RALPH_HARD_CEILING ]]; then
    RALPH_REASON="hard ceiling ($RALPH_HARD_CEILING iterations) reached. Stopping regardless of max_iterations."
    ralph_clear_active "$base"
    return 0
  fi

  # Stall guard. State paths in frontmatter are relative to the project root.
  if [[ -n "$state_file" && "$state_file" != "null" ]]; then
    project="$(ralph_project_dir "$agent")"
    if [[ "$state_file" == /* ]]; then
      state_path="$state_file"
    else
      state_path="$project/$state_file"
    fi
    if ralph_check_stall "$state_path" "$base/stall"; then
      RALPH_REASON="no progress in $RALPH_STALL_LIMIT consecutive iterations (state unchanged: $state_file). Stopping so a human can inspect. Run /ralph-loop:ralph-loop status."
      ralph_clear_active "$base"
      return 0
    fi
  fi

  RALPH_PROMPT="$(ralph_body "$loop_file")" || RALPH_PROMPT=""
  if [[ -z "${RALPH_PROMPT//[[:space:]]/}" ]]; then
    RALPH_REASON="active loop file has an empty prompt body. Stopping."
    ralph_clear_active "$base"
    return 0
  fi

  next=$((iteration + 1))
  if ! ralph_bump_iteration "$loop_file" "$next"; then
    # shellcheck disable=SC2034  # out-parameter, read by callers per the contract above
    RALPH_REASON="could not update iteration counter in $loop_file. Stopping rather than looping on a stale count."
    ralph_clear_active "$base"
    return 0
  fi

  # shellcheck disable=SC2034  # out-parameter, read by callers per the contract above
  RALPH_NEXT_ITER="$next"
  # shellcheck disable=SC2034  # out-parameter, read by callers per the contract above
  RALPH_DECISION="continue"
  return 0
}

# ralph_system_message <next_iteration> <promise>
ralph_system_message() {
  local next="${1:-}" promise="${2:-}"
  if ralph_promise_is_set "$promise"; then
    printf 'Ralph iteration %s | To stop: output <promise>%s</promise> ONLY when the statement is genuinely true. Do not output a false promise to escape the loop.' "$next" "$promise"
  else
    printf 'Ralph iteration %s | No completion promise set: the loop runs until max_iterations.' "$next"
  fi
}
