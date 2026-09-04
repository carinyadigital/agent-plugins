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
  - ARCHITECTURE.md
---

<!--
DRAFTING AIDE — DELETE BEFORE SAVING.
Filesystem-only fallback — see references/work-item-resolution.md. When
Linear or Jira resolves, this artefact is not used; the tracker holds the
epic list and skills read it directly.
§3 epic breakdown table; §4 epic detail for Now-phase epics.
Epic work path: specs/{work-short-name}/ — kebab-case from title, max two words; fall back to {work-id} when a short name cannot be discovered.
-->

# Backlog -- {Name}

- **Product:** [`docs/product/product.md`](../product/product.md)
- **Solution:** [`ARCHITECTURE.md`](../../ARCHITECTURE.md)
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
| Epic work path | `specs/{work-short-name}/` (title or short title slug, max two words, when work-id is internal) |
| Task ID | `{PREFIX}{nn}-{nn}` in `specs/{work-short-name}/TASKS.local.md` |
| Status | To do, In progress, In review, Blocked, Done |
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

**Status.** **Work path:** `specs/{work-short-name}/`

## 5. Dependency graph

```text
{PREFIX}01
  +-- {PREFIX}02
```

## 6. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
| -- | ---- | ---------- | ------ | ---------- |

Technical risks: see `ARCHITECTURE.md` §11.
