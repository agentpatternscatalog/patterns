# Compensating Action

**Also known as:** Saga, Undo Step, Rollback Action

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Pair every irreversible-looking agent action with a compensating action that can undo or counteract it.

## Context

Multi-step workflows where some steps succeed and later steps fail; without compensation, partial state is left inconsistent.

## Problem

Distributed transactions are not available across most agent tool palettes; failure mid-plan leaves the system in an inconsistent state.

## Forces

- Not every action has a clean compensator.
- Compensation logic is a separate code path.
- Idempotency matters: compensating an already-compensated action must be safe.

## Solution

For each forward action, define a compensating action (delete-after-create, refund-after-charge, archive-after-publish). On failure mid-plan, run compensators in reverse order to restore the prior state. Idempotent compensators.

## Consequences

**Benefits**

- Partial-failure consistency.
- Confidence to attempt multi-step writes.

**Liabilities**

- Doubles the number of action implementations.
- Some actions cannot truly be compensated (sent emails, public posts).

## What this pattern constrains

Forward actions cannot be invoked without a registered compensator; uncompensable actions need explicit operator approval.

## Known uses

- **Saga pattern in microservices, transferred to agents** — *Available*

## Related patterns

- *complements* → [human-in-the-loop](human-in-the-loop.md)
- *uses* → [provenance-ledger](provenance-ledger.md)
- *complements* → [approval-queue](approval-queue.md)
- *used-by* → [kill-switch](kill-switch.md)

## References

- (paper) *Sagas (Garcia-Molina, Salem)*, 1987

**Tags:** safety, saga, transaction
