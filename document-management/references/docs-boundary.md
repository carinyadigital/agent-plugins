# The docs/ scope boundary

The hard rule that keeps this plugin from colliding with practice-owned trees and repo-root context files. Every skill and both agents obey it.

## The rule

> **`docs-writer` only ever creates, moves, or edits files inside the configured `docs_root` (default `docs/`).** Everything outside `docs_root` is, at most, read-only context. `docs-reviewer` may *read* anywhere in the repo to judge accuracy — it needs the code to detect drift — but no change the plugin proposes ever lands outside `docs/`.

Staying inside `docs/` is enforced mechanically: an edit targeting a path outside `docs_root` is **refused**, not just discouraged. This is the filesystem counterpart of the review → approve → write privilege boundary.

## In scope vs out

| Path | Write? | Stance |
| :--- | :----- | :----- |
| `docs/**` (the configured `docs_root`) | **Yes** | Full ownership — subject to `protected_paths`. |
| Nested `README.md` / `index.md` *inside* `docs/` | **Yes** | These are `docs/` landing pages, not the repo's front door. |
| Root `README.md` | No | Read-only context. Raise a finding and defer the edit to a human. |
| `AGENTS.md` / `CLAUDE.md` | No | Read-only context (stack, conventions) that helps write better docs. Raise a finding and defer the edit to a human. |
| Source code, config, anything else | No | Read-only context, for drift detection only. |

## When something belongs elsewhere

If the plugin finds content that ought to live outside `docs/` — a full tutorial crammed into the root README, or a convention that belongs in `AGENTS.md` — it does **not** reach out and edit that file. It:

1. Raises a **finding** with the suggested destination.
2. Leaves the change to a human.

Read widely, write narrowly.

## Default protected_paths

Within `docs/`, `protected_paths` marks subtrees the writer must never auto-move or auto-edit even though they're under `docs_root`. Findings there are **reported, never applied automatically**.

This plugin's **defaults** keep it from stealing practice-owned trees:

| Path | Owner (typical) |
| :--- | :-------------- |
| `docs/architecture/` | architecture practice (`solution`, `adr`) |
| `docs/product/` | product-management practice |
| `docs/design/` | design practice |
| `docs/brand/` | brand-creative practice (standalone Try-tier brand artefacts) |

A repo may override the list via local config (`.claude/document-management.local.md` or `.cursor/document-management.local.md`). Extra entries are common for legal text or generated reference (for example `docs/reference/api/` built from OpenAPI). Replacing the defaults is allowed; do not silently drop the practice trees unless the user asked to.

## Coexistence with `/engineering:docs-review`

`/engineering:docs-review` is a **read-only quality/consistency review of any document set** (a handbook, `product.md`, `solution.md`, a wiki). This plugin owns the **`docs/` tree lifecycle** — scaffold/reorganise (`docs-setup`) and score/fix including drift and voice (`docs-improve`). The two do not compete: docs-review never restructures the tree; this plugin never reviews an arbitrary document set outside `docs_root`.
