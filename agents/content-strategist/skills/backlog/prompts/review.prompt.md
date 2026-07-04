# Backlog — review mode

Critical review of the **product backlog** for planning readiness.

Read [SKILL.md](../SKILL.md) and
[references/delivery-conventions.md](../references/delivery-conventions.md).

## Path

Default: `docs/product/backlog.md`. User-named paths override.

For Gherkin and sprint feasibility, use **tasks review** on `docs/work/{epic}/tasks.md`.

## Context

<artifacts>
[Required: backlog.md
Recommended: product.md, roadmap.md, solution.md
Optional: sprint retrospective notes]
</artifacts>

## Steps

1. Read backlog.md and context
2. Check alignment with product.md §4–§5 and roadmap current phase
3. Verify each epic has a valid `docs/work/{epic}/` path (title or short title slug, max two words)
4. Apply epic criteria; amend unambiguous fixes; report verdict

## Review checklist

- [ ] Now-phase epics trace to product.md §7 outcomes
- [ ] No contradiction with product §5 or roadmap deferred items
- [ ] Epic granularity: one integration boundary / phase objective per epic
- [ ] Work paths unique; slugs match title/short title (not Epic ID)
- [ ] No full Gherkin in product backlog
- [ ] Dependencies and estimates sound

## Verdict

**Planning-ready**, **Acceptable with amendments**, or **Not ready**.

## Output

Amend backlog.md for non-blocking fixes. Report verdict, findings, remaining risks.
