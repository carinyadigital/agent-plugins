# Brand voice — refine mode

Patch brand voice guidelines after team resolves open questions or new sources
arrive. Update, do not re-author.

Read [SKILL.md](../SKILL.md) and [references/confidence-scoring.md](../references/confidence-scoring.md).

## Path

Default: `docs/brand/brand-voice.md`. If the user names another path, use it.

## Arguments

Mode is `refine`. Optional: `--section voice|tone|terminology|messaging|examples`.

## Context

<artifacts>
[Required: brand-voice.md. Optional: resolved open questions, new transcripts,
discovery-report updates, --context notes.]
</artifacts>

## Steps

1. Read brand-voice.md and context
2. If `--section` given, limit edits to that section; otherwise patch all resolved items
3. Close or update open questions with team decisions
4. Re-score confidence for touched sections
5. Bump `version` (patch), `last_updated`, set `status: Current`
6. Report changes in chat

## Quality rules

- Every change traceable to team decision or new source
- Surgical edits — preserve stable terminology where possible
- Redact PII in new examples

## Output

Updated brand-voice.md plus change summary in chat.
