# Diátaxis structure — the docs/ standard

The organising backbone for a repo's `docs/` tree. Based on the [Diátaxis framework](https://diataxis.fr/) (Daniele Procida), proven at Django, Kubernetes, and Canonical. `docs-setup` scaffolds and reorganises against this file.

## The four content types

Technical documentation serves four distinct needs. Each doc should be exactly one type — mixing them is the single most common cause of unusable docs.

| Type | Serves | Reader is | Answers |
| :--- | :----- | :-------- | :------ |
| **Tutorial** | Learning | studying + doing | "take me by the hand through my first…" |
| **How-to guide** | A task | working + doing | "how do I solve this specific problem?" |
| **Reference** | Information | working + knowing | "what exactly is X / what are the options?" |
| **Explanation** | Understanding | studying + knowing | "why does it work this way?" |

## The compass

To classify any doc (or section, or paragraph), ask two questions:

1. **Action or cognition?** Is it about *doing* something, or *knowing* something?
2. **Acquisition or application?** Does it serve *study* (learning) or *work* (a task at hand)?

- action + acquisition → **tutorial**
- action + application → **how-to guide**
- cognition + application → **reference**
- cognition + acquisition → **explanation**

The two easy-to-confuse pairs: tutorials and how-tos both have steps (differ on learning-vs-working); reference and explanation are both knowledge (differ on working-vs-studying).

## The folder standard

```
docs/
├── index.md            # landing page: what's here, who it's for, where to start
├── tutorials/          # learning-oriented lessons
│   └── index.md
├── how-to/             # task-oriented recipes
│   └── index.md
├── reference/          # information-oriented, neutral, mirrors the product structure
│   └── index.md
└── explanation/        # understanding-oriented background and "why"
    └── index.md
```

- **One type per document; a place for everything.** If a doc doesn't fit a folder, that's usually a sign it's conflated and should be split.
- **`index.md` is the landing page** of `docs/` and of each type folder — it orients and points, it doesn't hold the content itself.
- Small or young repos can start with fewer folders and grow into the full set; the *types* still apply even before the folders do.
- **Do not scaffold into protected practice trees.** Default `protected_paths` (`docs/architecture/`, `docs/product/`, `docs/design/`, `docs/brand/`) stay where they are — see [`docs-boundary.md`](docs-boundary.md).

## Naming conventions

- **Lowercase kebab-case**, hyphens not underscores or spaces: `set-up-your-environment.md`. The filename becomes the URL slug, and search engines treat hyphens as word separators.
- **ASCII alphanumeric only.** No generic names (`document1.md`, `untitled.md`).
- **`index.md`** for directory landing pages.
- Preserve conventional uppercase for repo-root files only (`README`, `LICENSE`, `CHANGELOG`) — those live at the repo root, not in `docs/`.

## Navigation

- **Explicit navigation beats auto-discovery.** If the repo renders a docs site, define the nav order deliberately (for example `nav:` in a site config, or a table of contents) rather than relying on alphabetical ordering. This plugin stays generator-agnostic — it manages Markdown source and the nav intent, not a specific site tool.
- Keep the hierarchy shallow. Cross-link between types (a how-to links to the relevant reference; an explanation links to the tutorial) instead of deep nesting.
- Most important content first, on both the `index.md` and within each page.

## Where shared / cross-repo docs go

Docs that describe a single repo live in that repo's `docs/`. Docs that span repos (platform-wide architecture, cross-service runbooks) belong with the platform they describe — note the location and link to it rather than duplicating it into every repo. This plugin only ever writes inside the current repo's configured `docs_root` (see [`docs-boundary.md`](docs-boundary.md)).
