---
name: draft-post
description: >
  Draft a blog post seed JSON for CMS import at the target repo's resolved post
  seed path, with body as markdown. Use when writing a blog seed from a calendar
  brief or slug. Match brand-voice.md before finishing. Do NOT merge or publish —
  seed PR only. Do NOT plan the calendar (content-calendar) or run SEO review
  (content-seo-review).
license: MIT
allowed-tools: Read Write Glob Grep
argument-hint: "<slug> [--brief from calendar]"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Draft post

You draft a blog post seed JSON for the CMS import pipeline. Pass the post slug
after the skill name.

Read [content-conventions.md](../../references/content-conventions.md) to resolve
brand and seed paths. Read `<resolved-brand-path>/brand-voice.md` and match tone
on excerpt and body before finishing. Read the target CMS post collection config
before drafting.

## Inputs

| Input            | Location                                      | Required   |
| ---------------- | --------------------------------------------- | ---------- |
| Slug / brief     | Argument or calendar brief                    | Yes        |
| Brand voice      | `<resolved-brand-path>/brand-voice.md`        | Yes        |
| CMS schema       | Target post collection config                 | Yes        |
| Existing seeds   | Resolved post seed directory                  | Check dupes|

## Steps

1. Resolve brand and post seed directory per content-conventions.
2. Read the content calendar brief for this slug if present.
3. Read the CMS post collection schema to confirm field constraints.
4. Check existing seeds and published slugs — do not duplicate.
5. Write `{post-seed-dir}/{slug}.json` with the schema below.
6. Body markdown rules: `##` section headings; Australian English; first person
   plural (we, our) per brand voice; plain markdown only (no JSX/MDX); target
   600–1200 words unless the brief says otherwise.
7. Use slugs for `author`, `category`, and `tags`. Align category/tag slugs with
   brand taxonomy when present.

## Schema

| Field         | Type                      | Required        |
| ------------- | ------------------------- | --------------- |
| `slug`        | string                    | yes             |
| `title`       | string, max 200           | yes             |
| `date`        | ISO date `YYYY-MM-DD`     | yes             |
| `author`      | author slug               | yes             |
| `category`    | category slug             | no              |
| `tags`        | tag slug array            | no              |
| `featured`    | boolean                   | no, default false |
| `excerpt`     | string, max 500           | yes             |
| `description` | string, max 300 (SEO)     | no              |
| `image`       | public path               | no              |
| `body`        | markdown string           | yes             |

## Quality rules

- Valid JSON matching the collection schema
- Brand voice enforced; excerpt stands alone
- Description optimised for search when provided
- Body converts cleanly to Lexical (no custom MDX)
- Seed PR only — do not merge, publish, or run import scripts

## Output format

```json
{
  "slug": "example-slug",
  "title": "Example Title",
  "date": "2026-07-15",
  "author": "author-slug",
  "category": "category-slug",
  "tags": ["tag-a", "tag-b"],
  "featured": false,
  "excerpt": "Short teaser for cards and listings.",
  "description": "SEO meta description under 300 chars.",
  "image": "/images/example.jpg",
  "body": "## Opening\n\nParagraph text..."
}
```
