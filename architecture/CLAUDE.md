<!--
TEMPLATE — do not write user data here.

This file ships with the plugin and shows the structure the practice config should have.
It is replaced on every plugin update. Never write user data here.

The `setup` skill copies or updates the user config at:
  ~/.claude/plugins/config/digital-agency/architecture/CLAUDE.md

Instance-wide org facts live in the instance repo at:
  <instance-repo>/config/instance.json

Architecture artefacts (solution, ADRs) live in the target repo `docs/architecture/`
tree. Repo binding stays in `.agency/target.json`.
-->

# Architecture — Practice Profile

*Written by `/architecture:setup` or initialized on first use.*

---

## Status

`template` — run `/architecture:setup` to fill this in.

## Who's using this

- **Persona:** Principal Architect
- **Team size:** [PLACEHOLDER — solo | small | multi-squad]
- **Primary surface:** [PLACEHOLDER — system architecture | platform | product domain]

---

## Target binding

- **Target repo:** [PLACEHOLDER — path or slug from .agency/target.json]
- **Instance root:** [PLACEHOLDER — resolved instance path or none]
- **Binding status:** [PLACEHOLDER — bound | standalone | pending]

---

## Architecture scope

- **Solution stage default:** [PLACEHOLDER — stub | full]
- **ADR harvest habit:** [PLACEHOLDER — after each epic | sprint end | ad hoc]
- **Systems in scope:** [PLACEHOLDER — list or "whole product"]

---

## Available integrations

| Integration | Status | Fallback if unavailable |
| ----------- | ------ | ----------------------- |
| Source control | [✓ / ✗] | Manual work-id / path references |
| Project tracker | [✓ / ✗] | Filesystem backlog / tdd.md only |

*Re-check: `/architecture:setup --check-integrations`*

---

## Companion practices

- **engineering:** [PLACEHOLDER — installed | recommended | not needed]
- **product-management:** [PLACEHOLDER — installed | recommended | not needed]

---

## Known gaps / things to revisit

-

---

*Re-run: `/architecture:setup --redo`*
