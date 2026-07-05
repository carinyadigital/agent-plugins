# Brand voice — refine mode

Patch brand voice guidelines after team input or review findings.

Read [SKILL.md](../SKILL.md) and [references/confidence-scoring.md](../references/confidence-scoring.md).

## Path

Resolve `<brand-dir>` per [brand-conventions.md](../../references/brand-conventions.md).
Default artefact: `<brand-dir>/brand-voice.md`. If the user names another path, use it.

## Arguments

Mode is `refine`. Optional: `--section voice|tone|terminology|messaging|examples`.

## Steps

1. Read brand-voice.md and user/refinement context
2. Apply targeted section updates only when `--section` given; otherwise full pass
3. Resolve or update open questions with recommendations
4. Update confidence scores when evidence changes
5. Delete the `DRAFTING AIDE` block before saving

## Output

Updated brand-voice.md plus change summary in chat.
