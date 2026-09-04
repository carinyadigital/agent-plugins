# Readiness gate

What "Ready for Development" means. Apply this after the inventory, for the
resolved work-item **type**. Existence of a file is not completeness.

## Verdict

| Verdict | When |
| ------- | ---- |
| **Ready for Development** | No blocking findings. An implementer can start the first task without guessing slice, files, or done. |
| **Not ready** | One or more blocking findings. Name the owning skill for each. |

Warnings ride along with Ready. They do not fail the gate.

## Required by type

| Type | Must be present and usable |
| ---- | -------------------------- |
| **epic** | `{work-dir}/design.md` (skeleton or full, matching the work's mode); stories with testable AC in `{work-dir}/TASKS.local.md` or the tracker; out-of-scope listed; open questions that change the slice resolved or explicitly deferred with a default the implementer may use |
| **story** | Testable AC on the story; a Solution Design for this story **or** a parent epic Solution Design that this story can cite without inventing design; parent cited by ID |
| **bug** | Repro and expected fix that a third party could test. A Solution Design only if the fix needs design beyond the ticket |
| **spike** | The question to answer and the exit criterion (what artefact or decision comes back). Implementation of product behaviour is out of scope unless the spike says otherwise |

`ARCHITECTURE.md` is required when the work item crosses a module, API, or NFR
boundary already owned by architecture. If `ARCHITECTURE.md` is missing in that
case, that is blocking and the owner is `/architecture:solution`. If the work
item is a local change inside an already-described module, note the citation
and do not fail the gate for an absent system-wide rewrite.

## Completeness checks (all types)

- [ ] No leftover `DRAFTING AIDE` block in `design.md`.
- [ ] No `[NEEDS CLARIFICATION]` that decides files shipped, acceptance gates,
      data contracts, or error paths — those are blocking. Editorial TODOs are
      warnings.
- [ ] Skeleton Solution Design has §1–§6 in substance (slice, files, gates, not-delivered,
      open questions, handoff). Full Solution Design has the full section set in substance.
      Empty headings are blocking.
- [ ] Acceptance criteria are Gherkin (or EARS where a rule is clearer) and
      have a Then a third party could test. "It works" is blocking.
- [ ] First implementable task is identified (dependency order is stated).
- [ ] Tracker-backed work uses the tracker key as canonical ID; no parallel
      invented ID scheme.

## Blocking vs warning

Blocking — `implement` would guess:

- Missing required artefact for this type.
- Untestable or absent AC on a story (or on a foundational task with no parent).
- Open question or `[NEEDS CLARIFICATION]` that changes the slice or the files
  shipped.
- Contradiction between `design.md` and `TASKS.local.md` (or tracker) on what
  ships, or between `design.md` and `ARCHITECTURE.md` on a pattern the Solution Design restates
  wrongly.

Warning — proceed with an explicit assumption:

- Solution Design restates architecture that should be a citation (no factual clash yet).
- Optional ADR not yet harvested.
- Roadmap phase not named, but the slice is otherwise clear.
- Story Solution Design slightly thinner than the epic's, but AC are testable.

Suggestion — defer:

- Prose, naming, extra diagrams.
- Harvesting ADRs after the work ships (`/architecture:adr plan`).
