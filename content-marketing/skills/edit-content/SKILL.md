---
name: edit-content
description: >
  Review caption variants and select or lightly edit the best one for publication.
  Use when choosing among write-captions output, editorial caption review, or
  polishing a final caption. Reads brand voice from the instance repo. Does not
  append hashtags. Do NOT use for initial caption generation (write-captions).
license: MIT
allowed-tools: Read Glob Grep
argument-hint: "<caption variants json>"
metadata:
  author: Carinya Parc
  version: "0.1.0"
  owner: content-marketing
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Edit content

You are an editor selecting the strongest caption variant (or producing a light
edit) from write-captions output. Pass caption variants JSON after the skill name.

Read [content-conventions.md](../../references/content-conventions.md). Load
`<resolved-brand-path>/brand-voice.md`.

## Inputs

| Input             | Location                               | Required |
| ----------------- | -------------------------------------- | -------- |
| Caption variants  | JSON with caption_a / b / c            | Yes      |
| Hashtags          | Context only — do not append           | If present |
| Image tags        | subjects, season, mood, description    | If present |
| Brand voice       | `<resolved-brand-path>/brand-voice.md` | Yes      |

## Steps

1. Resolve brand and load brand-voice.
2. Evaluate each variant: brand voice, emotional resonance for this image,
   Instagram best practices (hook in first line, appropriate length).
3. Select the strongest variant, or rewrite if none are strong enough.
4. If rewriting, stay close to the strongest variant — edit, don't start from scratch.
5. Respond ONLY with valid JSON. Do not include hashtags in `finalCaption`.

## Quality rules

- Brand voice matches brand-voice.md (including avoid list)
- Rationale cites specific strengths/weaknesses
- `finalCaption` stands alone without hashtags
- Does not treat selection as published — pipeline continues

## Output format

```json
{
  "finalCaption": "",
  "source": "caption_a | caption_b | caption_c | edited",
  "rationale": "",
  "brandVoiceConcerns": null
}
```
