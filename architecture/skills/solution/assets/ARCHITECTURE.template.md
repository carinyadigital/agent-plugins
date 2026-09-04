---
type: Architecture
state: current
version: '0.1'
owner: <!-- team or squad name -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - docs/product/product.md
  - docs/architecture/decisions/register.md
---

<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.

arc42 drawers (keep these names). Do not add an Architecture Decisions
section — that is docs/architecture/decisions/ via /architecture:adr.

DO NOT INCLUDE in ARCHITECTURE.md:
  - ADR bodies or a decision log              → docs/architecture/decisions/
  - Commercial rationale or business case     → product.md
  - Target customer segments or personas      → product.md
  - Strategic thesis or product principles    → product.md
  - Positioning or messaging                  → product.md
  - User quotes                               → product.md
  - Story-level acceptance criteria           → specs/{work-short-name}/TASKS.local.md
  - Phase sequencing or epic ordering         → roadmap.md
  - Per-work-item APIs and file lists         → {work-dir}/design.md

state: current = as-is (code is source of truth).
state: target  = to-be (intended; project start or explicit evolution).

After every filled section, list **Source files:** (existing or planned).
current: omit a section only if it truly does not apply.
target: fill §1–§8 from intent; §10–§12 from what is known.
Never leave [NEEDS CLARIFICATION] or empty headings in the saved file.
-->

# Architecture

> **Ownership rule**: When <!-- authoring model, runtime split, protocol,
> public API, deployment topology, or the equivalent load-bearing facts
> for this system --> change, this document must be updated in the same PR.

> **State**: `current` (as-is). Architecture decisions live in
> [`docs/architecture/decisions/`](docs/architecture/decisions/).

<!-- One short paragraph: what this system is, in domain language. -->

---

# 1. Introduction and Goals

## Requirements Overview

<!-- Essential features and functional requirements that drive architecture.
     Link product.md; do not copy the commercial story. -->

## Quality Goals

<!-- Top 3–5 architecture quality goals, ordered. The first dominates on
     conflict. Concrete, not buzzwords. These are architecture qualities
     (availability, auditability, time-to-change), not project goals. -->

| Priority | Quality goal | Scenario (one line) |
| -------- | ------------ | ------------------- |
| 1        |              |                     |
| 2        |              |                     |
| 3        |              |                     |

## Stakeholders

| Role | Contact | Expectations of this architecture |
| ---- | ------- | --------------------------------- |
|      |         |                                   |

**Source files**:

---

# 2. Architecture Constraints

<!-- Technical, organisational, and convention constraints that any
     solution must respect. Conventions the team already follows belong
     here (language, cloud, compliance). -->

- **Technical:**
- **Organisational:**
- **Conventions:**

**Source files**:

---

# 3. Context and Scope

## Business Context

<!-- Who uses it, which neighbouring domain systems it talks to.
     ASCII or a table. Owns / does not own. -->

```text
[Actor]
  |
  +-- [{Name}]
        |
        +-- [{Neighbour}]
```

**{Name} owns:**

**{Name} does not own:**

## Technical Context

<!-- Channels, protocols, external technical interfaces.
     Map inputs/outputs to channels. -->

| Neighbour | Direction | Interface | Notes |
| --------- | --------- | --------- | ----- |
|           | up / down |           |       |

**Source files**:

---

# 4. Solution Strategy

<!-- 3–6 named principles with consequences. State what this system will
     NOT do as explicitly as what it will do. Close with a mapping from
     each principle to a §1 quality goal. Trade-offs, not only choices.

     If this file is current and a target delta exists, put the intended
     change here — do not fork a second architecture document. -->

| Principle | Consequence | Quality goal |
| --------- | ----------- | ------------ |
|           |             |              |

**Source files**:

---

# 5. Building Block View

## Whitebox Overall System

<!-- ASCII overview of the whole system. Motivation, contained building
     blocks (black boxes), important interfaces. -->

```text
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Motivation.**

**Contained building blocks.**

**Important interfaces.**

### Repository layout

<!-- The directory / module tree every later epic extends. current: the
     tree as it is. target: the tree as it should be. -->

```text
.
├── ARCHITECTURE.md              this file
├── AGENTS.md
└──
```

### {Black box 1}

- **Purpose / responsibility:**
- **Interfaces:**
- **Quality / performance:**
- **Directory / files:**
- **Open issues:**

### {Black box 2}

<!-- Repeat the black-box template. -->

## Level 2

<!-- White-box one important building block when a single black box is
     not enough to implement against. Omit Level 3 unless a third
     decomposition is load-bearing. -->

### White box {building block 1}

**Source files**:

---

# 6. Runtime View

<!-- 2–5 scenarios. Prefer the ones debugged at 3am. Each scenario: the
     flow, then what is notable about the interactions. -->

## {Runtime scenario 1}

1.
2.

**Notable interactions.**

## {Runtime scenario 2}

**Source files**:

---

# 7. Deployment View

## Infrastructure Level 1

| Service | Platform | Role |
| ------- | -------- | ---- |
|         |          |      |

**Motivation.**

**Quality / performance features.**

**Mapping of building blocks to infrastructure.**

## Infrastructure Level 2

<!-- Only when a node in Level 1 has its own internal topology
     (sidecars, workers, multiple processes). -->

**Source files**:

---

# 8. Cross-cutting Concepts

<!-- Recurring solution approaches. Include only concepts this system
     actually uses. Typical drawers: domain/persistence, UI, security,
     errors, observability, testing, build and release. Each concept
     must point at concrete behaviour, not only a tool name. -->

## Domain model and persistence

<!-- Entities, invariants, where state lives. Type-level contracts that
     every epic must respect. -->

## Security

```text
Trust boundary 1
    ↔ Trust boundary 2
```

## Observability

## Testing

| Tier | Where | What |
| ---- | ----- | ---- |
|      |       |      |

## Build and release

| Workflow | Trigger | Checks |
| -------- | ------- | ------ |
|          |         |        |

**Source files**:

---

<!-- arc42 §9 Architecture Decisions is not in this file.
     Write ADRs with /architecture:adr under docs/architecture/decisions/.
     Link an accepted ADR from the section it governs. -->

# 10. Quality Requirements

## Quality Requirements Overview

<!-- Expand the §1 quality goals into requirements precise enough to
     test. Do not duplicate the priority table; add scenarios. -->

## Quality Scenarios

| Quality goal | Scenario | Measure |
| ------------ | -------- | ------- |
|              |          |         |

**Source files**:

---

# 11. Risks and Technical Debts

## Risks

| ID  | Risk   | Likelihood        | Impact            | Mitigation   |
| --- | ------ | ----------------- | ----------------- | ------------ |
| R1  |        | Low / Medium / High | Low / Medium / High |            |

## Technical debt

- **{Item}.** {Description and how/when it closes.}

## Open questions

1. **{Question}.** {Context; owner; what it blocks.}

**Source files**:

---

# 12. Glossary

| Term | Definition |
| ---- | ---------- |
|      |            |
