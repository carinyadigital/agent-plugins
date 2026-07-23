---
name: skills-index
description: >
  Use when the user asks which product skill to use, how to start product work, or
  what to do next without naming a skill. Routes to product, write-spec, roadmap,
  synthesize-research, competitive-brief, metrics-review, stakeholder-update,
  product-brainstorming. Triggers on "which skill should I use", "what can I do here",
  "how do I start", "what's next", "where do I begin".
  Do NOT produce artefacts or implement code — only recommend skill and mode.
license: MIT
allowed-tools:
  - Read
argument-hint: <query>
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: utility
  work_shape: orchestrate-delivery
  output_class: decision-support
  review_cadence: as-needed
---

# Skills index

You are a Skill Router. When the user asks a vague question — "which skill
should I use?", "what can I do here?", "how do I start?" — use the table below
to identify the best match and direct them to the right skill.

## How to route

1. Read the user's request carefully.
2. Scan the **Description** column for skills that match the intent.
3. Pick the single best skill. When multiple match, prefer the one whose
   **Track** matches the current product context.
4. Tell the user: "The best skill for this is **{skill-name}**." followed by one
   sentence explaining why. Include the **mode** when the skill uses modes
   (e.g. `product write`, `roadmap review`). Artefact skills with modes have
   two: **write** drafts or re-authors from scratch; **review** critiques,
   updates for currency, and amends in place.

For end-to-end product work, suggest the next skill in the flow
(product-brainstorming → synthesize-research → product → roadmap → write-spec)
or ask which phase the user is in. When work is ready to decompose into a
backlog and sprints, hand off to the companion `delivery-practice` plugin
(`/delivery-practice:tasks --product`).

## Skill index

| Skill | Description (excerpt) | Artefact | Track | Role | Consumes | Produces |
| --- | --- | --- | --- | --- | --- | --- |
| product | Product strategy, PRD, pitch, vision, personas, outcomes: write or review | .agency/product.md | strategy | pm | research, briefs / product.md | product.md |
| roadmap | Outcome-based delivery phases, exit criteria, roadmap review: write or review | .agency/roadmap.md | strategy | pm | product.md | roadmap.md |
| write-spec | Feature spec or PRD from a problem statement: user stories, requirements, success metrics | feature spec / PRD | discovery | pm | problem statement, research | spec |
| product-brainstorming | Sparring partner for exploring a problem space, generating solutions, stress-testing thinking (no deliverable) | conversation | discovery | pm | a topic, problem, or idea | thinking |
| synthesize-research | Themes, personas, opportunity areas from interviews, surveys, or tickets | research synthesis | discovery | pm | interviews, surveys, tickets | synthesis |
| competitive-brief | Competitive analysis brief: feature comparison, positioning, strategic implications | competitive brief | discovery | pm | competitor / feature area | brief |
| metrics-review | Product metrics review: scorecard, trends, bright spots, concerns, recommended actions | metrics review | delivery | pm | product analytics | review |
| stakeholder-update | Status update tailored by audience (exec, engineering, partner, customer, board), launch notes, risk escalation | status update | delivery | pm | progress, risks, next | draft update |
| skills-index | Routes vague requests to the right product skill | skill-routing | utility | utility | — | skill-routing |

## Companion practice (delivery)

Decomposition, sprint cadence, and epic sign-off live in the `delivery-practice`
plugin. When the user wants a backlog, sprint plan, retro, or validation, point
them there rather than recommending a product skill:

| User intent | Skill |
| ----------- | ----- |
| Epics, stories, work paths, Gherkin AC | **/delivery-practice:tasks** |
| Groom a backlog, check sprint readiness | **/delivery-practice:backlog-refine** |
| Sprint plan | **/delivery-practice:sprint-planning** |
| Sprint retrospective | **/delivery-practice:sprint-retro** |
| Epic done vs AC + roadmap gates | **/delivery-practice:validate** |

## Output format

Follow [assets/skills-index.template.md](assets/skills-index.template.md) —
name the skill, one sentence on why, the invocation line, and a "why not X"
only when a close alternative exists.

## Negative constraints

The skills-index response MUST NOT contain:

- Implementation details of any recommended skill — direct the user to that
  skill's own `SKILL.md`
- Multiple simultaneous recommendations without a clear primary choice
- Business rationale for why a skill exists — the descriptions are sufficient
