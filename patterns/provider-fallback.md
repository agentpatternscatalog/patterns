# Provider Fallback

**Also known as:** Mid-Request Failover, Cross-Provider Recovery

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

When one provider's API errors mid-stream, transparently switch to another provider while preserving state.

## Context

A production agent product streams long responses to the user — multi-paragraph answers, generated code, structured documents — and is willing to integrate with more than one LLM provider to keep that experience working. The team already accepts that any single provider will have rate-limit windows, regional incidents, and the occasional mid-stream disconnect that drops the second half of a response. They control a gateway layer between the client and the upstream providers and can hold conversation state there.

## Problem

A single-provider deployment is hostage to that provider's worst hour: when its stream fails halfway through a generation, the user sees a half-rendered answer followed by an error and has to start over. A request-boundary fallback chain handles the case where a whole call fails before any output, but it cannot recover a stream that began on provider A and died after some tokens were already delivered. Without mid-stream failover, the team's only options are to lose the partial output or to lock in to whichever provider was most reliable last week.

## Forces

- Provider tool-call schemas differ; cross-provider continuation needs schema translation.
- Partial output reconciliation across providers.
- Routing logic must not amplify provider quirks.

## Therefore

Therefore: put a gateway in front that owns the conversation state and switches providers mid-stream with translated schemas, so that the client sees one continuous stream across a provider's outage.

## Solution

A gateway proxy holds the conversation state. On stream error, it switches to a fallback provider, optionally preserving partial output, and continues with translated message format. Tool-call schemas are normalised at the gateway. Streaming clients see one continuous stream.

## Structure

```
Client --request (stream)--> Gateway (holds conversation state) --> Provider A --partial stream--> Gateway --> Client; Provider A --stream error--> Gateway --continuation (translated messages + partial output)--> Provider B --rest of stream--> Gateway --> Client sees one continuous stream
```

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

## Example scenario

A code-review agent product runs on a single provider whose us-east region begins returning 529 errors mid-stream during peak hours. Users see half-rendered reviews abandoned with stack traces. The team puts a gateway in front: it holds conversation state, normalises tool-call schemas across two providers, and on stream error reconnects the user to the fallback provider continuing from the last clean delta. Uptime moves from the underlying provider's SLA to the union of two providers' SLAs, and the support inbox stops filling on incident days.

## Consequences

**Benefits**

- Uptime through provider outages.
- Multi-provider portfolio for cost arbitrage.

**Liabilities**

- Schema translation has its own bugs.
- Quality discontinuity when providers differ in capability.

## Failure modes

- Translation bug — the gateway maps a tool call or message role wrongly for provider B, and the continued stream calls the wrong tool or loses context.
- Visible seam — provider B continues in a different style or quality, and the user sees an answer that changes voice halfway through.
- Duplicated or dropped partial output — the continuation builder misjudges what was already streamed, so text repeats or a gap appears.
- Amplified quirk — the fallback provider has its own limits or formatting habits, and routing on every error spreads them across all traffic.

## What this pattern constrains

Clients must not see the underlying provider; only the provider-agnostic interface is exposed, and failover happens behind it.

## Applicability

**Use when**

- Single-provider outages mid-stream would otherwise drop the user's session.
- A gateway can hold conversation state and translate message formats across providers.
- Tool-call schemas can be normalised at the gateway.

**Do not use when**

- Request-boundary fallback (fallback-chain) is enough and mid-stream recovery is not needed.
- Operational cost of running a normalising gateway is unjustified.
- Cross-provider differences in capabilities make recovered streams unreliable.

## Components

- Gateway proxy — owns the conversation state and the client-facing stream
- Provider adapters — per-provider implementations of the unified chat and tool-call shape
- Schema translator — normalises tool-call formats and message roles across providers
- Stream-error detector — recognises mid-stream disconnects and triggers failover
- Continuation builder — reconstructs the prompt with partial output for the fallback provider

## Tools

- Model gateway — OpenRouter, Portkey, Helicone, LiteLLM proxy, or a custom service
- Multiple provider APIs — at least two with compatible enough capability surfaces
- Stream-aware HTTP client — server-sent events or chunked transfer with reconnection support

## Evaluation metrics

- Mid-stream failover success rate — share of stream errors recovered into one continuous response
- Schema-translation error rate — per-provider mismatches in tool-call or message shape
- Combined-provider uptime vs single-provider SLA — the resilience headline of the pattern
- User-visible discontinuity rate — recovered streams where the seam was noticeable in output
- Per-provider traffic share — confirms the fallback path actually carries production load when needed

## Known uses

- **OpenRouter automatic failover** _available_
- **Cursor model switching on rate-limit** _available_
- **Portkey gateway fallback** _available_
- **Helicone gateway fallback** _available_
- **[Sparrot](https://marco-nissen.com/sparrot/)** _available_ — Per-provider cooldown state is tracked so cooled-down providers are skipped in routing; the loop falls through to the next eligible provider rather than blocking.

## Related patterns

- _specialises_ **Fallback Chain**
- _complements_ **Circuit Breaker**
- _complements_ **Multi-Model Routing**
- _complements_ **Open-Weight Cascade**
- _complements_ **Degenerate-Output Detection**
- _complements_ **Provider-String Routing**
- _alternative-to_ **Vendor Lock-In**
- _complements_ **Complexity-Based Routing**
- _complements_ **Serving-Stack Attestation** — Fallback moves traffic to another provider on failure; a separated probe result is one of the signals that should move it, and each fallback target needs its own attestation.

## References

- [OpenRouter: Provider Routing](https://openrouter.ai/docs/features/provider-routing)
- [Portkey Gateway: Fallback](https://portkey.ai/docs)
