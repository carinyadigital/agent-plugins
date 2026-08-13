#!/usr/bin/env bash
#
# Tests for scripts/seed-ralph-loop.sh.
#
# The seed script exists to make one class of failure impossible: an
# unsubstituted {{PLACEHOLDER}} reaching the loop frontmatter, where it fails
# the hook's numeric validation and silently deletes the loop. Most of what
# follows guards that contract, plus the validation the agent should not be
# trusted to do in prose.
#
#   ./scripts/test-seed-ralph-loop.sh [-v]

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SEED="$ROOT/scripts/seed-ralph-loop.sh"
CLAUDE_HOOK="$ROOT/hooks/claude/stop-hook.sh"
VERBOSE=0
[[ "${1:-}" == "-v" ]] && VERBOSE=1

PASS=0
FAIL=0
FAILED_NAMES=()

TMPROOT="$(mktemp -d)"
trap 'rm -rf "$TMPROOT"' EXIT

ok() { PASS=$((PASS + 1)); [[ $VERBOSE -eq 1 ]] && printf '  ok   %s\n' "$1"; return 0; }
no() {
  FAIL=$((FAIL + 1)); FAILED_NAMES+=("$1")
  printf '  FAIL %s\n' "$1"
  [[ -n "${2:-}" ]] && printf '       %s\n' "$2"
  return 0
}
assert_eq() { [[ "$2" == "$3" ]] && ok "$1" || no "$1" "expected [$2] got [$3]"; }
assert_contains() { [[ "$3" == *"$2"* ]] && ok "$1" || no "$1" "expected [$2] in [${3:0:200}]"; }
assert_file() { [[ -f "$2" ]] && ok "$1" || no "$1" "missing $2"; }
assert_no_file() { [[ ! -f "$2" ]] && ok "$1" || no "$1" "unexpected $2"; }
section() { printf '\n%s\n' "$1"; }

new_project() {
  local dir="$TMPROOT/$1"
  mkdir -p "$dir"
  git -C "$dir" init -q 2>/dev/null
  printf '%s' "$dir"
}

PROMPT="$TMPROOT/prompt.md"
printf 'Build a REST API for todos with tests.\n' > "$PROMPT"
STEPS="$TMPROOT/steps.md"
printf '#### start\n\nDo the thing. Set current_step: finish.\n\n#### finish\n\nWrap up.\n' > "$STEPS"

# seed <project> <args...> -> stdout+stderr; exit code via seed_rc.
# The runner is called inside a command substitution, so the exit code goes
# through a file rather than a variable that the subshell would discard.
RCFILE="$TMPROOT/.seed_rc"
seed_rc() { cat "$RCFILE" 2>/dev/null || printf '0'; }
seed() {
  local project="$1"; shift
  local out rc
  out="$("$SEED" --project-dir "$project" "$@" 2>&1)"
  rc=$?
  printf '%s' "$rc" > "$RCFILE"
  printf '%s' "$out"
}

printf 'seed-ralph-loop tests\n=====================\n'

# ---------------------------------------------------------------------------
section 'Argument validation'
# ---------------------------------------------------------------------------

P="$(new_project args)"

OUT="$(seed "$P" --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D)"
assert_eq "missing --agent fails" "1" "$(seed_rc)"
assert_contains "missing --agent explains" "--agent is required" "$OUT"

OUT="$(seed "$P" --agent emacs --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D)"
assert_eq "unknown agent fails" "1" "$(seed_rc)"

OUT="$(seed "$P" --agent claude --preset nonsense --completion-promise D)"
assert_eq "unknown preset fails" "1" "$(seed_rc)"
assert_contains "unknown preset explains" "unknown preset" "$OUT"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --max-iterations abc --completion-promise D)"
assert_eq "non-numeric max-iterations fails" "1" "$(seed_rc)"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --max-iterations -5 --completion-promise D)"
assert_eq "negative max-iterations fails" "1" "$(seed_rc)"

# Neither a promise nor a limit means a loop nothing can stop except the hard
# ceiling. Refuse it at seed time rather than discover it at iteration 200.
OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --max-iterations 0)"
assert_eq "no promise and no limit is refused" "1" "$(seed_rc)"
assert_contains "refusal explains why" "neither a completion promise nor an iteration limit" "$OUT"

# A promise with a quote breaks the YAML; with an angle bracket breaks the tag.
for BAD in 'say "done"' 'a<b' 'a>b'; do
  OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise "$BAD")"
  assert_eq "promise [$BAD] rejected" "1" "$(seed_rc)"
done

OUT="$(seed "$P" --agent claude --preset ad-hoc --completion-promise D)"
assert_eq "ad-hoc without --prompt-file fails" "1" "$(seed_rc)"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$TMPROOT/nope.md" --completion-promise D)"
assert_eq "ad-hoc with missing prompt file fails" "1" "$(seed_rc)"

: > "$TMPROOT/empty.md"
OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$TMPROOT/empty.md" --completion-promise D)"
assert_eq "ad-hoc with empty prompt file fails" "1" "$(seed_rc)"

OUT="$(seed "$P" --agent claude --preset custom --completion-promise D)"
assert_eq "custom without --steps-file fails" "1" "$(seed_rc)"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --run-id ../escape)"
assert_eq "path traversal in run-id rejected" "1" "$(seed_rc)"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --set NOEQUALS)"
assert_eq "malformed --set rejected" "1" "$(seed_rc)"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --bogus-flag)"
assert_eq "unknown flag rejected" "1" "$(seed_rc)"

assert_no_file "no files written on any validation failure" "$P/.claude/loop/active.md"

# ---------------------------------------------------------------------------
section 'Placeholder resolution'
# ---------------------------------------------------------------------------

P="$(new_project placeholders)"
OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise DONE --max-iterations 20)"
assert_eq "ad-hoc seeds cleanly" "0" "$(seed_rc)"
assert_file "active.md written" "$P/.claude/loop/active.md"

LEFTOVER="$(grep -o '{{[A-Z_][A-Z0-9_]*}}' "$P/.claude/loop/active.md" | sort -u | tr '\n' ' ')"
assert_eq "no placeholders survive into active.md" "" "${LEFTOVER// /}"
assert_contains "task prompt is embedded" "Build a REST API for todos" "$(cat "$P/.claude/loop/active.md")"

# ad-hoc has no run directory, so its state_file must be null: a dangling
# state path would make the stall guard watch a file that never exists.
assert_contains "ad-hoc declares no state file" "state_file: null" "$(cat "$P/.claude/loop/active.md")"
assert_no_file "ad-hoc writes no state file" "$P/.claude/loop/ad-hoc/loop-state.md"

P="$(new_project eng)"
OUT="$(seed "$P" --agent claude --preset engineering-delivery --run-id ep-1 \
  --completion-promise EPIC_DONE --max-iterations 60 \
  --set WORK_ID=checkout --set BRANCH=feat/checkout \
  --set TASKS_PATH=specs/checkout/TASKS.local.md \
  --set TDD_PATH=specs/checkout/tdd.md \
  --set FIRST_ITEM=CHK01-01 --set 'WORK_SEQUENCE=1. CHK01-01' \
  --set 'GOAL=Ship checkout.' --set 'DONE_CRITERIA=MR raised.' \
  --set 'PRESET_CONTEXT=Node 20.')"
assert_eq "engineering-delivery seeds cleanly" "0" "$(seed_rc)"

for F in active.md ep-1/loop-state.md ep-1/context.md; do
  assert_file "wrote $F" "$P/.claude/loop/$F"
  LEFTOVER="$(grep -o '{{[A-Z_][A-Z0-9_]*}}' "$P/.claude/loop/$F" | sort -u | tr '\n' ' ')"
  assert_eq "no placeholders in $F" "" "${LEFTOVER// /}"
done

assert_contains "work item substituted" "checkout" "$(cat "$P/.claude/loop/active.md")"
assert_contains "state_file points at the run dir" \
  "state_file: .claude/loop/ep-1/loop-state.md" "$(cat "$P/.claude/loop/active.md")"
assert_contains "first item seeded into state" "current_item: CHK01-01" \
  "$(cat "$P/.claude/loop/ep-1/loop-state.md")"

# A missing --set must fail loudly rather than write a broken file. This is the
# exact failure the script exists to prevent.
P="$(new_project missing-set)"
OUT="$(seed "$P" --agent claude --preset engineering-delivery --run-id ep-2 \
  --completion-promise EPIC_DONE --set WORK_ID=checkout)"
assert_eq "missing --set values fail" "1" "$(seed_rc)"
assert_contains "failure names the placeholders" "unresolved placeholders" "$OUT"
assert_no_file "nothing written when placeholders unresolved" "$P/.claude/loop/active.md"

# ---------------------------------------------------------------------------
section 'Value escaping'
# ---------------------------------------------------------------------------

# Values are substituted with awk, not sed, so replacement metacharacters must
# survive literally.
P="$(new_project escaping)"
OUT="$(seed "$P" --agent claude --preset custom --run-id esc --steps-file "$STEPS" \
  --completion-promise DONE --max-iterations 10 \
  --set 'FIRST_ITEM=a/b&c\d' --set 'WORK_SEQUENCE=path/with/slashes & ampersand' \
  --set 'GOAL=100% of $HOME' --set 'DONE_CRITERIA=x' --set 'PRESET_CONTEXT=y' \
  --set FIRST_STEP=start)"
assert_eq "custom preset with metacharacters seeds" "0" "$(seed_rc)"
STATE="$(cat "$P/.claude/loop/esc/loop-state.md" 2>/dev/null)"
assert_contains "slashes and ampersands survive" 'a/b&c\d' "$STATE"
CTX="$(cat "$P/.claude/loop/esc/context.md" 2>/dev/null)"
assert_contains "percent and dollar survive" '100% of $HOME' "$CTX"
assert_contains "custom steps embedded" "Do the thing" "$(cat "$P/.claude/loop/active.md")"

# ---------------------------------------------------------------------------
section 'Overwrite protection'
# ---------------------------------------------------------------------------

P="$(new_project overwrite)"
seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10 >/dev/null
# Simulate a loop that has progressed past iteration 1.
sed -i.bak 's/^iteration: 1$/iteration: 7/' "$P/.claude/loop/active.md" 2>/dev/null || \
  sed -i '' 's/^iteration: 1$/iteration: 7/' "$P/.claude/loop/active.md"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10)"
assert_eq "refuses to clobber a running loop" "2" "$(seed_rc)"
assert_contains "refusal reports the iteration" "iteration 7" "$OUT"
assert_contains "refusal suggests cancel" "cancel" "$OUT"
assert_contains "running loop untouched" "iteration: 7" "$(cat "$P/.claude/loop/active.md")"

OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10 --force)"
assert_eq "--force overwrites" "0" "$(seed_rc)"
assert_contains "forced overwrite resets iteration" "iteration: 1" "$(cat "$P/.claude/loop/active.md")"

# An untouched loop at iteration 1 is safe to replace without --force.
P="$(new_project reseed)"
seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10 >/dev/null
OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise E --max-iterations 10)"
assert_eq "re-seeding an unstarted loop is allowed" "0" "$(seed_rc)"

# ---------------------------------------------------------------------------
section 'Agent separation and gitignore'
# ---------------------------------------------------------------------------

P="$(new_project agents)"
seed "$P" --agent cursor --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10 >/dev/null
assert_file "cursor seeds .cursor/loop" "$P/.cursor/loop/active.md"
assert_no_file "cursor does not seed .claude/loop" "$P/.claude/loop/active.md"
assert_contains "gitignore covers cursor loop" ".cursor/loop/" "$(cat "$P/.gitignore" 2>/dev/null)"

seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10 >/dev/null
assert_file "claude seeds .claude/loop" "$P/.claude/loop/active.md"
assert_contains "gitignore covers claude loop" ".claude/loop/" "$(cat "$P/.gitignore" 2>/dev/null)"

# Repeat seeding must not append duplicate gitignore entries.
seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10 --force >/dev/null
COUNT="$(grep -c '^\.claude/loop/$' "$P/.gitignore" 2>/dev/null || echo 0)"
assert_eq "gitignore entry not duplicated" "1" "$COUNT"

# ---------------------------------------------------------------------------
section 'Dry run'
# ---------------------------------------------------------------------------

P="$(new_project dryrun)"
OUT="$(seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" --completion-promise D --max-iterations 10 --dry-run)"
assert_eq "dry run succeeds" "0" "$(seed_rc)"
assert_contains "dry run shows the target path" "would write" "$OUT"
assert_no_file "dry run writes nothing" "$P/.claude/loop/active.md"

# ---------------------------------------------------------------------------
section 'Integration: seeded loop drives the real hook'
# ---------------------------------------------------------------------------

# The seed script and the stop hook agree on the file format only if a freshly
# seeded loop actually runs. Anything else is two components that each pass
# their own tests and fail together.

P="$(new_project integration)"
seed "$P" --agent claude --preset engineering-delivery --run-id run-1 \
  --completion-promise EPIC_DONE --max-iterations 12 --session-id sess-int \
  --set WORK_ID=checkout --set BRANCH=feat/checkout \
  --set TASKS_PATH=t.md --set TDD_PATH=d.md \
  --set FIRST_ITEM=CHK01-01 --set 'WORK_SEQUENCE=1. CHK01-01' \
  --set 'GOAL=g' --set 'DONE_CRITERIA=d' --set 'PRESET_CONTEXT=c' >/dev/null
assert_eq "integration seed succeeded" "0" "$(seed_rc)"

T="$P/transcript.jsonl"
printf '{"role":"assistant","message":{"content":[{"type":"text","text":"working"}]}}\n' > "$T"
HOOK_IN="$(jq -n --arg t "$T" '{transcript_path:$t, session_id:"sess-int", stop_hook_active:false}')"

CONTINUES=0
for i in $(seq 1 15); do
  printf 'current_step: step-%s\n' "$i" > "$P/.claude/loop/run-1/loop-state.md"
  OUT="$(printf '%s' "$HOOK_IN" | CLAUDE_PROJECT_DIR="$P" "$CLAUDE_HOOK" 2>/dev/null)"
  [[ "$OUT" == *'"decision": "block"'* ]] || break
  CONTINUES=$((CONTINUES + 1))
done
assert_eq "seeded loop runs to its iteration limit" "11" "$CONTINUES"
assert_no_file "loop file cleared at the limit" "$P/.claude/loop/active.md"

# The same loop, completed by the promise.
P="$(new_project integration-promise)"
seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" \
  --completion-promise SHIPPED --max-iterations 30 --session-id sess-p >/dev/null
T="$P/transcript.jsonl"
CONTINUES=0
for i in $(seq 1 10); do
  if [[ $i -eq 4 ]]; then
    printf '{"role":"assistant","message":{"content":[{"type":"text","text":"<promise>SHIPPED</promise>"}]}}\n' > "$T"
    printf '{"role":"assistant","message":{"content":[{"type":"tool_use","name":"Bash","input":{}}]}}\n' >> "$T"
  else
    printf '{"role":"assistant","message":{"content":[{"type":"text","text":"iteration %s"}]}}\n' "$i" > "$T"
  fi
  HOOK_IN="$(jq -n --arg t "$T" '{transcript_path:$t, session_id:"sess-p", stop_hook_active:false}')"
  OUT="$(printf '%s' "$HOOK_IN" | CLAUDE_PROJECT_DIR="$P" "$CLAUDE_HOOK" 2>/dev/null)"
  [[ "$OUT" == *'"decision": "block"'* ]] || break
  CONTINUES=$((CONTINUES + 1))
done
assert_eq "seeded ad-hoc loop stops on its promise" "3" "$CONTINUES"
assert_no_file "loop cleared on promise" "$P/.claude/loop/active.md"

# A foreign session must not be conscripted into a seeded loop.
P="$(new_project integration-session)"
seed "$P" --agent claude --preset ad-hoc --prompt-file "$PROMPT" \
  --completion-promise X --max-iterations 30 --session-id owner >/dev/null
HOOK_IN="$(jq -n '{transcript_path:"", session_id:"stranger", stop_hook_active:false}')"
OUT="$(printf '%s' "$HOOK_IN" | CLAUDE_PROJECT_DIR="$P" "$CLAUDE_HOOK" 2>/dev/null)"
assert_eq "foreign session sees no loop" "" "$OUT"
assert_file "foreign session leaves the loop alone" "$P/.claude/loop/active.md"

printf '\n=====================\n'
printf 'passed: %s\n' "$PASS"
printf 'failed: %s\n' "$FAIL"
if [[ $FAIL -gt 0 ]]; then
  printf '\nfailed assertions:\n'
  for n in "${FAILED_NAMES[@]}"; do printf '  - %s\n' "$n"; done
  exit 1
fi
printf '\nall green\n'
exit 0
