# Loop protocol

How the Ralph loop works, independent of any preset. The executable form is
generated into `{base}/active.md` by `scripts/seed-ralph-loop.sh` from
[../assets/loop.core.template.md](../assets/loop.core.template.md) plus a
preset. This file explains the design so changes to either stay coherent.

## Principles

**One step per iteration.** Each turn resolves `current_step` from the state
file, runs exactly that step, updates the state file, and ends. State lives in
files, never in memory, so any iteration can be resumed cold.

**Fresh sub-agent per skill step.** Steps that invoke another skill run it in a
new sub-agent. The orchestrating turn stays small (read state, launch, write
state) and each skill gets a clean context.

**The loop file never changes; the state does.** The stop hook re-feeds the
same prompt every iteration. Progress is encoded entirely in the state file,
the git history, and the run artefacts.

## Anatomy of a run

```
.claude/loop/                       (or .cursor/loop/)
├── active.md                       frontmatter + prompt body, re-fed each turn
├── done                            sentinel written when the promise is met
├── stall                           stall-guard bookkeeping
├── {run-id}/
│   ├── context.md                  static: goal, sequence, commands
│   ├── loop-state.md               mutable: current step, counters, notes
│   └── review-*.md                 per-step artefacts
└── archive/{run-id}/               completed and cancelled runs
```

The base directory is resolved from the agent, not from a pointer file. Each
hook knows which agent it belongs to, so discovery is unnecessary. The previous
design used a `.ralph-loop` pointer at the project root, read with a relative
path inside an unguarded pipeline under `set -e`; when it was missing the hook
died silently and the loop stopped after one iteration.

## Frontmatter contract

The stop hook reads these from the FIRST frontmatter block only:

| Field | Meaning |
| ----- | ------- |
| `iteration` | current iteration, incremented by the hook |
| `max_iterations` | 0 means unlimited, still subject to the hard ceiling |
| `completion_promise` | promise text, or `null` for none |
| `state_file` | project-relative path the stall guard watches, or `null` |
| `session_id` | owning session; other sessions ignore the loop |
| `preset`, `run_id`, `seeded_at` | provenance, not read by the hook |

Parsing is bounded to the first block, so `---` separators and key-like lines
in the prompt body are inert. The old parser used a `sed` range, which restarts
at each `---`, and swallowed a third of the prompt body as frontmatter.

## Stopping conditions

| Rail | Default | Behaviour |
| ---- | ------- | --------- |
| completion promise | none | `done` sentinel, or `<promise>` in the response |
| max_iterations | 50 | stops when `iteration >= max_iterations` |
| hard ceiling | 200 | stops even when `max_iterations: 0` |
| stall guard | 3 | state file unchanged 3 iterations running |
| corrupt state | n/a | non-numeric frontmatter stops and clears the loop |
| aborted turn | n/a | Cursor only: interrupted turns are not re-fed |

On any stop the hook removes `active.md`, `done` and `stall`. Run directories
are never touched.

## Promise detection

The `done` sentinel is the primary signal on both agents; text scanning is the
fallback.

That ordering matters. Claude Code has no response hook, so the fallback reads
the transcript, and a turn ending on a tool call has no text block to scan. A
loop that delegates every step to a sub-agent ends most turns on a tool call.
The old implementation read only the last transcript line, so it could detect
completion only on turns that happened to end in prose.

Comparison is literal, not glob. A promise containing `*` or `[` would
otherwise pattern-match and end the loop early.

## Budgets and guardrails

| Rail | Typical | Enforced by |
| ---- | ------- | ----------- |
| fix cycles per item | 3 | preset, via a state counter |
| secondary review cycles | 2 | preset, via a state counter |
| final review cycles | 3 | preset, via a state counter |
| false promise | never | prompt wording plus a verifying `done` step |

Exhausted budgets do not fail the loop. The step advances and unresolved
findings are recorded under `## Notes`, so the final review and the artefacts
surface them to a human.

Blockers needing a human (credentials, ambiguous requirements, destructive
decisions) are written to `## Notes` and the turn ends WITHOUT advancing
`current_step`. The stall guard then ends the loop within 3 iterations, leaving
the state pointing at the blocked step.

## Why one step per iteration

The stop hook gives each iteration a fresh turn against the same prompt. One
step per turn keeps the orchestrator's context tiny, makes every hop resumable
and inspectable via `/ralph-loop status`, and turns the transcript into an
auditable step log. Batching steps recreates the long-context drift the loop
exists to avoid.

The cost is iteration count. A 12-task engineering epic runs roughly 60 to 80
iterations at default budgets, which is why `ralph-loop-setup` proposes
`tasks × 6 + 10` rather than the default 50.
