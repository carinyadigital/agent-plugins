# Brand voice — enforce mode

Apply existing brand voice guidelines to content creation. Load guidelines,
apply voice constants and tone flexes, validate output, explain brand choices.

Read [SKILL.md](../SKILL.md) and [references/voice-constant-tone-flexes.md](../references/voice-constant-tone-flexes.md).

## Load guidelines (stop at first hit)

1. **Session** — guidelines generated earlier in this conversation
2. **File** — `docs/brand/brand-voice.md` (or user-named path)
3. **Ask user** — suggest `brand-voice discover`, `brand-voice write`, or paste guidelines

Read `docs/brand/brand.local.md` for `strictness` (strict | balanced | flexible)
and `always_explain` (default true if unset).

## Analyze the request

Identify before writing:

- Content type (email, proposal, social post, Slack message, deck copy, etc.)
- Target audience (role, seniority, industry)
- Key messages and length constraints

## Apply

1. Voice constants — We are / We are not, terminology, messaging pillars
2. Tone flex — use tone-by-context matrix row for this content type
3. Generate content matching guideline examples in quality and style
4. Check open questions — if content touches unresolved item, note it and apply
   agent recommendation unless user overrides

## Validate and explain

After generating:

- Highlight which guidelines were applied
- Explain key voice and tone decisions
- Note adaptations for context
- When `always_explain` is true, include brand application notes

## Conflicts

When user request conflicts with guidelines:

1. Explain the conflict
2. Recommend an approach
3. Offer: follow strictly, adapt with explanation, or override

Default: adapt with explanation of tradeoff unless `strictness: strict`.

## Output

On-brand content in chat. Do not overwrite `brand-voice.md` unless user asks.
