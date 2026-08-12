---
name: find
description: >
  Use when the user asks which skill to use, how to start, or what to do next
  without naming a skill. Routes to installed plugins' skills and offers
  marketplace install commands for plugins that are not installed. Triggers on
  "which skill should I use", "what can I do here", "how do I start", "what's
  next", "where do I begin", "/skills-index:find". Do NOT produce artefacts or
  implement code — only recommend skill and mode (or an install command).
license: MIT
allowed-tools:
  - Read
  - Glob
argument-hint: <query>
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: skills-index
  work_shape: orchestrate-delivery
  output_class: decision-support
  review_cadence: as-needed
---

# /skills-index:find

You are an install-aware Skill Router for the `carinya-plugins` marketplace.

## What this earns its place on

1. **Discovery of uninstalled plugins** — "install `search-optimisation` to get keyword-research"
2. **Workflow sequencing** — the delivery loop has an order; the platform doesn't know it

Claude Code already surfaces every *installed* skill's description, so do not
re-list the whole catalogue as trivia. Prefer a single best next step.

## How to route

1. Read the user's request carefully.
2. Detect which catalogue plugins appear installed (plugin roots under the
   session, `CLAUDE_PLUGIN_ROOT` siblings, or user-stated installs). When unsure,
   ask once which plugins they have installed.
3. Scan the **Catalogue** below for intent matches.
4. If the best skill's plugin **is installed**: recommend `/plugin:skill` with
   one sentence why, plus the next step in the sequence when relevant.
5. If the best skill's plugin **is not installed**: give the install command
   first, then the skill they will run after install:
   `/plugin install <plugin>@carinya-plugins` → `/plugin:skill …`
6. Never invent skills outside this catalogue.

## Workflow sequences

| Loop | Order |
| ---- | ----- |
| Strategy → delivery | `/product-management:product` → `roadmap` → `tasks --product` → `sprint-planning` → `validate` |
| Engineering delivery | `/architecture:solution` → `/engineering:tdd` → `implement` → `code-review` → `/design:ux-design-review` → `/product-management:validate` |
| Brand → content | `/brand-creative:brand-voice` → `/content-marketing:content-calendar` |

## Catalogue

| Plugin | Skill | Intent |
| ------ | ----- | ------ |
| product-management | product | PRD / vision / product.md |
| product-management | roadmap | Phases / Now-Next-Later |
| product-management | write-spec | Feature spec from a problem |
| product-management | product-brainstorming | Explore a problem space |
| product-management | synthesize-research | Themes from research inputs |
| product-management | competitive-brief | Competitor analysis |
| product-management | metrics-review | Metrics scorecard |
| product-management | stakeholder-update | Audience-tailored status |
| product-management | tasks | Decompose into backlog / stories / AC |
| product-management | backlog-refine | Groom backlog / sprint readiness |
| product-management | sprint-planning | Plan a sprint |
| product-management | sprint-retro | Sprint retrospective |
| product-management | validate | Work-item sign-off vs AC |
| architecture | solution | Architecture solution.md |
| architecture | adr | Architecture decision records |
| engineering | tdd | Work-item tdd.md |
| engineering | implement | Implement a task |
| engineering | code-review | Branch / PR code review |
| engineering | code-review-fix | Address review findings |
| engineering | merge-request | Open MR/PR |
| engineering | docs-review | Cross-document quality review |
| engineering | deploy-qa | Prepare QA workspace |
| engineering | run-automated-suite | Run automated tests |
| engineering | exploratory-pass | Exploratory QA |
| engineering | document-defects | Structure defect reports |
| engineering | platform-health | Platform health audit |
| engineering | debug | Investigate bugs |
| design | wireframe | Low-fidelity layout spec |
| design | ux-design-review | Live-browser UX review |
| design | ux-design-fix | Address UX findings |
| ralph-loop | ralph-loop-setup | Seed a Ralph loop |
| ralph-loop | ralph-loop | Start / status / cancel a loop |
| brand-creative | brand-voice | Brand voice lifecycle |
| brand-creative | brand-guide | Visual identity guide |
| content-marketing | content-calendar | Editorial calendar |
| content-marketing | curate-content | Rank social inventory |
| content-marketing | analyse-media | Vision analysis of media |
| content-marketing | write-captions | Caption variants |
| content-marketing | edit-content | Select / edit caption |
| content-marketing | draft-post | Blog seed JSON |
| content-marketing | draft-recipe | Recipe seed JSON |
| search-optimisation | keyword-research | Keyword research |
| search-optimisation | technical-seo-audit | Technical SEO audit |
| search-optimisation | content-seo-review | On-page SEO review |
| skill-authoring | skills-qa | Skill quality gate |
| skills-index | find | This router |
| skills-index | related-skills-surfacer | Suggest related uninstalled skills after a task |

## Output format

Follow [assets/skills-index.template.md](assets/skills-index.template.md).

When recommending an uninstalled plugin:

```
Install first: /plugin install <plugin>@carinya-plugins
Then run: /<plugin>:<skill> …
```

## Negative constraints

- Do not implement or draft the recommended skill's artefact here
- Do not recommend multiple primaries — one best skill (plus optional next step)
- Do not suggest deleted hub package-manager skills (`skill-installer`, etc.)
