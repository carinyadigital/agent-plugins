## Preset: ad-hoc

A single task repeated until it is genuinely done. No step machine, no run
directory, no state file: the working tree and git history are the state.

Because there is no state file, the stall guard does not apply to this preset.
The iteration limit is the only automatic backstop, which is why `--max-iterations`
is mandatory here unless a completion promise is set.

### Task

{{TASK_PROMPT}}

### Each iteration

1. Look at what already exists. Read the files you wrote on previous
   iterations and check `git status` and `git diff`. Your previous work is the
   only memory you have.
2. Identify the single most valuable next thing to do.
3. Do it.
4. Verify it, by running tests, a linter, or the program itself. Verification
   is what makes the loop converge rather than drift.
5. State briefly what you did and what remains.

### Do not

- Start again from scratch because you cannot remember the previous iteration.
  Read the files.
- Repeat work already done. Check before you write.
- Emit the completion promise because progress feels slow. See "Finishing".
