---
type: Solution
version: '0.1'
owner: <!-- team or squad name -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - <!-- product.md -->
  - docs/architecture/decisions/register.md
---

<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
DO NOT INCLUDE in solution.md:
  - Commercial rationale or business case       → product.md
  - Target customer segments or personas        → product.md
  - Strategic thesis or product principles      → product.md
  - Positioning or messaging                    → product.md
  - User quotes                                 → product.md
  - Story-level acceptance criteria             → docs/work/{epic}/tasks.md
  - Phase sequencing or epic ordering           → roadmap.md
-->

# Solution -- {Name}

{Name} solution design. Captures the architecture, cross-cutting concepts,
data contracts, and key decisions that apply across epics.
For product context, problem statement, and commercial scope see
[`product.md`](product.md).

## 1. Context and scope

### 1.1 System context

<!-- C4 Level 1 — text diagram. What does this system own?
     What upstream systems feed it? What downstream systems consume it?

```text
[Actor / Browser]
  |
  +-- [{Name} Surface]
        |
        +-- [{Upstream Service}]
```
-->

### 1.2 System boundary

**{Name} owns:**

<!-- Bullet list: surfaces, contracts, and APIs this system produces -->

**{Name} does not own:**

<!-- Bullet list: adjacent systems, upstream schemas, other teams' concerns -->

### 1.3 Upstream and downstream systems

- **Upstream — {provider}.** Provides {interface}. Schema evolution tracked in `dependencies/`.
- **Downstream — {consumer}.** Consumes {contract}.

## 2. Quality goals and constraints

### 2.1 Quality goals (top 3–5)

Ordered; the top goal dominates when goals conflict.

1. <!-- Most important NFR -->
2. <!-- Second most important NFR -->
3. <!-- Third -->

### 2.2 Constraints

- **Technical:** [NEEDS CLARIFICATION]
- **Regulatory:** [NEEDS CLARIFICATION]
- **Organisational:** [NEEDS CLARIFICATION]

## 3. Solution strategy

<!-- 3–6 named principles with consequences. State what this system will NOT do
as explicitly as what it will do. Close with a table mapping each principle to
the quality goal it satisfies. -->

[NEEDS CLARIFICATION]

## 4. Building block view

<!-- C4 Level 2 (containers) and selectively Level 3 (components).
     Show the directory / module layout that every epic will extend. -->

[NEEDS CLARIFICATION]

## 5. Runtime view

<!-- 2–5 key sequences as text flows. Focus on the scenarios debugged at 3 am. -->

[NEEDS CLARIFICATION]

## 6. Data model and ubiquitous language

<!-- Entities, relationships, invariants, and the glossary of canonical terms
     used in code, docs, and conversation. Type definitions live in solution.md §6. -->

[NEEDS CLARIFICATION]

## 7. Cross-cutting concepts

<!-- Observability, error taxonomy, security, feature flags, caching,
     accessibility, and testing strategy. Each pattern must reference a concrete
     system behaviour, not just name a tool. -->

[NEEDS CLARIFICATION]

## 8. Deployment and environments

<!-- Topology, CI/CD pipeline, rollout pattern, and environment matrix. -->

[NEEDS CLARIFICATION]

## 9. Architectural decisions (ADR log)

<!-- List ratified ADRs that govern this system.
     Mark unwritten candidates with _(Not yet written)_. -->

[NEEDS CLARIFICATION]

## 10. Risks, technical debt, and open questions

### 10.1 Risks

| ID  | Risk   | Likelihood        | Impact            | Mitigation   |
| --- | ------ | ----------------- | ----------------- | ------------ |
| R1  | {risk} | {Low/Medium/High} | {Low/Medium/High} | {mitigation} |

### 10.2 Technical debt

- **{Item}.** {Description and how/when it closes.}

### 10.3 Open questions

1. **{Question}.** {Context; owner; how it blocks.}

## 11. Graduation candidates

<!-- Patterns that should lift to a shared library when a second area adopts
     them. State the trigger; do not graduate speculatively. -->

| Pattern        | Current home    | Graduate to             | Trigger                        |
| -------------- | --------------- | ----------------------- | ------------------------------ |
| {pattern name} | §{N.M}          | `architecture/patterns/{name}.md` | {Second context that adopts it} |
