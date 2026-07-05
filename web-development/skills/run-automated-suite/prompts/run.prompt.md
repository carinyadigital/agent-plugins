# Run automated suite

Execute the project's automated test command and report pass/fail.

## Steps

1. Read acceptance criteria from `docs/work/{epic}/tasks.md` if available —
   context for interpreting failures.
2. From the workspace root, run the test command — read from `package.json`
   (typically `pnpm test`, `npm test`, or project-specific script). Use the
   override if the user provided one.
3. Capture stdout/stderr. Distinguish:
   - **Product failure** — tests ran but assertions failed
   - **Infrastructure failure** — runner crashed, OOM, missing binary, timeout
     before tests executed
4. For product failures, note failing test names and error messages.

## Output

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

## Constraints

- Do not skip the full suite or substitute a narrower subset without
  documenting why.
- Do not modify source code.
- Do not merge, approve, or push.
