# Brand voice — write mode

Generate or regenerate brand voice guidelines from discovery report, seed docs,
or user context.

Read [SKILL.md](../SKILL.md), [references/voice-constant-tone-flexes.md](../references/voice-constant-tone-flexes.md),
and [references/confidence-scoring.md](../references/confidence-scoring.md).

## Path

Resolve `<brand-dir>` per [brand-conventions.md](../../references/brand-conventions.md).
Default artefact: `<brand-dir>/brand-voice.md`. If the user names another path, use it.

## Arguments

Mode is `write`. Optional: `--from discovery-report|docs|transcripts|context`.

## Context

<artifacts>
[Discovery report, seed docs, transcripts, instance profile tone hints, user notes.]
</artifacts>

## Steps

1. Read all sources; prefer `<brand-dir>/discovery-report.md` when `--from discovery-report`
2. Fill [assets/brand-voice.template.md](../assets/brand-voice.template.md)
3. Separate voice constants from tone flexes ([voice-constant-tone-flexes.md](../references/voice-constant-tone-flexes.md))
4. Include terminology table and messaging pillars with examples
5. List open questions with agent recommendations — never dead ends
6. Assign confidence per section ([confidence-scoring.md](../references/confidence-scoring.md))
7. Delete the `DRAFTING AIDE` block before saving

## Output

Markdown with YAML frontmatter. Save to the resolved path.
