# Acceptance criteria

Gherkin is the default. EARS is available where a rule is clearer than a
scenario. This file specifies both.

---

## Gherkin (default)

Acceptance criteria live on the **story**, because that is where user-observable
behaviour lives. A foundational task with no parent story carries its own.

```gherkin
Scenario: Authenticated customer reaches checkout
  Given the customer is signed in and has items in the cart
  When the customer navigates to /checkout
  Then the page returns HTTP 200
  And the cart contents are rendered
```

### Rules

- **At least one scenario per story.** Two when the happy path and an edge case
  both matter — write the edge that actually breaks, not a symmetrical negative.
- **One behaviour per scenario.** A scenario testing two things fails
  ambiguously.
- **`Then` must be observable.** Something a test can assert or a reviewer can
  see on screen.
- **`Given` sets state, `When` is the single trigger, `Then` is the outcome.**
  Multiple `When` steps mean two scenarios.
- **No implementation detail.** "Then `OrderService.create()` is called" tests
  the design, not the behaviour. "Then the order appears in the customer's
  order history" survives a refactor.

### Observable vs not

| Not observable | Observable |
| -------------- | ---------- |
| Then it works correctly | Then the response status is 201 |
| Then the data is handled properly | Then the order total includes GST at 10% |
| Then performance is acceptable | Then the page reaches LCP under 2.5s at p75 |
| Then the user is happy | Then a confirmation email is queued within 5s |
| Then errors are handled | Then a 503 from the orders API surfaces as "Try again shortly" |

---

## EARS

Easy Approach to Requirements Syntax. Five patterns, each for a different shape
of requirement. Use `THE SYSTEM SHALL` in every one.

| Pattern | Syntax | Use for |
| ------- | ------ | ------- |
| Ubiquitous | THE SYSTEM SHALL {behaviour} | Invariants that always hold |
| Event-driven | WHEN {trigger} THE SYSTEM SHALL {behaviour} | Response to a discrete event |
| State-driven | WHILE {state} THE SYSTEM SHALL {behaviour} | Behaviour that holds throughout a state |
| Unwanted behaviour | IF {condition} THEN THE SYSTEM SHALL {behaviour} | Error handling, misuse, failure |
| Optional feature | WHERE {feature is included} THE SYSTEM SHALL {behaviour} | Behaviour behind a flag or tier |

### Worked examples

```
Ubiquitous
  THE SYSTEM SHALL store payment card numbers only as provider tokens.

Event-driven
  WHEN the customer submits the checkout form
  THE SYSTEM SHALL create exactly one order per idempotency key.

State-driven
  WHILE an order is in `pending_payment`
  THE SYSTEM SHALL reject any modification to its line items.

Unwanted behaviour
  IF the payment provider does not respond within 10 seconds
  THEN THE SYSTEM SHALL fail the order as `payment_timeout` and release the
  cart reservation.

Optional feature
  WHERE express checkout is enabled for the customer's region
  THE SYSTEM SHALL skip the shipping-address step for saved addresses.
```

---

## Choosing between them

**Gherkin** is better at journeys: a sequence of state, trigger, and outcome
that someone can walk through or a test can drive.

**EARS** is better at rules: invariants, constraints, NFRs, and always/never
statements. Expressing "the system never stores raw card numbers" as a scenario
is awkward — there is no natural `When`, and any scenario you write tests one
instance of a universal rule.

Reach for EARS when:

- The rule holds across all scenarios rather than in one
- It is a constraint or a quantified NFR (latency, throughput, retention)
- It is a security or compliance obligation
- The behaviour is conditional on a flag, tier, or region
- You catch yourself writing a scenario with no meaningful `Given`

### Applying it

- **Default** — Gherkin only. Add EARS where the rules above apply, and omit the
  section entirely when they do not.
- **`--ears`** — every story gets both: Gherkin for the journey, at least two
  EARS statements for the rules governing it.
- **Never duplicate.** An EARS statement that restates a scenario is noise.
  If the scenario already covers it, drop the EARS line.

---

## Definition of Done vs acceptance criteria

Acceptance criteria are per story: is *this behaviour* correct? The Definition
of Done is per epic and uniform: tests pass, CI green, review approved, docs
updated. Do not smuggle DoD items into a story's criteria — "and the code is
reviewed" is not acceptance criteria for a checkout page.
