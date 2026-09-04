# Artefact consistency

Cross-artefact checks. Authoritative homes are in
[delivery-conventions.md](../../../references/delivery-conventions.md)
§ Artefact boundaries — judge against those, not against a reconstructed ideal.

## Boundaries

Each fact has one home. A second copy is a finding unless it **cites** the
home.

| If you see this | Finding | Owner |
| --------------- | ------- | ----- |
| `design.md` re-narrates module layout, NFRs, or cross-epic patterns | Boundary — cite `solution.md §{N.M}` | `design` |
| Gherkin scenarios in `design.md` | Boundary — AC live in `TASKS.local.md` or the tracker | `design` / `/product-management:tasks` |
| Business rationale or personas in the Solution Design | Boundary — `docs/product/product.md` | `design` |
| Phase sequencing in the Solution Design or backlog | Boundary — `docs/product/roadmap.md` | `design` / `/product-management:tasks` |
| Architecture decisions only in `design.md`, never triaged | Suggestion — `/architecture:adr plan` after ship; blocking only if implement cannot start without the decision | `adr` |

A story or bug Solution Design that copies its parent epic's `design.md` instead of citing
the parent by ID is a boundary finding.

## Contradictions

Same question, different answers — always blocking until you know which
artefact wins.

| Clash | Authoritative |
| ----- | ------------- |
| Architecture pattern (modules, NFRs, cross-epic) | `solution.md`, then ADRs |
| What this work item ships | `design.md` slice / files / out-of-scope |
| Story and task AC, dependency order | `TASKS.local.md` or the tracker |
| Why we are building it | `product.md` |
| When / phase exit | `roadmap.md` |

State which is right and how you know. "These disagree" is half a finding.
If you cannot establish it, say so — still blocking, owner is the skill that
writes the non-authoritative copy.

Legitimate restatement: a one-line pointer ("see `solution.md §3.2`") is not
duplication. Flag only when the Solution Design restates enough that the two can drift.

## Citations

- [ ] `design.md` cites `solution.md` by section where it relies on architecture.
- [ ] A story/bug/spike Solution Design cites its parent epic by ID.
- [ ] Tasks map to the Solution Design slice — no story that is in-scope in tasks and
      out-of-scope in the Solution Design, or the reverse, without an explicit note.
- [ ] Named ADRs exist at the cited path.

## Inventory honesty

State what you included and what was absent. A review that silently skipped
`TASKS.local.md` because the tracker had titles only must say that AC were
not found, not that they passed.
