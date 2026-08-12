# Content conventions

Canonical rules for paths, brand consumption, and skill boundaries. All
`content-marketing` skills read this file when resolving paths or routing
near-miss requests.

## Brand voice (artifact consumption)

Before generating customer-facing copy, read `<resolved-brand-path>/brand-voice.md`.
Resolve the brand directory using the same order as `brand-creative` conventions:

1. **Explicit path named by the user** in the request.
2. **Inside an instance repo** — `config/instance.json` at working root →
   `<instance-root>/brand/`.
3. **Inside a target repo** — `config/target.json` at working root →
   resolve instance root, then `<instance-root>/brand/`.
4. **Standalone** — no instance or target pointer → `docs/brand/` in the current
   project.

When `config/instance.json` defines `brand.voice` or related paths, treat them as
relative to the instance root unless the user overrides.

If `brand-voice.md` does not exist, ask the user for tone guidance inline — do not
require `brand-creative` to be installed. Do not bundle or invoke the brand-voice
skill; read the artefact directly and match its guidance.

Optional brand files (when present): `brand/taxonomy.md`, `brand/hashtags.md`,
`brand/seasonal-calendar.md` — paths relative to the resolved brand directory or
as keyed in `config/instance.json`.

## Companion practice (delivery)

For backlog alignment and research synthesis, invoke companion skills directly — do
not bundle local copies:

| Need | Invoke |
| ---- | ------ |
| Content epic registry, backlog alignment | `/product-management:tasks --product` |
| Research themes for planning | `/product-management:synthesize-research` |

Recommend `product-management` (backlog and research synthesis) as co-installs. Document in CONNECTORS.md.

## Content calendar

Default path: `docs/content/content-calendar.md` in the instance repo or target
repo `docs/` tree.

Write new and updated calendars under `docs/content/`.

Override when the user names a path explicitly or when
`config/targets/{target}.json` defines a content calendar path.

## Content seeds (CMS drafts)

Seed JSON paths are target-specific. Resolve in this order:

1. **Explicit path** named by the user.
2. **`config/targets/{target}.json`** — content seed paths for posts and recipes.
3. **Inspect target repo** — read CMS collection config (e.g. Payload collections)
   and place seeds under the project's established seed directory.

Draft skills produce seed JSON in a PR only — never merge, publish, or run import
scripts without explicit human instruction.

## Social content pipeline

Media analysis, caption variants, curation, and editorial selection produce
structured JSON for review. Scheduling and publishing are human gates outside these
skills.

## Skill routing

| User intent | Skill | Persona |
| ----------- | ----- | ------- |
| Monthly editorial plan | **content-calendar** | Content Strategist |
| Rank social inventory | **curate-content** | Content Strategist |
| Vision/media tags | **analyse-media** | Shared |
| Caption variants | **write-captions** | Content Writer |
| Select best caption | **edit-content** | Content Writer |
| Blog post seed | **draft-post** | Content Writer |
| Recipe seed | **draft-recipe** | Content Writer |
| Backlog alignment | `/product-management:tasks --product` | Content Strategist (companion) |
| Research for planning | `/product-management:synthesize-research` | Content Strategist (companion) |

## Personas

Two personas share one skill library. Choose the default persona during
`setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Content Strategist** | `content-calendar`, `curate-content` | Planning — what to produce and when |
| **Content Writer** | `draft-post`, `draft-recipe`, `write-captions`, `edit-content` | Production — drafts for review |
| **Shared (both)** | `analyse-media` | Media analysis for any pipeline stage |

Invoke skills directly — there is no separate agent plugin per persona:

```
/content-marketing:content-calendar write
/content-marketing:draft-post my-post-slug
/content-marketing:write-captions
```
