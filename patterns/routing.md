# Routing

**Also known as:** Mode Selector, Intent Classifier, Task Router

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

Classify an incoming request and dispatch it to the specialist (lane / agent / model) best suited to handle it.

## Context

Heterogeneous traffic where different requests benefit from different prompts, tool palettes, or models.

## Problem

A single prompt that handles everything either over-pays (cheap requests routed through expensive paths) or under-serves (complex requests stuck in cheap paths).

## Forces

- Routing itself costs a model call.
- Misrouting can be worse than not routing at all.
- The router needs visibility into capabilities of each downstream specialist.

## Solution

A lightweight classifier model (often the cheapest available) returns a label. The host dispatches the request to the specialist for that label. Common lanes: command (deterministic action), agent (multi-step), chat (no tools).

## Consequences

**Benefits**

- Cheap requests pay cheap prices.
- Each lane can be tuned in isolation.

**Liabilities**

- Two-call latency on every request.
- Lane definitions ossify; reclassification is hard once users learn the lanes.

## What this pattern constrains

A request gets exactly one lane; downstream specialists cannot accept work outside their declared lane.

## Known uses

- **Bobbin (Stash2Go)** — *Available*. mode_selector classifies intent into command / agent / chat.
- **Anthropic Building Effective Agents (Workflow #2)** — *Available*

## Related patterns

- *generalises* → [multi-model-routing](multi-model-routing.md)
- *used-by* → [supervisor](supervisor.md)
- *generalises* → [mixture-of-experts-routing](mixture-of-experts-routing.md)
- *complements* → [fallback-chain](fallback-chain.md)
- *used-by* → [dynamic-scaffolding](dynamic-scaffolding.md)
- *alternative-to* → [hero-agent](hero-agent.md)
- *used-by* → [disambiguation](disambiguation.md)
- *complements* → [prompt-chaining](prompt-chaining.md)
- *used-by* → [tool-loadout](tool-loadout.md)

## References

- (blog) *Anthropic: Building Effective Agents*, 2024, <https://www.anthropic.com/research/building-effective-agents>

**Tags:** routing, classifier
