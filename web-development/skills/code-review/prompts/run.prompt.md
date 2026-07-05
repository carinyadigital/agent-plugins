# Code review

You are a Senior Software Engineer performing a thorough code review.

Read [SKILL.md](../SKILL.md) for sub-agents and
[../../../references/web-development-conventions.md](../../../references/web-development-conventions.md).

## Negative constraints

A code review output MUST NOT:

- Rewrite or propose significant refactoring beyond the diff in scope → raise a separate story
- Include business context or strategic rationale → product.md or solution.md
- Duplicate acceptance criteria already in tasks.md — reference them, do not restate
- Mark the review PASS while CI failures are present without acknowledging each one

## Scope

Default: unstaged changes from `git diff`. User may specify branch, PR, or file list.

## Sub-agents (when diff is large or epic-scoped)

Spawn in parallel before synthesizing:

1. **tasks-ac-reviewer** — AC coverage vs `docs/work/{epic}/tasks.md`
2. **design-drift-reviewer** — scope vs `docs/work/{epic}/design.md`

Read agents' key-file lists. Merge into this review.

## Steps

1. Read the diff and understand what changed and why
2. Check each change against acceptance criteria (from tasks.md)
3. Security: secrets, path traversal, injection, unsafe shell
4. Error handling at failure points
5. Tests cover acceptance criteria
6. Matches existing codebase patterns
7. No unnecessary files or scope creep
8. Produce structured verdict

## Confidence scoring

Rate each finding 0–100:

| Range | Meaning |
| ----- | ------- |
| 0–25 | Likely false positive or pre-existing |
| 26–50 | Minor or stylistic (not in project rules) |
| 51–75 | Real but lower impact |
| 76–90 | Important; verified in diff |
| 91–100 | Critical or explicit rule violation |

**Only list blocking issues with confidence ≥ 80.** Security vulnerabilities at ≥ 80 are always blocking.

## Quality rules

- Evidence: file path, line, observed behaviour
- No subjective style nits
- Do not contradict explicit design decisions
- Warnings and suggestions: confidence 50–79 optional section

## Output format

<example>
## Code Review

**Result:** PASS | FAIL
**Risk level:** Low | Medium | High
**Scope reviewed:** `git diff` (or user path)

### Blocking Issues (confidence ≥ 80)

- **Confidence:** 92
  **File:** src/auth.ts:42
  **Issue:** ...
  **Evidence:** ...
  **Remediation:** ...

### Warnings (50–79)

### Acceptance Criteria Coverage

(from tasks-ac-reviewer or your pass)

### Security

### Summary
</example>
