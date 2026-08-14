---
name: debug
description: >
  Investigate bugs, errors, or unexpected behaviour — reproduce, isolate,
  diagnose, and fix. Use when given an error message, stack trace, "works in
  staging but not prod", or "broke after deploy". Do NOT use for incident
  response workflows, code review (code-review), or implementation (implement).
license: Apache-2.0
allowed-tools: Read Write Glob Grep Bash
argument-hint: "<error message or problem description>"
metadata:
  author: Carinya Parc
  version: "0.1.1"
  owner: engineering
  review_cadence: as-needed
  work_shape: implement-and-ship
  output_class: applied-change
---

# Debug

Structured debugging — reproduce, isolate, diagnose, and fix. Pass the error
message, stack trace, or problem description after the skill name.

See [CONNECTORS.md](../../CONNECTORS.md) for monitoring and source-control tools.

## Steps

1. **Reproduce** — expected vs actual; exact steps; scope (when started, who affected)
2. **Isolate** — narrow component/service/path; check recent deploys, config,
   dependencies; review logs and exact error text
3. **Diagnose** — form hypotheses and test them; trace the code path; find root
   cause (not just symptoms)
4. **Fix** — propose a fix with explanation; consider side effects and edge cases;
   suggest regression tests. Comments in the fix MUST follow
   [doc-comments.md](../../references/doc-comments.md): they MUST stand on their
   own so they can be read inline, and MUST NOT cite issue systems, working
   documents, or any other external source.

## What to gather

- Exact error message or stack trace (do not paraphrase)
- Steps to reproduce; expected vs actual; scope
- What changed recently (deploys, deps, config)
- Logs or screenshots

If monitoring is connected: pull logs, error rates, and metrics around the issue
time; correlate with recent deploys. If source control is connected: identify
commits/PRs on affected paths. If project tracker is connected: search related
bugs; create a ticket for the fix once identified.

## Constraints

A fix MUST NOT add comments that cite issue systems, working documents, or any
other external source. Comments MUST stand on their own so they can be read
inline. See [doc-comments.md](../../references/doc-comments.md).

## Output format

```markdown
## Debug Report: [Issue Summary]

### Reproduction
- **Expected**: …
- **Actual**: …
- **Steps**: …

### Root Cause
…

### Fix
…

### Prevention
- [Test to add]
- [Guard to put in place]
```
