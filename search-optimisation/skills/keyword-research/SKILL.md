---
name: keyword-research
description: >
  Research keywords for a topic area — search intent, volume signals, and content
  opportunities. Use when planning content around a topic or building keyword
  targets for the calendar. Writes
  `docs/work/seo/keyword-research-{topic}.md` on the target repo. Do NOT use
  for technical site audits (technical-seo-audit) or competitive product analysis
  (competitive-brief).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<topic-slug>"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Keyword research

You research keywords for a topic and document findings for content planning.
Pass a kebab-case topic slug after the skill name — it becomes the filename segment.

Read [search-optimisation-conventions.md](../../references/search-optimisation-conventions.md).

## Inputs

| Input        | Location                                      | Required   |
| ------------ | --------------------------------------------- | ---------- |
| Topic slug   | Argument (kebab-case)                         | Yes        |
| Product / backlog | `docs/product/product.md`, `docs/product/backlog.md` | If present |
| Existing research | `docs/work/seo/keyword-research-*.md` | Check dupes|
| Locale       | Instance profile or user input                | Yes        |

## Steps

1. Resolve target repo via `config/target.json` or instance target config.
2. Read product/backlog context when present. Check existing SEO work files to
   avoid duplication.
3. Research via web search: SERP analysis, People Also Ask, related queries.
   Match locale/geography from instance profile or user input. Prioritise intent
   aligned with the customer's product and content strategy.
4. Write `docs/work/seo/keyword-research-{topic}.md` using the output format.
5. Confirm recommendations are actionable for content calendar planning.

## Quality rules

- Primary keyword clearly identified with rationale
- Actionable content recommendations (not keyword lists alone)
- No duplicate of existing keyword research files
- Realistic for the customer's current search maturity
- Companion only — full competitive landscape is `competitive-brief`

## Output format

```markdown
# Keyword research — {Topic title}

**Date:** {YYYY-MM-DD}
**Topic slug:** {topic}
**Researcher:** search-optimisation

## Business context
Why this topic matters for the customer's site and audience.

## Primary keyword
| Keyword | Intent | Priority | Notes |
| ------- | ------ | -------- | ----- |

## Secondary keywords
| Keyword | Intent | Priority | Notes |

## Long-tail opportunities
Bulleted list with suggested content angles.

## Content recommendations
Specific content ideas with target keyword per slot.

## Competitor snapshot
Brief notes on who ranks and content gaps (not a full competitive brief).

## Open questions
Items needing human sign-off.
```
