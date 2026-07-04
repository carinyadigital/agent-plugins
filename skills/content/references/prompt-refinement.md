---
type: prompt-refinement-notes
source: steward/docs/prompt-refinement-notes.md
date: 2026-04-13
status: iteration-1
---

# Prompt refinement notes

Vision and caption prompt quality rationale — ported from steward. Use when refining
`analyse-media` and `write-captions` skills. Quality checklists below belong in each
skill's review criteria.

---

## Vision / analyse-media

### Issues identified in initial prompt review

**1. Missing Australian seasonal context**

The original prompt had no guidance on seasons specific to NSW's mid-north coast. Without
this, the model applies Northern Hemisphere assumptions: green lush grass = spring, golden
grass = autumn/fall. In subtropical NSW, the opposite is often true:

- Lush green pasture → winter or early autumn (post-summer recovery)
- Yellow/brown parched grass → summer (dry season)
- Active wildflowers → spring

**Fix:** Explicit Australian seasonal guidance with climate cues. Golden hour is year-round.

**2. Subject selection lacked specificity guidance**

**Fix:** 1–4 subjects; "drone aerial" only for overhead shots; prefer specific over generic.

**3. Description guidance was too generic**

**Fix:** Brand voice examples with good/bad contrast; "we are building this, not arrived".

**4. Alt text guidance was vague**

**Fix:** Required elements: primary subject, visual elements, setting, mood + example.

**5. No quality score rubric**

**Fix:** Five bands (0.0–1.0); example anchored at 0.75 not 0.0.

**6. Publishable criteria were too vague**

**Fix:** Binary technical criteria; documentary shots valuable even when unpolished.

### Quality checks (analyse-media)

| Check | What to look for |
| ----- | ---------------- |
| Subjects | Specific (e.g. "Dexter cattle") not generic ("wildlife") |
| Season | Consistent with NSW climate cues |
| Description | Honest, "we are building" register |
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

**Fix:** Include "farm fresh", "paddock to plate", "sustainable future".

**4. Shared opening words across variants**

**Fix:** Never repeat opening word/phrase across caption_a/b/c.

**5. Channel copy guidance thin**

**Fix:** google_post = discovery intent; email_excerpt = momentum without "click here".

### Quality checks (write-captions)

| Check | What to look for |
| ----- | ---------------- |
| Variant differentiation | Three distinct editorial angles |
| Brand voice | First person plural; establishing phase honest |
| Clichés | None from brand-voice avoid list |
| Hashtags | Not embedded in caption body |

---

## Iteration log

| Iteration | Date | Changes |
| --------- | ---- | ------- |
| 1 | 2026-04-13 | Initial refinement (steward SW-06-07) |
| 2 | 2026-07-04 | Ported to digital-agency content discipline |
