---
type: Backlog
level: epic
version: '0.1'
owner: <!-- squad -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - docs/product/product.md
  - docs/product/roadmap.md
  - docs/architecture/solution.md
---

<!--
DRAFTING AIDE — DELETE BEFORE SAVING.
Filesystem-only fallback — see references/work-item-resolution.md. When
Linear or Jira resolves, this artefact is not used; the tracker holds the
epic list and skills read it directly.
§3 epic breakdown table; §4 epic detail for Now-phase epics.
Epic work path: docs/work/{work-id}/ — slug from title or short title, max two words, kebab-case (the work-id IS the slug in this fallback; a tracker key would be used verbatim instead).
-->

# Backlog -- {Name}

- **Product:** [`docs/product/product.md`](../product/product.md)
- **Solution:** [`docs/architecture/solution.md`](../architecture/solution.md)
- **Roadmap:** [`docs/product/roadmap.md`](../product/roadmap.md)

## 1. Summary

**Objective.**

**Delivery approach.**

**Prerequisites (complete).**

**Prerequisites (required).**

**Out of scope.** See `product.md` §5 and `roadmap.md` deferred section.

## 2. Conventions

| Convention | Value |
| ---------- | ----- |
| Epic ID | `{PREFIX}{nn}` (internal — filesystem-only fallback; a tracker key is used verbatim when one resolves) |
| Epic work path | `docs/work/{work-id}/` (title or short title slug, max two words, when work-id is internal) |
| Task ID | `{PREFIX}{nn}-{nn}` in `docs/work/{work-id}/tasks.md` |
| Status | Not started, In progress, In review, Done, Blocked |
| Priority | P0–P3 |
| Estimation | Fibonacci story points |

## 3. Epic breakdown

| Epic ID | Title | Phase | Priority | Deps | Points | Work path | Status |
| ------- | ----- | ----- | -------- | ---- | ------ | --------- | ------ |

## 4. Epic detail (Now phase)

### {PREFIX}01 -- {Title}

**Scope.**

**Key deliverables.**

**Dependencies.**

**Status.** **Work path:** `docs/work/{work-id}/`

## 5. Dependency graph

```text
{PREFIX}01
  +-- {PREFIX}02
```

## 6. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
| -- | ---- | ---------- | ------ | ---------- |

Technical risks: see `solution.md` §10.1.
