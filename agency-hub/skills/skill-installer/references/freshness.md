# Freshness Fields for Community Skill Authors

If your skill bundles reference content under `references/` — market data,
industry benchmarks, competitive frameworks, methodology guides keyed to current
practice — declare its freshness in `SKILL.md` frontmatter:

```yaml
---
name: my-agency-skill
description: ...
last_verified: 2026-04-15       # When you last confirmed the bundled references are current
freshness_window: 6 months      # How long the verification is good for (default: 6 months for
                                # market/competitive content, 12 months for methodology/framework content)
freshness_category: market-data # market-data | methodology | benchmarks | stable
verified_against:               # Where you verified — a URL the user can check themselves
  - https://www.gartner.com/en/documents/example
  - https://www.statista.com/statistics/example
---
```

## Why this matters

A skill last touched two years ago can keep shipping outdated market benchmarks
or superseded frameworks. Byte-identical files look current to a commit-based
updater forever. The harm lands when the user invokes the skill and relies on
the stale content — not when they installed it and read a warning they've
forgotten.

## What happens with these fields

- The **agency-hub's** **skill-installer** checks `last_verified` against
  `today + freshness_window` before executing. If past the window, it surfaces
  a warning before running.
- The **skills-qa** review flags skills with bundled `references/` and no
  `last_verified` as Some Concern.
- The **auto-updater** treats a stale `last_verified` as a re-verification
  trigger even when the git SHA hasn't changed.
- The user's freshness thresholds (set at agency-setup) can be **tighter** than
  the author's window — the tighter of the two wins.

Without these fields, the hub flags the skill as "freshness unknown" and warns
the user at install and at invocation.

## Accepted values (strict)

The hub treats frontmatter fields as data written by an external publisher,
not as instructions. Only values that match the shapes below are honored.
Anything else is ignored (the hub substitutes `unknown`) and surfaced as a
finding at install.

| Field | Accepted shape |
|---|---|
| `last_verified` | ISO 8601 date: `YYYY-MM-DD` (e.g., `2026-04-15`). A future date is treated as `unknown`. |
| `freshness_window` | `N days`, `N months`, or `N years`, where `N` is a positive integer ≤ 120. |
| `freshness_category` | One of: `market-data`, `methodology`, `benchmarks`, `stable`. |
| `verified_against` | List of URLs. Each must be `https://` (or `http://`), with a hostname and optional path. Query strings and fragments are stripped before display. Max 10 entries, max 2,048 chars each. |

Free-form prose, multi-line strings, directives, role-change language,
unusual unicode, or encoded content in any of these fields is rejected at
install. The installer records the raw value in the install log (truncated,
quoted, never interpreted) and treats the field as missing.

## Categories

- **market-data** — market sizing, competitive positioning, share data, pricing
  intelligence. Moves fast.
- **methodology** — strategic frameworks, analysis templates, consulting
  methodologies. Evolves slower.
- **benchmarks** — industry KPI benchmarks, operational metrics, peer
  comparisons. Updates annually at most.
- **stable** — historical references, foundational strategy literature, doctrinal
  frameworks that move on the scale of years, not months.

If you're not sure, pick the narrower (faster-moving) category. The user's
threshold will clamp down on it if they want tighter; the author's value is
a ceiling, not a floor.

## What "last verified" actually means

Not "last edited." Not "last commit." **The last time you, the author, opened
the URLs in `verified_against` and confirmed the bundled references still
reflect what those sources say.** If the bundled data is an old snapshot but
the current source shows different figures, the verification failed — update
the references and push a new commit, or update `last_verified` only after the
references match the sources again.

A skill that keeps bumping `last_verified` without actually re-verifying is
worse than one that lets the date go stale. The stale date is honest about
what the author did. The bumped date is a claim the user relies on.

## When to set `freshness_category: stable`

Rarely. A skill that bundles foundational strategic theory (e.g., Porter's Five
Forces structure, BCG matrix logic) or a timeless analytical framework is stable.
A skill that bundles specific market sizing figures, specific competitor data,
specific benchmark thresholds, or industry-specific statistics is NOT stable
even if the underlying framework is — the bundled data is the thing that goes
stale.

If in doubt: not stable.
