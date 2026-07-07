# Tasks — write mode

Break an **epic** into implementable tasks with Gherkin-first acceptance criteria.

Read [SKILL.md](../SKILL.md) and
[../../../references/delivery-conventions.md](../../../references/delivery-conventions.md).

## Path

Default: `.agency/work/{epic}/tasks.md`. Resolve `{epic}` from the argument or backlog row.

## Arguments

- `--ears` — add EARS to every task (≥2 each); still require Gherkin

## Context

<artifacts>
[Required: .agency/work/{epic}/design.md OR user spec
Recommended: .agency/backlog.md (epic row), .agency/architecture/solution.md]
</artifacts>

## Acceptance workflow

1. Gherkin first — ≥1 scenario per task; two when happy path + edge matter
2. If `--ears` — add EARS not redundant with Gherkin
3. Else — EARS only when rules are clearer than scenarios alone; omit section if unused

## Steps

1. Read design.md (or spec), epic in backlog.md, solution.md
2. Draft using [assets/tasks.template.md](../assets/tasks.template.md)
3. Summary, conventions, tasks with canonical schema, traceability, DoD, handoff

## Pre-save validation

- [ ] `{epic}` slug resolved correctly (ID → backlog row, not folder named `CHK01`)
- [ ] Every task has ≥1 Gherkin scenario with observable `Then` clauses
- [ ] No new epics, no architecture narrative, no full design copy-paste
- [ ] Task IDs match epic prefix from backlog conventions
- [ ] Depends-on references valid task IDs only

## Output

Example: [examples/checkout-foundation.md](../examples/checkout-foundation.md).

**Handoff:** suggest **implement** per task when design and tasks are approved.
