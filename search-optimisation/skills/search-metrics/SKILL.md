---
name: search-metrics
description: >
  Define and measure search KPIs — organic clicks, impressions, average position,
  indexed pages, organic landing-page engagement, and the conversions organic search
  drives (enquiries, sign-ups). Takes a weekly snapshot or writes the monthly SEO report
  with movement against baseline and targets. Use for "how is SEO going", "search
  report", "organic traffic", "set SEO targets", or "measure SEO". Reads Search
  Console, analytics, and SEO tools via connector or signed-in browser. Do NOT use for
  product-wide metrics (metrics-review) or site defects (technical-seo-audit).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "[snapshot|report|define]"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: monitor-and-report
  output_class: decision-support
---

# Search metrics

You measure whether search work is paying off, and say plainly when the numbers are
too small to tell. Pass a mode: `snapshot` (default), `report`, or `define`.

Read [search-optimisation-conventions.md](../../references/search-optimisation-conventions.md)
and [search-data-sources.md](../../references/search-data-sources.md).

## When to use

- Weekly snapshot and monthly report (called by the `seo-agency` agent).
- The user asks how search is performing, or wants targets set.

## What this skill does not do

- Does not change analytics, Search Console, or tag settings — missing tracking
  becomes a tracker item.
- Does not estimate, extrapolate, or round up figures to make a trend.
- Does not attribute a change to a specific action unless the timing and pages line
  up; otherwise it says "cause not established".

## Preconditions

| Input | Location | On missing |
| ----- | -------- | ---------- |
| Search Console property | Practice profile | Record `not available` |
| Analytics property and key events | Practice profile | Record `not available` |
| Baseline and targets | Practice profile **Measurement** section | Mode `define` proposes them |
| Previous snapshots | `docs/work/seo/metrics/*.json` | First run sets the baseline |

## Trust spine

Every figure carries source, route, and window (see search-data-sources.md).
Comparisons are like-for-like windows. On a small base (under ~100 clicks or ~20
conversions in the window) report counts, not percentage change, and call movement
"not yet meaningful".

## Workflow

### `define`

1. Read the profile's business goals (enquiries, bookings, subscribers).
2. Propose a short KPI set: one outcome metric (conversions from organic search), two
   or three leading metrics (impressions, clicks, pages indexed, queries in top 10),
   and one health metric (indexing errors or audit errors).
3. Check each KPI is measurable today. If the conversion isn't tracked (for example
   analytics shows 0 key events), file a tracker item to set it up.
4. Present the set and draft targets for the person to confirm. Write them to the
   profile only after a yes.

### `snapshot`

1. Pull for the last 28 days vs the previous 28: GSC clicks, impressions, CTR,
   average position, top 10 queries and pages; pages indexed vs not indexed; GA4
   organic sessions, engaged sessions, and key events from organic; SEO-tool health
   score and referring domains if available.
2. Write `docs/work/seo/metrics/{YYYY-MM-DD}.json` (one object per metric with
   `value`, `previous`, `window`, `source`, `route`, or `notAvailable` with reason).
3. Flag anything that needs action now: a drop in indexed pages, a jump in audit
   errors, a page that lost most of its clicks.

### `report`

1. Read the month's snapshots and this month's workstream reports in
   `docs/work/seo/`.
2. Compare against baseline and targets. Separate signal from noise.
3. Answer first: one paragraph saying whether search is moving in the right
   direction and what matters most next month.

## Outputs

- `snapshot` → `docs/work/seo/metrics/{YYYY-MM-DD}.json`
- `report` → `docs/work/seo/search-report-{YYYY-MM}.md`:

```markdown
# Search report — {Month YYYY}

{Answer first: one paragraph.}

## Scorecard
| KPI | This period | Previous | Target | Source |

## What moved and why
## Top queries and pages
## Work done this month
Tracker items filed / resolved; content published; listings and links.
## Next month
Three priorities, each tied to a KPI.
## Data gaps
```
- `define` → proposed KPI table in the conversation; profile update on approval.
