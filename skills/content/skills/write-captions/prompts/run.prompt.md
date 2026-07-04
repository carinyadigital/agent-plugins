# Write captions

## Before running

1. Resolve brand per [../../references/brand-resolution.md](../../references/brand-resolution.md).
2. Load `brand/brand-voice.md` and `brand/hashtags.md`.
2. Accept structured tags (subjects, season, moods, contentType, description) as input.
3. If recent captions provided, avoid repeating themes.

## Hashtags

Combine core + subject-specific tags from `brand/hashtags.md`. Cap at 20. Return separately
— do not embed in caption body.

## Caption variants

Three genuinely distinct angles:

**caption_a — Storytelling (3–5 sentences):** Specific moment from the property's journey.

**caption_b — Short and visual (max 150 chars before hashtags):** One strong observation;
stop-the-scroll version.

**caption_c — Educational (3–4 sentences):** Regenerative practice or ecological principle
shown; teach without preaching.

## Channel copy

- **google_post:** 200–280 chars, plain text, no hashtags; discovery intent
- **email_excerpt:** One sentence teaser with natural momentum; no "click here"

## Rules

- First person plural (we, our)
- Never claim fully operational — establishing phase
- Australian English
- No hashtags inside captions
- Avoid clichés from brand-voice.md
- Never repeat opening word/phrase across caption_a, caption_b, caption_c

## Output JSON

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

Respond ONLY with valid JSON.

## Review criteria

See [../../references/prompt-refinement.md](../../references/prompt-refinement.md) caption checks.
