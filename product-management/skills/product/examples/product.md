---
type: Product Strategy
---

# Product -- Checkout

## 1. Problem

Shoppers cannot complete a purchase on the new storefront. The checkout page renders but the "Place order" button does nothing, and there is no order confirmation.

- No payment entry. The payment section is scaffolded but empty.
- No placement action. Clicking "Place order" discards the request silently.
- No confirmation. After a successful charge there is nowhere to redirect.
- No funnel visibility. With zero placed orders there is no conversion baseline.

## 2. Appetite

Two phases. Now (Alpha): end-to-end placement reaches staging with real payment processing. Next: guest checkout, order history, and error recovery.

## 3. Sketch

- A payment form with real-time card validation and provider tokenisation.
- A server-side placement action: validate → charge → create order → redirect.
- An order confirmation page with order number, line items, and delivery estimate.

## 4. Rabbit holes

- Owning the payment provider. The storefront calls one charge endpoint and surfaces the result — nothing more.
- Client-side order state. The confirmation page reads from a server fetch. The customer lands on `/order/[id]` only when the ID exists on the server.
- Multi-currency. One locale and currency in scope. Regional variants are deferred.

## 5. No-gos

- Subscriptions or recurring orders.
- Split-payment or pay-later workflows.
- Saved payment methods.
- Order cancellation or returns.
- Real-time delivery tracking.
