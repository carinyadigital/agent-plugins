#!/usr/bin/env bash
#
# Behavioural test harness for the Ralph loop hooks.
#
# Every test maps to a defect found in the July 2026 review, or to a guardrail
# the loop depends on. Run with:
#
#   ./scripts/test-ralph-hooks.sh
#   ./scripts/test-ralph-hooks.sh -v     # show per-assertion detail
#
# The harness drives the real hook scripts through their real stdin contract
# in a throwaway project directory. It does not mock the library.

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERBOSE=0
[[ "${1:-}" == "-v" ]] && VERBOSE=1

PASS=0
FAIL=0
FAILED_NAMES=()

CLAUDE_HOOK="$ROOT/hooks/claude/stop-hook.sh"
CURSOR_HOOK="$ROOT/hooks/cursor/ralph-stop.sh"
CURSOR_CAPTURE="$ROOT/hooks/cursor/ralph-capture.sh"

TMPROOT="$(mktemp -d)"
trap 'rm -rf "$TMPROOT"' EXIT

# ---------------------------------------------------------------------------
# Assertions
# ---------------------------------------------------------------------------

ok() {
  PASS=$((PASS + 1))
  [[ $VERBOSE -eq 1 ]] && printf '  ok   %s\n' "$1"
  return 0
}

no() {
  FAIL=$((FAIL + 1))
  FAILED_NAMES+=("$1")
  printf '  FAIL %s\n' "$1"
  [[ -n "${2:-}" ]] && printf '       %s\n' "$2"
  return 0
}

assert_eq() {
  local name="$1" expected="$2" actual="$3"
  if [[ "$expected" == "$actual" ]]; then
    ok "$name"
  else
    no "$name" "expected [$expected] got [$actual]"
  fi
}

assert_contains() {
  local name="$1" needle="$2" haystack="$3"
  if [[ "$haystack" == *"$needle"* ]]; then
    ok "$name"
  else
    no "$name" "expected to contain [$needle] in [${haystack:0:200}]"
  fi
}

assert_not_contains() {
  local name="$1" needle="$2" haystack="$3"
  if [[ "$haystack" != *"$needle"* ]]; then
    ok "$name"
  else
    no "$name" "expected NOT to contain [$needle]"
  fi
}

assert_file() {
  local name="$1" path="$2"
  if [[ -f "$path" ]]; then ok "$name"; else no "$name" "missing file $path"; fi
}

assert_no_file() {
  local name="$1" path="$2"
  if [[ ! -f "$path" ]]; then ok "$name"; else no "$name" "unexpected file $path"; fi
}

section() {
  printf '\n%s\n' "$1"
}

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# new_project <name> -> echoes project dir with .claude/loop and .cursor/loop
new_project() {
  local dir="$TMPROOT/$1"
  mkdir -p "$dir/.claude/loop" "$dir/.cursor/loop"
  printf '%s' "$dir"
}

# write_loop <base> <iteration> <max> <promise> [state_file]
write_loop() {
  local base="$1" iter="$2" max="$3" promise="$4" state="${5:-}"
  {
    printf -- '---\n'
    printf 'iteration: %s\n' "$iter"
    printf 'max_iterations: %s\n' "$max"
    printf 'completion_promise: "%s"\n' "$promise"
    [[ -n "$state" ]] && printf 'state_file: %s\n' "$state"
    printf -- '---\n'
    printf '\n'
    printf 'Do the next step of the work.\n'
  } > "$base/active.md"
}

# Claude hook stdin payload
claude_input() {
  local transcript="${1:-}" session="${2:-sess-1}" active="${3:-false}"
  jq -n --arg t "$transcript" --arg s "$session" --argjson a "$active" \
    '{transcript_path: $t, session_id: $s, stop_hook_active: $a}'
}

# These runners are invoked inside command substitutions, so any variable they
# set would be lost with the subshell. Side channels go to files instead, read
# back through last_stderr / last_rc.
ERRFILE="$TMPROOT/.last_stderr"
RCFILE="$TMPROOT/.last_rc"

last_stderr() { cat "$ERRFILE" 2>/dev/null || true; }
last_rc() { cat "$RCFILE" 2>/dev/null || printf '0'; }

run_claude() {
  local project="$1" input="$2" out rc
  out="$(printf '%s' "$input" | CLAUDE_PROJECT_DIR="$project" "$CLAUDE_HOOK" 2>"$ERRFILE")"
  rc=$?
  printf '%s' "$rc" > "$RCFILE"
  printf '%s' "$out"
}

run_cursor() {
  local project="$1" input="$2" out rc
  out="$(printf '%s' "$input" | CURSOR_PROJECT_DIR="$project" "$CURSOR_HOOK" 2>"$ERRFILE")"
  rc=$?
  printf '%s' "$rc" > "$RCFILE"
  printf '%s' "$out"
}

run_capture() {
  local project="$1" input="$2"
  printf '%s' "$input" | CURSOR_PROJECT_DIR="$project" "$CURSOR_CAPTURE" >/dev/null 2>&1
  return 0
}

# Build a Claude JSONL transcript. Each content block is its own line, which
# is how Claude Code actually writes them.
make_transcript() {
  local path="$1"; shift
  : > "$path"
  while [[ $# -gt 0 ]]; do
    local kind="$1" payload="$2"; shift 2
    case "$kind" in
      text)
        jq -nc --arg t "$payload" \
          '{role:"assistant", message:{content:[{type:"text", text:$t}]}}' >> "$path"
        ;;
      tool)
        jq -nc --arg n "$payload" \
          '{role:"assistant", message:{content:[{type:"tool_use", name:$n, input:{}}]}}' >> "$path"
        ;;
      user)
        jq -nc --arg t "$payload" \
          '{role:"user", message:{content:[{type:"text", text:$t}]}}' >> "$path"
        ;;
      userstr)
        # A plain-text user turn whose message.content is a bare JSON string,
        # not an array of content blocks. Claude Code has been observed to
        # use either shape for a real text-only turn; the boundary detection
        # must recognise both, not just the array-of-blocks one.
        jq -nc --arg t "$payload" \
          '{role:"user", message:{content:$t}}' >> "$path"
        ;;
    esac
  done
}

printf 'Ralph hook harness\n==================\n'

# ---------------------------------------------------------------------------
section 'Syntax'
# ---------------------------------------------------------------------------

for f in "$ROOT"/hooks/lib/*.sh "$ROOT"/hooks/claude/*.sh "$ROOT"/hooks/cursor/*.sh "$ROOT"/scripts/*.sh; do
  [[ -f "$f" ]] || continue
  if bash -n "$f" 2>/dev/null; then
    ok "bash -n $(basename "$f")"
  else
    no "bash -n $(basename "$f")" "$(bash -n "$f" 2>&1 | head -3)"
  fi
done

for f in "$ROOT"/hooks/*/hooks.json "$ROOT"/.claude-plugin/plugin.json "$ROOT"/.cursor-plugin/plugin.json "$ROOT"/skills.sh.json; do
  [[ -f "$f" ]] || continue
  if python3 -c "import json,sys; json.load(open('$f'))" 2>/dev/null; then
    ok "valid JSON $(basename "$(dirname "$f")")/$(basename "$f")"
  else
    no "valid JSON $f"
  fi
done

if [[ -x "$CLAUDE_HOOK" && -x "$CURSOR_HOOK" && -x "$CURSOR_CAPTURE" ]]; then
  ok "hook scripts are executable"
else
  no "hook scripts are executable" "chmod +x required"
fi

# ---------------------------------------------------------------------------
section 'Defect 1: unguarded pipeline under set -e must not kill the hook'
# ---------------------------------------------------------------------------

# No loop file at all: the single most common case. Must exit 0, print nothing
# on stdout, and produce no diagnostic noise.
P="$(new_project no-loop)"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_eq "claude: no active loop exits 0" "0" "$(last_rc)"
assert_eq "claude: no active loop is silent on stdout" "" "$OUT"
assert_eq "claude: no active loop is silent on stderr" "" "$(last_stderr)"

OUT="$(run_cursor "$P" '{"status":"completed"}')"
assert_eq "cursor: no active loop exits 0" "0" "$(last_rc)"
assert_eq "cursor: no active loop is silent on stdout" "" "$OUT"

# Missing project dir variable entirely (falls back to PWD), still must not die.
OUT="$(printf '%s' '{"status":"completed"}' | (cd "$P" && env -u CURSOR_PROJECT_DIR "$CURSOR_HOOK" 2>/dev/null))"
assert_eq "cursor: unset CURSOR_PROJECT_DIR still exits 0" "0" "$?"

# Unreadable loop file must not abort the hook.
P="$(new_project unreadable)"
write_loop "$P/.claude/loop" 1 10 "DONE"
chmod 000 "$P/.claude/loop/active.md" 2>/dev/null || true
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_eq "claude: unreadable loop file exits 0" "0" "$(last_rc)"
chmod 644 "$P/.claude/loop/active.md" 2>/dev/null || true

# ---------------------------------------------------------------------------
section 'Defect 3: transcript parse must find text behind trailing tool calls'
# ---------------------------------------------------------------------------

P="$(new_project promise-behind-tool)"
write_loop "$P/.claude/loop" 3 50 "ALL_DONE"
T="$P/transcript.jsonl"

# Turn ends on a tool call, promise is in an earlier text block. The old
# tail -1 implementation missed this entirely.
make_transcript "$T" \
  text "Working on it." \
  text "<promise>ALL_DONE</promise>" \
  tool "Bash"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_eq "promise found despite trailing tool_use" "" "$OUT"
assert_contains "stop reason names the promise" "ALL_DONE" "$(last_stderr)"
assert_no_file "loop file cleared on completion" "$P/.claude/loop/active.md"

# Turn that is only tool calls: no promise, must continue.
P="$(new_project only-tools)"
write_loop "$P/.claude/loop" 3 50 "ALL_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" tool "Read" tool "Edit"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "all-tool turn continues the loop" '"decision": "block"' "$OUT"

# Non-matching promise text must not stop the loop.
P="$(new_project wrong-promise)"
write_loop "$P/.claude/loop" 3 50 "ALL_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" text "<promise>SOMETHING_ELSE</promise>"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "wrong promise does not stop the loop" '"decision": "block"' "$OUT"

# Malformed JSONL must not abort the hook.
P="$(new_project bad-jsonl)"
write_loop "$P/.claude/loop" 3 50 "ALL_DONE"
T="$P/transcript.jsonl"
printf '{"role":"assistant" NOT JSON\n' > "$T"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_eq "malformed transcript exits 0" "0" "$(last_rc)"
assert_contains "malformed transcript still continues loop" '"decision": "block"' "$OUT"

# ---------------------------------------------------------------------------
section 'Defect 5 (P0-2): mentioning the promise must not fulfil it'
# ---------------------------------------------------------------------------

# The model talking ABOUT its own stop condition must not be read as meeting
# it. A bare substring search matches all three of these; only a turn that
# ENDS on the bare tag, alone on its own line, may stop the loop.

P="$(new_project promise-mentioned-not-set)"
write_loop "$P/.claude/loop" 3 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text 'I am NOT finished. I will only output <promise>EPIC_DONE</promise> once every task is committed.'
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "declaring intent to emit the promise later does not stop the loop" '"decision": "block"' "$OUT"
assert_file "loop file survives a mentioned-not-set promise" "$P/.claude/loop/active.md"

P="$(new_project promise-quoted-as-reminder)"
write_loop "$P/.claude/loop" 3 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text 'Reminder: only output `<promise>EPIC_DONE</promise>` when true.'
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "a backtick-quoted reminder does not stop the loop" '"decision": "block"' "$OUT"

P="$(new_project promise-in-closed-fence)"
write_loop "$P/.claude/loop" 3 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text $'Here is the tag for reference:\n```\n<promise>EPIC_DONE</promise>\n```'
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "a closed fenced quote does not stop the loop (last line is the fence, not the tag)" '"decision": "block"' "$OUT"

P="$(new_project promise-in-unclosed-fence)"
write_loop "$P/.claude/loop" 3 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text $'Reminder about the tag:\n```\n<promise>EPIC_DONE</promise>'
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "an unclosed fenced quote does not stop the loop (tag is the last line, but still fenced)" '"decision": "block"' "$OUT"
assert_file "loop file survives an unclosed-fence quote" "$P/.claude/loop/active.md"

# The genuine case: the tag alone is the entire, final line of the turn.
P="$(new_project promise-alone-on-final-line)"
write_loop "$P/.claude/loop" 3 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text $'All tasks are committed and the tests pass.\n\n<promise>EPIC_DONE</promise>'
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_eq "promise alone on the final line stops the loop" "" "$OUT"
assert_contains "stop reason names the promise" "EPIC_DONE" "$(last_stderr)"

# ---------------------------------------------------------------------------
section 'Defect 6 (P0-3): a stale promise from before this turn must not stop it'
# ---------------------------------------------------------------------------

# The exact reproduction: a promise sits earlier in the transcript (an
# earlier iteration, or an already-finished prior loop), a genuine new user
# turn follows (the Stop-hook re-feed), and every assistant line since is
# tool-use-only. The old tail-100-assistant-lines scan reached back past the
# turn boundary and found the stale promise; the current turn made none.
P="$(new_project stale-promise-before-boundary)"
write_loop "$P/.claude/loop" 1 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text "<promise>EPIC_DONE</promise>" \
  user "Do the next step of the work." \
  tool "Read" \
  tool "Edit" \
  tool "Bash"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "stale promise before the turn boundary does not stop a fresh iteration" '"decision": "block"' "$OUT"
assert_file "loop file survives the stale promise" "$P/.claude/loop/active.md"

# Same shape, but the tag is genuinely emitted AFTER the boundary: must stop.
P="$(new_project promise-after-boundary)"
write_loop "$P/.claude/loop" 1 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text "<promise>NOT_YET</promise>" \
  user "Do the next step of the work." \
  tool "Read" \
  text "<promise>EPIC_DONE</promise>"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_eq "promise after the boundary stops the loop" "" "$OUT"
assert_contains "stop reason names the current-turn promise" "EPIC_DONE" "$(last_stderr)"

# Same shape, but the re-fed user turn is a bare JSON string rather than an
# array of content blocks — the other real shape Claude Code can write for a
# plain-text turn. The boundary detection must recognise this too, or it
# silently degrades back to scanning the whole window.
P="$(new_project stale-promise-before-string-boundary)"
write_loop "$P/.claude/loop" 1 50 "EPIC_DONE"
T="$P/transcript.jsonl"
make_transcript "$T" \
  text "<promise>EPIC_DONE</promise>" \
  userstr "Do the next step of the work." \
  tool "Read" \
  tool "Edit"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "stale promise before a string-shaped turn boundary does not stop a fresh iteration" '"decision": "block"' "$OUT"
assert_file "loop file survives the stale promise" "$P/.claude/loop/active.md"

# ---------------------------------------------------------------------------
section 'Defect 4: frontmatter parse bounded to the first block'
# ---------------------------------------------------------------------------

# A body containing --- separators AND key-like lines. Under the old sed range
# parser this produced a multi-line iteration value, failed numeric validation,
# and deleted the loop file.
P="$(new_project hostile-body)"
B="$P/.claude/loop"
cat > "$B/active.md" <<'FIXTURE'
---
iteration: 2
max_iterations: 50
completion_promise: "EPIC_DONE"
---

Body begins here.

---

## A section that mentions frontmatter keys

The state file records fields like:

iteration: 99
max_iterations: 1
completion_promise: "FAKE"

---

End of body.
FIXTURE

OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "hostile body still continues the loop" '"decision": "block"' "$OUT"
assert_file "hostile body did not delete the loop file" "$B/active.md"
NEWITER="$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^iteration:/{print $2}' "$B/active.md")"
assert_eq "iteration incremented to 3 (not 100)" "3" "$NEWITER"

# The decoy keys in the body must survive untouched: bump must only rewrite
# the frontmatter occurrence.
DECOY="$(grep -c '^iteration: 99$' "$B/active.md")"
assert_eq "decoy body key left intact" "1" "$DECOY"

# Discriminating case for the frontmatter scope. A key present in the BODY but
# absent from the FRONTMATTER must read as unset. An unbounded range parser
# picks up the body value instead, which would let prose in the prompt
# configure the loop. Here a body-only completion_promise would stop the loop
# on a promise the user never set.
P="$(new_project body-only-keys)"
B="$P/.claude/loop"
cat > "$B/active.md" <<'FIXTURE'
---
iteration: 1
max_iterations: 50
---

Body begins.

---

Never configure the loop from prose. These are documentation, not settings:

completion_promise: "FAKE_DONE"
state_file: bogus/does-not-exist.md

---

End.
FIXTURE
T="$P/transcript.jsonl"
make_transcript "$T" text "<promise>FAKE_DONE</promise>"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "body-only promise must not stop the loop" '"decision": "block"' "$OUT"
assert_file "body-only promise leaves loop file intact" "$B/active.md"
assert_not_contains "body-only promise never reported as fulfilled" "fulfilled" "$(last_stderr)"

# Duplicated keys inside the real frontmatter must resolve to the first.
P="$(new_project dup-keys)"
B="$P/.claude/loop"
printf -- '---\niteration: 4\niteration: 999\nmax_iterations: 50\ncompletion_promise: "X"\n---\n\nBody\n' > "$B/active.md"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "duplicated key does not corrupt parse" '"decision": "block"' "$OUT"
NEWITER="$(awk 'NR==1&&/^---/{f=1;next} f&&/^---/{exit} f&&/^iteration:/{print $2; exit}' "$B/active.md")"
assert_eq "duplicated key resolves to the first" "5" "$NEWITER"

# Body separators must be preserved in the fed-back prompt.
P="$(new_project hostile-body)"
B="$P/.claude/loop"
cat > "$B/active.md" <<'FIXTURE'
---
iteration: 2
max_iterations: 50
completion_promise: "EPIC_DONE"
---

Body begins here.

---

## A section that mentions frontmatter keys

The state file records fields like:

iteration: 99
max_iterations: 1
completion_promise: "FAKE"

---

End of body.
FIXTURE
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
FEDBACK="$(printf '%s' "$OUT" | jq -r '.reason')"
assert_contains "body --- separators preserved" $'\n---\n' "$FEDBACK"
assert_contains "body content preserved" "End of body." "$FEDBACK"
assert_not_contains "frontmatter not leaked into prompt" "max_iterations: 50" "$FEDBACK"

# ---------------------------------------------------------------------------
section 'Corruption handling'
# ---------------------------------------------------------------------------

P="$(new_project corrupt-iter)"
B="$P/.claude/loop"
printf -- '---\niteration: abc\nmax_iterations: 10\ncompletion_promise: "X"\n---\n\nBody\n' > "$B/active.md"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_eq "corrupt iteration produces no stdout" "" "$OUT"
assert_contains "corrupt iteration is diagnosed" "corrupted" "$(last_stderr)"
assert_no_file "corrupt loop file is cleared" "$B/active.md"

P="$(new_project unsubstituted)"
B="$P/.claude/loop"
printf -- '---\niteration: 1\nmax_iterations: {{MAX_ITERATIONS}}\ncompletion_promise: "X"\n---\n\nBody\n' > "$B/active.md"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "unsubstituted placeholder is diagnosed" "max_iterations" "$(last_stderr)"

P="$(new_project empty-body)"
B="$P/.claude/loop"
printf -- '---\niteration: 1\nmax_iterations: 10\ncompletion_promise: "X"\n---\n\n   \n' > "$B/active.md"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "empty prompt body is diagnosed" "empty prompt body" "$(last_stderr)"

P="$(new_project no-frontmatter)"
B="$P/.claude/loop"
printf 'Just a prompt with no frontmatter at all.\n' > "$B/active.md"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "missing frontmatter is diagnosed" "no frontmatter" "$(last_stderr)"

# ---------------------------------------------------------------------------
section 'Iteration limits'
# ---------------------------------------------------------------------------

P="$(new_project at-max)"
B="$P/.claude/loop"
write_loop "$B" 10 10 "X"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_eq "at max_iterations produces no stdout" "" "$OUT"
assert_contains "max iterations is reported" "max iterations (10)" "$(last_stderr)"
assert_no_file "loop file cleared at max" "$B/active.md"

P="$(new_project below-max)"
B="$P/.claude/loop"
write_loop "$B" 9 10 "X"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "below max continues" '"decision": "block"' "$OUT"

# Unlimited loops are still capped by the hard ceiling.
P="$(new_project ceiling)"
B="$P/.claude/loop"
write_loop "$B" 200 0 "X"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "hard ceiling stops unlimited loop" "hard ceiling" "$(last_stderr)"

P="$(new_project unlimited-ok)"
B="$P/.claude/loop"
write_loop "$B" 5 0 "X"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "unlimited loop below ceiling continues" '"decision": "block"' "$OUT"

# ---------------------------------------------------------------------------
section 'Stall guard'
# ---------------------------------------------------------------------------

P="$(new_project stall)"
B="$P/.claude/loop"
mkdir -p "$P/.claude/loop/run-1"
STATE=".claude/loop/run-1/loop-state.md"
printf 'current_step: implement\n' > "$P/$STATE"
write_loop "$B" 1 50 "X" "$STATE"

# Three consecutive unchanged iterations must stop the loop, not two.
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "stall 1 of 3 continues" '"decision": "block"' "$OUT"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "stall 2 of 3 continues" '"decision": "block"' "$OUT"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_contains "stall 3 of 3 stops" "no progress in 3" "$(last_stderr)"
assert_no_file "stalled loop file cleared" "$B/active.md"

# A changing state file resets the counter and never stalls.
P="$(new_project no-stall)"
B="$P/.claude/loop"
mkdir -p "$P/.claude/loop/run-1"
printf 'current_step: implement\n' > "$P/$STATE"
write_loop "$B" 1 50 "X" "$STATE"
STALLED=0
for i in 1 2 3 4 5; do
  printf 'current_step: step-%s\n' "$i" > "$P/$STATE"
  OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
  [[ "$OUT" == *'"decision": "block"'* ]] || STALLED=1
done
assert_eq "changing state never stalls over 5 iterations" "0" "$STALLED"

# ---------------------------------------------------------------------------
section 'Session isolation'
# ---------------------------------------------------------------------------

P="$(new_project sessions)"
B="$P/.claude/loop"
{
  printf -- '---\niteration: 1\nmax_iterations: 50\ncompletion_promise: "X"\nsession_id: owner-session\n---\n\nBody\n'
} > "$B/active.md"

OUT="$(run_claude "$P" "$(claude_input '' owner-session)")"
assert_contains "owning session continues the loop" '"decision": "block"' "$OUT"

OUT="$(run_claude "$P" "$(claude_input '' other-session)")"
assert_eq "foreign session is not conscripted" "" "$OUT"
assert_file "foreign session leaves loop file intact" "$B/active.md"

# Loop files with no session_id run in every session.
P="$(new_project no-session-id)"
B="$P/.claude/loop"
write_loop "$B" 1 50 "X"
OUT="$(run_claude "$P" "$(claude_input '' any-session)")"
assert_contains "loop without session_id still runs" '"decision": "block"' "$OUT"

# ---------------------------------------------------------------------------
section 'Completion sentinel'
# ---------------------------------------------------------------------------

P="$(new_project sentinel)"
B="$P/.claude/loop"
write_loop "$B" 4 50 "EPIC_DONE"
: > "$B/done"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
assert_eq "sentinel stops the loop" "" "$OUT"
assert_contains "sentinel completion is reported" "fulfilled at iteration 4" "$(last_stderr)"
assert_no_file "sentinel is cleaned up" "$B/done"

# ---------------------------------------------------------------------------
section 'Loops with no completion promise'
# ---------------------------------------------------------------------------

# An unset promise is written as YAML null. Nothing must be treated as a
# promise in that mode: the loop runs until max_iterations.
for NULLFORM in "null" "~" ""; do
  P="$(new_project "nopromise-${NULLFORM:-empty}")"
  B="$P/.claude/loop"
  printf -- '---\niteration: 1\nmax_iterations: 20\ncompletion_promise: %s\n---\n\nBody\n' "$NULLFORM" > "$B/active.md"
  T="$P/transcript.jsonl"
  make_transcript "$T" text "<promise>$NULLFORM</promise>"
  OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
  assert_contains "promise '${NULLFORM:-empty}' does not stop an unset-promise loop" '"decision": "block"' "$OUT"
  MSG="$(printf '%s' "$OUT" | jq -r '.systemMessage')"
  assert_contains "unset promise '${NULLFORM:-empty}' announced correctly" "No completion promise set" "$MSG"
done

# Any promise text at all must be inert when none is configured.
P="$(new_project nopromise-arbitrary)"
B="$P/.claude/loop"
printf -- '---\niteration: 1\nmax_iterations: 20\ncompletion_promise: null\n---\n\nBody\n' > "$B/active.md"
T="$P/transcript.jsonl"
make_transcript "$T" text "<promise>DONE</promise> <promise>COMPLETE</promise>"
OUT="$(run_claude "$P" "$(claude_input "$T" sess-1)")"
assert_contains "arbitrary promise inert when none configured" '"decision": "block"' "$OUT"
assert_file "unset-promise loop stays active" "$B/active.md"

# The Cursor capture hook must never write a sentinel without a promise.
P="$(new_project nopromise-capture)"
B="$P/.cursor/loop"
printf -- '---\niteration: 1\nmax_iterations: 20\ncompletion_promise: null\n---\n\nBody\n' > "$B/active.md"
run_capture "$P" "$(jq -n '{text: "<promise>null</promise>"}')"
assert_no_file "capture writes no sentinel without a promise" "$B/done"
run_capture "$P" "$(jq -n '{text: "<promise>ANYTHING</promise>"}')"
assert_no_file "capture ignores arbitrary promise without config" "$B/done"

# A configured promise still announces the stop instruction.
P="$(new_project promise-announced)"
B="$P/.claude/loop"
write_loop "$B" 1 20 "SHIP_IT"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
MSG="$(printf '%s' "$OUT" | jq -r '.systemMessage')"
assert_contains "configured promise is announced" "<promise>SHIP_IT</promise>" "$MSG"
assert_contains "announcement warns against false promises" "genuinely true" "$MSG"

# ---------------------------------------------------------------------------
section 'Cursor capture hook'
# ---------------------------------------------------------------------------

P="$(new_project capture)"
B="$P/.cursor/loop"
write_loop "$B" 2 50 "SHIP_IT"

run_capture "$P" "$(jq -n '{text: "still working"}')"
assert_no_file "capture: no promise writes no sentinel" "$B/done"

run_capture "$P" "$(jq -n '{text: "<promise>WRONG</promise>"}')"
assert_no_file "capture: wrong promise writes no sentinel" "$B/done"

run_capture "$P" "$(jq -n '{text: "All good.\n<promise>SHIP_IT</promise>\n"}')"
assert_file "capture: matching promise writes sentinel" "$B/done"

OUT="$(run_cursor "$P" '{"status":"completed"}')"
assert_eq "cursor stop honours the sentinel" "" "$OUT"
assert_no_file "cursor clears loop on completion" "$B/active.md"

# Multi-line and whitespace-padded promises normalise correctly.
P="$(new_project capture-multiline)"
B="$P/.cursor/loop"
write_loop "$B" 2 50 "TASK COMPLETE"
run_capture "$P" "$(jq -n '{text: "<promise>\n  TASK   COMPLETE\n</promise>"}')"
assert_file "capture: whitespace-normalised promise matches" "$B/done"

# ---------------------------------------------------------------------------
section 'Cursor stop hook semantics'
# ---------------------------------------------------------------------------

P="$(new_project cursor-continue)"
B="$P/.cursor/loop"
write_loop "$B" 1 50 "X"
OUT="$(run_cursor "$P" '{"status":"completed"}')"
assert_contains "cursor emits followup_message" "followup_message" "$OUT"
MSG="$(printf '%s' "$OUT" | jq -r '.followup_message')"
assert_contains "cursor followup carries the prompt" "Do the next step" "$MSG"
assert_contains "cursor followup carries iteration header" "Ralph iteration 2" "$MSG"

# Aborted turns must not be re-fed: that would fight the user for the session.
P="$(new_project cursor-abort)"
B="$P/.cursor/loop"
write_loop "$B" 1 50 "X"
OUT="$(run_cursor "$P" '{"status":"aborted"}')"
assert_eq "aborted turn does not continue" "" "$OUT"
assert_file "aborted turn leaves loop intact for resume" "$B/active.md"

# ---------------------------------------------------------------------------
section 'Agent isolation'
# ---------------------------------------------------------------------------

# A Claude loop must be invisible to the Cursor hook and vice versa.
P="$(new_project isolation)"
write_loop "$P/.claude/loop" 1 50 "X"
OUT="$(run_cursor "$P" '{"status":"completed"}')"
assert_eq "cursor ignores a claude loop" "" "$OUT"
assert_file "claude loop untouched by cursor hook" "$P/.claude/loop/active.md"

# ---------------------------------------------------------------------------
section 'End-to-end: multi-iteration run to completion'
# ---------------------------------------------------------------------------

# Drive the Claude hook the way a real session would: repeated stops, with the
# promise appearing only at the end. Proves the loop neither dies early nor
# runs past its promise.
P="$(new_project e2e-claude)"
B="$P/.claude/loop"
mkdir -p "$B/run-1"
STATE=".claude/loop/run-1/loop-state.md"
write_loop "$B" 1 20 "EPIC_DONE" "$STATE"
T="$P/transcript.jsonl"

ITERATIONS=0
COMPLETED=0
for i in $(seq 1 12); do
  # Simulate real work: state changes every turn.
  printf 'current_step: step-%s\n' "$i" > "$P/$STATE"
  if [[ $i -eq 8 ]]; then
    make_transcript "$T" text "Finished everything." text "<promise>EPIC_DONE</promise>" tool "Bash"
  else
    make_transcript "$T" text "Completed step $i." tool "Edit"
  fi
  OUT="$(run_claude "$P" "$(claude_input "$T" sess-e2e)")"
  if [[ "$OUT" == *'"decision": "block"'* ]]; then
    ITERATIONS=$((ITERATIONS + 1))
  else
    COMPLETED=$i
    break
  fi
done

assert_eq "e2e claude: ran 7 continuations before completing" "7" "$ITERATIONS"
assert_eq "e2e claude: completed on iteration 8" "8" "$COMPLETED"
assert_no_file "e2e claude: loop file cleared at completion" "$B/active.md"

# Same run, promise never emitted: must stop exactly at max_iterations.
P="$(new_project e2e-maxout)"
B="$P/.claude/loop"
mkdir -p "$B/run-1"
write_loop "$B" 1 6 "NEVER" "$STATE"
T="$P/transcript.jsonl"
ITERATIONS=0
for i in $(seq 1 20); do
  printf 'current_step: step-%s\n' "$i" > "$P/$STATE"
  make_transcript "$T" text "Still going." tool "Edit"
  OUT="$(run_claude "$P" "$(claude_input "$T" sess-max)")"
  [[ "$OUT" == *'"decision": "block"'* ]] || break
  ITERATIONS=$((ITERATIONS + 1))
done
assert_eq "e2e maxout: stopped after 5 continuations (1 -> 6)" "5" "$ITERATIONS"
assert_no_file "e2e maxout: loop file cleared" "$B/active.md"

# End-to-end on Cursor, driven through the capture hook.
P="$(new_project e2e-cursor)"
B="$P/.cursor/loop"
write_loop "$B" 1 20 "SHIP_IT"
ITERATIONS=0
for i in $(seq 1 12); do
  if [[ $i -eq 5 ]]; then
    run_capture "$P" "$(jq -n '{text: "<promise>SHIP_IT</promise>"}')"
  else
    run_capture "$P" "$(jq -n --arg t "step $i done" '{text: $t}')"
  fi
  OUT="$(run_cursor "$P" '{"status":"completed"}')"
  [[ "$OUT" == *"followup_message"* ]] || break
  ITERATIONS=$((ITERATIONS + 1))
done
assert_eq "e2e cursor: stopped on the promise turn" "4" "$ITERATIONS"
assert_no_file "e2e cursor: loop file cleared" "$B/active.md"

# ---------------------------------------------------------------------------
section 'Prompt fidelity'
# ---------------------------------------------------------------------------

# Prompts containing shell metacharacters, quotes, backslashes and unicode
# must round-trip through the JSON payload byte for byte.
P="$(new_project fidelity)"
B="$P/.claude/loop"
{
  printf -- '---\niteration: 1\nmax_iterations: 50\ncompletion_promise: "X"\n---\n\n'
  printf 'Use $(whoami) and `backticks` and "double" and '"'"'single'"'"'.\n'
  printf 'Backslash: C:\\path\\to\\file\n'
  printf 'Unicode: café — naïve — 日本語\n'
  printf 'Glob chars: *.md ?.txt [a-z]\n'
} > "$B/active.md"
OUT="$(run_claude "$P" "$(claude_input '' sess-1)")"
FEDBACK="$(printf '%s' "$OUT" | jq -r '.reason')"
assert_contains "fidelity: command substitution literal" 'Use $(whoami)' "$FEDBACK"
assert_contains "fidelity: backticks literal" '`backticks`' "$FEDBACK"
assert_contains "fidelity: backslashes literal" 'C:\path\to\file' "$FEDBACK"
assert_contains "fidelity: unicode preserved" 'café' "$FEDBACK"
assert_contains "fidelity: glob chars literal" '[a-z]' "$FEDBACK"

# Promises containing glob metacharacters must compare literally, not as
# patterns. This is why the library uses = rather than == inside [[ ]].
P="$(new_project glob-promise)"
B="$P/.cursor/loop"
write_loop "$B" 1 50 "DONE*"
run_capture "$P" "$(jq -n '{text: "<promise>DONEXYZ</promise>"}')"
assert_no_file "glob promise does not pattern-match" "$B/done"
run_capture "$P" "$(jq -n '{text: "<promise>DONE*</promise>"}')"
assert_file "glob promise matches literally" "$B/done"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

printf '\n==================\n'
printf 'passed: %s\n' "$PASS"
printf 'failed: %s\n' "$FAIL"

if [[ $FAIL -gt 0 ]]; then
  printf '\nfailed assertions:\n'
  for n in "${FAILED_NAMES[@]}"; do printf '  - %s\n' "$n"; done
  exit 1
fi

printf '\nall green\n'
exit 0
