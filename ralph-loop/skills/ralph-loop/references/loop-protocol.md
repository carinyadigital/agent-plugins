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

Claude and Cursor each have exactly one completion-detection mechanism, not a
primary and a fallback of each other — they use it because it is the only one
the platform's hooks make available to that agent.

- **Cursor**'s Stop hook receives no response text, so it cannot scan
  anything itself. Detection happens earlier, in the `afterAgentResponse`
  hook (`ralph-capture.sh`), which scans the response as it is produced and
  writes the `done` sentinel on a match. The Stop hook only checks whether
  that file exists.
- **Claude Code** has no `afterAgentResponse` equivalent, so there is no
  sentinel to write. Its Stop hook scans the transcript directly — the only
  point at which it has access to the assistant's text at all.

Text scanning must find text behind trailing tool calls: a turn ending on a
tool call has no text block in that position, and a loop that delegates every
step to a sub-agent ends most turns on a tool call. An early implementation
read only the last transcript line and so could detect completion only on
turns that happened to end in prose.

Scanning must also be scoped to the CURRENT turn and anchored to the end of
the message, or it detects the wrong thing in two different ways:

- **Unscoped** (no turn boundary), it can reach past the current turn into an
  earlier iteration — or an earlier, already-finished loop — and find a stale
  promise nobody made this run, stopping a fresh loop at iteration 1. Scoping
  to the current turn uses the transcript's own structure: every Ralph
  continuation is a Stop-hook "block" whose `reason` Claude Code re-injects as
  a genuine new user turn, which is an unambiguous boundary.
- **Unanchored** (bare substring match), it fires on the model merely
  *mentioning* its own stop condition — "I will only output
  `<promise>DONE</promise>` once every task is committed" contains the tag
  without the turn being complete. Requiring the tag to be alone on the
  message's final line rejects a mention (there is always more text on that
  line afterward) while still matching a genuine completion turn, which ends
  on the tag.

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
