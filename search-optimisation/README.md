# search-optimisation

Root-level **practice plugin** — one install delivers the complete search and
technical SEO service: setup interview, keyword research, production audits, and
content SEO review. Self-contained under the MECE practice model: edit skills here
only; nothing is vendored from elsewhere.

Install standalone or after practice `setup` (writes `config/instance.json` if absent) recommends it. Declare
`product-management` as a **companion practice** for competitive brief — invoke
`/product-management:competitive-brief` directly rather than bundling a duplicate copy.

## Persona

One persona owns the full skill library:

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **SEO Specialist** | `keyword-research`, `technical-seo-audit`, `content-seo-review`, `local-authority`, `search-metrics`; `seo-agency` agent | Research, audits, on-page review, local authority, measurement |

Invoke skills directly — there is no separate agent plugin:

```
/search-optimisation:keyword-research topic-slug
/search-optimisation:technical-seo-audit
/search-optimisation:content-seo-review <pr-url or seed path>
```

For competitive landscape input, invoke the companion practice:

```
/product-management:competitive-brief
```

## First run: setup

After instance bootstrap (or standalone):

```
/search-optimisation:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Default target site + one-off audit cadence |
| `--full` | Full interview including keyword themes and competitor set |
| `--redo` | Re-run SEO setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile and SEO defaults |
| **keyword-research** | Topic keyword docs with intent and content opportunities |
| **technical-seo-audit** | Production audit → GitHub issues |
| **content-seo-review** | On-page SEO review of content seeds |
| **local-authority** | Business listing, NAP consistency, link and citation prospects, outreach drafts |
| **search-metrics** | KPI definition, weekly snapshots, monthly search report |

## Agent

| Agent | Purpose |
| ----- | ------- |
| **seo-agency** | Scheduled orchestrator — gathers every reachable source, runs the due workstreams (technical audit, keyword and content, local and authority, metrics), files recommendations to tracker triage, writes `docs/work/seo/runs/{date}.md`. Recommends only. |

Run it as a weekly scheduled task on a device with the signed-in browser, with a
prompt such as: *"Run the search-optimisation seo-agency agent for {site}: read
`search-optimisation/agents/seo-agency.md` and follow it."*

Path, target, and boundary rules: `references/search-optimisation-conventions.md`.

## Optional companion (content-marketing)

`content-seo-review` often operates on content that `content-marketing` produced, but
neither practice requires the other installed. See CONNECTORS.md for the optional
pairing — paste or reference content directly when `content-marketing` is not present.

## Prerequisites

- **Instance profile** (optional) — practice `setup` (writes `config/instance.json` if absent) writes
  `config/instance.json`; setup reads business identity without re-asking.
- **product-management** (recommended companion) — competitive brief; see CONNECTORS.md.
- **Connectors** (optional) — source control for issues; Playwright for live site checks; Ahrefs for keyword and backlink data (requires subscription).

## After setup

1. Run `/search-optimisation:keyword-research` for priority topics.
2. Run `/search-optimisation:technical-seo-audit` on a cadence defined at setup.
3. Run `/search-optimisation:content-seo-review` on seed PRs before merge.
4. Re-run `/search-optimisation:setup --redo` to refresh SEO defaults.

## References

- `references/search-optimisation-conventions.md` — path resolution, tracker rules, workstreams, run state
- `references/search-data-sources.md` — connector → signed-in browser → pasted export; read-only browser rules
