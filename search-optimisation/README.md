# search-optimisation

Root-level **practice plugin** — one install delivers the complete search and
technical SEO service: setup interview, keyword research, production audits, and
content SEO review. Self-contained under the MECE practice model: edit skills here
only; nothing is vendored from elsewhere.

Install standalone or after `agency-hub:setup` recommends it. Declare
`delivery-practice` as a **companion practice** for competitive brief — invoke
`/delivery-practice:competitive-brief` directly rather than bundling a duplicate copy.

## Persona

One persona owns the full skill library:

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **SEO Specialist** | `keyword-research`, `technical-seo-audit`, `content-seo-review` | Research, audits, on-page review |

Invoke skills directly — there is no separate agent plugin:

```
/search-optimisation:keyword-research topic-slug
/search-optimisation:technical-seo-audit
/search-optimisation:content-seo-review <pr-url or seed path>
```

For competitive landscape input, invoke the companion practice:

```
/delivery-practice:competitive-brief
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

Path, target, and boundary rules: `references/search-optimisation-conventions.md`.

## Optional companion (content-marketing)

`content-seo-review` often operates on content that `content-marketing` produced, but
neither practice requires the other installed. See CONNECTORS.md for the optional
pairing — paste or reference content directly when `content-marketing` is not present.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:setup` writes
  `config/instance.json`; setup reads business identity without re-asking.
- **delivery-practice** (recommended companion) — competitive brief; see CONNECTORS.md.
- **Connectors** (optional) — source control for issues; Playwright for live site checks; Ahrefs for keyword and backlink data (requires subscription).

## After setup

1. Run `/search-optimisation:keyword-research` for priority topics.
2. Run `/search-optimisation:technical-seo-audit` on a cadence defined at setup.
3. Run `/search-optimisation:content-seo-review` on seed PRs before merge.
4. Re-run `/search-optimisation:setup --redo` to refresh SEO defaults.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/search-optimisation-conventions.md` — path resolution, labels, artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; synced copy)

Meta-framework files (`instance-profile-template.md`, `setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
