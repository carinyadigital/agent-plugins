---
type: Design
mode: <!-- walking-skeleton | tdd -->
epic: <!-- kebab-case from title or short title, max two words -->
epic_id: <!-- e.g. CHK01 -->
version: '0.1'
owner: <!-- team or squad name -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - <!-- solution.md -->
  - docs/work/{epic}/tasks.md
  - docs/architecture/solution.md
---

<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
DO NOT INCLUDE in this design.md:
  - Architecture-wide patterns already in solution.md
    → cite solution.md §{N.M} instead; do not re-narrate
  - Business rationale                  → product.md
  - Phase sequencing                    → roadmap.md
  - Story-level acceptance criteria     → docs/work/{epic}/tasks.md (tasks skill)

Walking-skeleton mode (2–4 pages): §1 The slice, §2 Files shipped,
  §3 Acceptance gates, §4 What was NOT delivered, §5 Open questions, §6 Handoff.

TDD mode (5–10 pages): §1 Scope, §2 Architecture fit, §3 Files and components,
  §4 Data contracts, §5 Runtime view, §6 Cross-squad coordination (if applicable),
  §7 Error paths, §8 Observability, §9 Testing strategy, §10 Acceptance gates,
  §11 Handoff, §12 Open questions.
-->

# Design -- {Epic Title} ({EPIC-ID})

Design for epic {EPIC-ID} at `docs/work/{epic}/`. Architecture-wide patterns are authoritative in
[`solution.md`](solution.md) and are not repeated here.

## 1. Scope / The slice

<!--
Walking-skeleton: one paragraph naming the end-to-end path this sprint proves
and what does NOT yet work.

TDD: in-scope capabilities, explicit out-of-scope deferrals, and a map from
capabilities to task IDs in tasks.md.
-->

[NEEDS CLARIFICATION]

## 2. Files

<!--
Walking-skeleton: every file with NEW / EVOLVE / KEEP label and a one-line
description. Grouped by layer (data, logic, UI, routes, tests).

TDD: new files, modified files, and files explicitly NOT modified.
Each entry: path + purpose.
-->

```text
{module}/
  {file}.ts    NEW     <!-- what it does -->
  {file}.ts    EVOLVE  <!-- what changes -->
```

## 3. Acceptance gates

<!--
Walking-skeleton: four subsections:
  3.1 End-to-end path (the request/response round-trip succeeds)
  3.2 Observability hook fires (one trace span, one log line)
  3.3 Error path exercised (typed error surface renders)
  3.4 Scaffolds complete and quality gates pass (typecheck, unit tests)

TDD: the subset of solution.md §2.1 quality goals this epic must satisfy,
plus layer-specific acceptance criteria.
-->

[NEEDS CLARIFICATION]

## 4. Data contracts

<!--
TDD mode: TypeScript signatures, Zod schemas, and types introduced by this work
epic. Code fences only — no prose descriptions of shapes.

Walking-skeleton mode: omit or note "No new contracts; schema stable from foundation."
-->

[NEEDS CLARIFICATION]

## 5. What was NOT delivered / Handoff

<!--
Walking-skeleton §4 + §6: explicit list of what this sprint did NOT ship
(so later sprints do not assume it was done), then what the next epic
can safely assume is ready.

TDD §11: what is stable when this epic closes; what comes next.
-->

**Not delivered:**

- <!-- capability deferred to a later epic -->

**Stable on close:**

- <!-- contract / file / interface that is now stable -->

## 6. Open questions

1. **{Question}.** {Context; owner; how it blocks.}
