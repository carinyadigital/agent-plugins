# Search optimisation conventions

Canonical rules for paths, target resolution, issue labels, and skill boundaries.
All `search-optimisation` skills read this file when resolving paths or routing
near-miss requests.

## Target resolution

Resolve the website or app target in this order:

1. **Explicit path or URL** named by the user in the request.
2. **Inside a target repo** — `config/target.json` at working root → read
   `productionUrl`, content seed paths, and squad label conventions.
3. **Instance target config** — `config/targets/{target}.json` in the instance repo.
4. **Inspect project** — infer production URL from deployment config or ask the user.

Default audit URL is the resolved production URL. Override with `--url` on
`technical-seo-audit`.

## SEO work documents

Default path: `docs/work/seo/` on the target repo `docs/` tree (binding lives in `config/target.json`).

Override when the user names a path explicitly or when target config defines an SEO
work directory.

Keyword research writes `keyword-research-{topic}.md` under that directory.
Technical audits may write `technical-seo-audit-{YYYY-MM-DD}.md` as an audit trail
when no GitHub issues are created.

## GitHub issue conventions

Technical findings are filed as GitHub issues — not implementation PRs.

| Field | Default |
| ----- | ------- |
| Title prefix | `[SEO]` |
| Recommendation label | `type:seo-recommendation` |
| Owning squad label | From target or instance squad charter (e.g. `squad:site`, `squad:blog`) |

Read squad charter and label conventions from the instance repo when present. Ask
the user when labels are undefined.

## Companion practice (delivery)

For competitive landscape analysis, invoke the companion skill directly — do not
bundle a local copy:

| Need | Invoke |
| ---- | ------ |
| Competitive landscape brief | `/product-management:competitive-brief` |

Recommend `product-management` as a co-install. Document in CONNECTORS.md.

## Optional companion (content-marketing)

`content-seo-review` operates on drafted content — often content produced by
`content-marketing`. Neither practice requires the other:

- Paste or reference content directly for SEO review without `content-marketing`.
- `content-marketing` can produce content without an SEO review pass.

When both are installed, review seed PRs from `/content-marketing:draft-post` or
`/content-marketing:draft-recipe` and link keyword targets from
`/search-optimisation:keyword-research`.

## Content seeds

Seed paths are target-specific. Resolve in this order:

1. **Explicit path** named by the user (PR URL or seed file path).
2. **`config/targets/{target}.json`** — content seed paths for posts and pages.
3. **Inspect target repo** — read CMS collection config and established seed directory.

## Skill routing

| User intent | Skill |
| ----------- | ----- |
| Keyword research for a topic | **keyword-research** |
| Production site technical audit | **technical-seo-audit** |
| On-page SEO review of content seeds | **content-seo-review** |
| Competitive landscape | `/product-management:competitive-brief` (companion) |
| Draft blog or recipe content | `/content-marketing:draft-post` or `draft-recipe` (optional companion) |
| Implement SEO fixes in code | Engineering practice — issues only from this practice |
