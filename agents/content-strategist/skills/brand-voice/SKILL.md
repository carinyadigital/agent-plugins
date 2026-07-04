---
name: brand-voice
description: >
  Use for brand voice lifecycle: discover materials (discover), generate
  guidelines (write), audit completeness (review), patch after team input
  (refine), or apply voice to content (enforce). Triggers on "find brand
  guidelines", "generate brand voice", "style guide for copy", "write an email",
  "on-brand", "doesn't sound like us", "enforce voice", or "brand content audit".
  Default artefact docs/brand/brand-voice.md. Do NOT use for visual colors/fonts
  (brand-guide) or product strategy (product).
license: MIT
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
argument-hint: "<mode: discover|write|review|refine|enforce> [args...]"
---

# Brand voice

Voice, tone, messaging, and terminology for agents writing copy or reviewing
content.

## Conventions

Read [../references/brand-conventions.md](../references/brand-conventions.md) when
resolving paths, loading settings, or routing near-miss requests.

## Artefacts

| Mode | Default path |
| ---- | ------------ |
| `discover` | `docs/brand/discovery-report.md` (optional save) |
| `write`, `review`, `refine` | `docs/brand/brand-voice.md` |
| `enforce` | inline content (no file) |

## Path resolution

If the user names a different path, use it for read/write instead of defaults.

## Settings

Read `docs/brand/brand.local.md` when present for company name, enabled
platforms, search depth, `strictness`, and `always_explain`.

## Gotchas

- **No visual styling** — colors, fonts, logo rules belong in `brand-guide.md`.
- **Delete DRAFTING AIDE** block before saving guides.
- **Open questions** must include an agent recommendation — never dead ends.
- **Redact PII** from examples (customer names, emails, phone numbers).
- **enforce** loads guidelines in order: session → `brand-voice.md` → ask user.

## Supporting files

- [assets/brand-voice.template.md](assets/brand-voice.template.md)
- [assets/discovery-report.template.md](assets/discovery-report.template.md)
- [references/voice-constant-tone-flexes.md](references/voice-constant-tone-flexes.md)
- [references/confidence-scoring.md](references/confidence-scoring.md)

## Related skills

- `brand-guide` — visual identity

## Router

1. Mode: `discover`, `write`, `review`, `refine`, or `enforce`. If no mode given,
   orient the user (show modes and suggest next step from repo state).
2. Resolve paths (default or user override).
3. One prompt under [prompts/](prompts/).

| Mode | Prompt |
| ---- | ------ |
| discover | [prompts/discover.prompt.md](prompts/discover.prompt.md) |
| write | [prompts/write.prompt.md](prompts/write.prompt.md) |
| review | [prompts/review.prompt.md](prompts/review.prompt.md) |
| refine | [prompts/refine.prompt.md](prompts/refine.prompt.md) |
| enforce | [prompts/enforce.prompt.md](prompts/enforce.prompt.md) |

**write** — optional `--from discovery-report|docs|transcripts|context`.

**refine** — optional `--section voice|tone|terminology|messaging|examples`.

**enforce** — pass content request after mode token.
