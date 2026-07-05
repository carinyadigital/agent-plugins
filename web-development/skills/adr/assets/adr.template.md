---
type: adr
id: ADR-{NUMBER}
title: { Decision title }
status: Proposed
date: { YYYY-MM-DD }
deciders: [{ Role }, { Role }]
supersedes: null
---

<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
DO NOT INCLUDE in ADR-NNNN.md:
  - Business rationale or commercial justification    → product.md
  - Implementation instructions or code               → solution.md or docs/work/{epic}/design.md
  - Requirements that are not directly relevant to the decision
  - Epic-level scope or delivery sequencing            → roadmap.md or backlog.md
An ADR records one decision: context, options, the choice, and its consequences.
-->

# ADR-{NUMBER} -- {Decision title}

## Context

{Describe the situation, forces, and constraints that make this decision
necessary. Include relevant technical, organisational, and timeline factors.
Explain what is at stake if the decision is wrong or deferred.}

## Decision drivers

- {Driver 1: specific, measurable criterion}
- {Driver 2: specific, measurable criterion}
- {Driver 3: specific, measurable criterion}

## Options considered

### Option 1: {Name}

Pros: {genuine advantages against the decision drivers}

Cons: {genuine disadvantages and trade-offs}

### Option 2: {Name}

Pros: {genuine advantages}

Cons: {genuine disadvantages}

### Option 3: {Name / Status quo}

Pros: {genuine advantages}

Cons: {genuine disadvantages}

## Decision

**{Option chosen}** (Option {N}).

Rationale: {Explain why this option was selected. Reference specific
decision drivers by name. Do not simply restate that the option is better —
explain which drivers it satisfies and which trade-offs are acceptable.}

## Consequences

Positive: {Benefits that follow from this decision.}

Negative: {Trade-offs and limitations this decision introduces. At least
one negative consequence is required.}

## Confirmation

{Describe how adherence to this decision will be validated. Be concrete:
name the test file, CI check, architecture review criterion, or linting
rule that confirms the decision is being followed.}

## Related

- {ADR-XXXX: Related decision title}
