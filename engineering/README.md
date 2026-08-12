# engineering

Root-level **practice plugin** — one install delivers the complete web engineering
service: setup interview, technical design (tdd), implementation, code review, QA,
and platform operations. Self-contained under the MECE practice model: edit skills
here only; nothing is vendored from elsewhere.

Install standalone or after practice `setup` (writes `config/instance.json` if absent) recommends it. Declare
`architecture` as a **companion practice** for `solution` / `adr`, and
`product-management` for backlog, tasks, sprint, and validate — invoke
`/architecture:solution` and `/product-management:tasks --product` directly rather
than bundling duplicate copies.

## Personas

Five personas share one skill library. Choose the default persona during
`setup` (merged for one-person shops; distinct for larger teams).

| Persona | Primary skills | Focus |
| ------- | -------------- | ----- |
| **Frontend Engineer** | `implement`, `code-review-fix`, `merge-request`, `ux-design-fix` | Build — UI, client state, styling |
| **Senior Frontend Engineer** | `code-review`, `tdd`, `ux-design-review` | Peer review — diffs vs design and AC |
| **Principal Frontend Engineer** | `final-code-review`, `code-review`, `tdd` | Final gate — architecture and AC on open PRs |
| **QA Engineer** | `deploy-qa`, `run-automated-suite`, `exploratory-pass`, `document-defects` | Validation — automated and exploratory QA |
| **WebOps Engineer** | `deploy-qa`, `debug`, `platform-health` | Platform — CI/CD, deploy, health |

System solution design and ADRs live in the **architecture** companion
(`/architecture:solution`, `/architecture:adr`).

Invoke skills directly — there is no separate agent plugin per persona:

```
/engineering:implement CHK01-01
/engineering:code-review feat/checkout
/engineering:tdd checkout-foundation
/engineering:deploy-qa feat/my-branch
```

For architecture and planning cadence:

```
/architecture:solution
/architecture:adr plan
/product-management:backlog-refine
/product-management:tasks checkout-foundation
/product-management:sprint-planning 3
/product-management:validate checkout-foundation
```

## First run: setup

After instance bootstrap (or standalone):

```
/engineering:setup
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
| **tdd** | write — `docs/work/{work-id}/tdd.md`; review via `docs-review` |
| **implement** | Implement a task against approved tdd.md and AC |
| **code-review** | Read-only peer review; state in `docs/reviews/` |
| **code-review-fix** | Address code-review findings without behaviour change |
| **final-code-review** | Final technical gate on open PRs |
| **merge-request** | Open merge request for implemented work |
| **merge-request-babysit** | Drive an open MR/PR to merge-ready |
| **merge-request-review** | Review an MR/PR as its reviewer |
| **docs-review** | Read-only document-set quality and consistency review |
| **debug** | Bug investigation |
| **tech-debt** | Technical debt audit |
| **deploy-qa** | Prepare QA workspace (shared by QA and WebOps personas) |
| **run-automated-suite** | Run automated tests in QA workspace |
| **exploratory-pass** | AC-driven exploratory validation |
| **document-defects** | Record defects from QA pass |
| **platform-health** | CI/CD, deploy, and platform health check |

Path, brand, and boundary rules: `references/engineering-conventions.md`.

## Brand guide (artifact consumption)

UI skills read `<resolved-brand-path>/brand-guide.md` directly — no bundled
`brand-guide` skill and no install dependency on `brand-creative`. If the file does
not exist, ask the user for design guidance inline.

## Prerequisites

- **Instance profile** (optional) — practice `setup` (writes `config/instance.json` if absent) writes
  `config/instance.json`; setup reads cadence and target hints without
  re-asking.
- **architecture** (recommended companion) — `solution`, `adr`; see CONNECTORS.md.
- **product-management** (recommended companion) — tasks, backlog-refine, sprint-planning, sprint-retro, validate;
  see CONNECTORS.md.
- **Connectors** (optional) — source control, hosting, observability, and chat MCP
  servers supercharge deploy, QA, and platform-health workflows.

## After setup

1. Use Frontend Engineer skills for build; Senior/Principal FE for review gates.
2. Use `/architecture:solution` / `/architecture:adr` upstream of implementation.
3. Use QA and WebOps skills for validation and platform operations.
4. Re-run `/engineering:setup --redo` to refresh engineering defaults.
5. Read brand-guide from the resolved brand path before every UI implementation task.

## References

- `references/practice-setup-framework.md` — invocation, config paths, interview structure
- `references/engineering-conventions.md` — path resolution, personas, artefact boundaries
- `references/instance-profile-template.md` — Tier 1 schema (canonical in brand-creative; synced copy)

Meta-framework files (`instance-profile-template.md`, `setup-framework.md`)
are kept in sync across practice plugins via `python3 scripts/sync-references.py`.

## Ralph loop contribution

This plugin contributes the `engineering-delivery` preset at `assets/ralph-presets/engineering-delivery.md`. Install the companion `ralph-loop` plugin to run loops; seed resolves this preset automatically when both plugins are installed side by side.
