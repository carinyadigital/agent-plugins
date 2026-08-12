# Worked example: the smallest command that still passes validation

Every section from the enforcement table still has to be present, but each can be a
single line when the command itself is simple. If you were adding this, it would live
at `commands/check-status.md`.

```markdown
---
description: Report whether the local environment is ready to run this project.
---

Check whether the local environment is ready and report what's missing.

## Preflight

Confirm this is being run from the project root (a marker file like `package.json` or
`pyproject.toml` is present); if not, say so and stop.

## Plan

Check each required tool/config in turn and report pass/fail for each — no changes are
made, so no destructive-operation confirmation is needed here.

## Commands

1. Check each required CLI is on `PATH`.
2. Check each required environment variable is set (report which are missing by name
   only, never their values).
3. Check any required local service (e.g. a database) is reachable.

## Verification

Re-confirm each check's result before reporting it — don't report a tool as present
just because it was present the last time this command ran in this session.

## Summary

## Result
- **Action**: check-status
- **Status**: ready | not ready
- **Details**: which checks passed/failed

## Next Steps

- If anything failed, name the exact command to fix it (install the missing CLI, set
  the missing variable) rather than leaving the user to figure it out.
```

Compare with [`command-example.md`](command-example.md) — that one has
a destructive step (key revocation) and needs the `⚠`/"explicit" confirmation language
this one doesn't, precisely because this command never changes anything. Six
sections are required either way; how much each section says scales with what the
command actually does.
