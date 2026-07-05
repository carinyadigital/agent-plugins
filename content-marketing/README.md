# content-marketing

Root-level **practice plugin** — one install delivers the complete content service:
setup interview, editorial calendar, social curation, media analysis, and CMS seed
drafting. Self-contained under the MECE practice model: edit skills here only; nothing
is vendored from elsewhere.

Install standalone or after `agency-hub:agency-setup` recommends it. Declare
`delivery-practice` as a **companion practice** for backlog and research synthesis —
invoke `/delivery-practice:backlog` and `/delivery-practice:synthesize-research`
directly rather than bundling duplicate copies.

## Personas

Two personas share one skill library. Choose the default persona during
`practice-setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Content Strategist** | `content-calendar`, `curate-content` | Planning — calendar, briefs, inventory |
| **Content Writer** | `draft-post`, `draft-recipe`, `write-captions`, `edit-content` | Production — drafts for review |
| **Shared (both)** | `analyse-media` | Media analysis for any pipeline stage |

Invoke skills directly — there is no separate agent plugin per persona:

```
/content-marketing:content-calendar write
/content-marketing:draft-post my-post-slug
/content-marketing:curate-content inventory.json
```

For backlog alignment and research themes, invoke the companion practice:

```
/delivery-practice:backlog review
/delivery-practice:synthesize-research
```

## First run: practice-setup

After instance bootstrap (or standalone):

```
/content-marketing:practice-setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Primary channels default + one seed source; skip deep interview |
| `--full` | Full interview including persona preference |
| `--redo` | Re-run content setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **practice-setup** | Interview → write practice profile and content defaults |
| **content-calendar** | write, review — editorial calendar and slot briefs |
| **curate-content** | Rank social inventory for upcoming posts |
| **analyse-media** | Vision analysis — subjects, season, mood, quality |
| **write-captions** | Caption variants + channel copy |
| **edit-content** | Select or lightly edit best caption variant |
| **draft-post** | Blog post seed JSON for CMS import |
| **draft-recipe** | Recipe seed JSON for CMS import |

Path, brand, and boundary rules: `references/content-conventions.md`.

## Brand voice (artifact consumption)

Content skills read `<resolved-brand-path>/brand-voice.md` directly — no bundled
`brand-voice` skill and no install dependency on `brand-creative`. If the file does
not exist, ask the user for tone guidance inline.

## Optional companion (search-optimisation)

Content seeds produced by `draft-post` and `draft-recipe` can be reviewed for on-page
SEO via `/search-optimisation:content-seo-review`. Neither practice requires the other
installed — document the optional pairing in both READMEs rather than a hard dependency.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:agency-setup` writes
  `config/instance.json`; practice-setup reads business identity and house tone hints
  without re-asking.
- **delivery-practice** (recommended companion) — backlog and research synthesis;
  see CONNECTORS.md.
- **Connectors** (optional) — source control for seed PRs; CMS and social scheduling
  tools when connected supercharge distribution workflows.

## After setup

1. Use Content Strategist skills for planning; Content Writer skills for drafts.
2. Re-run `/content-marketing:practice-setup --redo` to refresh content defaults.
3. Read brand voice from the resolved brand path before every customer-facing draft.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/content-conventions.md` — path resolution, personas, artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; synced copy)
- `references/prompt-refinement.md` — quality checks for analyse-media and write-captions

Meta-framework files (`instance-profile-template.md`, `practice-setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
