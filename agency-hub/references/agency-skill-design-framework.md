# Agency Skill Design Framework

> Vendored copy for `agency-hub:skills-qa`. Sync from `.agents/references/agency-skill-design-framework.md` when the maintainer source changes. Do not drift.

**Version:** 0.1.0
**Last updated:** 2026-06-27

Single source of truth for what makes a digital-agency skill well-designed.
Three things consume it:

- **`.agents/skills/skills-qa/SKILL.md`** — evaluates a skill against
  this framework and produces a verdict. Cite this file; do not let the two drift.
- **`references/skill-authoring-template.md`** (when added) — starting skeleton
  for new skills, built to pass this framework by construction.
- **`scripts/validate.py`** — mechanical validation of frontmatter, required
  headings (with `--strict`), marketplace manifests, cross-references, bundled-skill
  drift, and evals schema.

Agency skills are **execution-oriented**: they draft or apply work against a
definition of done, with a human review gate where stakes warrant it. The
framework checks design quality and trust surface — not whether the substantive
output is correct for a specific client.

---

## Work Shapes

Every skill declares exactly one dominant work shape in frontmatter
(`metadata.work_shape`). The shape determines which failure modes are mandatory
and how delegation thresholds are calibrated.

| Value | What it is | Example skills | Mandatory failure modes |
|---|---|---|---|
| `implement-and-ship` | Changes code or repo artefacts toward a stated task and definition of done. | implement, create-mr, component-scaffold | Direct apply vs draft; Repo blast radius; Definition-of-done bypass |
| `review-and-gate` | Reads diffs or artefacts and produces a verdict — blocking or non-blocking. Does not apply changes. | code-review, brand-guide review, validate | Accountability gap; Definition-of-done bypass |
| `generate-draft` | Produces markdown or copy for human review before use or publish. | design write, product write, brand-voice write | Direct apply vs draft; Brand/client safety |
| `orchestrate-delivery` | Plans, decomposes, or routes work across artefacts without directly shipping. | backlog, tasks, sprint plan, skills-index | Accountability gap; Scope boundaries |
| `monitor-and-report` | Aggregates status, metrics, or evidence into a report. | metrics-review, stakeholder-update, debug report | Definition-of-done bypass; Brand/client safety |

A skill's declared shape must match its actual behavior. A skill claiming
`generate-draft` that silently writes to production paths without a review gate
is miscalibrated at the root.

---

## Failure Modes

Five named modes. Each skill's Trust Spine section states how it addresses every
mode mandatory for its declared work shape. Silence on a mandatory mode is not
allowed.

**a. Direct apply vs draft-for-review.**
Does the skill apply changes (code, deploy, publish, send) without an explicit
human gate when stakes are non-trivial? Draft-for-review skills must say where
output lands and what happens before merge/publish.

**b. Brand and client safety.**
Could output go off-brand, off-brief, or to the wrong audience without a check?
Skills touching client-facing copy, brand voice, or external comms must name
the guardrail (brand guide, voice doc, destination check).

**c. Accountability gap.**
Is the human reviewer structurally the decision-maker, or does the output format
make ratification easy without engagement? Review skills must surface blocking vs
non-blocking findings; draft skills must not present conclusions as shipped fact.

**d. Repo and deploy blast radius.**
What can this skill change? Repo writes outside declared paths, undeclared Bash,
deploy MCP calls, or credential handling must be explicit. Undeclared elevated
tools are a hard trust-surface failure.

**e. Definition-of-done bypass.**
Does the skill mark work complete, merge-ready, or validated without evidence
against stated acceptance criteria? Validate and review shapes must not invent
passing status.

**Hard disqualifier:** any failure mode mandatory for the skill's declared work
shape, left unaddressed, forces at least **MATERIAL CONCERNS** regardless of
other scores.

---

## The 12 Design Parameters

For each parameter, a well-designed skill addresses it explicitly.

### 1. Audience
Role and fluency level (practitioner, senior reviewer, non-specialist with
practitioner access). Output format and handoff must match.

**Flag 🔴 if:** audience undefined.

### 2. Work Shape
See [Work Shapes](#work-shapes). Declared shape must match behavior.

**Flag 🔴 if:** shape missing, not in enum, or contradicted by behavior.

### 3. Delegation Threshold
Line between agent draft and human apply — structural in output format, not a
footer disclaimer. Frontmatter `metadata.output_class` should match behavior:
`draft-for-review`, `decision-support`, `structured-data`, `tracking-update`,
`applied-change`.

**Flag 🔴 if:** outputs treated as final without review on non-trivial work.

### 4. Input Requirements
Minimum inputs defined. On missing input: ask, halt, or proceed with labeled
assumptions — never proceed silently.

**Flag 🔴 if:** silent proceed on insufficient inputs.

### 5. Definition of Done
What artefact or state counts as complete? Path conventions (`docs/work/{epic}/`,
target repo layout) stated or deferred explicitly to target repo docs.

**Flag 🔴 if:** no completion criteria for `implement-and-ship` or
`review-and-gate` work.

### 6. Versioning and Ownership
Named owner and review cadence in frontmatter. Community skills: version and
source at minimum.

**Flag 🔴 if** (first-party): no owner.

### 7. Failure Modes
See [Failure Modes](#failure-modes). Mandatory modes for the shape must be
addressed.

**Flag 🔴 if:** mandatory mode unaddressed (hard disqualifier).

### 8. Scope Boundaries
In-scope work and explicit "does not do" section.

**Flag 🔴 if:** no scope boundaries.

### 9. Escalation Logic
When to stop and hand back — novel input, missing design/tasks, conflicting
signals, out-of-repo conventions.

**Flag 🔴 if:** absent on `implement-and-ship`, `review-and-gate`, or
`orchestrate-delivery` work.

### 10. Trust Surface
Hooks, MCP (`.mcp.json`), `allowed-tools`, network calls, writes outside skill
directory, prompt-injection patterns, authority overclaiming.

**Flag 🔴 if:** undeclared Bash/deploy, hooks without justification, writes
outside declared paths.

### 11. Schema
Required frontmatter: `name`, `description`, `allowed-tools`, `metadata.version`,
`metadata.owner`, `metadata.review_cadence`, `metadata.work_shape`,
`metadata.output_class`.

Required sections: When to use; What this skill does not do; Preconditions;
Trust spine; Workflow; Outputs (exact heading).

**Flag ⚠️ if:** missing fields or sections.

### 12. Conflicts
Overlap with installed first-party skills — trigger overlap, instruction conflict,
scope creep.

**Flag ⚠️ if:** duplicates a first-party skill without differentiation.

---

## Verdict Tiers

**READY** — All 12 parameters addressed. Mandatory failure modes addressed.
Fit for incorporation or team deployment.

**SOME CONCERN** — One or two partial gaps. Mandatory failure modes addressed.
Usable with awareness; fix before broad rollout.

**MATERIAL CONCERNS** — Mandatory failure mode unaddressed; scope or escalation
absent on high-stakes shapes; silent proceed on bad inputs; delegation overreach.
Do not ship until resolved.

**REFUSE** — Confirmed malicious instruction, credential theft, data exfiltration,
or environment modification patterns. No override path.

---

## Changelog

- **0.1.0** (2026-06-27) — Initial version for local maintainer tooling in `.agents/`.
