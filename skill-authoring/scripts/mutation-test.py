#!/usr/bin/env python3
"""Mutation testing for the Ralph loop hooks.

A green test suite proves nothing unless it fails when the code is wrong.
This driver reintroduces each defect found in the July 2026 review, one at a
time, and asserts that ``scripts/test-ralph-hooks.sh`` goes red.

A SURVIVING mutant means the suite has a blind spot at exactly the place a
real bug once lived. Surviving mutants fail this run.

    ./scripts/mutation-test.py
    ./scripts/mutation-test.py -k frontmatter    # run a subset
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RALPH_ROOT = REPO_ROOT / "ralph-loop"
LIB = RALPH_ROOT / "hooks/lib/ralph-common.sh"
CLAUDE_HOOK = RALPH_ROOT / "hooks/claude/stop-hook.sh"
CURSOR_HOOK = RALPH_ROOT / "hooks/cursor/ralph-stop.sh"
SUITE = RALPH_ROOT / "scripts/test-ralph-hooks.sh"

TRACKED = (LIB, CLAUDE_HOOK, CURSOR_HOOK)

# Mutants that provably do not change behaviour, so a test cannot kill them.
# Listing one here is a claim that must be backed by evidence, not a way to
# silence an inconvenient result.
#
# The three errexit mutants were checked by differential execution: both
# variants were run across eight scenarios (no loop, max reached, corrupt
# frontmatter, stalled, done sentinel, normal continue, missing frontmatter,
# empty body) and produced byte-identical stdout, stderr and exit codes.
#
# `set -e` is inert here because the hardening removed every unguarded
# pipeline and every library function returns 0 on its success path. The
# sources still use `set -uo pipefail` rather than `set -euo pipefail`,
# because errexit would silently become load-bearing again the moment
# somebody adds a pipeline without a guard, which is precisely how the
# original defect arose.
EXPECTED_EQUIVALENT = {
    "errexit: set -e reintroduced in library",
    "errexit: set -e reintroduced in claude hook",
    "errexit: set -e reintroduced in cursor hook",
}


# Each mutant is (name, target, old, new). `old` must appear verbatim in the
# target file, which keeps the mutations honest: if the code is refactored and
# an anchor disappears, the mutant errors loudly instead of silently passing.
MUTANTS: list[tuple[str, Path, str, str]] = [
    # --- Defect 4: frontmatter scope -------------------------------------
    (
        "frontmatter: sed range parser (original)",
        LIB,
        """  awk '
    NR == 1 && /^---[[:space:]]*$/ { inblock = 1; next }
    inblock && /^---[[:space:]]*$/ { exit }
    inblock { print }
  ' "$file" 2>/dev/null""",
        """  sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$file" 2>/dev/null""",
    ),
    (
        "frontmatter: grep without -m1 (original)",
        LIB,
        'grep -m1 "^${key}:" 2>/dev/null',
        'grep "^${key}:" 2>/dev/null',
    ),
    (
        "frontmatter: quote stripping removed",
        LIB,
        '      value="${value:1:${#value}-2}"',
        "      value=\"$value\"",
    ),
    # --- Defect 3: transcript parsing ------------------------------------
    (
        "transcript: tail -1 instead of tail -N (original)",
        LIB,
        'raw="$(tail -n "$RALPH_TRANSCRIPT_WINDOW" "$transcript" 2>/dev/null)" || raw=""',
        'raw="$(tail -n 1 "$transcript" 2>/dev/null)" || raw=""',
    ),
    (
        "transcript: first text block instead of last",
        LIB,
        "| last // \"\"",
        "| first // \"\"",
    ),
    # --- P0-2: promise mention treated as fulfilment ----------------------
    (
        "promise: bare substring match instead of anchored to the final line",
        LIB,
        '/\\A(.*?)(?:^|\\n)[ \\t]*<promise>(.*?)<\\/promise>[ \\t]*\\n*\\z/s',
        '/(.*?)<promise>(.*?)<\\/promise>/s',
    ),
    # --- P0-3: no turn boundary, stale promise reaches a fresh iteration --
    (
        "transcript: turn boundary never found (always scans the whole window)",
        LIB,
        "range(0; ($all | length))",
        "range(0; 0)",
    ),
    # --- P0-2 fix-up: unclosed fenced quote bypassed the final-line anchor --
    (
        "promise: fence-parity check removed (unclosed fence bypasses anchor)",
        LIB,
        "      if ($fences % 2 == 0) {",
        "      if (1) {",
    ),
    # --- P0-3 fix-up: bare-string user content not recognised as a boundary
    (
        "transcript: string-shaped user content ignored as a turn boundary",
        LIB,
        '(($all[.].message.content | type) == "string"\n                       and ($all[.].message.content | length) > 0)\n                     or ',
        "",
    ),
    # --- Iteration bookkeeping -------------------------------------------
    (
        "bump: global sed rewrite (original)",
        LIB,
        """  # NOTE: the awk variable must not be called `next`, which is an awk keyword.
  awk -v newiter="$next" '
    NR == 1 && /^---[[:space:]]*$/ { inblock = 1; print; next }
    inblock && /^---[[:space:]]*$/ { inblock = 0; print; next }
    inblock && /^iteration:[[:space:]]/ { print "iteration: " newiter; next }
    { print }
  ' "$loop_file" > "$tmp" 2>/dev/null""",
        """  sed "s/^iteration: .*/iteration: $next/" "$loop_file" > "$tmp" 2>/dev/null""",
    ),
    (
        "bump: iteration never incremented",
        LIB,
        "  next=$((iteration + 1))",
        "  next=$iteration",
    ),
    # --- Defect 1: fatal error handling ----------------------------------
    (
        "errexit: set -e reintroduced in library",
        LIB,
        "set -uo pipefail",
        "set -euo pipefail",
    ),
    (
        "errexit: set -e reintroduced in claude hook",
        CLAUDE_HOOK,
        "set -uo pipefail",
        "set -euo pipefail",
    ),
    (
        "errexit: set -e reintroduced in cursor hook",
        CURSOR_HOOK,
        "set -uo pipefail",
        "set -euo pipefail",
    ),
    # --- Guardrails -------------------------------------------------------
    (
        "limits: max_iterations check removed",
        LIB,
        "  if [[ $max_iter -gt 0 ]] && [[ $iteration -ge $max_iter ]]; then",
        "  if false; then",
    ),
    (
        "limits: off-by-one on max_iterations",
        LIB,
        "  if [[ $max_iter -gt 0 ]] && [[ $iteration -ge $max_iter ]]; then",
        "  if [[ $max_iter -gt 0 ]] && [[ $iteration -gt $max_iter ]]; then",
    ),
    (
        "limits: hard ceiling removed",
        LIB,
        "  if [[ $iteration -ge $RALPH_HARD_CEILING ]]; then",
        "  if false; then",
    ),
    (
        "stall: guard disabled",
        LIB,
        "  [[ $count -ge $RALPH_STALL_LIMIT ]]",
        "  false",
    ),
    (
        "stall: counter never resets on change",
        LIB,
        """  else
    count=1
  fi""",
        """  else
    count=$((prev_count + 1))
  fi""",
    ),
    (
        "session: isolation check removed",
        LIB,
        '  if [[ -n "$session_id" && -n "${RALPH_SESSION_ID:-}" && "$session_id" != "${RALPH_SESSION_ID}" ]]; then',
        "  if false; then",
    ),
    # --- Promise handling -------------------------------------------------
    (
        "promise: glob comparison instead of literal",
        LIB,
        '  [[ -n "$found" && "$found" = "$expected" ]]',
        '  [[ -n "$found" && "$found" == $expected ]]',
    ),
    (
        "promise: sentinel ignored",
        LIB,
        '  if [[ -f "$base/done" ]]; then',
        "  if false; then",
    ),
    (
        "promise: null treated as a real promise",
        LIB,
        '  [[ -n "$v" && "$v" != "null" && "$v" != "~" ]]',
        '  [[ -n "$v" ]]',
    ),
    (
        "promise: whitespace not normalised",
        LIB,
        "      $p =~ s/\\s+/ /g;",
        "      ;",
    ),
    # --- Body extraction ---------------------------------------------------
    (
        "body: original awk drops --- separators",
        LIB,
        """  awk '
    NR == 1 && /^---[[:space:]]*$/ { inblock = 1; next }
    inblock && !closed && /^---[[:space:]]*$/ { closed = 1; next }
    closed { print }
  ' "$file" 2>/dev/null""",
        """  awk '/^---$/{i++; next} i>=2' "$file" 2>/dev/null""",
    ),
    (
        "body: empty-prompt check removed",
        LIB,
        '  if [[ -z "${RALPH_PROMPT//[[:space:]]/}" ]]; then',
        "  if false; then",
    ),
    # --- Agent separation --------------------------------------------------
    (
        "agent: cursor and claude share one base dir",
        LIB,
        "    cursor) printf '%s/.cursor/loop' \"$project\" ;;",
        "    cursor) printf '%s/.claude/loop' \"$project\" ;;",
    ),
    (
        "cursor: aborted turns are re-fed",
        CURSOR_HOOK,
        'if [[ "$STATUS" == "aborted" || "$STATUS" == "error" ]]; then',
        "if false; then",
    ),
    # --- Validation --------------------------------------------------------
    (
        "validation: numeric check always passes",
        LIB,
        '  [[ "${1:-}" =~ ^[0-9]+$ ]]',
        "  true",
    ),
]


# Backups live inside the repo, not in a temp dir, so a hard kill (which
# bypasses even a finally block) leaves a recoverable state. An interrupted
# run once left the library mutated and the test suite mysteriously red.
BACKUP = RALPH_ROOT / ".mutation-backup"


STATE = BACKUP / "state"


def snapshot(_tmp: Path | None = None) -> None:
    BACKUP.mkdir(exist_ok=True)
    for path in TRACKED:
        shutil.copy2(path, BACKUP / path.name)
    # Marker state is recorded by content rather than by file existence: some
    # sandboxed and network filesystems refuse unlink, and a restore that
    # cannot clear its own marker would wedge every later run.
    STATE.write_text("dirty\n")


def restore(_tmp: Path | None = None) -> None:
    if not BACKUP.is_dir():
        return
    for path in TRACKED:
        backup = BACKUP / path.name
        if backup.is_file():
            shutil.copy2(backup, path)
    STATE.write_text("clean\n")


def check_dirty() -> bool:
    """True when a previous run died mid-mutation."""
    if not STATE.is_file():
        return False
    return STATE.read_text().strip() == "dirty"


def syntax_ok() -> bool:
    for path in TRACKED:
        if subprocess.run(
            ["bash", "-n", str(path)], capture_output=True
        ).returncode != 0:
            return False
    return True


def run_suite() -> int:
    """Return the number of failed assertions, or -1 if the suite errored."""
    proc = subprocess.run(
        ["bash", str(SUITE)], capture_output=True, text=True, cwd=RALPH_ROOT
    )
    match = re.search(r"^failed:\s*(\d+)$", proc.stdout, re.MULTILINE)
    if not match:
        return -1
    return int(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest="filter", default="", help="substring filter")
    parser.add_argument(
        "--restore",
        action="store_true",
        help="recover source files after an interrupted run, then exit",
    )
    parser.add_argument(
        "--skip-baseline",
        action="store_true",
        help="skip the pre-flight green check (use when chunking a run)",
    )
    parser.add_argument(
        "--slice",
        default="",
        metavar="START:END",
        help="run mutants by index, e.g. 0:5",
    )
    parser.add_argument(
        "--list", action="store_true", help="list mutants with indices, then exit"
    )
    args = parser.parse_args()

    if args.list:
        for i, (name, target, _, _) in enumerate(MUTANTS):
            print(f"{i:3d}  {target.name:20s}  {name}")
        return 0

    if args.restore:
        restore()
        print("restored hook sources from .mutation-backup/")
        return 0

    if check_dirty():
        print("A previous mutation run was interrupted and left sources mutated.")
        print("Recover with: ./scripts/mutation-test.py --restore")
        return 1

    selected = [m for m in MUTANTS if args.filter in m[0]]
    if args.slice:
        start_s, _, end_s = args.slice.partition(":")
        start = int(start_s) if start_s else 0
        end = int(end_s) if end_s else len(selected)
        selected = selected[start:end]
    if not selected:
        print(f"no mutants match {args.filter!r}")
        return 1

    print("Ralph mutation testing")
    print("======================\n")

    tmp = Path(tempfile.mkdtemp())
    snapshot(tmp)

    killed: list[str] = []
    survived: list[str] = []
    errored: list[str] = []
    equivalent: list[str] = []

    try:
        # Sanity: the unmutated suite must be green, otherwise every result
        # below is meaningless.
        if not args.skip_baseline:
            baseline = run_suite()
            if baseline != 0:
                print(f"BASELINE IS RED ({baseline} failures). Fix the suite first.")
                return 1
            print(f"baseline: green ({len(selected)} mutants queued)\n")
        else:
            print(f"baseline: skipped ({len(selected)} mutants queued)\n")

        for name, target, old, new in selected:
            restore(tmp)
            source = target.read_text()

            if old not in source:
                print(f"  ERROR    {name}")
                print(f"           anchor not found in {target.name}")
                errored.append(name)
                continue

            target.write_text(source.replace(old, new, 1))

            if not syntax_ok():
                print(f"  killed   {name} (syntax error)")
                killed.append(name)
                continue

            failures = run_suite()
            if failures == -1:
                print(f"  killed   {name} (suite crashed)")
                killed.append(name)
            elif failures > 0:
                print(f"  killed   {name} ({failures} assertions)")
                killed.append(name)
            elif name in EXPECTED_EQUIVALENT:
                print(f"  survived {name} (expected: equivalent mutation)")
                equivalent.append(name)
            else:
                print(f"  SURVIVED {name}  <-- blind spot")
                survived.append(name)
    finally:
        restore(tmp)
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n======================")
    print(f"killed:   {len(killed)}")
    print(f"survived: {len(survived)}")
    print(f"errored:  {len(errored)}")
    if equivalent:
        print(f"equivalent: {len(equivalent)} (expected, see EXPECTED_EQUIVALENT)")

    if survived:
        print("\nsurviving mutants (test-suite blind spots):")
        for name in survived:
            print(f"  - {name}")
    if errored:
        print("\nmutants whose anchor no longer exists (update mutation-test.py):")
        for name in errored:
            print(f"  - {name}")

    if survived or errored:
        return 1

    print("\nall mutants killed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
