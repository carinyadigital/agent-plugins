---
name: content-seo-review
description: >
  Review content seed PRs for on-page SEO — titles, meta descriptions, heading
  structure, keyword usage, and internal linking. Use when reviewing seed JSON or
  draft content before merge. Produces PR review comments only. Do NOT use for
  technical site audits (technical-seo-audit) or drafting content (draft-post).
license: MIT
allowed-tools: Read Glob Grep
argument-hint: "<pr-url or seed path>"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Content SEO review

You review content seed JSON or pasted draft content for on-page SEO. Pass a PR
URL or seed path after the skill name. Read-only — comments only; do not rewrite
seeds or approve merge.

Read [search-optimisation-conventions.md](../../references/search-optimisation-conventions.md).

## Inputs

| Input           | Location                                         | Required   |
| --------------- | ------------------------------------------------ | ---------- |
| Seed / PR       | PR diff or seed path                             | Yes        |
| Keyword targets | `.agency/work/seo/keyword-research-*.md`         | If present |
| Site routing    | Target site slug/URL conventions                 | Yes        |

## Steps

1. Load seed JSON from the PR diff or named path.
2. Read relevant keyword-research docs for target keywords.
3. Check slug uniqueness and URL structure against the target site's routing.
4. Run the checklist below.
5. Post PR review comments grouped as **Blocking** vs **Suggestion**, with a
   verdict: approve · approve with suggestions · request changes.

## Checklist

### Posts and articles

- [ ] Title includes primary keyword naturally; under ~60 chars ideal
- [ ] `description` or `excerpt` works as meta description (under ~160 chars)
- [ ] Slug is short, kebab-case, keyword-relevant
- [ ] Body has logical H2 structure (maps to headings on import)
- [ ] Internal linking opportunities noted (suggest anchor text + target slug)
- [ ] Image path set; alt text guidance if hero image referenced in body

### Structured content (recipes, products, etc.)

- [ ] Title and description optimised for search intent
- [ ] Structured data fields complete per content type
- [ ] Seasonal or topical keyword alignment where applicable

## Quality rules

- Comments cite specific JSON fields or content sections
- Keyword usage reads naturally (no stuffing)
- Recommendations actionable by content authors without a full SEO re-run
- Blocking: duplicate slug, missing description, keyword stuffing
- Suggestion: internal links, heading tweaks
