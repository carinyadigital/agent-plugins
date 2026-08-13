<!--
TEMPLATE — do not write user data here.

This file ships with the plugin and shows the structure the practice config should have.
It is replaced on every plugin update. Never write user data here.

The `setup` skill copies or updates the user config at:
  ~/.claude/plugins/config/digital-agency/engineering/CLAUDE.md

Instance-wide org facts live in the instance repo at:
  <instance-repo>/config/instance.json

Engineering artefacts (`docs/work/`, `reviews/`) live in the target repo.
`reviews/` is gitignored local state.
Architecture (`docs/architecture/`) is owned by the `architecture` companion.
Repo binding stays in `config/target.json`.
Brand guide is read from the resolved brand path — see references/engineering-conventions.md.
-->

# Web Development — Practice Profile

*Written by `/engineering:setup` or initialized on first use.*

---

## Status

`template` — run `/engineering:setup` to fill this in.

## Who's using this

- **Default persona:** [PLACEHOLDER — frontend-engineer | senior-frontend-engineer | principal-frontend-engineer | qa-engineer | webops-engineer | merged]
- **Team size:** [PLACEHOLDER — solo | small | multi-squad]

---

## Target binding

- **Target repo:** [PLACEHOLDER — path or slug from config/target.json]
- **Instance root:** [PLACEHOLDER — resolved instance path or none]
- **Binding status:** [PLACEHOLDER — bound | standalone | pending]

---

## Tech stack

- **Framework:** [PLACEHOLDER — e.g. Next.js App Router, React, Vue]
- **Language:** [PLACEHOLDER — e.g. TypeScript]
- **Styling:** [PLACEHOLDER — e.g. Tailwind CSS]
- **CMS / backend:** [PLACEHOLDER — e.g. Payload, headless CMS, none]
- **Database:** [PLACEHOLDER — e.g. Postgres via Neon, local Docker]
- **Test runner:** [PLACEHOLDER — e.g. Vitest, Playwright]

---

## Deployment platform

- **Hosting:** [PLACEHOLDER — e.g. Vercel, Netlify, self-hosted]
- **CI/CD:** [PLACEHOLDER — e.g. GitHub Actions, GitLab CI]
- **Observability:** [PLACEHOLDER — e.g. Sentry, Datadog, none configured]

---

## Available integrations

| Integration | Status | Fallback if unavailable |
| ----------- | ------ | ----------------------- |
| Source control | [✓ / ✗] | Manual branch paths |
| Hosting / deploy | [✓ / ✗] | Local build instructions |
| Chat | [✓ / ✗] | Paste status in chat |
| Project tracker | [✓ / ✗] | Manual issue references |
| Observability | [✓ / ✗] | Manual log paste |

*Re-check: `/engineering:setup --check-integrations`*

---

## Persona preference

- **Frontend Engineer surface:** [PLACEHOLDER — primary | secondary | merged]
- **Senior Frontend Engineer surface:** [PLACEHOLDER — primary | secondary | merged]
- **Principal Frontend Engineer surface:** [PLACEHOLDER — primary | secondary | merged]
- **QA Engineer surface:** [PLACEHOLDER — primary | secondary | merged]
- **WebOps Engineer surface:** [PLACEHOLDER — primary | secondary | merged]

When merged, greet as a single engineering partner and route internally to the right skill.

---

## Known gaps / things to revisit

-

---

*Re-run: `/engineering:setup --redo`*
