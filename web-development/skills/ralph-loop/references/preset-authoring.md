# Preset authoring

A preset defines the steps of a loop. The core template
([../assets/loop.core.template.md](../assets/loop.core.template.md)) owns
everything else: the one-step-per-iteration rule, the state contract, the
completion promise rules, the stuck protocol, and budget handling.

That split is the point. A preset author cannot accidentally weaken a
guardrail, because the guardrails are not in the preset.

## What a preset is

A markdown file at `../assets/presets/{name}.md` containing a `## Preset:`
heading, whatever context the steps need, and one section per step.

It may use any `{{PLACEHOLDER}}` token, which the seeding agent supplies with
`--set KEY=VALUE`. The seed script fails loudly if any placeholder is left
unresolved, so a typo is caught at seed time rather than at iteration 1.

## The step contract

Every step must do three things:

1. **One unit of work.** If you cannot describe the step in a sentence without
   using "and then", it is two steps.
2. **Write something durable.** A file, a commit, an appended note. A step that
   leaves no trace is indistinguishable from a step that did not run.
3. **Set the next `current_step`,** or deliberately leave it unchanged to
   signal that a human is needed.

The third point is what makes the stall guard work. Three iterations with an
unchanged state file stop the loop. That is a feature: a step that cannot
progress should stop the loop, not spin.

## Designing the step list

Start from the question "what would a careful person do, one sitting at a
time?" Then check each step against three tests:

- **Verifiable.** Can the agent tell whether the step succeeded, without
  asking a human? A step whose success is a matter of taste belongs to a
  review step with an explicit rubric, or to a human.
- **Resumable.** If the process died right after this step, could a fresh
  agent pick up from the state file alone? If not, the step is writing too
  little state.
- **Bounded.** Can this step loop with another step forever? If so it needs a
  fix budget, like `review → review_fix → review`.

## Fix budgets

Any pair of steps that can cycle needs a cap. Convention:

```
review → review_fix → review    (fix_count, max 3)
```

The reviewing step checks `fix_count` and advances regardless once the budget
is spent, recording what is still unresolved under `## Notes`. Exhausting a
budget is not a failure: it is how unresolved work reaches a human instead of
being retried forever.

## Worked example: a research loop

Not everything is software. This preset researches a topic and produces a
briefing, with no git, no tests, and no merge request.

```markdown
## Preset: research-briefing

Research `{{TOPIC}}` and produce a briefing at `{{OUTPUT_PATH}}`.

### Sources

- Working notes: `{{RUN_DIR}}/notes.md`
- Source log: `{{RUN_DIR}}/sources.md`
- Open questions: `{{RUN_DIR}}/questions.md`

### Steps

#### plan

1. Write 5 to 8 specific questions the briefing must answer to
   `{{RUN_DIR}}/questions.md`, each with a `status: open` line.
2. Set `current_step: research`.

#### research

1. Take the first question with `status: open`.
2. Search for it. Read at least two independent sources.
3. Append findings to `notes.md` and every source to `sources.md` with its
   URL, publication date, and a one-line note on its reliability.
4. Mark the question `status: answered`, or `status: unanswerable` with a
   reason.
5. If any question is still open, leave `current_step: research`. Otherwise
   set `current_step: draft`.

Note: this step advances by changing questions.md, so the stall guard still
protects it even though current_step is unchanged across iterations.

#### draft

1. Write the briefing to `{{OUTPUT_PATH}}` from `notes.md` alone. Every claim
   must trace to a source in `sources.md`.
2. Set `current_step: review`, `fix_count: 0`.

#### review

Check the draft against a fixed rubric:

- every claim traceable to a logged source
- every question in `questions.md` either answered or explicitly noted as
  unanswerable
- no source older than `{{FRESHNESS_LIMIT}}` used for a time-sensitive claim
- contradictions between sources surfaced, not silently resolved

If it passes, or `fix_count` has reached 3, set `current_step: done` and
record any unresolved items under `## Notes`. Otherwise write the findings to
`{{RUN_DIR}}/review.md` and set `current_step: revise`.

#### revise

Address the review findings, increment `fix_count`, set
`current_step: review`.

#### done

Verify: the briefing exists, every question is resolved or explicitly noted,
and every claim is sourced. If so, emit the completion promise. If not, record
why under `## Notes` and do not advance.
```

Three things to notice, because they generalise:

**The `research` step advances without changing `current_step`.** It changes
`questions.md` instead. The stall guard watches the state file, so a step that
loops on itself must still write state each iteration, here by marking a
question answered. A `research` step that found nothing three times running
would correctly stall.

**The review rubric is explicit.** "Is the briefing good?" is not checkable.
"Every claim traces to a logged source" is. A preset is only as reliable as its
most subjective advance condition.

**The `done` step re-verifies.** It does not trust that earlier steps did their
job; it checks the artefacts. The completion promise is the one thing the
system cannot detect a lie about, so the step that emits it should be the most
paranoid one in the preset.

## Testing a preset

Before trusting a preset with a real job:

1. `scripts/seed-ralph-loop.sh --preset {name} --dry-run` and read the output.
   Every placeholder resolved? Do the steps read clearly with real values in?
2. Seed it and run `/ralph-loop status`. Does the state file describe a
   sensible starting position?
3. Run 3 or 4 iterations, then read the state file. Can you tell what happened
   from the file alone, without the transcript? If not, the steps write too
   little.
4. Deliberately break something (rename a file a step depends on) and confirm
   the loop stalls rather than inventing a workaround.

## Anti-patterns

- **A step that does everything.** "Implement and test and commit" is three
  steps. Batching recreates the long-context drift the loop exists to avoid.
- **Advance conditions requiring judgement without a rubric.** "When the code
  is clean enough" gives the agent nothing to check.
- **No fix budget on a cycle.** Two steps pointing at each other with no
  counter will burn the whole iteration budget on one problem.
- **A completion promise the preset cannot verify.** If the `done` step cannot
  mechanically check the criteria, the promise is decoration.
- **Duplicating core rules in the preset.** The core template already forbids
  false promises and mandates one step per iteration. Repeating it invites
  contradiction when one copy is edited.
