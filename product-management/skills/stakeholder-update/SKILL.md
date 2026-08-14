---
name: stakeholder-update
description: >
  Write a weekly or monthly status for leadership, announce a launch, escalate a
  risk, or tailor the same progress for exec, engineering, partner, customer, or
  board audiences. Use when drafting status updates or launch notes. Do NOT use
  for product strategy (product) or roadmap updates (roadmap).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<update type and audience>"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: product
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Stakeholder update

You generate a stakeholder update tailored to audience and cadence. Pass update
type, audience, and cadence after the skill name.

See [CONNECTORS.md](../../CONNECTORS.md) for tracker/chat connectors. For full
audience templates, G/Y/R status guidance, and ROAM risk framing, read
[update-templates.md](references/update-templates.md) when needed.

## Steps

### 1. Determine type and audience

**Type:** weekly · monthly · launch · ad-hoc (escalation, pivot, decision)

**Audience:** executives · engineering · cross-functional partners · customers /
external · board

### 2. Pull context

If project tracker / chat / knowledge base is connected, pull completed work,
at-risk items, decisions, and blockers. Otherwise ask: accomplishments since last
update, blockers/risks, decisions made or needed, what's next.

### 3. Generate the update

| Audience | Focus | Length |
| -------- | ----- | ------ |
| Executives | TL;DR, G/Y/R, outcomes vs goals, asks | <300 words |
| Engineering | Shipped (links), in progress, blockers, decisions | Structured, skimable |
| Partners | What's coming that affects them; asks with dates | Short |
| Customers | Benefits, coming soon, known issues — no jargon | Short |
| Launch | What launched, why it matters, scope, metrics, rollout | Medium |

### 4. Review and deliver

Offer tone/detail adjustments and formatting for email, chat, doc, or slides.

## Quality rules

- Lead with the most important thing; bad news first when it matters
- Status colors reflect reality — Yellow is good risk communication, not failure
- Asks must be specific: "Decision on X by Friday", not "support needed"
- Executives get outcomes; engineers get links and blockers

## Output format

Scannable markdown. Bold key points; bullets for lists. Match length to audience
attention.
