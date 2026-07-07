# Loop protocol

Canonical definition of the Ralph epic step machine. The executable version
is generated into `.ralph/loop.md` from
[../assets/loop.template.md](../assets/loop.template.md); this file explains
the design so changes to the template stay coherent.

## Principles

- **One step per iteration.** Each loop turn resolves `current_task` +
  `current_step` from the state file, runs exactly that step, updates the
  state file, and ends the turn. State lives in files, never in memory —
  any iteration can be resumed cold.
- **Fresh sub-agent per skill step.** `/implement`, `/code-review`,
  `/code-review fix`, `/ux-design-review`, `/ux-design-review fix`,
  `/validate`, and `/merge-request` each run in a new sub-agent (Cursor
  Task tool / Claude Code agent). The orchestrating turn stays small; each
  skill gets a clean context.
- **The loop file never changes; the state does.** The stop hook re-feeds
  the same prompt every iteration (Ralph Wiggum technique); progress is
  encoded entirely in `loop-state.md`, the git history, and the review
  artefacts.

## Per-task cycle

```
task-start → implement → review → review_fix (max 3) →
ux_review (UI only, fix max 2) → validate_and_commit → task-progress → [next task]
```

| Step | Runs | Advances when |
| ---- | ---- | ------------- |
| task-start | tracker start action; read task AC | always |
| implement | `/implement {TASK_ID}` sub-agent (no commit) | sub-agent completes |
| review | `/code-review` sub-agent → `review-{TASK_ID}.md` | no `[blocking]` findings, or fix budget spent |
| review_fix | `/code-review fix` sub-agent | returns to review |
| ux_review | `/ux-design-review` sub-agent → `ux-review-{TASK_ID}.md`; only when the diff touches UI | no `[blocking]` findings, or budget spent |
| ux_review_fix | `/ux-design-review fix blocking` sub-agent | returns to ux_review |
| validate_and_commit | fast validation (lint, typecheck) inline; commit to the epic branch | checks pass and commit lands |
| task-progress | tracker progress action; mark task done; advance `current_task` | always |

Commit message: `{TASK_ID}: <imperative summary>` with an `Epic:` trailer.
No `Co-authored-by`, no emojis.

## Final phase (once, after every task is committed)

```
final_review (strongest model) → final_review_fix (max 3) →
final_validation (full commands) → final_validate (/validate) →
create_mr (/merge-request create --draft) → done
```

- **final_review** reviews the whole epic branch diff, not one task. Use
  the strongest model the host allows for sub-agents; fixes can run on a
  cheaper model.
- **final_validation** runs the full resolved command list (install,
  format, lint, typecheck, build, test) and must pass before advancing.
- **final_validate** runs `/validate {epic}` — Gherkin AC + roadmap exit
  criteria. Gaps stop the loop; they never get promised over.
- **done** is the only step allowed to output the completion promise.

## Budgets and guardrails

| Rail | Value | Enforced by |
| ---- | ----- | ----------- |
| max_iterations | default 50 | stop hook (frontmatter) |
| review_fix cycles per task | 3 | loop-state counter |
| ux_review_fix cycles per task | 2 | loop-state counter |
| final_review_fix cycles | 3 | loop-state counter |
| stall guard | state file unchanged 3 consecutive iterations | stop hook |
| false promise | never emit `<promise>` unless the done conditions hold | prompt + review of budget notes |

Exhausted budgets do not fail the loop: the step advances and the
unresolved findings are recorded under `## Notes` in `loop-state.md`, so
the final review and the MR description surface them to humans.

Blockers that need a human (credentials, ambiguous requirements,
destructive decisions) are written to `## Notes` and the turn ends WITHOUT
advancing `current_step` — the stall guard then ends the loop within 3
iterations, leaving the state pointing at the blocked step.

## Why one step per iteration

The stop hook gives each iteration a fresh turn against the same prompt.
Doing one step per turn keeps the orchestrator's context tiny (read state,
launch sub-agent, write state), makes every hop resumable and inspectable
(`/ralph status`), and turns the transcript into an auditable step log.
Batching steps re-creates the long-context drift the loop exists to avoid.
