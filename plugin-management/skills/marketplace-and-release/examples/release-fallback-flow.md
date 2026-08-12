# Worked example: the generic fallback release flow

What to do when a repo has **no** existing `/release` command, `release` npm script,
or `Makefile` target — the fallback path from the main skill body, end to end, for a
brand-new plugin's first release.

## 1. Confirm there's genuinely no existing automation

```bash
# Look for common release entry points before assuming there's none.
ls .claude/skills/ .cursor/skills/ 2>/dev/null | grep -i release
grep -A2 '"scripts"' package.json 2>/dev/null | grep -i release
ls Makefile 2>/dev/null && grep -i "^release:" Makefile
```

Nothing found — proceed with the fallback below.

## 2. Determine the version

`changelog-helper` is a brand-new plugin, so this is `0.1.0` regardless of the
patch/minor/major table — a first release isn't a bump.

## 3. Set the version in every manifest flavor

```json
// plugins/changelog-helper/.claude-plugin/plugin.json
// plugins/changelog-helper/.cursor-plugin/plugin.json
{
  "version": "0.1.0"
  // ...
}
```

Both files, same value — this is the same manifest-pair rule `plugin-structure` states
for every other field.

## 4. Re-run the validator

```bash
python3 scripts/validate.py   # or whatever this repo's own structural check is
```

Confirms the new manifest and the new catalogue entries (§ registration, done earlier)
are all consistent before anything gets committed.

## 5. Commit and push, with explicit confirmation first

```
⚠ This pushes to main. Confirm before proceeding: yes/no?
```

```bash
git add plugins/changelog-helper .claude-plugin/marketplace.json .cursor-plugin/marketplace.json
git commit -m "feat(changelog-helper): add plugin for project-style changelog entries"
git push
```

Only the files this change touched are staged — not `git add -A`, which could sweep
in unrelated in-progress work sitting in the same working tree.

## Contrast with the existing-automation path

If step 1 *had* found a `/release` skill, none of steps 2-5 above would run by hand —
the main skill body says to hand off to that automation instead, since it likely
already encodes this repo's specific versioning/commit conventions more precisely
than this generic fallback can.
