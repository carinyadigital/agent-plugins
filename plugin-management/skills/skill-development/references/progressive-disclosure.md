# Progressive disclosure: the router pattern

Progressive disclosure means a skill loads in three stages, each cheaper than the
last:

1. **Metadata** (always loaded, for every skill in every installed plugin): just
   `name` and `description` from the frontmatter. This has to be cheap because it's
   loaded whether or not the skill ends up being used.
2. **`SKILL.md` body** (loaded once the description matches the current task): the
   core guidance — should be readable in one pass, a few hundred lines at most.
3. **Bundled resources** (loaded only if the body's own logic decides it needs them):
   `references/`, `prompts/`, `agents/`, `examples/`.

## Why this matters

If stage 2 is too big, every triggering of the skill costs more context than it needs
to — most tasks that match the skill's topic don't need every reference doc, just the
part relevant to what's being asked. If stage 2 is too thin and pushes everything into
stage 3 immediately, the agent has to guess which reference file answers the current
question, which is slower and less reliable than just reading a well-organized body.

## The router shape in practice

Once a skill grows resources, restructure `SKILL.md` itself into a **router**:

- Frontmatter (unchanged).
- A short "what this covers, when to use it" section — same content as before
  splitting, not expanded.
- One paragraph or table per resource file, saying what's in it and when to read it —
  not a summary of its content, just enough to route to the right file.
- Nothing else. If you find yourself writing more than a sentence or two of actual
  guidance in the router before pointing at a resource, that guidance probably belongs
  in the resource instead.

## Sharing knowledge across skills in the same plugin

When two skills in the same plugin would otherwise duplicate a reference doc, promote
it to a plugin-level shared location (e.g. a plugin-root `references/` directory) and
have both skills' routers point at it by relative path. Never copy the same paragraph
into two `SKILL.md` files — the moment one copy is updated and the other isn't, the
skill set has silently drifted.

## Sharing sub-agents across skills

The same rule applies to `agents/`: if a sub-agent is genuinely shared by more than one
skill, it belongs at the plugin root's `agents/` directory, cited by relative path from
each skill that uses it — not duplicated into each skill's own `agents/` subdirectory.
Only give a skill its own private `agents/` when the sub-agent is truly specific to
that one skill's workflow and no other skill in the plugin would ever invoke it.
