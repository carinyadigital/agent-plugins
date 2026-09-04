---
name: metrics-review
description: >
  Run a weekly, monthly, or quarterly metrics review: scorecard, trends, bright
  spots, concerns, and recommended actions. Use when investigating a spike or
  drop, comparing performance against targets, or preparing a metrics readout.
  Do NOT use for stakeholder status updates (stakeholder-update) or product
  strategy (product).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<time period or metric focus>"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: product
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Metrics review

You review product metrics, identify trends, and surface actionable insights.
Pass the time period or metric focus after the skill name.

See [CONNECTORS.md](../../CONNECTORS.md) for analytics connectors. For North Star /
L1 hierarchy, OKRs, cadences, and dashboard design, read
[metrics-frameworks.md](references/metrics-frameworks.md) when needed.

## Steps

### 1. Gather data

If product analytics is connected, pull key metrics, prior-period comparison,
targets, and segments. Otherwise ask the user for values, comparisons, and known
events (launches, outages, campaigns, seasonality).

Confirm: time period, metric focus (or full suite), targets, known events.

### 2. Organize

Structure around North Star → L1 health indicators (acquisition, activation,
engagement, retention, monetization, satisfaction) → L2 diagnostics. If the user
has no hierarchy, help identify North Star and key L1s first.

### 3. Analyze

For each key metric: current value, trend, vs target, rate of change, anomalies.
Note correlations, leading indicators, and segment drivers of aggregate moves.

### 4. Generate the review

1. **Summary** — 2–3 sentences: overall health, notable changes, key callout
2. **Metric scorecard** — table: Metric | Current | Previous | Change | Target | Status
3. **Trend analysis** — what happened, likely why, one-time vs sustained
4. **Bright spots** — beating targets, positive trends, strong segments
5. **Areas of concern** — misses, early warnings, visibility gaps
6. **Recommended actions** — investigations, experiments, investments, alerts
7. **Context and caveats** — data quality, comparability events, missing metrics

### 5. Follow up

Offer deeper investigation, dashboard spec, experiment proposals, or a recurring
review template.

## Quality rules

- Lead with the "so what" — absolute numbers without comparison are useless
- Attribution is uncertain; say so when correlating events to metric moves
- Every review should drive at least one action
- Focus on meaningful changes; small fluctuations are noise

## Output format

Tables for the scorecard. Clear status indicators (On track / At risk / Miss).
Summary scannable in ~30 seconds.
