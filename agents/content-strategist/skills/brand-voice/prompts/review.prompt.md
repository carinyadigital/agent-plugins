# Brand voice — review mode

Audit brand voice guidelines for completeness, consistency, and enforceability.
Strengthen the document — do not validate uncritically.

Read [SKILL.md](../SKILL.md), [references/voice-constant-tone-flexes.md](../references/voice-constant-tone-flexes.md),
and [references/confidence-scoring.md](../references/confidence-scoring.md).

## Path

Default: `docs/brand/brand-voice.md`. If the user names another path, review that file.

## Context

<artifacts>
[Required: brand-voice.md. Optional: discovery-report.md, brand-guide.md for boundary check.]
</artifacts>

## Steps

1. Read brand-voice.md and context
2. Apply review criteria below
3. For each finding: gap, recommendation, amend where clear
4. Update `status: Reviewed` and `last_updated` in frontmatter
5. Report verdict in chat

## Review criteria

- **We are / We are not** — 4+ rows, counters meaningful, evidence cited
- **Voice vs tone** — voice constant; tone flexes in matrix only
- **Tone matrix** — covers minimum contexts with concrete guidance
- **Terminology** — must-use and avoid lists actionable
- **Examples** — on-brand and off-brand samples when section present
- **Confidence scores** — match evidence in appendix
- **Open questions** — each has agent recommendation
- **Boundary** — no visual specs (colors/fonts) that belong in brand-guide.md
- **Enforceability** — an agent could write copy without guessing

## Output

Updated file (if amendments made) plus review summary in chat.
