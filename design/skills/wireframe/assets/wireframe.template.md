---
type: Wireframe
page_or_flow: <!-- kebab-case slug, e.g. home-page -->
version: '0.1'
owner: <!-- team or role -->
status: Draft
last_updated: <!-- YYYY-MM-DD -->
related:
  - <!-- brand-guide.md when present -->
  - <!-- product.md or brief source -->
---

<!--
DRAFTING AIDE — DELETE THIS BLOCK BEFORE SAVING THE OUTPUT FILE.
DO NOT INCLUDE in this wireframe:
  - Component names, file paths, or API contracts → /engineering:tdd
  - Brand tokens (hex, font stacks) → brand-guide.md (cite when used)
  - Task Gherkin acceptance criteria → specs/{work-short-name}/TASKS.local.md
  - Business strategy narrative → product.md

Low-fidelity only: layout regions, content hierarchy, interaction notes, key states.
-->

# Wireframe — {Page or Flow Title}

Brief summary of what this page or flow lets the user accomplish.

## 1. User goal

- **Primary:** <!-- one sentence -->
- **Secondary:** <!-- optional -->

## 2. Entry and exit

| Entry | Exit (success) | Exit (abandon) |
| ----- | -------------- | -------------- |
| <!-- how user arrives --> | <!-- where they go next --> | <!-- back, cancel, close --> |

## 3. Layout (desktop)

<!--
ASCII or structured region list. Name regions, not React components.
-->

```text
+--------------------------------------------------+
|  [Header — logo, primary nav]                    |
+--------------------------------------------------+
|  [Hero — headline, subcopy, primary CTA]         |
|                                                  |
|  [Section — supporting content blocks]           |
+--------------------------------------------------+
|  [Footer]                                        |
+--------------------------------------------------+
```

### Regions

| Region | Content | Notes |
| ------ | ------- | ----- |
| Header | <!-- items --> | <!-- sticky, mobile collapse, etc. --> |
| Hero | <!-- items --> | <!-- --> |

## 4. Layout (mobile)

<!--
Note stacking order, tap targets, and what hides or moves to a menu.
-->

[NEEDS CLARIFICATION or mirror desktop with mobile notes]

## 5. Interactions

| Element | Action | Result |
| ------- | ------ | ------ |
| Primary CTA | click / tap | <!-- --> |
| <!-- --> | <!-- --> | <!-- --> |

## 6. States

| State | What the user sees |
| ----- | ------------------ |
| Default | <!-- --> |
| Empty | <!-- when applicable --> |
| Loading | <!-- when applicable --> |
| Error | <!-- when applicable --> |
| Success | <!-- when applicable --> |

## 7. Content notes

- **Headline tone:** <!-- align with brand voice when known -->
- **Required fields / labels:** <!-- for forms -->
- **Placeholder copy:** <!-- lorem or realistic draft — not final marketing copy -->

## 8. Out of scope for this wireframe

- <!-- defer to another page, epic, or later sprint -->

## 9. Open questions

1. **{Question}.** {Context; owner; how it blocks implementation.}
