# Fallback Chain

**Also known as:** Cascade Fallback, Try-Then-Try-Else, Tool Failed Fall Back, Provider Failed Retry Other

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

Try a primary handler; on failure or low confidence, fall through to a sequence of fallback handlers.

## Context

Production agents where any single model or tool can fail (rate limits, errors, low-confidence outputs); end-users still need an answer.

## Problem

Single-handler failure cascades to the user as an outage; low-confidence outputs degrade UX silently.

## Forces

- Fallback handlers may be slower or worse.
- Detecting 'failure' requires a confidence signal.
- Cascade depth must be bounded.

## Solution

Define an ordered chain of handlers. Each handler returns either a confident answer or a failure/low-confidence signal. On failure, the next handler runs. Final fallback is a generic 'I don't know' rather than a wrong answer.

## Consequences

**Benefits**

- Graceful degradation under partial failures.
- Each layer can be tuned independently.

**Liabilities**

- Cumulative latency on full cascade.
- Hides quality regressions in the primary.

## What this pattern constrains

Each handler may produce a result or pass; only the chain may decide to terminate.

## Known uses

- **Most production routing layers** — *Available*
- **AI-Standards Fallback Chain pattern** — *Available*

## Related patterns

- *complements* → [routing](routing.md)
- *composes-with* → [circuit-breaker](circuit-breaker.md)
- *complements* → [multi-model-routing](multi-model-routing.md)
- *generalises* → [provider-fallback](provider-fallback.md)
- *complements* → [confidence-reporting](confidence-reporting.md)
- *complements* → [exception-recovery](exception-recovery.md)
- *complements* → [graceful-degradation](graceful-degradation.md)
- *used-by* → [open-weight-cascade](open-weight-cascade.md)

**Tags:** routing, fallback, reliability
