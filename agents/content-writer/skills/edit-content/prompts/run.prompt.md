# Edit content

## Before running

1. Resolve brand per [../../references/brand-resolution.md](../../references/brand-resolution.md).
2. Load `brand/brand-voice.md`.
2. Input: three caption variants (caption_a/b/c), hashtags (for context only — do not append),
   and image tags (subjects, season, mood, description).

## Task

1. Evaluate each variant: brand voice, emotional resonance for this image, Instagram best
   practices (hook in first line, appropriate length).
2. Select the strongest variant, or rewrite if none are strong enough.
3. If rewriting, stay close to the strongest variant — edit, don't start from scratch.

## Output JSON

```json
{
  "finalCaption": "",
  "source": "caption_a | caption_b | caption_c | edited",
  "rationale": "",
  "brandVoiceConcerns": null
}
```

Respond ONLY with valid JSON. Do not include hashtags in finalCaption.

## Review criteria

- Brand voice matches plugin guidelines
- Rationale cites specific strengths/weaknesses
- finalCaption stands alone without hashtags
