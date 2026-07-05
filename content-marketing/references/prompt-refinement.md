---
type: prompt-refinement-notes
status: iteration-2
---

# Prompt refinement notes

Vision and caption prompt quality rationale. Use when refining `analyse-media` and
`write-captions` skills. Quality checklists below belong in each skill's review
criteria.

---

## Vision / analyse-media

### Issues identified in initial prompt review

**1. Missing local seasonal context**

The original prompt had no guidance on seasons for the business's geography. Without
this, the model applies generic Northern Hemisphere assumptions.

**Fix:** Read `brand/seasonal-calendar.md` when present; otherwise ask the user for
climate/season cues. Golden hour is year-round.

**2. Subject selection lacked specificity guidance**

**Fix:** 1–4 subjects; use specific labels (breed, crop, product) over generic terms;
prefer "drone aerial" only for overhead shots.

**3. Description guidance was too generic**

**Fix:** Brand voice examples with good/bad contrast; honest "building toward" register
when the business is in an establishing phase.

**4. Alt text guidance was vague**

**Fix:** Required elements: primary subject, visual elements, setting, mood + example.

**5. No quality score rubric**

**Fix:** Five bands (0.0–1.0); example anchored at 0.75 not 0.0.

**6. Publishable criteria were too vague**

**Fix:** Binary technical criteria; documentary shots valuable even when unpolished.

### Quality checks (analyse-media)

| Check | What to look for |
| ----- | ---------------- |
| Subjects | Specific (e.g. named breed or product) not generic ("wildlife") |
| Season | Consistent with brand seasonal calendar or stated climate cues |
| Description | Honest, on-brand register |
| Alt text | Specific — not "a photo of a farm" |
| qualityScore | Consistent with visible technical quality |
| publishable | Only false for genuine technical failures |

---

## Caption / write-captions

### Issues identified

**1. Three variants insufficiently differentiated**

**Fix:** Explicit angle per variant — storytelling, short/visual (max 150 chars), educational.

**2. Length guidance missing for caption_b**

**Fix:** Max 150 chars before hashtags.

**3. Cliché list incomplete**

**Fix:** Include terms from brand-voice avoid list when present.

**4. Shared opening words across variants**

**Fix:** Never repeat opening word/phrase across caption_a/b/c.

**5. Channel copy guidance thin**

**Fix:** google_post = discovery intent; email_excerpt = momentum without "click here".

### Quality checks (write-captions)

| Check | What to look for |
| ----- | ---------------- |
| Variant differentiation | Three distinct editorial angles |
| Brand voice | Matches brand-voice.md tone and avoid list |
| Clichés | None from brand-voice avoid list |
| Hashtags | Not embedded in caption body |

---

## Iteration log

| Iteration | Date | Changes |
| --------- | ---- | ------- |
| 1 | 2026-04-13 | Initial refinement |
| 2 | 2026-07-05 | Genericized for content-marketing practice plugin |
