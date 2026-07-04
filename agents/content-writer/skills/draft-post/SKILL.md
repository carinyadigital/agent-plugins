---
name: draft-post
description: >
  Use when drafting a blog post seed JSON for Payload import. Output at
  website/apps/site/content/seeds/posts/{slug}.json with body as markdown.
  Run brand-voice enforce before finishing. Do NOT merge or publish — seed PR only.
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<slug> [--brief from calendar]"
---

# Draft post

Create a blog post seed file for the Payload import pipeline.

## Brand resolution

Read [../../references/brand-resolution.md](../../references/brand-resolution.md).
Run `brand-voice` **enforce** on excerpt and body before committing the seed.

## Artefact

`apps/site/content/seeds/posts/{slug}.json` on the **website** target repo.

Schema derived from `apps/site/src/collections/Posts.ts`:

| Field | Type | Required |
| ----- | ---- | -------- |
| `slug` | string | yes |
| `title` | string | yes, max 200 |
| `date` | ISO date `YYYY-MM-DD` | yes |
| `author` | author slug | yes |
| `category` | category slug | no |
| `tags` | tag slug array | no |
| `featured` | boolean | no, default false |
| `excerpt` | string, max 500 | yes |
| `description` | string, max 300 | no (SEO meta) |
| `image` | public path | no |
| `body` | markdown string | yes |

## Router

Follow [prompts/run.prompt.md](prompts/run.prompt.md).

## Related skills

- `edit-content` — editorial pass on captions/social; use for tone review if needed
- `content-seo-review` — SEO review on the seed PR
- `brand-voice` — enforce before finalising
