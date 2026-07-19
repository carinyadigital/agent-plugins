# Environment resolution

How to get a **runnable UI** to review, and what to do when there isn't
one. Live-first is this skill's method: judge rendered pixels and real
interaction wherever possible. Resolve once, up front, and share the result
with every sub-agent.

## Resolution ladder

Stop at the first level that works:

1. **Already-running app** — the user passed a URL, or a dev server is
   already up (check the obvious ports before starting anything).
2. **Start the project's dev server** — discover the command in priority
   order: `AGENTS.md`/`CLAUDE.md` → a project `run`/dev skill if one exists
   → package scripts (`dev`, `start`, `serve`) or the framework default.
   Run it in the background; wait for the ready signal; verify with one
   probe request.
3. **Storybook / component workshop** — when the app won't run but
   `storybook` (or an equivalent) is configured, review changed components
   in isolation. Full flows can't be judged — say so.
4. **Static HTML / artifacts** — for plain HTML/CSS changes, open the files
   directly in the browser.
5. **Static-only review** — nothing runs (missing env vars, backend
   dependencies, non-installable toolchain). Do not fight the environment
   for more than a few minutes: fall back to reviewing templates/JSX/CSS
   statically, run only the static lenses (design-system audit, semantic
   markup, labels/alt/ARIA in the diff), and **state the reduced coverage
   in the verdict**. A static-only review can still FAIL on what it sees,
   but its PASS is explicitly partial.

## Driving the browser

Use whatever the host provides, in preference order:

- **Playwright library + bundled Chromium** — hosted Claude Code
  environments have Chromium preinstalled with Playwright configured
  (`PLAYWRIGHT_BROWSERS_PATH`); write small Node/Python scripts to
  navigate, interact, resize, and screenshot. Do not run
  `playwright install`; if the project pins a different Playwright, launch
  with the preinstalled executable path.
- **Browser MCP tools** — the Playwright MCP server (Cursor and others):
  navigate / click / type / resize / screenshot / console-messages tools.
- **Project harness** — an existing E2E setup (Playwright/Cypress config)
  can be borrowed for state setup, but drive the review interactions
  yourself.

## Standard review pass

The capture itself — what to capture, in what states and viewports, and how to make it
reproducible — is specified in
[capture-protocol.md](capture-protocol.md). Drive the browser **once**, produce the
evidence bundle there, and hand it to every lens. Do not let lenses drive the browser
independently.

## Browser coverage

One Chromium, unless the host provides more. Cross-browser rendering differences
(Safari's form controls, Firefox's font rendering) are **out of scope** and go in the
coverage statement as a stated limitation, not silently omitted. A reader who assumes
Safari was checked because the review did not say otherwise has been misled.

## Review state

Look for `.agency/reviews/ux-{branch}.json`. If present, this branch has been reviewed
before and the run is **incremental**.

```json
{
  "branch": "feat/checkout-summary",
  "last_reviewed_sha": "a1b2c3d",
  "design_source_ref": "figma:123:456@v12",
  "reviewed_at": "2026-07-19T09:00:00Z",
  "findings": [
    {
      "id": "ux-001",
      "component": "PaymentForm",
      "states": ["default", "focus"],
      "viewports": [375, 1440],
      "category": "Accessibility",
      "criterion": "2.4.7",
      "severity": "Major",
      "action": "blocking",
      "status": "open",
      "summary": "Card number field has no visible focus indicator"
    }
  ],
  "accepted_deviations": [
    { "component": "SummaryCard", "what": "denser padding than mockup", "why": "work item PROJ-12 states intentional" }
  ],
  "unreachable_states": [
    { "component": "PaymentForm", "state": "declined", "why": "needs gateway sandbox" }
  ]
}
```

On an incremental run:

- Re-capture only the components the diff touched, plus anything whose design source
  ref changed (see
  [design-source-resolution.md](design-source-resolution.md) — Design-side drift).
- **Never re-raise a `dismissed` finding** for unchanged code and an unchanged design.
- **Never re-raise an `accepted_deviation`.** These are re-litigated on every run today,
  which is the fastest way to make a reviewer stop reading the fidelity section.
- **Retry `unreachable_states`** rather than skipping them silently — the environment
  may have improved.
- Report the delta: fixed, still open, newly introduced, and *newly diverged because the
  design moved*.

## Recording the resolution

```text
Environment: <URL | dev-server cmd | storybook | static-only>
Driver: <playwright script | browser MCP | n/a>
Browser: <Chromium only | list>
Viewports: <tested list>
Theme: <light only | light + dark | forced-colors tested>
Review mode: <full | incremental from <sha>>
Not testable: <states/flows unreachable, and why>
```

Every verdict includes a coverage statement derived from this bundle and the capture
manifest: which lenses ran live, which ran static, which did not run, which states were
unreachable, and which browsers and themes were **not** covered.
