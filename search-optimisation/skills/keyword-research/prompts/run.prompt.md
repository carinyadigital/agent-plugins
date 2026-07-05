# Keyword research

## Before running

1. Read `${CLAUDE_PLUGIN_ROOT}/references/search-optimisation-conventions.md`.
2. Resolve target repo via `.digital-agency/target.json` or instance target config.
3. Read `docs/product/product.md` and relevant backlog epics for context when present.
4. Check existing files in the SEO work directory to avoid duplication.

## Task

Research keywords for the given topic and write `docs/work/seo/keyword-research-{topic}.md`.

### Document structure

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

## Research approach

Use web search for SERP analysis, People Also Ask, and related queries.
Match locale and geography from instance profile or user input.
Prioritise intent aligned with the customer's product and content strategy.

## Review criteria

- Actionable recommendations for content planning
- Primary keyword clearly identified with rationale
- No duplicate of existing keyword research files
- Realistic for the customer's current search maturity
