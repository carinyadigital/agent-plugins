---
name: write-captions
description: >
  Write Instagram caption variants and channel copy from media tags or
  analyse-media output. Use when drafting social captions, Google Business copy,
  or email teasers from tagged media. Reads brand from the instance repo. Do NOT
  use for selecting the final caption (edit-content) or vision analysis
  (analyse-media).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<tags json or media context>"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Write captions

You generate three distinct Instagram caption variants plus channel copy from
media tags or analyse-media output. Pass tags JSON or media context after the
skill name.

Read [content-conventions.md](../../references/content-conventions.md). Load
`brand-voice.md` and `hashtags.md` from the resolved brand path. Quality checks:
[prompt-refinement.md](../../references/prompt-refinement.md).

## Inputs

| Input           | Location                                     | Required   |
| --------------- | -------------------------------------------- | ---------- |
| Media tags      | subjects, season, moods, contentType, description | Yes   |
| Brand voice     | `<resolved-brand-path>/brand-voice.md`       | Yes        |
| Hashtags        | `<resolved-brand-path>/hashtags.md`          | If present |
| Recent captions | Prior captions to avoid theme repeat         | If known   |

## Steps

1. Resolve brand. Load brand-voice and hashtags.
2. Combine core + subject-specific tags from hashtags.md. Cap at 20. Return
   separately — do not embed in caption body.
3. Write three genuinely distinct angles:
   - **caption_a — Storytelling (3–5 sentences):** Specific moment from the
     property's journey.
   - **caption_b — Short and visual (max 150 chars):** One strong observation;
     stop-the-scroll version.
   - **caption_c — Educational (3–4 sentences):** Regenerative practice or
     ecological principle shown; teach without preaching.
4. Write channel copy:
   - **google_post:** 200–280 chars, plain text, no hashtags; discovery intent
   - **email_excerpt:** One sentence teaser with natural momentum; no "click here"
5. Respond ONLY with valid JSON in the output format below.

## Quality rules

- First person plural (we, our); Australian English
- Never claim fully operational — establishing phase
- No hashtags inside captions; avoid clichés from brand-voice.md
- Never repeat opening word/phrase across caption_a, caption_b, caption_c
- Variants for editorial review — `edit-content` selects

## Output format

```json
{
  "instagram": {
    "caption_a": "",
    "caption_b": "",
    "caption_c": ""
  },
  "google_post": "",
  "email_excerpt": "",
  "hashtags": ""
}
```
