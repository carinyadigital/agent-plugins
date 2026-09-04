---
name: competitive-brief
description: >
  Create a competitive analysis brief for product strategy, feature
  prioritization, or sales enablement. Use when comparing competitors, mapping
  a feature area across rivals, or drafting battle cards. Do NOT use for user
  research synthesis (synthesize-research) or product strategy doc (product).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<competitor or feature area>"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: product
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: decision-support
---

# Competitive brief

You produce an evidence-based competitive analysis brief. Pass competitor name(s)
or a feature area after the skill name.

See [CONNECTORS.md](../../CONNECTORS.md) for connected tools. For matrices,
positioning frameworks, win/loss method, and trend analysis, read
[competitive-analysis.md](references/competitive-analysis.md) when needed.

## Steps

### 1. Scope

Ask: which competitor(s) or feature area; focus (full product, feature, pricing,
GTM, positioning); what decision this informs (strategy, sales, board, prioritization).

### 2. Research

Via web search: product/pricing pages, changelogs, press, reviews (G2/Capterra),
job postings, community discussion. If knowledge base or chat is connected, pull
existing competitive docs, win/loss notes, and deal feedback.

### 3. Generate the brief

Include:

1. **Competitor overview** — company summary, positioning, recent momentum
2. **Feature comparison** — rate Strong / Adequate / Weak / Absent; use buyer
   capability areas (see reference for matrix templates)
3. **Positioning analysis** — target customer, category claim, differentiator
4. **Strengths and weaknesses** — evidence-based; do not inflate or dismiss
5. **Opportunities and threats** — gaps to exploit; competitor bets; nightmare moves
6. **Strategic implications** — what to build, differentiate vs parity, monitor next

### 4. Follow up

Offer deeper dive, one-page exec summary, sales battle cards, or a monitoring plan.

## Quality rules

- Be honest about competitor strengths — dismissive analysis is useless
- Focus on what matters to customers, not internal architecture
- Lead with strategic implications ("so what"), not raw feature lists
- Date the brief; flag areas that change quickly

## Output format

Markdown with clear section headers. Use tables for feature comparisons. Keep
strategic implications concise and actionable.
