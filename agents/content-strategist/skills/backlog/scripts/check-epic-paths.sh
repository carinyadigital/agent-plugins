#!/usr/bin/env bash
# Validate docs/work/{epic}/ paths in a backlog markdown file.
# Usage: check-epic-paths.sh [path-to-backlog.md]
# Exit 0 if all paths pass; 1 if any fail.

set -euo pipefail

BACKLOG="${1:-docs/product/backlog.md}"

if [[ ! -f "$BACKLOG" ]]; then
  echo "skip: $BACKLOG not found"
  exit 0
fi

fail=0

check_slug() {
  local slug="$1"
  local line="$2"
  if [[ "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)?$ ]]; then
    return 0
  fi
  echo "FAIL line ~$line: slug '$slug' must be kebab-case with at most one hyphen (two words)"
  fail=1
}

# Match docs/work/slug/ in table cells
while IFS= read -r line; do
  if [[ "$line" =~ docs/work/([a-z0-9-]+)/ ]]; then
    slug="${BASH_REMATCH[1]}"
    # Count words (split on hyphen)
    IFS='-' read -ra parts <<< "$slug"
    if ((${#parts[@]} > 2)); then
      echo "FAIL: '$slug' has more than two words (${#parts[@]} parts)"
      fail=1
    fi
    check_slug "$slug" "$line"
    # Epic ID used as folder name
    if [[ "$slug" =~ ^[A-Z]{2,}[0-9]+$ ]]; then
      echo "FAIL: '$slug' looks like an Epic ID, not a title slug"
      fail=1
    fi
  fi
done < <(grep -n 'docs/work/[a-z0-9-]*/' "$BACKLOG" || true)

if [[ $fail -eq 0 ]]; then
  echo "ok: epic work paths in $BACKLOG"
fi
exit "$fail"
