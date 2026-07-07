# Comment guidelines

How to write review comments that get acted on. A review comment has one
job: give the author a clear, justified action they can take without a
follow-up question.

## Label every comment

Use Conventional Comments-style labels so severity is machine- and
human-readable at a glance:

| Label | Meaning | Blocking? |
| ----- | ------- | --------- |
| `issue:` | A defect — correctness, security, missing tests, undeclared scope | Yes, unless suffixed `(non-blocking)` |
| `suggestion:` | A concrete improvement with the proposed change included | No, unless suffixed `(blocking)` with a reason |
| `question:` | A genuine question whose answer may change the verdict | Blocks only until answered |
| `nit:` | Minor polish — naming, wording, formatting the linter missed | Never |
| `praise:` | Something genuinely well done | Never |
| `thought:` | An idea for later; explicitly not asked of this MR | Never |

If the provider or repo uses a different labelling convention (visible in
recent reviews), follow it instead — never mix two conventions in one
review.

## Anatomy of a good comment

1. **Label** first.
2. **Evidence** — what the code does, at this line, in observable terms.
3. **Why it matters** — the failure case, the reader cost, the convention it
   breaks. Skip when self-evident.
4. **The action** — what change unblocks it. For suggestions, include the
   code (as a provider suggestion block where supported, so it is
   one-click applicable).

> `issue:` `refreshToken` is written to the debug log on line 41. Anyone
> with log access can replay a session. Redact it or drop the line.

## Tone

- Comment on the code, never the author: "this loop re-reads the file per
  iteration", not "you re-read the file".
- Prefer questions when the author may know something you don't: "was
  the retry deliberately removed?" beats "you deleted the retry".
- No sarcasm, no "obviously", no "just". Terse is fine; curt is not.
- One genuine `praise:` where deserved beats reflexive positivity.

## Discipline

- **One concern per comment**, anchored to the most specific line — not a
  paragraph of five issues on the file header.
- The same finding repeated across many lines: comment once, note "applies
  to the other N occurrences", and trust the author.
- **Blocking must be scarce.** If more than a handful of comments are
  blocking, the real verdict is "request changes for the pattern" — say
  that in the summary instead of carpet-bombing.
- Every blocking comment states what unblocks it.
- The summary comment carries the verdict rationale: 2–4 sentences —
  what you checked, what stands out, what (if anything) blocks approval.
