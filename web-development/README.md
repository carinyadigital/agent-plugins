# web-development

Root-level **practice plugin** — one install delivers the complete web engineering
service: setup interview, architecture, epic design, implementation, code review, QA,
and platform operations. Self-contained under the MECE practice model: edit skills
here only; nothing is vendored from elsewhere.

Install standalone or after `agency-hub:setup` recommends it. Declare
`delivery-practice` as a **companion practice** for backlog, tasks, sprint, and
validate — invoke `/delivery-practice:tasks --product` and related skills directly rather
than bundling duplicate copies.

## Personas

Six personas share one skill library. Choose the default persona during
`setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Frontend Engineer** | `implement`, `code-review-fix`, `merge-request`, `ux-design-fix` | Build — UI, client state, styling |
| **Senior Frontend Engineer** | `code-review`, `design`, `ux-design-review` | Peer review — diffs vs design and AC |
| **Principal Frontend Engineer** | `final-code-review`, `code-review`, `design` | Final gate — architecture and AC on open PRs |
| **Principal Architect** | `solution`, `adr`, `design`, `docs-review` | Architecture — solution, ADRs, epic design |
| **QA Engineer** | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Validation — automated and exploratory QA |
| **WebOps Engineer** | `deploy-qa`, `debug`, `platform-health` | Platform — CI/CD, deploy, health |

Invoke skills directly — there is no separate agent plugin per persona:

```
/web-development:implement CHK01-01
/web-development:code-review feat/checkout
/web-development:solution
/web-development:deploy-qa feat/my-branch
```

For planning cadence during implementation, invoke the companion practice:

```
/delivery-practice:backlog-refine
/delivery-practice:tasks checkout-foundation
/delivery-practice:sprint-planning 3
/delivery-practice:validate checkout-foundation
```

## First run: setup

After instance bootstrap (or standalone):

```
/web-development:setup
```

| Flag | Behaviour |
| ---- | --------- |
| `--quick` | Tech stack defaults + deployment platform; skip deep interview |
| `--full` | Full interview including persona preference and connector audit |
| `--redo` | Re-run web development setup only; overwrite on confirmation |
| `--resume` | Continue a paused interview |
| `--check-integrations` | Report MCP connector status only; no interview |

`setup` detects or creates `.agency/target.json` for Golden Path 2
target binding.

## Skills

| Skill | Purpose |
| ----- | ------- |
| **setup** | Interview → write practice profile, target binding, stack defaults |
| **solution** | write — `docs/architecture/solution.md`; review via `docs-review` |
| **adr** | plan, write, review — `docs/architecture/decisions/` |
| **design** | write — `docs/work/{work-id}/design.md`; review via `docs-review` |
| **implement** | Implement a task against approved design and AC |
| **code-review** | Read-only peer review against design and tasks |
| **code-review-fix** | Address code-review findings without behaviour change |
| **final-code-review** | Final technical gate on open PRs |
| **merge-request** | Open merge request for implemented work |
| **merge-request-babysit** | Drive an open MR/PR to merge-ready |
| **merge-request-review** | Review an MR/PR as its reviewer |
| **ux-design-review** | Read-only UX review of implemented UI vs design source |
| **ux-design-fix** | Address UX review findings or direct UI fixes |
| **ralph-loop-setup** | Seed and configure an autonomous delivery loop |
| **ralph-loop** | Run an autonomous work-item delivery loop |
| **docs-review** | Read-only document-set quality and consistency review |
| **debug** | Bug investigation |
| **tech-debt** | Technical debt audit |
| **deploy-qa** | Prepare QA workspace (shared by QA and WebOps personas) |
| **run-automated-suite** | Run automated tests in QA workspace |
| **exploratory-pass** | AC-driven exploratory validation |
| **document-defects** | Record defects from QA pass |
| **platform-health** | CI/CD, deploy, and platform health check |

Path, brand, and boundary rules: `references/web-development-conventions.md`.

## Brand guide (artifact consumption)

UI skills read `<resolved-brand-path>/brand-guide.md` directly — no bundled
`brand-guide` skill and no install dependency on `brand-creative`. If the file does
not exist, ask the user for design guidance inline.

## Prerequisites

- **Instance profile** (optional) — `agency-hub:setup` writes
  `config/instance.json`; setup reads cadence and target hints without
  re-asking.
- **delivery-practice** (recommended companion) — tasks, backlog-refine, sprint-planning, sprint-retro, validate;
  see CONNECTORS.md.
- **Connectors** (optional) — source control, hosting, observability, and chat MCP
  servers supercharge deploy, QA, and platform-health workflows.

## After setup

1. Use Frontend Engineer skills for build; Senior/Principal FE for review gates.
2. Use Principal Architect skills upstream of implementation.
3. Use QA and WebOps skills for validation and platform operations.
4. Re-run `/web-development:setup --redo` to refresh engineering defaults.
5. Read brand-guide from the resolved brand path before every UI implementation task.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/web-development-conventions.md` — path resolution, personas, artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (owned by agency-hub; synced copy)

Meta-framework files (`instance-profile-template.md`, `setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.
