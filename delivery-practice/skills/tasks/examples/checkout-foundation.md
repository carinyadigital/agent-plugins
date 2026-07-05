---
type: Tasks
epic: checkout-foundation
epic_id: CHK01
---

# Tasks -- Checkout Foundation (CHK01)

Tasks for `docs/work/checkout-foundation/`, epic CHK01 from `docs/product/backlog.md`.

Companion artefacts: `./design.md` · `docs/architecture/solution.md`

## 1. Summary

- **Epic.** CHK01 -- Checkout Foundation
- **Phase.** Now / Alpha
- **Priority.** P0 (blocks CHK02+)
- **Estimate.** 13 points across 4 tasks

**Scope.** Module scaffold, orders API client, `OrderViewModel` + mapper, `placeOrder` Server Action (stub), `(checkout)` route group, checkout page shell, loading skeleton.

**Out of scope (this epic).** Live payment form (CHK02), confirmation page (CHK03), guest checkout (CHK05).

## 3. Tasks

- [ ] **[CHK01-01] Checkout module scaffold and view-model types**
  - **Status:** Not started | **Priority:** P0 | **Estimate:** 2
  - **Epic:** CHK01 | **Labels:** phase:alpha, checkout, type:scaffold
  - **Depends on:** -
  - **Deliverable:** `modules/checkout/` with `logic/types.ts` defining `OrderViewModel` and all slice types; server and client barrels.
  - **Design:** `./design.md#21-module-layout`
  - **Acceptance (Gherkin):**

    ```gherkin
    Scenario: Server barrel exposes the canonical view model
      Given the checkout module is installed
      When a server component imports { OrderViewModel } from '@/modules/checkout'
      Then the import resolves without error
      And the type matches solution.md §6 exactly

    Scenario: Client barrel exports only client-safe symbols
      Given the checkout module is installed
      When a client component imports from the checkout client barrel
      Then no server-only modules are re-exported
    ```

- [ ] **[CHK01-02] Orders API client**
  - **Status:** Not started | **Priority:** P0 | **Estimate:** 3
  - **Epic:** CHK01 | **Labels:** phase:alpha, checkout, type:integration
  - **Depends on:** CHK01-01
  - **Deliverable:** `data/clients/orders-api.server.ts` with `createOrder()`, `getOrder()`, and `listOrders()`; `import 'server-only'` at the top.
  - **Design:** `./design.md#22-data-layer`
  - **Acceptance (Gherkin):**

    ```gherkin
    Scenario: createOrder reaches the orders API with a typed body
      Given a valid PlaceOrderBody
      When createOrder(body) is called
      Then a POST is made to ORDERS_API_URL/orders
      And the response is mapped to ApiOrder

    Scenario: Non-2xx response throws a typed error
      Given the orders API returns 503
      When createOrder(body) is called
      Then an OrderApiError is thrown with status 503
    ```

- [ ] **[CHK01-03] Checkout route group and page shell**
  - **Status:** Not started | **Priority:** P0 | **Estimate:** 5
  - **Epic:** CHK01 | **Labels:** phase:alpha, checkout, type:scaffold
  - **Depends on:** CHK01-01
  - **Deliverable:** `app/(checkout)/checkout/page.tsx` RSC shell; `CheckoutSkeleton`; `placeOrder` Server Action returning `NOT_IMPLEMENTED` (placeholder until CHK02).
  - **Design:** `./design.md#24-route-group`
  - **Acceptance (Gherkin):**

    ```gherkin
    Scenario: Authenticated customer reaches the checkout page
      Given the customer is signed in and has items in the cart
      When the customer navigates to /checkout
      Then the page returns HTTP 200
      And CheckoutSkeleton is rendered

    Scenario: Unauthenticated customer is redirected
      Given the customer is not signed in
      When the customer navigates to /checkout
      Then the response redirects to /login

    Scenario: placeOrder stub does not call external services
      Given the checkout page is loaded
      When placeOrder is invoked
      Then the result is { error: 'NOT_IMPLEMENTED' }
    ```

- [ ] **[CHK01-04] Mapper and error registry**
  - **Status:** Not started | **Priority:** P0 | **Estimate:** 3
  - **Epic:** CHK01 | **Labels:** phase:alpha, checkout, type:mapper
  - **Depends on:** CHK01-01
  - **Deliverable:** `data/mappers/order.mapper.ts` with `orderToViewModel(ApiOrder): OrderViewModel`; `OrderPlacementErrorCode` closed enum; `getOrderErrorMessage(code)` copy helper.
  - **Design:** `./design.md#23-mapper`
  - **Acceptance (EARS):**
    - THE SYSTEM SHALL export `orderToViewModel` mapping every field in `ApiOrder` to a corresponding `OrderViewModel` slice.
    - WHEN an optional `ApiOrder` field is absent, THE SYSTEM SHALL map it to `null` or a documented default.
    - THE SYSTEM SHALL export `OrderPlacementErrorCode` covering every error code defined in solution.md §7.
  - **Acceptance (Gherkin):**

    ```gherkin
    Scenario: Mapper produces a valid view model
      Given a fully populated ApiOrder fixture
      When orderToViewModel(fixture) is called
      Then every OrderViewModel field has a non-undefined value
      And money fields are formatted as locale currency strings
    ```
