---
name: write-spec
description: >
  Turn a feature idea or problem statement into a structured feature spec or PRD
  with user stories, requirements, and success metrics. Use when drafting a PRD,
  feature spec, or requirements doc. Do NOT use for product strategy doc
  (product), epic task breakdown (tasks), or roadmap phasing (roadmap).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<feature or problem statement>"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: product
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Write spec

You write a feature specification or PRD. Pass the feature name, problem
statement, or idea after the skill name.

See [CONNECTORS.md](../../CONNECTORS.md) for tracker/knowledge connectors. For
detailed PRD section guidance, MoSCoW tips, metrics definition, and acceptance
criteria patterns, read [prd-structure.md](references/prd-structure.md) when needed.

## Steps

### 1. Understand the feature

Accept a feature name, problem statement, user request, or vague idea. Clarify
conversationally — do not dump all questions at once.

### 2. Gather context

Ask as needed: user problem and who experiences it; target segments; success
metrics; constraints (tech, timeline, regulatory, dependencies); prior art.

If project tracker / knowledge base / design tools are connected, pull related
tickets, research, and mockups. Otherwise proceed from what the user provides.

### 3. Generate the PRD

| Section | Content |
| ------- | ------- |
| Problem statement | Who, what, cost of not solving — 2–3 sentences, evidence-grounded |
| Goals | 3–5 measurable outcomes (not outputs) |
| Non-goals | 3–5 explicit out-of-scope items with rationale |
| User stories | "As a [type], I want [capability] so that [benefit]" — priority order |
| Requirements | P0 must-have / P1 nice-to-have / P2 future — each with AC |
| Success metrics | Leading + lagging indicators with specific targets |
| Open questions | Tagged with who answers; blocking vs non-blocking |
| Timeline | Hard deadlines, dependencies, suggested phasing |

### 4. Review and iterate

Offer section expansions and follow-ups (design brief, ticket breakdown,
stakeholder pitch). If the idea is too big, suggest phases and spec phase 1.

## Quality rules

- Be ruthless about P0 — if everything is must-have, nothing is
- Non-goals prevent scope creep; include them every time
- Success metrics are specific ("50% adoption in 30 days"), not vague
- Outcomes over outputs ("reduce time to first value 50%", not "build wizard")

## Output format

Scannable markdown with clear headers. Busy stakeholders should get the gist from
headers and bold text alone.
