---
name: skills-index
description: >
  Use when the user asks which skill to use, how to start delivery, or what to
  do next without naming a skill. Routes to tasks, backlog-refine,
  sprint-planning, validate, etc. Triggers on "which skill should I use", "what can I do here",
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
   **Track** matches the current delivery context.
4. Tell the user: "The best skill for this is **{skill-name}**." followed by one
   sentence explaining why. Include the **mode** when the skill uses modes
   (e.g. `adr plan CHK01`, `tasks checkout-foundation`, `sprint-planning 3`).
   Most artefact skills are write-only — drafting or re-authoring from scratch.
   For reviewing or critiquing an existing artefact, route to **/web-development:docs-review**
   instead. `adr` is the exception: it keeps its own **plan**, **write**, and
   **review** modes.

For end-to-end delivery, suggest the next skill in the flow
(tasks → design → tasks → implement → validate) or ask which phase the user is
in. Strategy inputs (product, roadmap) come from the companion
**product-management** plugin; architecture and code (solution, design,
implement) from **web-development**.

## Skill index

| Skill | Description (excerpt) | Artefact | Track | Role | Consumes | Produces |
| --- | --- | --- | --- | --- | --- | --- |
| adr | Plan the register — survey product/solution for decisions still to make, or `adr plan <work-id>` to harvest decisions already made in design.md — then write or review ADRs | register.md / ADR-NNNN.md | architecture | architect | solution.md, design.md | ADR-NNNN.md |
| tasks | Decompose anything into delivery work: product/roadmap into epics, an epic into stories and tasks with Gherkin AC, or any spec/RFC into both | backlog.md / tasks.md | strategy / discovery | delivery | product.md, roadmap.md, design.md, any spec | backlog.md, tasks.md |
| backlog-refine | Groom a backlog or judge sprint readiness: reprioritise, split, re-estimate, defer; amends in place with a verdict | docs/product/backlog.md / docs/work/{work-id}/tasks.md | discovery / delivery | delivery | backlog.md, tasks.md | groomed artefact |
| implement | Implements a task against design.md and tasks.md | code | delivery | engineer | design.md, tasks.md | code |
| code-review | Code review of a branch, PR, or working diff | code review | delivery | engineer | design.md, tasks.md | review |
| code-review-fix | Addresses code review findings without behaviour change | code | delivery | engineer | review output | code |
| ux-design-review | Read-only UX review of implemented UI vs its design source: accessibility, states, responsiveness, fidelity | UX review | delivery | engineer | design source, UI diff | review |
| ux-design-fix | Change how existing UI looks or behaves, from a UX review verdict or a direct instruction; verifies visually and commits | code | delivery | engineer | UX review output, or an instruction | code |
| merge-request | Open an MR/PR for the current branch on any provider: title, description, labels, reviewer suggestions | MR / PR | delivery | engineer | — | MR / PR |
| merge-request-babysit | Drive an open MR/PR to merge-ready: watch CI, fix objective failures, triage threads, sync conflicts | merge-ready MR | delivery | engineer | open MR / PR | code / MR |
| merge-request-review | Review an MR/PR as its reviewer; publish inline comments and a verdict | published review | delivery | engineer | MR / PR | published review |
| ralph-loop-setup | Seed and configure a Ralph loop: pick a preset (engineering delivery, ad-hoc, custom), resolve the environment, set the completion promise and iteration budget; never starts the loop | seeded loop | delivery | delivery | design.md, tasks.md | loop files |
| ralph-loop | Run an autonomous loop: one step per iteration until a completion promise or a safety rail (`start`, `status`, `cancel`) | committed work item + MR | delivery | delivery | seeded loop | code / MR |
| design | docs/work/{work-id}/design.md: write (review via docs-review) | design.md | discovery | architect | solution.md, backlog.md | design.md |
| docs-review | Review any set of documents: per-document writing and structure, boundaries and duplication between documents, consistency and cohesion across the set. Read-only | doc review | any | architect | any doc set | review |
| sprint-planning | Plan a sprint: goal, carry-over, capacity, committed scope, dependencies, DoD | docs/work/sprint-{id}/plan.md | delivery | delivery | backlog.md, tasks.md, prior retrospective.md | plan.md |
| sprint-retro | Review a finished sprint: commitment vs actual, themes with evidence, actions routed to owning skills | docs/work/sprint-{id}/retrospective.md | delivery | delivery | plan.md, tasks.md | retrospective.md |
| solution | Architecture solution.md: write (review via docs-review) | docs/architecture/solution.md | architecture | architect | product.md | solution.md |
| skills-index | Routes vague requests to the right skill | skill-routing | utility | utility | — | skill-routing |
| validate | Work-item validation vs AC and roadmap gates | validation report | delivery | delivery | backlog.md, tasks.md, solution.md | validation |

## Companion practices (cross-plugin)

Strategy, discovery, and stakeholder communication live in the
`product-management` plugin. When the user wants these, point them there rather
than recommending a delivery skill:

| User intent | Skill |
| ----------- | ----- |
| PRD, vision, personas, product strategy | **/product-management:product** |
| Feature spec from a problem statement | **/product-management:write-spec** |
| Phases, exit criteria, roadmap | **/product-management:roadmap** |
| Themes from interviews, surveys, tickets | **/product-management:synthesize-research** |
| Competitor comparison, battle cards | **/product-management:competitive-brief** |
| Metrics scorecard, trends, actions | **/product-management:metrics-review** |
| Status for leadership, launch note, escalation | **/product-management:stakeholder-update** |

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
