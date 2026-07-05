# Brand voice — write mode

Generate comprehensive brand voice guidelines from discovery reports, uploaded
documents, transcripts, or direct user input.

Read [SKILL.md](../SKILL.md), [references/voice-constant-tone-flexes.md](../references/voice-constant-tone-flexes.md),
and [references/confidence-scoring.md](../references/confidence-scoring.md).

## Path

Default: `docs/brand/brand-voice.md`. If the user names another path, use it.

## Arguments

Mode is `write`. Optional: `--from discovery-report|docs|transcripts|context`.

## Context

<artifacts>
[Discovery report, uploaded PDFs/decks, transcript excerpts, direct user input
about voice and values.]
</artifacts>

## Steps

1. Read all sources; prefer `docs/brand/discovery-report.md` when `--from discovery-report`
2. Extract voice attributes, messaging themes, terminology, tone guidance, examples
3. Fill [assets/brand-voice.template.md](../assets/brand-voice.template.md)
4. **We are / We are not** — minimum 4 rows with evidence; target 5–7
5. **Tone matrix** — minimum cold outreach, proposals, social media
6. Assign confidence per section ([confidence-scoring.md](../references/confidence-scoring.md))
7. Surface open questions with agent recommendations for unresolved ambiguity
8. Redact PII from all examples
9. Delete the `DRAFTING AIDE` comment block before saving
10. If file exists, archive prior version to `brand-voice-YYYY-MM-DD.md` in same directory

## Quality bar

Before presenting:

- All major sections populated or explicitly omitted with reason
- At least 3 voice attributes with evidence
- Terminology guide present when sources support it
- Source appendix complete

## Output

Save markdown with YAML frontmatter. Summarize in chat: confidence breakdown,
strongest attribute, open question count. Offer `brand-voice review` or `enforce`.
