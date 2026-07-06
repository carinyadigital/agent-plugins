---
type: Backlog
level: epic
---

# Backlog -- Checkout

- **Product:** `.agency/product.md`
- **Solution:** `.agency/architecture/solution.md`
- **Roadmap:** `.agency/roadmap.md`

## 1. Summary

**Objective.** Deliver end-to-end order placement: payment form, placement action, and order confirmation.

**Prerequisites (required).** Cart service delivers `CartViewModel` with line items and totals. Payments sandbox in staging. Orders API staging endpoint verified.

**Out of scope.** See `product.md` §5 and `roadmap.md` deferred section.

## 2. Conventions

| Convention | Value |
| ---------- | ----- |
| Epic ID | `CHK{nn}` |
| Epic work path | `.agency/work/{epic}/` — kebab-case from title or short title, max two words |
| Task ID | `CHK{nn}-{nn}` in `.agency/work/{epic}/tasks.md` |
| Priority | P0–P2 |
| Estimation | Fibonacci points |

## 3. Epic breakdown

| Epic ID | Title | Phase | Priority | Deps | Points | Work path | Status |
| ------- | ----- | ----- | -------- | ---- | ------ | --------- | ------ |
| CHK01 | Checkout Foundation | Now | P0 | - | 13 | `.agency/work/checkout-foundation/` | Done |
| CHK02 | Payment Placement | Now | P0 | CHK01 | 18 | `.agency/work/payment-placement/` | Not started |
| CHK03 | Order Confirmation | Now | P0 | CHK02 | 8 | `.agency/work/order-confirmation/` | Not started |

## 4. Critical path

```text
CHK01 → CHK02 → CHK03
```
