<!--
TEMPLATE — do not write user data here.

This file ships with the plugin and shows the structure the practice config should have.
It is replaced on every plugin update. Never write user data here.

The `setup` skill copies or updates the user config at:
  ~/.claude/plugins/config/digital-agency/product-management/CLAUDE.md

Instance-wide org facts live in the instance repo at:
  <instance-repo>/config/instance.json

Product and delivery artefacts (product, roadmap, backlog, work/) live in the target
repo `docs/` tree — see references/product-conventions.md and
references/delivery-conventions.md. Repo binding stays in `.agency/target.json`.
-->

# Product Management — Practice Profile

*Written by `/product-management:setup` or initialized on first use.*

---

## Status

`template` — run `/product-management:setup` to fill this in.

## Who's using this

- **Personas:** Product Manager, Delivery Lead
- **Team size:** [PLACEHOLDER — solo | small | multi-squad]
- **Primary product surface:** [PLACEHOLDER — what the PM owns]
- **Sprint cadence:** [PLACEHOLDER — one week | two weeks | continuous]

---

## Reporting cadence

- **Stakeholder update frequency:** [PLACEHOLDER — weekly | fortnightly | monthly | ad hoc]
- **Update format:** [PLACEHOLDER — brief bullets | narrative | dashboard summary]
- **Primary audience:** [PLACEHOLDER — exec | engineering | partner | customer | board | sponsor]

---

## Discovery workflow

- **Input sources:** [PLACEHOLDER — user interviews | support tickets | analytics | sales | competitive signal]
- **Roadmap format:** [PLACEHOLDER — Now/Next/Later | quarterly themes | OKR-aligned]

---

## Escalation model

- **Triggers:** [PLACEHOLDER — blocked > N days | scope change | risk threshold]
- **Escalate to:** [PLACEHOLDER — role or name]
- **Channel:** [PLACEHOLDER — chat | email | meeting]

---

## Available integrations

| Integration | Status | Fallback if unavailable |
| ----------- | ------ | ----------------------- |
| Project tracker | [✓ / ✗] | Manual status from docs/ |
| Chat | [✓ / ✗] | Paste threads in chat |
| Knowledge base | [✓ / ✗] | Manual upload |
| Product analytics | [✓ / ✗] | Paste metrics |
| User feedback | [✓ / ✗] | Paste tickets |
| Meeting transcription | [✓ / ✗] | Paste notes |
| Competitive intelligence | [✓ / ✗] | Manual competitor notes |

*Re-check: `/product-management:setup --check-integrations`*

---

## Known gaps / things to revisit

-

---

*Re-run: `/product-management:setup --redo`*
