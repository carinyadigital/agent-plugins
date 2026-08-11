<!--
TEMPLATE — do not write user data here.

This file ships with the plugin and shows the structure the practice config should have.
It is replaced on every plugin update. Never write user data here.

The `setup` skill copies or updates the user config at:
  ~/.claude/plugins/config/digital-agency/content-marketing/CLAUDE.md

Instance-wide org facts live in the instance repo at:
  <instance-repo>/config/instance.json

Brand voice is read from the resolved brand path — see references/content-conventions.md.
Content artefacts (calendar, seeds) live in the instance or target repo `docs/` tree.
Repo binding stays in `.agency/target.json`.
-->

# Content Marketing — Practice Profile

*Written by `/content-marketing:setup` or initialized on first use.*

---

## Status

`template` — run `/content-marketing:setup` to fill this in.

## Who's using this

- **Default persona:** [PLACEHOLDER — content-strategist | content-writer | merged]
- **Team size:** [PLACEHOLDER — solo | small | multi-role]

---

## Primary channels

- **Web copy:** [PLACEHOLDER — yes | no]
- **Social:** [PLACEHOLDER — yes | no]
- **Email:** [PLACEHOLDER — yes | no]

Determines which artefact types this practice actually produces.

---

## Content cadence

- **Calendar rhythm:** [PLACEHOLDER — weekly | fortnightly | monthly | ad hoc]
- **Primary content types:** [PLACEHOLDER — blog | recipes | social | mixed]

---

## Available integrations

| Integration | Status | Fallback if unavailable |
| ----------- | ------ | ----------------------- |
| Source control | [✓ / ✗] | Manual file paths |
| CMS | [✓ / ✗] | Seed JSON in local folder |
| Social scheduling | [✓ / ✗] | Manual export of captions |
| Knowledge base | [✓ / ✗] | Manual upload of seed material |
| Chat | [✓ / ✗] | Paste threads in chat |

*Re-check: `/content-marketing:setup --check-integrations`*

---

## Persona preference

- **Content Strategist surface:** [PLACEHOLDER — primary | secondary | merged]
- **Content Writer surface:** [PLACEHOLDER — primary | secondary | merged]

When merged, greet as a single content partner and route internally to the right skill.

---

## Seed material reviewed

_(URLs or paths from setup — pattern-match tone; do not copy proprietary content.)_

-
-

---

## Known gaps / things to revisit

-

---

*Re-run: `/content-marketing:setup --redo`*
