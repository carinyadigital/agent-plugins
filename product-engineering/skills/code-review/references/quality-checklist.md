# Quality checklist

A stable, project-agnostic checklist applied to every review. Use
**best-practices-reviewer** for library-specific, version-correct guidance and
**conventions-reviewer** for this team's own written and spoken rules. This file is for
timeless principles, with the team's stance where one exists. Do not flag
textbook definitions the code obviously follows.

## Design principles (priority order)

When these principles conflict, the earlier one wins: **YAGNI > KISS > DRY**.

- [ ] YAGNI: no speculative generality — build for today's requirement, not a hypothetical future. Flag abstractions, options, parameters, or config with no current caller.
- [ ] KISS: prefer the simplest thing that works. A defensive guard for a state that cannot occur, or an abstraction that adds indirection without a second caller, is over-engineering — raise it.
- [ ] DRY: remove genuine duplication, but only after YAGNI and KISS. A premature abstraction is worse than the duplication it removes.

## Correctness and flow

- [ ] Errors: fail fast; typed/domain errors, not bare strings; no silent catch-and-continue.
- [ ] Resource cleanup on every path (files, connections, locks) — prefer `with`/`defer`/`finally`.
- [ ] Boundaries validated: null/empty, off-by-one, unexpected input.
- [ ] Async: awaited where it matters; no fire-and-forget that drops errors.

## Duplication and structure

- [ ] DRY: extract on the **third** occurrence, not the second — avoid premature abstraction.
- [ ] Reuse audit: search for an existing helper/util before adding new code. Check adjacent files and shared modules.
- [ ] Single responsibility per unit; no god functions.

## Testing

- [ ] Tests assert **behaviour**, not implementation detail.
- [ ] Error, loading, empty, and edge-case states covered — not just the happy path.
- [ ] Key user journeys covered end-to-end where the stack supports it.
- [ ] Coverage not weakened: existing tests kept; a wrong test is fixed, not deleted.

## Data and contracts

Apply when the diff touches migrations, schema definitions, persisted models,
event payloads, or any published API. Findings here take the **Data Integrity**
category. Rate against reversibility, not immediate blast radius: a bad
migration outlives the deploy that shipped it.

- [ ] Migration is reversible, or its irreversibility is deliberate, documented, and called out in the change description.
- [ ] A rollback path exists and has been stated — not assumed.
- [ ] Adding a non-nullable column supplies a default or a backfill; the backfill is batched, resumable, and safe to re-run.
- [ ] Index creation on a large table uses the non-blocking form the engine provides (`CONCURRENTLY` or equivalent), or the lock window is acknowledged.
- [ ] Schema change and the code that depends on it can deploy independently — expand/contract, not a single breaking step.
- [ ] Changes to published API responses, event payloads, or shared schemas are additive; removals and type changes are versioned or gated.
- [ ] Consumers of a changed contract are identified. "Who reads this field?" has an answer before the field changes shape.
- [ ] Data written in one format and read in another has a migration for the in-flight case (queued messages, cached payloads, partially-migrated rows).

## Observability

- [ ] Logging: structured, at boundaries; **no PII or secrets**; correct level (no debug spam in hot paths).
- [ ] Errors surfaced with enough context to diagnose, not swallowed.
- [ ] A correlation/request ID is propagated end-to-end across service calls.
- [ ] New endpoints/routes have monitoring and alert thresholds.

## Resilience

- [ ] External calls degrade gracefully — timeouts, retries where appropriate, no unbounded waits.
- [ ] Failures are contained (error boundaries where the platform provides them) and never silently swallowed.

## Performance

- [ ] Independent I/O runs in parallel; non-critical work is deferred or streamed.
- [ ] No obvious N+1 or repeated work in hot paths.
- [ ] Cache entries document their TTL and invalidation strategy.

## Naming and clarity

- [ ] Names reveal intent; no abbreviations that need a comment to decode.
- [ ] Comments explain **why**, never **what**.

## Type safety and hygiene

- [ ] Single source of truth for types — inferred from the schema, not duplicated by hand.
- [ ] Zero lint errors and zero type errors introduced.
