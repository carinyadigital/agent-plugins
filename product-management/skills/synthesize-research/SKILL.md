---
name: synthesize-research
description: >
  Synthesize interview notes, survey data, or support tickets into themes,
  personas, opportunity areas, and roadmap recommendations. Use when turning
  raw research into structured findings. Do NOT use for competitive analysis
  (competitive-brief) or product strategy doc (product).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "<research topic or question>"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: product
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: decision-support
---

# Synthesize research

You synthesize user research from multiple sources into structured insights and
recommendations. Pass the research topic or paste source material after the
skill name.

See [CONNECTORS.md](../../CONNECTORS.md) for feedback/analytics connectors. For
thematic analysis, affinity mapping, survey pitfalls, personas, and opportunity
sizing, read [research-synthesis.md](references/research-synthesis.md) when needed.

## Steps

### 1. Gather inputs

Accept pasted notes, uploads, or connected knowledge base / feedback / analytics /
transcripts. Confirm: research type, source/participant count, research question,
and what decision this informs.

### 2. Process each source

Extract: key observations, verbatim quotes, behaviors vs stated preferences, pain
points, positive signals, and context (segment, use case, experience).

### 3. Theme and prioritize

Group into themes; count frequency; assess impact. Priority matrix:

|            | High impact              | Low impact                |
| ---------- | ------------------------ | ------------------------- |
| High freq  | Top priority findings    | Quality-of-life           |
| Low freq   | Important for segments   | Note; deprioritize        |

### 4. Generate the synthesis

1. **Research overview** — methods, participants, questions, timeframe
2. **Key findings** (5–8) — statement, evidence, frequency, impact, confidence
3. **Segments / personas** — if distinct patterns emerge
4. **Opportunity areas** — unmet needs, prioritized by impact
5. **Recommendations** — specific actions tied to findings
6. **Open questions** — gaps and suggested follow-up research

### 5. Extend

Offer persona docs, opportunity maps, follow-up research plans, or product
implications for the roadmap.

## Quality rules

- Let the data speak; do not force a predetermined narrative
- Behavioral evidence beats stated preferences
- Explicit confidence levels (2 interviews = hypothesis, not conclusion)
- 5–8 strong findings beat 20 weak ones
- Recommendations must be specific enough to act on

## Output format

Clear headers. Each finding stands alone with supporting evidence and attribution
to participant type (not name).
