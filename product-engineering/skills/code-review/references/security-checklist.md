# Security checklist

A condensed, high-consequence checklist for the review's security pass.

Security-category findings at Medium+ confidence are always blocking. Cite the CWE/OWASP ID when known.

## Input provenance (triage before flagging)

A vulnerability is only real if the data can be attacker-controlled. Trace each
flagged value to its source **before** raising an injection, ReDoS, SSRF, or
path-traversal finding:

- [ ] Static literals, internal enums/constants, and config-derived values are **not** user input — downgrade or drop the finding.
- [ ] Test fixtures and test-only code are not a production attack surface — e.g. a regex passed to a test matcher (`toHaveTextContent(/…/)`) is not production ReDoS.
- [ ] Only escalate when the value provably originates from a request, upload, URL, header, or other external channel and reaches the sink unsanitised.

Scanner findings (CodeRabbit, Datadog, SAST) that ignore provenance are common
false positives — verify the source, do not forward the label verbatim.

## Injection

- [ ] SQL/NoSQL: parameterised queries or ORM — never string-concatenated input.
- [ ] Command/shell: no user input in shell strings; use argument arrays.
- [ ] Deserialization: no untrusted input into unsafe deserializers.

## Web

- [ ] XSS: output encoded for its context; no raw HTML from user input.
- [ ] CSRF: state-changing endpoints protected.
- [ ] SSRF: outbound URLs from user input validated against an allowlist.

## Access and data

- [ ] Authz / IDOR: object access checks the caller owns/may access the resource — not just authentication.
- [ ] Secrets: none hardcoded or logged; read from config/env.
- [ ] Path traversal: file paths from input validated against a base directory.

## Transport and dependencies

- [ ] TLS/cert verification not disabled.
- [ ] New dependencies from trusted sources; no known-vulnerable versions pinned.
