# Worked examples: rewriting host-coupled content as portable

Four before/after pairs across the places portability tends to slip in unnoticed.

## 1. A skill body describing a mechanism instead of an outcome

```markdown
# Host-coupled
When the user wants to explore three options at once, use the Workflow tool to fan
out three parallel sub-agents, one per option, then merge their outputs.

# Portable
Explore the three options. Where the host supports running independent sub-agents
concurrently, dispatch one per option and merge their findings; otherwise work through
them one at a time. Either way, produce one comparison at the end.
```

## 2. A command step assuming one specific CLI is always present

```markdown
# Host-coupled
Run `gh pr view --json reviews` to check review status.

# Portable
Check the PR's review status: prefer a connected code-review MCP server if one is
configured; otherwise fall back to this host's git-hosting CLI (`gh` for GitHub,
`glab` for GitLab) — detect which one is on PATH rather than assuming a specific one.
```

## 3. An agent's `tools:` field, and why this one is different

```markdown
# Written for advisory prose elsewhere in the same file — generic is fine here:
"This agent needs to read files and run shell commands."

# Written in the tools: frontmatter field itself — a specific host's runtime parses
# this literally, so the generic name doesn't just under-describe, it can silently
# fail to grant the capability at all:
tools: Read, Glob, Grep, Bash
```

Don't "fix" the second one to `Shell` for genericity's sake — see the main skill body
for why the field that's mechanically parsed needs the real name, while the prose
around it can and should stay generic.

## 4. A skill that hard-fails without a specific integration

```markdown
# Host-coupled
Fetch the current on-call schedule from the paging MCP server.

# Portable
Fetch the current on-call schedule: use the paging MCP server if one is connected.
If none is configured, say so explicitly and ask the user to paste the current
on-call name rather than blocking the rest of the task on a missing integration.
```

Notice the shared shape across all four: name what should ideally happen, then state
what happens when the ideal path isn't available — in the same sentence or the same
short block, not as an afterthought caveat several paragraphs later.
