# Documentation style guide

The **mechanical layer** of documentation style: how docs *format*. Everything here is objective and rule-based. Its judgement companion is `<resolved-brand-path>/brand-voice.md` when that artefact exists — this plugin does not bundle a voice file.

**Base guide: follow the [Google developer documentation style guide](https://developers.google.com/style) except where noted below.** Google covers the cases this file doesn't; the exceptions and additions below are the agency overlay.

## Exceptions to Google

- **Australian/UK spelling, always.** organise, colour, centre, licence (noun), analyse, catalogue, -ise not -ize. Google defaults to US spelling; we override it.
- **Sentence case for all headings and titles.** "Set up your environment", not "Set Up Your Environment".
- **No emoji** in docs. For status and inline signalling use these Unicode symbols instead: `✓` success, `✗` failure, `!` alert/warning, `-` neutral, `+` change/addition.
- **Dates as "4 September 2026"** (day month year, no leading zero on the day). Prefer 24-hour time.

## Brand voice (judgement, not bundled)

Read `<resolved-brand-path>/brand-voice.md` the same way content-marketing does. Resolve the brand directory in this order:

1. **Explicit path named by the user** in the request.
2. **Inside an instance repo** — `config/instance.json` at working root → `<instance-root>/brand/`.
3. **Inside a target repo** — `config/target.json` at working root → resolve instance root, then `<instance-root>/brand/`.
4. **Standalone** — no instance or target pointer → `docs/brand/` in the current project.

If `brand-voice.md` is absent, ask for tone guidance inline and apply this style guide. Do not require the brand-creative plugin to be installed. Do not invent a bundled voice file.

## Page structure

Every content page follows this skeleton:

1. **Front matter** — see the contract below.
2. **Opening paragraph** — one or two sentences stating what this page is for.
3. **Body** — organised by the doc's [Diátaxis](diataxis-structure.md) type. For how-to and tutorial pages, follow **Why → What → How → References** (why you'd do this, what you'll end up with, the steps, where to go next).
4. **Expected output** — after any command, show what success looks like.
5. **See also** — a short list of related pages with one-line descriptions.

Keep one topic per document. If a page grows past ~3 H2 sections or ~800 words, split it — a long page is a structural failure, not thoroughness.

## Front-matter contract

Every doc carries YAML front matter (the fields drift detection reads for freshness):

```yaml
---
title: Set up your development environment   # sentence case, action-oriented
purpose: Get a new engineer from clone to running locally.
audience: Engineers new to the repo
owner: docs-owner                            # team or CODEOWNERS pointer
status: current                               # draft | current | deprecated
last_reviewed: 2026-09-04                      # ISO date; drives the 90-day freshness check
---
```

## Headings

- H1 comes from the front-matter `title` — never write a second H1 in the body.
- H2 (`##`) for top-level sections, imperative where the page is task-oriented ("Install Node.js", "Verify your setup").
- H3 (`###`) only when a section genuinely needs sub-steps.
- Never use an abstract-noun heading where an imperative fits — "Install Node.js", not "Prerequisites"; "Authenticate to npm", not "Configuration".

## Links

- **Descriptive link text**, never "click here" or a bare URL: `[Set up your environment](../how-to/set-up-your-environment.md)`.
- **Relative paths** for internal links within the repo.
- Cross-link generously in a "See also" footer (supports Diátaxis: link deep content rather than inlining it).

## Code blocks

- Always tag the language (`bash`, `tsx`, `ini`, `json`, …).
- Add `title="filename"` when a block shows a file's contents (for example `title="~/.npmrc"`).
- After an install/setup command, show a verification step with expected output.
- **No secrets.** Never embed a real credential, token, or connection string — use a placeholder like `<PROJECT_ID>` or `<API_TOKEN>`.
- Examples must be runnable, or explicitly marked `// pseudo-code`.
- Keep code blocks under ~40 lines; one per section where possible.

## Tables

Use tables for reference data — commands, options, environments, constraints. Keep cells short and scannable; no paragraphs inside a cell.

## Diagrams

Commit the diagram source (Mermaid or PlantUML) alongside any rendered image, so the diagram can be regenerated and reviewed as text.

## What a linter covers vs what judgement covers

The machine-checkable subset of this guide — AU spelling, sentence-case headings, no emoji, descriptive link text, readability grade — is delegated to Vale when the target repo has it configured, otherwise to the built-in fallbacks in [`linters.md`](linters.md). Anything a linter can't check — is this the right content type, does the tone fit brand-voice.md — is the judgement layer's job.
