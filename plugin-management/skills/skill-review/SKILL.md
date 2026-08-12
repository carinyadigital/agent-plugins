---
name: skill-review
description: >
  Use when the user wants to research, review, or enhance an agent skill on a
  regular cadence — weekly skill uplift, audit a SKILL.md against best practice,
  compare with popular external skills, fix working issues, or align with
  agentskills.io. Triggers on "review this skill", "enhance the X skill",
  "weekly skills review", "uplift this skill", "align with agentskills.io".
  Works on one skill or a batch. Do NOT use to create a skill from scratch
  (template/SKILL.md or `/plugin-management:skills-qa` to author a new skill), route which skill to use (skills-index),
  or review product documentation (docs-review).
license: MIT
compatibility: Requires network access for external research. Spec validation optional via skills-ref.
allowed-tools: Read Write Edit Glob Grep WebFetch WebSearch Bash
argument-hint: "<skill-name|path> [--batch] [--review-only] [--apply]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: plugin-management
  review_cadence: quarterly
  work_shape: review-and-gate
  output_class: decision-support
---

# Skill review

You are a Skills Lead researching and enhancing agent skills. You review one
skill (or a batch) against its own purpose, similar popular skills, and the
open [Agent Skills specification](https://agentskills.io/specification), then
apply agreed improvements.

Run this on a regular cadence (e.g. weekly) or on demand when a skill is
misbehaving, drifting, or due for uplift.

## Modes

| Mode | When | Writes |
| ---- | ---- | ------ |
| **review** (default with `--review-only`) | Analyse and recommend only | Report only |
| **enhance** (default when applying) | Full pipeline including fixes | Skill files + report |

If the user does not specify a mode: **research and propose first**, then apply
only after they confirm — unless they said "fix", "enhance", "uplift", or
`--apply`, in which case apply non-controversial fixes and surface judgement
calls before changing behaviour or public interfaces.

## Inputs

| Input | Source | Required |
| ----- | ------ | -------- |
| Target skill | Path, name, or "all skills in `{skills-root}`" | Yes |
| Spec | https://agentskills.io/specification | Yes (fetch current) |
| Authoring guidance | https://agentskills.io + Anthropic skill best practices | Yes for research |
| Peer skills | skills.sh, GitHub, official plugin registries | When researching |
| Working issues | User-reported bugs, broken steps, known gaps | If provided |
| Repo conventions | This repo's other `SKILL.md` files, changelog, template | If in a skill pack |

## Steps

Copy this checklist and track progress:

```
Skill review progress:
- [ ] 1. Scope
- [ ] 2. Comprehensive review
- [ ] 3. External research
- [ ] 4. Opportunities
- [ ] 5. Working issues
- [ ] 6. Spec alignment
- [ ] 7. Plan
- [ ] 8. Apply (enhance mode)
- [ ] 9. Report
```

Work **one skill at a time** in a batch. Finish the report (and apply, if
enhancing) before starting the next.

---

### 1. Scope

1. Resolve the target: explicit path → skill name under the skills root → user
   intent ("the ralph loop skill", "all delivery skills").
2. Confirm the skill directory contains `SKILL.md`. List bundled
   `references/`, `assets/`, `scripts/`, prompts, and agents.
3. State the review boundary: single skill vs batch; review-only vs enhance.
4. Read the skill's current `description`, version/metadata, and any changelog
   entries that mention it.

Do not expand scope mid-flight (e.g. rewriting neighbouring skills) unless the
user asked for a batch.

---

### 2. Conduct a comprehensive and thorough review of the skill

Read the entire skill package before judging. Use the checklist in
[references/review-checklist.md](references/review-checklist.md).

Cover at least:

| Lens | Questions |
| ---- | --------- |
| **Purpose** | Is the job clear? One skill, one job? Description WHAT + WHEN + negative triggers? |
| **Discoverability** | Would the agent activate this for the right prompts and skip it for the wrong ones? |
| **Procedure** | Are steps ordered, complete, and unambiguous? Missing gates or decision points? |
| **Structure** | Frontmatter valid? Progressive disclosure? References one level deep? Body lean? |
| **Correctness** | Do scripts, hooks, paths, and cross-skill links actually work? |
| **Consistency** | Same terms throughout? Matches sibling skills in this pack? |
| **Safety** | Clear read-only vs write contracts? Dangerous actions gated? |
| **Maintainability** | Time-sensitive claims? Duplicated prompt files that should be folded? Example-only templates that should be generalised? |

Record findings as **blocking** (broken / spec-invalid), **improve** (clear
uplift), or **optional** (nice-to-have).

For single-mode skills that still split instructions into a separate prompt
file or `prompts/` directory: plan to fold the prompt into `SKILL.md`, delete
the redundant prompt surface, and tighten the body.

---

### 3. External research — similar popular skills and leading best practices

Research **before** proposing large structural changes.

1. Fetch the current [Agent Skills specification](https://agentskills.io/specification)
   and relevant authoring pages (description optimisation, progressive
   disclosure).
2. Find **3–5** comparable skills: same job, similar name, or same domain.
   Prefer popular sources — [skills.sh](https://skills.sh), official plugin
   registries, well-starred GitHub skills/plugins, and vendor examples.
3. For each peer, note: trigger description, step shape, progressive disclosure,
   scripts vs prose, safety rails, and anything this skill lacks or does better.
4. Capture leading practices that apply (concise instructions, degrees of
   freedom, eval/trigger tests for descriptions, one-level references, etc.).

Summarise research as evidence tied to recommendations — not a link dump.
If the user named specific repos or URLs, treat those as required reading.

---

### 4. Identify opportunities to enhance and optimise the skill

From the internal review + external research, produce an opportunity list:

| ID | Opportunity | Source (review / research / user) | Impact | Effort | Risk |
| -- | ----------- | --------------------------------- | ------ | ------ | ---- |
| O1 | … | … | H/M/L | H/M/L | H/M/L |

Prioritise:

1. Broken behaviour and spec violations
2. Discoverability (description / triggers)
3. Clarity and reliability of steps
4. Token cost (lean `SKILL.md`, move detail to references)
5. Generalisation (templates, presets, cross-agent compatibility)
6. Polish (examples, naming, changelog)

Do not recommend changes that fight the skill's stated job or this pack's
conventions without calling out the trade-off.

---

### 5. Address any working issues identified

Collect working issues from:

- Explicit user reports in the request
- Failures found while reading scripts, hooks, and paths
- Contradictions between `SKILL.md` and bundled references/assets

For each issue:

1. **Reproduce** from the skill text and files (and a minimal dry-run if safe).
2. **Root cause** in one or two sentences.
3. **Fix** — concrete file/step change.
4. **Verify** — how you will confirm the fix (re-read, script dry-run, checklist).

In **review** mode: document fixes; do not apply.
In **enhance** mode: apply fixes for confirmed issues; do not leave known
breakage documented-only when the user asked to enhance.

---

### 6. Ensure alignment with industry standards (e.g. agentskills.io)

Validate against the live spec and the checklist in
[references/review-checklist.md](references/review-checklist.md):

- `name` / `description` constraints; `name` matches directory
- Optional fields used correctly (`license`, `compatibility`, `metadata`,
  `allowed-tools` as a space-separated string)
- Directory layout (`SKILL.md`, optional `scripts/`, `references/`, `assets/`)
- Progressive disclosure: lean body, on-demand references, no deep reference chains
- Relative one-level file links from `SKILL.md`

If `skills-ref` (or an equivalent validator) is available, run it on the skill
directory and fix reported violations in enhance mode.

Also check **pack-local** standards: sibling frontmatter shape, changelog
expectations, and index/routing entries when the skill is part of a published
pack.

---

### 7. Plan

Present a short plan before applying non-trivial edits:

```markdown
## Plan — {skill-name}

### Apply now
- …

### Needs confirmation
- … (behaviour change, rename, split/merge skill, public interface)

### Defer
- … (optional / high-risk / out of scope)
```

Wait for confirmation when the plan renames the skill, splits or merges
skills, changes invocation/CLI surfaces, or alters user-visible behaviour.
Pure spec fixes, broken links, folded single-mode prompts, and copy clarity
may proceed in enhance mode without a blocker.

---

### 8. Apply (enhance mode)

1. Edit `SKILL.md` and bundled files per the approved plan.
2. Keep changes minimal and coherent — prefer tightening steps over adding
   essays.
3. Move bulky detail into `references/` or `assets/`; keep `SKILL.md` under
   ~500 lines.
4. Update pack index, changelog, or cross-links only when this repo expects it.
5. Re-run the spec checklist (and validator if available) on the result.
6. Do not commit unless the user asks.

---

### 9. Report

Deliver a structured report:

```markdown
# Skill review — {skill-name}

## Verdict
{healthy | needs work | broken} — one sentence.

## Comprehensive review
- Blocking: …
- Improve: …
- Optional: …

## External research
| Peer | What we learned | Implication |
| ---- | --------------- | ----------- |
| … | … | … |

## Opportunities
| ID | Change | Priority | Status (proposed / applied / deferred) |
| -- | ------ | -------- | -------------------------------------- |

## Working issues
| Issue | Root cause | Fix | Status |
| ----- | ---------- | --- | ------ |

## Spec alignment (agentskills.io)
- Pass / fail summary
- Remaining gaps

## Files touched
- …

## Recommended next review
{cadence or trigger — e.g. after next breaking change, or weekly batch}
```

For batches, one short roll-up plus a per-skill section (or linked report).

## Negative constraints

- Do not invent peer skills — cite real sources from research.
- Do not expand into rewriting the whole pack unless scoped as a batch.
- Do not commit, tag, or publish without an explicit ask.
- Do not remove intentional product opinion just to mimic a popular peer.
- Do not skip steps 2–6 to "just edit" — research and review first.

## Additional resources

- [references/review-checklist.md](references/review-checklist.md) — spec and authoring checklist
- Spec: https://agentskills.io/specification
- Description guidance: https://agentskills.io/skill-creation/optimizing-descriptions
