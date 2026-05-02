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


## Applicability

**Use when**

- Single-provider outages mid-stream would otherwise drop the user's session.
- A gateway can hold conversation state and translate message formats across providers.
- Tool-call schemas can be normalised at the gateway.

**Do not use when**

- Request-boundary fallback (fallback-chain) is enough and mid-stream recovery is not needed.
- Operational cost of running a normalising gateway is unjustified.
- Cross-provider differences in capabilities make recovered streams unreliable.

## Solution

A gateway proxy holds the conversation state. On stream error, it switches to a fallback provider, optionally preserving partial output, and continues with translated message format. Tool-call schemas are normalised at the gateway. Streaming clients see one continuous stream.

## Example scenario

A code-review agent product runs on a single provider whose us-east region begins returning 529 errors mid-stream during peak hours. Users see half-rendered reviews abandoned with stack traces. The team puts a gateway in front: it holds conversation state, normalises tool-call schemas across two providers, and on stream error reconnects the user to the fallback provider continuing from the last clean delta. Uptime moves from the underlying provider's SLA to the union of two providers' SLAs, and the support inbox stops filling on incident days.

## Diagram

```mermaid
sequenceDiagram
  participant C as Client
  participant GW as Gateway
  participant P1 as Provider A
  participant P2 as Provider B
  C->>GW: request (stream)
  GW->>P1: forward
  P1-->>GW: partial stream
  P1--xGW: stream error
  GW->>P2: continue (translated msgs)
  P2-->>GW: rest of stream
  GW-->>C: one continuous stream
```

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
