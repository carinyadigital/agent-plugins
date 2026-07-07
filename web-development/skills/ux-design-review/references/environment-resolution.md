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

- **Viewports:** 1440×900 (desktop, default), 768 (tablet), 375 (mobile).
- **Screenshots:** every finding gets one; captures go to the session
  scratch directory or a gitignored `.ux-review/` — **never committed**.
  Name them `<page-or-component>-<state>-<viewport>.png`.
- **Console:** collect errors/warnings while exercising flows.
- **Accessibility scan:** inject axe-core (`@axe-core/playwright` or
  equivalent) on each changed page — see
  [accessibility-checklist.md](accessibility-checklist.md) for what the
  scan does and does not cover.
- **State setup:** reach loading/empty/error states by throttling,
  emptying data, or invalid input; a state you cannot reach is reported as
  unverified, not assumed to pass.

## Recording the resolution

```text
Environment: <URL | dev-server cmd | storybook | static-only>
Driver: <playwright script | browser MCP | n/a>
Viewports: <tested list>
Not testable: <states/flows unreachable, and why>
```

Every verdict includes a coverage statement derived from this bundle:
which lenses ran live, which ran static, which did not run.
