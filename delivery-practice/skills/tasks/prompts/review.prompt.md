# Tasks — review mode

Review `.agency/work/{epic}/tasks.md` for sprint readiness.

Read [SKILL.md](../SKILL.md) and
[../../references/delivery-conventions.md](../../references/delivery-conventions.md).
Resolve `{epic}` from the argument or backlog.

## Context

[Required: tasks.md. Recommended: design.md, backlog epic row, solution.md]

## Review checklist

- [ ] Every task has ≥1 Gherkin scenario; `Then` clauses are observable
- [ ] Tasks trace to design.md sections; no scope outside epic
- [ ] Sprint feasibility: dependencies acyclic; estimates present
- [ ] No architecture re-write; no new epics
- [ ] EARS only where warranted (or `--ears` was requested on write)

## Verdict

**Sprint-ready**, **Acceptable with amendments**, or **Not ready**.

## Output

Amend tasks.md for non-blocking fixes; report findings.
