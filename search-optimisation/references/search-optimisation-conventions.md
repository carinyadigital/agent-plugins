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

## Recommendation tracker

Findings are filed as tracker items, never as implementation PRs. The practice
profile's **Recommendation tracker** section picks the tracker; GitHub issues are
the default when it is unset.

| Field | GitHub issues (default) | Linear |
| ----- | ----------------------- | ------ |
| Title prefix | `[SEO]` | `[SEO]` |
| Recommendation label | `type:seo-recommendation` | Label named in profile (e.g. `SEO`) |
| Owner label | Squad label from charter (e.g. `squad:site`) | Workstream label from profile (e.g. `Content`, `Bug`) |
| Landing state | Open, unassigned | `Triage` when the team has triage enabled; otherwise the fallback status in the profile (e.g. `Backlog`) |

Rules for every filed item:

- **Search before filing.** Match on title prefix plus the root cause. Comment on
  the existing open item with new evidence rather than filing a duplicate.
- **One root cause per item.** Group pages that share one generator or template
  bug into a single item with example URLs.
- **Never** assign, set priority, change another item's status, or close items.
  Humans promote out of triage.
- Body: evidence (URL, observed value, source and date), impact, recommended fix,
  and which surface owns it (content vs code).

Read squad charter and label conventions from the instance repo when present. Ask
the user when labels are undefined.

## Workstreams and run state

The `seo-agency` agent runs four workstreams. Each one maps to a skill:

| Workstream | Skill | Default cadence |
| ---------- | ----- | --------------- |
| Technical audit | `technical-seo-audit` | Weekly |
| Keyword and content strategy | `keyword-research` + `content-seo-review` | Monthly |
| Local and authority building | `local-authority` | Monthly |
| Metrics and measurement | `search-metrics` | Weekly snapshot, monthly report |

The profile can override cadences. Run state lives at
`docs/work/seo/agency-state.json` on the target repo:

```json
{
  "lastRun": "2026-10-20",
  "workstreams": {
    "technical-audit": { "lastRun": "2026-10-20", "openItems": ["WEB-41"] },
    "keyword-content": { "lastRun": "2026-10-06", "lastTopic": "syntropic-agroforestry" },
    "local-authority": { "lastRun": "2026-10-06" },
    "metrics": { "lastSnapshot": "2026-10-20", "lastReport": "2026-10-01" }
  }
}
```

Run reports go to `docs/work/seo/runs/{YYYY-MM-DD}.md`; metric snapshots to
`docs/work/seo/metrics/{YYYY-MM-DD}.json`.

## Data sources

Read [search-data-sources.md](./search-data-sources.md) before pulling figures from
Search Console, analytics, or SEO tools — connector first, signed-in browser
second (read-only), pasted export third.

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
| Local listings, citations, link prospects, outreach drafts | **local-authority** |
| Search KPIs, snapshots, monthly SEO report | **search-metrics** |
| Run all workstreams on a schedule | **seo-agency** agent |
| Competitive landscape | `/product-management:competitive-brief` (companion) |
| Draft blog or recipe content | `/content-marketing:draft-post` or `draft-recipe` (optional companion) |
| Implement SEO fixes in code | Engineering practice — issues only from this practice |
