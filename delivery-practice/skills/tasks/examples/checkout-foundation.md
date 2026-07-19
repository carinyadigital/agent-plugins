---
type: Tasks
epic: checkout-foundation
epic_id: CHK01
version: '0.1'
owner: commerce-squad
status: Draft
last_updated: 2026-07-19
source: .agency/work/checkout-foundation/design.md
related:
  - .agency/backlog.md
  - .agency/work/checkout-foundation/design.md
  - .agency/architecture/solution.md
---

# Tasks — Checkout Foundation (CHK01)

## 1. Summary

**Epic:** CHK01 | **Phase:** Now / Alpha | **Priority:** P0 | **Estimate:** 16 points across 2 stories / 6 tasks

**Source.** `./design.md`, epic CHK01 in `.agency/backlog.md`.

**Scope.** Checkout module scaffold, orders API client, view model and mapper,
the `(checkout)` route group, and a page shell that renders a real cart behind
authentication.

**Out of scope (this epic).** Live payment form (CHK02), confirmation page
(CHK03), guest checkout (CHK05).

**MVP.** Story S1 — a signed-in customer can reach `/checkout` and see their
cart. Nothing is payable yet, but the route, auth gate, and data path are proven
end to end.

## 2. Conventions

| Convention | Value |
| ---------- | ----- |
| Story ID | `CHK01-S{n}` |
| Task ID | `CHK01-{nn}` — sequential across the epic, never reused |
| Story label | `[S{n}]` on every task with a parent story |
| Parallel marker | `[P]` — different files, no incomplete dependency |
| Acceptance | Gherkin on the story; EARS where a rule is clearer |
| Estimate | Story points, Fibonacci |

## 3. Foundational

- [ ] **[CHK01-01]** Checkout module scaffold and view-model types — `modules/checkout/logic/types.ts`
  - **Status:** not started | **Estimate:** 2 | **Owner:** TBD
  - **Depends on:** —
  - **Deliverable:** `modules/checkout/` with `logic/types.ts` defining
    `OrderViewModel` and all slice types; separate server and client barrels.
  - **Design:** [`./design.md`](design.md#21-module-layout)
  - **Acceptance (Gherkin):**

    ```gherkin
    Scenario: Server barrel exposes the canonical view model
      Given the checkout module is installed
      When a server component imports { OrderViewModel } from '@/modules/checkout'
      Then the import resolves without error
      And the type matches solution.md §6 exactly

    Scenario: Client barrel leaks no server-only code
      Given the checkout module is installed
      When a client component imports from the checkout client barrel
      Then no server-only module is re-exported
    ```

## 4. Stories

### S1 — Signed-in customer reaches checkout

**As a** signed-in customer, **I want** to open the checkout page and see the
items I am about to buy, **so that** I can confirm my order before paying.

**Independent test criterion.** Sign in, add an item to the cart, navigate to
`/checkout`, and see those items rendered. Signed out, the same URL redirects to
login.

**Priority:** P0 | **Design:** [`./design.md`](design.md#24-route-group)

**Acceptance (Gherkin):**

```gherkin
Scenario: Authenticated customer reaches the checkout page
  Given the customer is signed in and has two items in the cart
  When the customer navigates to /checkout
  Then the page returns HTTP 200
  And both cart line items are rendered with their prices

Scenario: Unauthenticated customer is redirected
  Given the customer is not signed in
  When the customer navigates to /checkout
  Then the response redirects to /login
  And the return path is preserved as a query parameter
```

**Acceptance (EARS):**

```
WHILE the cart is empty
THE SYSTEM SHALL redirect /checkout to /cart rather than rendering an empty page.
```

**Tasks:**

- [ ] **[CHK01-02]** [S1] Orders API client — `data/clients/orders-api.server.ts`
  - **Status:** not started | **Estimate:** 3 | **Owner:** TBD
  - **Depends on:** CHK01-01
  - **Deliverable:** `createOrder()`, `getOrder()`, `listOrders()` with
    `import 'server-only'` at the top and typed error responses.
- [ ] **[CHK01-03]** [P] [S1] Mapper and error registry — `data/mappers/order.mapper.ts`
  - **Status:** not started | **Estimate:** 3 | **Owner:** TBD
  - **Depends on:** CHK01-01
  - **Deliverable:** `orderToViewModel(ApiOrder): OrderViewModel`, the
    `OrderPlacementErrorCode` closed enum, and `getOrderErrorMessage(code)`.
- [ ] **[CHK01-04]** [S1] Checkout route group and page shell — `app/(checkout)/checkout/page.tsx`
  - **Status:** not started | **Estimate:** 5 | **Owner:** TBD
  - **Depends on:** CHK01-02, CHK01-03
  - **Deliverable:** RSC page shell with the auth gate and cart rendering, plus
    `CheckoutSkeleton` for the loading state.

### S2 — Order placement is stubbed safely

**As an** engineer, **I want** `placeOrder` to exist and fail loudly, **so that**
CHK02 can implement payment against a settled contract without the stub ever
reaching a real provider.

**Independent test criterion.** Invoke `placeOrder` from the checkout page and
observe a `NOT_IMPLEMENTED` result, with no outbound call in the network log.

**Priority:** P1 | **Design:** [`./design.md`](design.md#25-server-actions)

**Acceptance (Gherkin):**

```gherkin
Scenario: placeOrder returns a typed not-implemented result
  Given the checkout page is loaded
  When placeOrder is invoked
  Then the result is { error: 'NOT_IMPLEMENTED' }
  And no request is made to the orders API
```

**Acceptance (EARS):**

```
THE SYSTEM SHALL expose placeOrder with the signature specified in
solution.md §7, so that CHK02 can replace the body without changing callers.

IF placeOrder is invoked in a production build
THEN THE SYSTEM SHALL log a warning naming CHK02 as the implementing epic.
```

**Tasks:**

- [ ] **[CHK01-05]** [S2] placeOrder server action stub — `modules/checkout/actions/place-order.ts`
  - **Status:** not started | **Estimate:** 2 | **Owner:** TBD
  - **Depends on:** CHK01-03
  - **Deliverable:** Server Action matching the solution.md §7 signature,
    returning `NOT_IMPLEMENTED` and making no external call.

## 5. Cross-cutting

- [ ] **[CHK01-06]** Checkout module README and env documentation — `modules/checkout/README.md`
  - **Status:** not started | **Estimate:** 1 | **Owner:** TBD
  - **Deliverable:** Module README covering the barrel split, plus
    `ORDERS_API_URL` added to `.env.example`.

## 6. Dependencies

```text
CHK01-01 ──┬── S1: -02 ──┬── -04
           │       [P] -03 ──┘
           └── S2: -05
                          -06 (cross-cutting)
```

**Parallel opportunities.** CHK01-03 runs alongside CHK01-02 — different files,
both depend only on CHK01-01.

**External dependencies.** Orders API v2 staging endpoint — platform squad —
available, no action needed.

## 7. Traceability and Definition of Done

### Stories to design and architecture

| Story | design.md § | solution.md § |
| ----- | ----------- | ------------- |
| S1 | §2.4 Route group | §6 Data model, §4 Building blocks |
| S2 | §2.5 Server actions | §7 Error taxonomy |

### Definition of Done (epic-wide)

- [ ] All Gherkin scenarios pass; all stated EARS rules hold
- [ ] Tests written and CI green
- [ ] Code review approved and merged
- [ ] `ORDERS_API_URL` documented in `.env.example`

## 8. Handoff

Leaves a working `/checkout` route behind auth, a typed orders client, and a
settled `placeOrder` contract. CHK02 replaces the stub body with the live
payment flow; no caller changes.
