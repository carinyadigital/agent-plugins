# UX heuristics

The judgement bar when comparing against taste rather than a design source
— and the whole bar when no design source exists (say so in the verdict).
Timeless, framework-agnostic; the app's own internal consistency always
outranks these when the two conflict.

## Hierarchy & layout

- One clear primary action per view; it looks more prominent than
  secondary actions, and destructive actions never look primary.
- Visual weight follows importance: the user's eye lands on the most
  important element first.
- Alignment is deliberate — elements align to a consistent grid; nothing
  sits one-off by a few pixels.
- Spacing communicates grouping: related elements sit closer than
  unrelated ones; spacing rhythm is consistent across siblings.
- Density fits the task: dashboards may be dense, first-run and forms
  breathe.

## Consistency

- The same action looks and behaves the same everywhere (icon, label,
  placement, confirmation behaviour).
- Terminology is one-to-one: one name per concept across UI, copy, and
  URLs.
- New UI follows the patterns of its siblings — an inconsistent
  improvement is still an inconsistency; propose it as a pattern change
  instead.
- Interactive and non-interactive elements are visually distinct;
  clickable things look clickable, and nothing that looks clickable is
  not.

## Feedback & state

- Every user action gets a visible response within ~100ms — even if just
  a pressed state or spinner.
- Long operations show progress; the UI never dead-ends without a next
  step.
- Empty states guide ("create your first…"), never just "no data". Error
  states say what happened and what to do, in human language.
- State is visible: selected, active, syncing, unsaved — the user should
  never have to act to find out.

## Forgiveness

- Destructive actions confirm, or better, are undoable.
- Input is forgiving: trims whitespace, accepts obvious formats, preserves
  the user's work on error.
- Validation happens at the right time — inline after the field is left,
  not on every keystroke, not only after submit.

## Typography & color

- Type hierarchy is limited and consistent — a handful of sizes/weights
  used the same way everywhere.
- Line length and line height keep body text readable (~45–90 characters).
- Color carries meaning consistently (one red = one meaning) and is never
  the only carrier of meaning.
- Text over images/gradients stays readable in all states.

## Motion

- Animation explains (where things came from / went), never decorates at
  the cost of speed; nothing essential is animation-only.
- Durations are quick (~100–300ms for most transitions); nothing blocks
  input while animating; `prefers-reduced-motion` is respected.

## Copy

- Labels say what things do ("Save changes", not "OK"); sentence case
  unless the app's convention differs.
- Copy is concise, front-loaded, and free of blame ("Couldn't save — check
  your connection", not "You entered invalid data").

## Using this reference

Findings from this bar are category **Visual Polish**, **Interaction/UX**,
or **Content**, and are held to the same evidence rule as everything else:
where it happens, what the user experiences, why it matters. If the app
consistently does something differently from this list, that is the app's
convention — do not flag it.
