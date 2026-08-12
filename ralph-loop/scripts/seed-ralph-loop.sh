#!/usr/bin/env bash
#
# Seed a Ralph loop.
#
# Writes the active loop file and the run directory from packaged templates.
# The agent resolves the values; this script owns validation and writing.
#
# Placeholder substitution used to be the agent's job. That produced a
# recurring failure where a {{PLACEHOLDER}} survived into the frontmatter,
# failed the hook's numeric validation, and silently deleted the loop file.
# The old setup prompt even listed "leaving any {{PLACEHOLDER}} unsubstituted"
# as an anti-pattern, which was an admission that it happened. Doing it here
# makes the failure impossible: unresolved placeholders are a hard error.
#
# Usage:
#   seed-ralph-loop.sh --agent claude --preset engineering-delivery \
#     --run-id checkout-foundation-20260719-101500 \
#     --max-iterations 60 --completion-promise CHECKOUT_FOUNDATION_COMPLETE \
#     --set WORK_ID=checkout-foundation --set BRANCH=feat/checkout-foundation ...
#
#   seed-ralph-loop.sh --agent claude --preset ad-hoc \
#     --prompt-file /tmp/task.md --completion-promise DONE --max-iterations 20
#
# Run with --help for the full option list.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ASSETS="$REPO_ROOT/skills/ralph-loop/assets"

die() {
  printf 'seed-ralph-loop: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'USAGE'
Seed a Ralph loop.

Required:
  --agent <claude|cursor>       Which agent's directory to seed
  --preset <name>               ad-hoc | custom | engineering-delivery (contributed by product-engineering)

Common:
  --project-dir <path>          Project root (default: $PWD)
  --run-id <id>                 Run directory name (default: derived)
  --max-iterations <n>          0 means unlimited (default: 50)
  --completion-promise <text>   Promise phrase (default: none)
  --session-id <id>             Owning session, for session isolation
  --prompt-file <path>          Prompt body for the ad-hoc preset
  --steps-file <path>           Step definitions for the custom preset
  --set KEY=VALUE               Template placeholder (repeatable)
  --force                       Overwrite an in-progress loop
  --dry-run                     Print what would be written, write nothing
  -h, --help                    This message

Exit codes:
  0 seeded   1 usage or validation error   2 refused (loop in progress)
USAGE
}

AGENT=""
PRESET=""
PROJECT_DIR="$PWD"
RUN_ID=""
MAX_ITERATIONS="50"
COMPLETION_PROMISE=""
SESSION_ID=""
PROMPT_FILE=""
STEPS_FILE=""
FORCE=0
DRY_RUN=0
declare -a SET_KEYS=()
declare -a SET_VALS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)               AGENT="${2:-}"; shift 2 || die "--agent needs a value" ;;
    --preset)              PRESET="${2:-}"; shift 2 || die "--preset needs a value" ;;
    --project-dir)         PROJECT_DIR="${2:-}"; shift 2 || die "--project-dir needs a value" ;;
    --run-id)              RUN_ID="${2:-}"; shift 2 || die "--run-id needs a value" ;;
    --max-iterations)      MAX_ITERATIONS="${2:-}"; shift 2 || die "--max-iterations needs a value" ;;
    --completion-promise)  COMPLETION_PROMISE="${2:-}"; shift 2 || die "--completion-promise needs a value" ;;
    --session-id)          SESSION_ID="${2:-}"; shift 2 || die "--session-id needs a value" ;;
    --prompt-file)         PROMPT_FILE="${2:-}"; shift 2 || die "--prompt-file needs a value" ;;
    --steps-file)          STEPS_FILE="${2:-}"; shift 2 || die "--steps-file needs a value" ;;
    --force)               FORCE=1; shift ;;
    --dry-run)             DRY_RUN=1; shift ;;
    -h|--help)             usage; exit 0 ;;
    --set)
      [[ -n "${2:-}" ]] || die "--set needs KEY=VALUE"
      [[ "$2" == *=* ]] || die "--set expects KEY=VALUE, got '$2'"
      SET_KEYS+=("${2%%=*}")
      SET_VALS+=("${2#*=}")
      shift 2
      ;;
    *) die "unknown option '$1' (try --help)" ;;
  esac
done

# --- validation -------------------------------------------------------------

case "$AGENT" in
  claude) BASE="$PROJECT_DIR/.claude/loop" ;;
  cursor) BASE="$PROJECT_DIR/.cursor/loop" ;;
  "")     die "--agent is required (claude or cursor)" ;;
  *)      die "unknown agent '$AGENT' (expected claude or cursor)" ;;
esac

[[ -n "$PRESET" ]] || die "--preset is required"
resolve_preset_file() {
  local name="$1"
  if [[ -f "$ASSETS/presets/$name.md" ]]; then
    printf '%s\n' "$ASSETS/presets/$name.md"
    return 0
  fi
  local d
  # Contributed presets (product-engineering ships engineering-delivery)
  if [[ -n "${RALPH_PRESET_DIRS:-}" ]]; then
    IFS=':' read -ra _ralph_preset_dirs <<< "$RALPH_PRESET_DIRS"
    for d in "${_ralph_preset_dirs[@]}"; do
      [[ -f "$d/$name.md" ]] && { printf '%s\n' "$d/$name.md"; return 0; }
    done
  fi
  for d in \
    "$REPO_ROOT/../product-engineering/assets/ralph-presets" \
    "${CLAUDE_PLUGIN_ROOT:-}/../product-engineering/assets/ralph-presets" \
    "${CURSOR_PLUGIN_ROOT:-}/../product-engineering/assets/ralph-presets"
  do
    [[ -f "$d/$name.md" ]] && { printf '%s\n' "$d/$name.md"; return 0; }
  done
  return 1
}
PRESET_FILE="$(resolve_preset_file "$PRESET")" || die "unknown preset '$PRESET' (not in ralph-loop assets/presets or contributed product-engineering ralph-presets)"

[[ -d "$PROJECT_DIR" ]] || die "project dir does not exist: $PROJECT_DIR"

[[ "$MAX_ITERATIONS" =~ ^[0-9]+$ ]] \
  || die "--max-iterations must be a non-negative integer, got '$MAX_ITERATIONS'"

# A promise containing a quote or angle bracket breaks either the YAML
# frontmatter or the <promise> tag matching.
if [[ -n "$COMPLETION_PROMISE" ]]; then
  case "$COMPLETION_PROMISE" in
    *'"'*|*'<'*|*'>'*) die "--completion-promise must not contain quotes or angle brackets" ;;
  esac
fi

if [[ "$MAX_ITERATIONS" == "0" && -z "$COMPLETION_PROMISE" ]]; then
  die "refusing to seed a loop with neither a completion promise nor an iteration limit"
fi

if [[ "$PRESET" == "ad-hoc" ]]; then
  [[ -n "$PROMPT_FILE" ]] || die "the ad-hoc preset requires --prompt-file"
  [[ -f "$PROMPT_FILE" ]] || die "prompt file not found: $PROMPT_FILE"
  [[ -s "$PROMPT_FILE" ]] || die "prompt file is empty: $PROMPT_FILE"
fi

if [[ "$PRESET" == "custom" ]]; then
  [[ -n "$STEPS_FILE" ]] || die "the custom preset requires --steps-file"
  [[ -f "$STEPS_FILE" ]] || die "steps file not found: $STEPS_FILE"
fi

if [[ -z "$RUN_ID" ]]; then
  RUN_ID="$PRESET-$(date -u +%Y%m%d-%H%M%S)"
fi
case "$RUN_ID" in
  */*|*..*|"") die "invalid --run-id '$RUN_ID'" ;;
esac

ACTIVE="$BASE/active.md"
RUN_DIR="$BASE/$RUN_ID"

# Refuse to clobber a live loop. Iteration 1 with no progress is safe to
# replace; anything further is somebody's in-flight work.
if [[ -f "$ACTIVE" && $FORCE -eq 0 ]]; then
  EXISTING_ITER="$(awk '
    NR == 1 && /^---[[:space:]]*$/ { f = 1; next }
    f && /^---[[:space:]]*$/ { exit }
    f && /^iteration:/ { print $2; exit }
  ' "$ACTIVE" 2>/dev/null)"
  if [[ "$EXISTING_ITER" =~ ^[0-9]+$ ]] && [[ "$EXISTING_ITER" -gt 1 ]]; then
    printf 'seed-ralph-loop: a loop is already running at iteration %s.\n' "$EXISTING_ITER" >&2
    printf '  Inspect it with /ralph-loop:ralph-loop status, stop it with /ralph-loop:ralph-loop cancel,\n' >&2
    printf '  or pass --force to overwrite it.\n' >&2
    exit 2
  fi
fi

# --- substitution -----------------------------------------------------------

# Append a key/value pair. Always use this rather than appending to the two
# arrays separately: an interleaved append left them out of sync and, under
# `set -u`, substitution then died on an unbound SET_VALS index.
add_kv() {
  SET_KEYS+=("$1")
  SET_VALS+=("$2")
}

# Substitute {{KEY}} for every declared key. Values are applied with awk rather
# than sed so that slashes, ampersands and backslashes in a value cannot be
# reinterpreted as replacement syntax.
substitute() {
  local text="$1" i
  for ((i = 0; i < ${#SET_KEYS[@]}; i++)); do
    # Values travel through the environment, not through `awk -v`. awk expands
    # escape sequences in -v assignments, so a value containing `\d` (a Windows
    # path, a regex, a LaTeX command) silently lost its backslash. ENVIRON is
    # passed through literally.
    text="$(
      RALPH_SUB_KEY="{{${SET_KEYS[$i]}}}" \
      RALPH_SUB_VAL="${SET_VALS[$i]}" \
      awk '
        BEGIN { k = ENVIRON["RALPH_SUB_KEY"]; v = ENVIRON["RALPH_SUB_VAL"] }
        {
          out = ""
          rest = $0
          while ((idx = index(rest, k)) > 0) {
            out = out substr(rest, 1, idx - 1) v
            rest = substr(rest, idx + length(k))
          }
          print out rest
        }
      ' <<< "$text"
    )"
  done
  printf '%s' "$text"
}

# Any surviving {{...}} is a hard error. This is the check that makes the old
# unsubstituted-placeholder failure mode impossible.
assert_no_placeholders() {
  local text="$1" label="$2" leftover
  leftover="$(printf '%s' "$text" | grep -o '{{[A-Z_][A-Z0-9_]*}}' 2>/dev/null | sort -u | tr '\n' ' ')"
  if [[ -n "${leftover// /}" ]]; then
    die "unresolved placeholders in $label: $leftover"
  fi
}

read_file() {
  local path="$1"
  [[ -f "$path" ]] || die "missing template: $path"
  cat "$path"
}

PRESET_BODY="$(read_file "$PRESET_FILE")"

# The ad-hoc and custom presets inject user-supplied content.
if [[ "$PRESET" == "ad-hoc" ]]; then
  add_kv TASK_PROMPT "$(cat "$PROMPT_FILE")"
fi
if [[ "$PRESET" == "custom" ]]; then
  add_kv CUSTOM_STEPS "$(cat "$STEPS_FILE")"
fi

# Values every preset can rely on.
if [[ -n "$COMPLETION_PROMISE" ]]; then
  PROMISE_YAML="\"$COMPLETION_PROMISE\""
  PROMISE_TEXT="$COMPLETION_PROMISE"
else
  PROMISE_YAML="null"
  PROMISE_TEXT="(none configured)"
fi

if [[ "$PRESET" == "ad-hoc" ]]; then
  STATE_FILE_YAML="null"
else
  STATE_FILE_YAML="$(printf '%s' "$RUN_DIR/loop-state.md" | sed "s|^$PROJECT_DIR/||")"
fi

add_kv RUN_ID             "$RUN_ID"
add_kv RUN_DIR            "${RUN_DIR#"$PROJECT_DIR"/}"
add_kv MAX_ITERATIONS     "$MAX_ITERATIONS"
add_kv COMPLETION_PROMISE "$PROMISE_TEXT"
add_kv SEEDED_DATE        "$(date -u +%Y-%m-%d)"
add_kv AGENT              "$AGENT"
add_kv PRESET             "$PRESET"

# The completion instruction is generated, not templated, because its wording
# is a guardrail. A loop with no promise must not be told to emit one.
if [[ -n "$COMPLETION_PROMISE" ]]; then
  COMPLETION_BLOCK="When the work is genuinely complete, output exactly:

    <promise>$COMPLETION_PROMISE</promise>

That tag is the only thing that ends this loop early. Before you emit it,
re-read the definition of done and confirm every criterion actually holds.

You may ONLY output it when the statement is completely and unequivocally
true. Do not output it because you are stuck, because the task looks
impossible, because you have been running a long time, or because you judge
that stopping would be sensible. If the loop should stop for any of those
reasons, follow \"Getting stuck\" below instead. A false promise is the one
failure this system cannot detect or recover from.

The loop also stops on its own after $(if [[ "$MAX_ITERATIONS" == "0" ]]; then printf '200 iterations (the hard ceiling)'; else printf '%s iterations' "$MAX_ITERATIONS"; fi), so you do not need to
end it yourself to avoid running forever."
else
  COMPLETION_BLOCK="No completion promise is configured for this loop. It runs until it reaches
its iteration limit ($MAX_ITERATIONS) or stalls.

There is no tag you can emit to end it early. If the work is finished, say so
plainly and stop making changes; if you are blocked, follow \"Getting stuck\"
below."
fi

add_kv COMPLETION_BLOCK "$COMPLETION_BLOCK"

# The state rules differ by preset: ad-hoc has no state file, so telling it to
# read one would send the agent looking for a file that does not exist.
RUN_DIR_REL="${RUN_DIR#"$PROJECT_DIR"/}"
if [[ "$PRESET" == "ad-hoc" ]]; then
  add_kv STATE_BLOCK "1. **Read your previous work first.** You have no memory of earlier
   iterations. Before doing anything, inspect the working tree, \`git status\`,
   \`git diff\`, and the files you created. That is your only state.

2. **Do one meaningful unit of work per iteration**, then end the turn.

3. **Leave the work in a verifiable state.** Run the tests, the linter, or the
   program itself before ending the turn, so the next iteration starts from a
   known position."
  add_kv STUCK_BLOCK "1. Say plainly what is blocking you and what you tried.
2. Leave the working tree in a clean, committed state so the next iteration is
   not confused by half-finished edits.
3. Stop making speculative changes."
else
  add_kv STATE_BLOCK "1. **Read state first.** Every iteration begins by reading
   \`$RUN_DIR_REL/loop-state.md\` to find \`current_step\`, and
   \`$RUN_DIR_REL/context.md\` for the static run context. Never assume you
   remember where you were: you may be resuming cold after a crash.

2. **Exactly one step per iteration.** Run the single step named by
   \`current_step\`, update the state file, then end your turn. Do not chain
   steps even when the next one looks trivial. One step per turn is what keeps
   each iteration's context small and every hop resumable and auditable.

3. **Write state before ending the turn.** If the state file does not change,
   the loop made no progress. Three consecutive unchanged iterations stop the
   loop automatically."
  add_kv STUCK_BLOCK "1. Write what is blocking you to \`$RUN_DIR_REL/loop-state.md\` under
   \`## Notes\`, with enough detail that someone can act on it without reading
   the transcript.
2. Say so plainly in your response.
3. Do NOT advance \`current_step\`.

Leaving the step unchanged is the correct signal. The stall guard ends the loop
within three iterations and the state file points at exactly where you stopped."
fi

# Defaults for core-template keys the caller did not supply, so a minimal
# invocation still produces a valid file rather than failing the placeholder
# check on something optional.
add_default() {
  local key="$1" value="$2" i
  for ((i = 0; i < ${#SET_KEYS[@]}; i++)); do
    [[ "${SET_KEYS[$i]}" == "$key" ]] && return 0
  done
  add_kv "$key" "$value"
}

add_default FIRST_STEP     "$(if [[ "$PRESET" == "engineering-delivery" ]]; then printf 'task-start'; else printf 'start'; fi)"
add_default FIRST_ITEM     "(none)"
add_default WORK_SEQUENCE  "(single item)"
add_default GOAL           "See the loop prompt in ${ACTIVE#"$PROJECT_DIR"/}."
add_default DONE_CRITERIA  "$(if [[ -n "$COMPLETION_PROMISE" ]]; then printf 'The conditions under which <promise>%s</promise> may be emitted.' "$COMPLETION_PROMISE"; else printf 'Runs until the iteration limit.'; fi)"
add_default PRESET_CONTEXT "(none)"

CORE="$(read_file "$ASSETS/loop.core.template.md")"
STATE_TPL="$(read_file "$ASSETS/loop-state.core.template.md")"
CONTEXT_TPL="$(read_file "$ASSETS/context.core.template.md")"

# The core template carries the guardrails; the preset supplies the steps.
# Resolve the preset body fully before registering it, so the arrays never go
# out of sync mid-substitution.
PRESET_BODY_RESOLVED="$(substitute "$PRESET_BODY")"
add_kv PRESET_BODY "$PRESET_BODY_RESOLVED"

LOOP_BODY="$(substitute "$CORE")"
STATE_BODY="$(substitute "$STATE_TPL")"
CONTEXT_BODY="$(substitute "$CONTEXT_TPL")"

assert_no_placeholders "$LOOP_BODY" "active.md"
assert_no_placeholders "$STATE_BODY" "loop-state.md"
assert_no_placeholders "$CONTEXT_BODY" "context.md"

# Frontmatter is assembled here, never by a template, so its shape is fixed and
# always machine-valid.
FRONTMATTER="$(
  printf -- '---\n'
  printf 'iteration: 1\n'
  printf 'max_iterations: %s\n' "$MAX_ITERATIONS"
  printf 'completion_promise: %s\n' "$PROMISE_YAML"
  printf 'state_file: %s\n' "$STATE_FILE_YAML"
  [[ -n "$SESSION_ID" ]] && printf 'session_id: %s\n' "$SESSION_ID"
  printf 'preset: %s\n' "$PRESET"
  printf 'run_id: %s\n' "$RUN_ID"
  printf 'seeded_at: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf -- '---\n'
)"

ACTIVE_CONTENT="$FRONTMATTER
$LOOP_BODY"

# --- write ------------------------------------------------------------------

if [[ $DRY_RUN -eq 1 ]]; then
  printf '=== would write %s ===\n' "$ACTIVE"
  printf '%s\n' "$ACTIVE_CONTENT"
  if [[ "$PRESET" != "ad-hoc" ]]; then
    printf '\n=== would write %s/loop-state.md ===\n' "$RUN_DIR"
    printf '%s\n' "$STATE_BODY"
    printf '\n=== would write %s/context.md ===\n' "$RUN_DIR"
    printf '%s\n' "$CONTEXT_BODY"
  fi
  exit 0
fi

mkdir -p "$BASE" || die "could not create $BASE"
printf '%s\n' "$ACTIVE_CONTENT" > "$ACTIVE" || die "could not write $ACTIVE"

if [[ "$PRESET" != "ad-hoc" ]]; then
  mkdir -p "$RUN_DIR" || die "could not create $RUN_DIR"
  printf '%s\n' "$STATE_BODY" > "$RUN_DIR/loop-state.md" || die "could not write loop-state.md"
  printf '%s\n' "$CONTEXT_BODY" > "$RUN_DIR/context.md" || die "could not write context.md"
fi

# Keep loop state out of version control. .claude/ and .cursor/ are usually
# already ignored, so only add an entry when they are not.
GITIGNORE="$PROJECT_DIR/.gitignore"
IGNORE_ENTRY=".${AGENT}/loop/"
if [[ -d "$PROJECT_DIR/.git" ]]; then
  if ! git -C "$PROJECT_DIR" check-ignore -q "$BASE" 2>/dev/null; then
    if ! grep -qxF "$IGNORE_ENTRY" "$GITIGNORE" 2>/dev/null; then
      if grep -qxF '# Ralph loop state' "$GITIGNORE" 2>/dev/null; then
        printf '%s\n' "$IGNORE_ENTRY" >> "$GITIGNORE"
      else
        printf '\n# Ralph loop state\n%s\n' "$IGNORE_ENTRY" >> "$GITIGNORE"
      fi
      printf 'seed-ralph-loop: added %s to .gitignore\n' "$IGNORE_ENTRY" >&2
    fi
  fi
fi

# --- report -----------------------------------------------------------------

cat <<EOF
Ralph loop seeded.

  agent:      $AGENT
  preset:     $PRESET
  run:        $RUN_ID
  active:     ${ACTIVE#"$PROJECT_DIR"/}
  state:      $STATE_FILE_YAML
  iterations: $(if [[ "$MAX_ITERATIONS" == "0" ]]; then echo "unlimited (hard ceiling 200)"; else echo "$MAX_ITERATIONS"; fi)
  promise:    $PROMISE_TEXT

The loop is seeded but NOT running. Start it with: /ralph-loop:ralph-loop start
EOF

exit 0
