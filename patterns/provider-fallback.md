# Provider Fallback

**Also known as:** Mid-Request Failover, Cross-Provider Recovery

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

When one provider's API errors mid-stream, transparently switch to another provider while preserving state.

## Context

Production agent products that depend on multiple LLM providers and need uptime across provider outages, rate limits, and regional incidents.

## Problem

Single-provider deployments take outages personally; fallback-chain handles request boundaries but cannot recover a stream that fails mid-generation.

## Forces

- Provider tool-call schemas differ; cross-provider continuation needs schema translation.
- Partial output reconciliation across providers.
- Routing logic must not amplify provider quirks.

## Solution

A gateway proxy holds the conversation state. On stream error, it switches to a fallback provider, optionally preserving partial output, and continues with translated message format. Tool-call schemas are normalised at the gateway. Streaming clients see one continuous stream.

## Consequences

**Benefits**

- Uptime through provider outages.
- Multi-provider portfolio for cost arbitrage.

**Liabilities**

- Schema translation has its own bugs.
- Quality discontinuity when providers differ in capability.

## What this pattern constrains

Clients must not see the underlying provider; only the provider-agnostic interface is exposed, and failover happens behind it.

## Known uses

- **OpenRouter automatic failover** — *Available*
- **Cursor model switching on rate-limit** — *Available*
- **Portkey gateway fallback** — *Available*
- **Helicone gateway fallback** — *Available*

## Related patterns

- *specialises* → [fallback-chain](fallback-chain.md)
- *complements* → [circuit-breaker](circuit-breaker.md)
- *complements* → [multi-model-routing](multi-model-routing.md)
- *complements* → [open-weight-cascade](open-weight-cascade.md)

## References

- (doc) *OpenRouter: Provider Routing*, <https://openrouter.ai/docs/features/provider-routing>
- (doc) *Portkey Gateway: Fallback*, <https://portkey.ai/docs>

**Tags:** routing, failover, gateway
