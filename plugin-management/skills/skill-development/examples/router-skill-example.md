# Worked example: a skill that outgrew one file

Once a skill's detail gets too large to inline every time it triggers, split it into
`references/` and turn `SKILL.md` into a thin router. If you were adding this to a
real plugin, it would live at `skills/api-error-handling/`:

```
skills/api-error-handling/
├── SKILL.md
└── references/
    ├── envelope-format.md
    ├── status-mapping.md
    ├── retry-classification.md
    └── client-surfacing.md
```

## `SKILL.md` — the router

```markdown
---
name: api-error-handling
description: Explains this codebase's API error-handling conventions — error envelope shape, HTTP status mapping, retry classification, and client-side surfacing. Use when the user asks to "handle an API error", "add error handling to an endpoint", "what status code should this return", or is writing a new API client call.
---

# API error handling

Four related but separable concerns, each detailed in its own reference so a task
that only touches one of them doesn't load all four:

| Question | Read |
| :------- | :--- |
| What shape does an error response have on the wire? | `references/envelope-format.md` |
| Which HTTP status code for which failure? | `references/status-mapping.md` |
| Should the client retry this error automatically? | `references/retry-classification.md` |
| How should the UI show this error to a user? | `references/client-surfacing.md` |

## When to use this skill

Writing or reviewing a new endpoint's failure paths; deciding a status code for an
ambiguous case; writing client code that needs a retry-vs-surface decision.
```

Notice the router **states what each reference covers and when to read it**, but
doesn't restate the reference's content. A task about retry behavior only pulls in
`retry-classification.md`, not all four files.

## `references/envelope-format.md` (excerpt)

```markdown
Every API error response uses the same JSON envelope:

{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Order 12345 was not found.",
    "field": null,
    "requestId": "a1b2c3d4"
  }
}

`code` is a stable, machine-readable identifier clients may switch on — never repurpose
an existing code, add a new one instead. Never include a stack trace or secret value
in the envelope.
```

## `references/status-mapping.md` (excerpt)

```markdown
| Situation | Status |
| :-------- | :----- |
| Malformed request | 400 |
| Missing/invalid auth | 401 |
| Authenticated, not permitted | 403 |
| Resource doesn't exist | 404 |
| Conflicts with current state | 409 |
| Well-formed but invalid | 422 |
| Rate limited | 429 |

422 vs 400 is the distinction asked about most often: 400 means "couldn't parse this
at all"; 422 means "parsed fine, fails a business rule."
```

The same split continues for `retry-classification.md` (which statuses retry
automatically, with what backoff) and `client-surfacing.md` (how the UI maps a `code`
to user-facing copy) — each is its own file for the same reason: a task about UI copy
shouldn't have to load the HTTP status table to get there.

This mirrors the pattern described in
[`../references/progressive-disclosure.md`](../references/progressive-disclosure.md) —
read that file for the full rationale on when and how to make this split.
