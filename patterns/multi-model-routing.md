# Multi-Model Routing

**Also known as:** Cascade Routing, Cheap-First Routing, Model Cascading

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

Send each request to the cheapest model that can handle it well.

## Context

Model prices and capabilities vary by an order of magnitude; using the strongest model for every call is wasteful.

## Problem

Static model choice either pays too much or misses quality on hard cases.

## Forces

- Quality bar must be measurable per request type.
- Cheap models hallucinate confidently; the router must not trust them blindly.
- Falling back from cheap to expensive on failure costs more than starting expensive.


## Applicability

**Use when**

- Cost and quality goals diverge across request types.
- A classifier can route requests to a cheap or strong model with acceptable accuracy.
- A cascade with low-confidence fallback to the strong model is feasible.

**Do not use when**

- A single model already meets the price-performance target.
- Routing classification is too inaccurate to be safe.
- Operational complexity of multi-model deployment is unjustified by the savings.

## Solution

Combine routing (classify the request) with a per-class model preference. Routing and filter extraction go to the cheap model; the screen-aware dialog or final answer goes to the strong model. Optionally cascade: try cheap, fall back to strong if confidence is low.

## Consequences

**Benefits**

- Bill drops 5-10x without quality loss when class boundaries match cost boundaries.
- Dev/test runs naturally on cheap models.

**Liabilities**

- Two-model debug surface.
- Vendor lock-in when models diverge in tool calling.

## What this pattern constrains

Each request class is bound to a model tier; agents cannot escalate without routing approval.

## Known uses

- **Bobbin (Stash2Go)** — *Available*. gpt-5.4-mini for routing/filters; gpt-5.4 for screen-aware dialog.

## Related patterns

- *specialises* → [routing](routing.md)
- *complements* → [cost-gating](cost-gating.md)
- *complements* → [fallback-chain](fallback-chain.md)
- *alternative-to* → [hero-agent](hero-agent.md)
- *complements* → [provider-fallback](provider-fallback.md)
- *alternative-to* → [hidden-mode-switching](hidden-mode-switching.md)
- *used-by* → [dual-system-gui-agent](dual-system-gui-agent.md)
- *generalises* → [open-weight-cascade](open-weight-cascade.md)
- *complements* → [multilingual-voice-agent](multilingual-voice-agent.md)
- *used-by* → [degenerate-output-detection](degenerate-output-detection.md)

## References

- (doc) *OpenAI / Anthropic model selection guides*, 2024

**Tags:** routing, cost, cascade
