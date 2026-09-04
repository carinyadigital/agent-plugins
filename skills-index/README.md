# skills-index

Install-aware skill router for the `agent-plugins` marketplace.

## Skills

| Skill | Purpose |
| ----- | ------- |
| **find** | Route vague requests to an installed skill, or offer an install command |
| **related-skills-surfacer** | After a task, mention one strong uninstalled match (optional) |

```
/skills-index:find how do I start delivery?
```

## Why a separate plugin

With the hub gone there is no meta-plugin to absorb the router. Scope is
intentionally narrow: discovery of uninstalled plugins, and workflow sequencing
the platform does not know.
