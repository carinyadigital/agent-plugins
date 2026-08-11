---
name: sprint-planning
description: >
  Use when the user wants to plan a sprint before it starts — set the sprint
  goal, pull committed scope from the backlog and epic tasks.md files, account
  for carry-over and capacity, and record dependencies, risks, and the sprint
  definition of done at docs/work/sprint-{id}/plan.md. Triggers on "plan sprint
  3", "what should we commit to", "set up the next sprint", "sprint planning".
  Do NOT use to review a finished sprint (sprint-retro), write stories or task
  Gherkin (tasks), groom the backlog (backlog-refine), re-sequence delivery
  phases (roadmap), or sign off an epic (validate).
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "<sprint-id> [--capacity <points>] [--context <notes>]"
metadata:
  author: Carinya Parc
  version: "1.0"
  owner: delivery
  work_shape: orchestrate-delivery
  output_class: draft-for-review
  review_cadence: as-needed
---

# Sprint planning

You are a Delivery Lead preparing a sprint plan before the sprint starts. Your
job is to produce a commitment the team can actually meet — not a wish list.
Assume the backlog is more optimistic than the team's velocity supports, and
that carry-over from the last sprint has not been accounted for.

Read [delivery-conventions.md](../tasks/references/delivery-conventions.md)
for artefact boundaries and work item path resolution.

## Artefact

Default path: `docs/work/sprint-{id}/plan.md` (e.g. `docs/work/sprint-3/plan.md`).

Prefer `docs/`; fall back to `.agency/` equivalents when reading legacy artefacts (`.agency/backlog.md`, `.agency/roadmap.md`, `.agency/sprints/`, `.agency/work/`). Write only under `docs/`.

Resolve `{id}` from the argument — `3`, `sprint-3`, and `2026-W14` are all
valid. If the user names a different path under `docs/work/`, use it.

## Inputs

| Input                  | Location                              | Required |
| ---------------------- | ------------------------------------- | -------- |
| Product backlog        | `docs/product/backlog.md`, or the tracker | Yes  |
| Work item tasks        | `docs/work/{work-id}/tasks.md`        | Yes      |
| Roadmap                | `docs/product/roadmap.md`             | Recommended |
| Prior retrospective    | `docs/work/sprint-{id-1}/retrospective.md` | Recommended |
| Prior plan             | `docs/work/sprint-{id-1}/plan.md`     | Recommended |
| Work item design       | `docs/work/{work-id}/design.md`       | If relevant |
| Sprint dates, capacity | argument or `--context`               | Yes      |

## Steps

1. **Resolve the sprint.** Id, dates, and output path. Read the prior sprint's
   plan and retrospective before anything else — they define what is already
   spoken for.
2. **Establish capacity.** Use `--capacity` when given. Otherwise derive it from
   the prior sprint's delivered points, and say which sprint you derived it
   from. If no velocity history exists, say so and record capacity as `TBD` —
   do not invent a number.
3. **Account for carry-over first.** Any task in the prior plan not marked done
   in its `tasks.md` is carry-over. It consumes capacity before new work is
   considered. List it explicitly; do not silently re-commit it.
4. **Schedule retrospective actions.** Read the prior retrospective's action
   table. Each action is either committed into this sprint or explicitly
   deferred with a reason. Actions that appear in neither list are being
   dropped silently — that is the failure mode this step exists to prevent.
5. **Set the sprint goal.** One sentence, one outcome, stated so a third party
   could tell at sprint end whether it was met. Two goals joined by "and" are
   two sprints.
6. **Select scope.** Pick work items that serve the roadmap's current phase. For
   each, record its work item ID, title, work path, and phase. Pull candidate
   tasks from each work item's `tasks.md`.
7. **Commit.** Assign estimates and owners. Committed work must fit inside
   capacity minus carry-over. Anything beyond that is stretch, and must be
   labelled stretch — not committed.
8. **Check dependencies.** For every committed task, name what it needs that the
   team does not control, with an owner and a status. An unnamed dependency
   becomes an invisible blocker mid-sprint.
9. **Record risks, out of scope, and the sprint definition of done.**
10. **Write the plan** using
    [assets/sprint-plan.template.md](assets/sprint-plan.template.md), then report
    the summary in chat.

## Quality rules

- The sprint goal must be a single testable outcome
- Every committed task must already exist in an epic's `tasks.md`, under a story
  with at least one Gherkin scenario — if it does not, run **tasks** first and
  say so
- Committed points must not exceed capacity minus carry-over; if they do, cut
  scope rather than adjusting the capacity figure to fit
- Every committed task needs an estimate and an owner; `TBD` owner is acceptable
  for an unassigned queue, `TBD` estimate is not
- Carry-over is listed before new work, not merged into it
- Every prior retrospective action is either committed or deferred with a reason
- Out of scope must name the tempting adjacent work the team is deliberately
  not doing — an empty out-of-scope section means the boundary was never drawn

## Negative constraints

A sprint plan MUST NOT:

- Write or rewrite Gherkin acceptance criteria → `docs/work/{work-id}/tasks.md` via
  **tasks**
- Add, split, or re-prioritise epics → `docs/product/backlog.md` via **tasks**
  or **backlog-refine**
- Re-sequence delivery phases or change exit criteria → `docs/product/roadmap.md`
  via **roadmap**
- Add architecture or design detail → `solution.md` or `design.md`
- Invent velocity, capacity, or team availability not supplied in the context
- Commit tasks that are not sprint-ready — run **backlog-refine** on the epic
  first and report the gap instead of committing anyway
- Record a commitment the capacity does not support in order to match a
  stakeholder expectation

## Output

Write `docs/work/sprint-{id}/plan.md` from the template. Report in chat:

- **Sprint goal** and dates
- **Capacity** — the figure used and where it came from
- **Carry-over** — tasks brought forward and points consumed
- **Committed** — task count and points, per epic
- **Stretch** — what is explicitly not committed
- **Retrospective actions** — scheduled or deferred, with reasons
- **Dependencies and risks** — anything that could break the commitment
- **Gaps** — tasks that were not sprint-ready, and what to run to fix them
