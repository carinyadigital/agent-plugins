## Preset: custom

A user-defined step machine. The core rules above still apply: read state, run
exactly one step, write state, end the turn.

### Sources

- Run context: `{{RUN_DIR}}/context.md`
- Loop state: `{{RUN_DIR}}/loop-state.md`

### Steps

Resolve `{STEP}` from `current_step` in the state file and run only that step.
Each step below states what to do and what to set `current_step` to next.

{{CUSTOM_STEPS}}

### Step contract

Every step must:

1. Do one unit of work.
2. Write its outcome somewhere durable (a file, a commit, an appended note).
3. Set `current_step` to the next step, or leave it unchanged to signal that a
   human is needed.

A step that changes nothing on disk will look like a stall, and after three
such iterations the loop stops. That is intended: it is the difference between
a loop that is working and a loop that is spinning.
