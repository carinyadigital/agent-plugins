---
preset: {{PRESET}}
run_id: {{RUN_ID}}
agent: {{AGENT}}
seeded: {{SEEDED_DATE}}
metadata:
  version: "1.0"
  owner: web-development
  review_cadence: as-needed
  work_shape: orchestrate-delivery
  output_class: applied-change
---

# Run context: {{RUN_ID}}

Static reference for the loop. Written once at seed time and read every
iteration. The loop never edits this file; mutable state lives in
`loop-state.md`.

## Goal

{{GOAL}}

## Work sequence

{{WORK_SEQUENCE}}

## Definition of done

{{DONE_CRITERIA}}

## Preset context

{{PRESET_CONTEXT}}
