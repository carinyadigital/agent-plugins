# Brand conventions

Canonical rules for paths, artefacts, and skill boundaries. All `brand-creative`
skills read this file when resolving paths or routing near-miss requests.

## Brand path resolution

Resolve the brand directory before reading or writing any artefact. Apply this
order — first match wins:

1. **Explicit path named by the user** in the request — highest priority; use
   that directory or file path.
2. **Inside an instance repo** — `config/instance.json` exists at the working
   root → `<instance-root>/brand/`.
3. **Inside a target repo** — `.agency/target.json` exists at the working
   root → read the pointer, resolve the instance root, then
   `<instance-root>/brand/`.
4. **Standalone** — no instance or target pointer → `docs/brand/` in the current
   project.

When `config/instance.json` defines `brand.voice` or related paths, treat them as
relative to the instance root unless the user overrides.

## Document layout

Artefacts relative to the resolved brand directory:

```text
<brand-dir>/
├── brand-guide.md          # Visual identity — colors, type, logo, UI tokens
├── brand-voice.md          # Voice, tone, terminology, messaging
├── discovery-report.md     # Optional output from brand-voice discover
└── brand.local.md          # Gitignored firm settings (platforms, strictness)
```

## Artefact boundaries

| Content | Belongs in | Not in |
| ------- | ---------- | ------ |
| Colors, fonts, logo, spacing, UI tokens | `brand-guide.md` | `brand-voice.md` |
| Voice, tone, messaging, terminology | `brand-voice.md` | `brand-guide.md` |
| Source triage, platform search results | `discovery-report.md` | final guides |
| On-brand copy (emails, posts, decks text) | inline output | either guide file |

## Skill routing

| User intent | Skill | Mode |
| ----------- | ----- | ---- |
| Style guide, colors, fonts, logo, UI tokens | **brand-guide** | write, review, refine |
| Find existing brand docs across platforms | **brand-voice** | discover |
| Generate or update voice guidelines | **brand-voice** | write, refine |
| Audit voice doc completeness | **brand-voice** | review |
| Write email/post/proposal in our voice | **brand-voice** | enforce |
| Which brand skill to use | **brand-voice** (no mode) | orient |

## Settings (`brand.local.md`)

Optional gitignored file at `<brand-dir>/brand.local.md` (see path resolution above):

```yaml
company: Example Co
platforms:
  notion: true
  atlassian: true
  figma: true
  slack: true
search_depth: standard  # or deep
strictness: balanced    # strict | balanced | flexible (enforce mode)
always_explain: true
known_materials:
  - url or path to existing style guide
```

## Typical flow

```text
brand-voice discover → brand-voice write → brand-voice review
                              ↓
                    (team resolves open questions)
                              ↓
                    brand-voice refine → brand-voice enforce (ongoing)

brand-guide write  (parallel or after Figma/design sources)
```
