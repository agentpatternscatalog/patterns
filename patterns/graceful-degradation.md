# Graceful Degradation

**Also known as:** Feature-Level Fallback, Degraded Mode

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

When a dependency fails, downgrade the user-facing experience to a working subset rather than failing entirely.

## Context

Agent products that depend on multiple optional capabilities (retrieval, vision, code-execution) where any single dependency may fail without the whole product needing to.

## Problem

Failing entirely on any dependency outage frustrates users; silently producing degraded output without disclosure erodes trust.

## Forces

- Degradation paths multiply test surface.
- User-visible degradation messaging is its own UX problem.
- Some failures must hard-fail (PII path, payment).

## Solution

Define per-feature fallback behaviour. On dependency failure, downgrade (text-only when vision fails, no citations when retrieval fails, simple summary when code execution fails) and disclose to the user that degraded mode is active. Feature flags double as degradation switches.

## Consequences

**Benefits**

- Product resilience under partial outages.
- User trust via transparent degradation.

**Liabilities**

- Test matrix grows with feature count.
- Degraded modes can themselves have bugs.

## What this pattern constrains

On failure, the agent must produce a degraded response with disclosure rather than a generic error.

## Applicability

**Use when**

- A dependency outage would otherwise fail the user request entirely.
- Per-feature fallback behaviour can be defined (text when vision fails, no citations when retrieval fails).
- The user can be told that degraded mode is active without breaking trust.

**Do not use when**

- There is no meaningful subset of working features to degrade to.
- Silent degradation would mislead the user and explicit failure is more honest.
- Feature flags do not exist and per-feature fallback cannot be wired without a major refactor.

## Known uses

- **Perplexity (citations missing under retrieval issues)** — *Available*
- **ChatGPT (vision unavailable falls back to text)** — *Available*

## Related patterns

- *complements* → [fallback-chain](fallback-chain.md)
- *uses* → [circuit-breaker](circuit-breaker.md)
- *specialises* → [exception-recovery](exception-recovery.md)

## References

- (book) *Release It! (Michael Nygard, ch. 4)*, 2007

**Tags:** routing, resilience, degradation
