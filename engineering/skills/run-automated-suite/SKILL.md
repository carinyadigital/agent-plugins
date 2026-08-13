---
name: run-automated-suite
description: >
  Run the project's automated test suite in a prepared QA workspace. Use after
  deploy-qa when executing CI-equivalent tests. Do NOT use for workspace setup
  (deploy-qa), manual AC checks (exploratory-pass), or fixing failures
  (implement).
license: MIT
allowed-tools: Read Bash Glob Grep
argument-hint: "[test-command override]"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: engineering
  review_cadence: as-needed
  work_shape: review-and-gate
  output_class: decision-support
---

# Run automated suite

Execute the project's automated test command from the QA workspace root
(delivery-qa crew automated suite step). Optionally pass a test command override
after the skill name.

## Steps

1. Read acceptance criteria from `specs/{work-short-name}/TASKS.local.md` if available —
   context for interpreting failures.
2. From the workspace root, run the test command — read from `package.json`
   (typically `pnpm test`, `npm test`, or project-specific script). Use the
   override if the user provided one.
3. Capture stdout/stderr. Distinguish:
   - **Product failure** — tests ran but assertions failed
   - **Infrastructure failure** — runner crashed, OOM, missing binary, timeout
     before tests executed
4. For product failures, note failing test names and error messages.

## Constraints

- Do not skip the full suite or substitute a narrower subset without documenting why
- Do not modify source code; do not merge, approve, or push

## Output format

```markdown
## Automated suite — {branch or epic}

**Verdict:** pass | fail (product) | fail (infra)

**Command:** `…`

**Summary:** …

### Failures (if any)

| Test | Error |
| ---- | ----- |
| … | … |
```
