# Brand voice — discover mode

Orchestrate discovery of brand materials across connected enterprise platforms.
Produce a structured discovery report with ranked sources, conflicts, and open
questions.

Read [SKILL.md](../SKILL.md) and [../references/brand-conventions.md](../../references/brand-conventions.md).

## Orient the user

Before starting, briefly explain:

1. **Search** — connected platforms for style guides, decks, templates, transcripts
2. **Analyze** — categorize, rank, and note conflicts
3. **Next** — `brand-voice write` from the report; optional `brand-guide write` for visual sources

Wait for confirmation unless the user already invoked discover explicitly.

## Settings

Read `docs/brand/brand.local.md` if present: company name, enabled platforms,
search depth, known material URLs.

## Validate platform coverage

**Document platforms** (formal brand docs): ~~knowledge base (Notion), Atlassian
(Confluence), file storage if connected.

**Supplementary**: ~~chat (Slack), ~~meeting transcription (Fireflies), ~~design
(Figma).

Rules:

1. If zero document platforms connected: stop and ask user to connect at least one
   or provide files manually.
2. If no primary file storage: warn but proceed.
3. If only one platform: warn about lower confidence; proceed.

## Confirm scope

Briefly confirm: platforms to search, include transcripts or documents only,
known locations to prioritize.

## Search

Search connected MCP tools in parallel for:

- Brand guidelines, style guide, voice and tone, messaging framework
- Pitch decks, proposal templates, marketing one-pagers
- Figma files named brand, style, design system
- Slack channels or threads tagged brand/marketing (supplementary)

Use company name from settings or user input in queries.

## Output

1. Fill [assets/discovery-report.template.md](../assets/discovery-report.template.md)
2. Save to `docs/brand/discovery-report.md` unless user asks for session-only
3. Present summary: sources found, key elements, conflicts, open questions
4. Offer: `brand-voice write`, resolve questions, expand search

## Error handling

- Empty results → flag low coverage; suggest manual upload or broader search
- Permission errors on a platform → note gap; continue with others
