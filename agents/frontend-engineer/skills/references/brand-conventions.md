# Brand conventions

Canonical rules for paths, artefacts, and skill boundaries. Skills under
`skills/brand/` should read this file when resolving paths or
routing near-miss requests.

## Document layout

```text
docs/brand/
├── brand-guide.md          # Visual identity — colors, type, logo, UI tokens
├── brand-voice.md          # Voice, tone, terminology, messaging
├── discovery-report.md     # Optional output from brand-voice discover
└── brand.local.md          # Gitignored firm settings (platforms, strictness)
```

Override paths when the user names them explicitly in the request.

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

Optional gitignored file at `docs/brand/brand.local.md`:

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
