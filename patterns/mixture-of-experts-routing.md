# Mixture of Experts Routing

**Also known as:** MoE Routing (Agent-Level), Expert Selection

**Category:** Routing & Composition  
**Status in practice:** emerging

## Intent

Route each request to one or more domain-expert agents, where each expert holds deep capability in a narrow area.

## Context

Heterogeneous domains where one agent cannot credibly cover all expertise (legal + medical + finance + technical).

## Problem

A generalist agent's depth in any one domain is shallow; users in specialist domains feel under-served.

## Forces

- Expert maintenance scales with domain count.
- Routing classification must match expert coverage.
- Cross-domain queries challenge single-expert routing.

## Solution

Define experts (specialised system prompts, tool palettes, possibly fine-tuned models). A router classifies queries by domain. Route to one expert (top-1) or to multiple experts whose outputs are aggregated. Distinct from standard routing by emphasising deep specialisation per expert.

## Consequences

**Benefits**

- Depth per domain.
- Independent expert evolution.

**Liabilities**

- Domain count grows expert maintenance linearly.
- Cross-domain queries fall through cracks.

## What this pattern constrains

Each request is bound to one or more named experts; generalist fallback is explicit, not default.

## Known uses

- **Vendor knowledge-base products with domain agents** — *Available*

## Related patterns

- *specialises* → [routing](routing.md)
- *complements* → [supervisor](supervisor.md)
- *complements* → [role-assignment](role-assignment.md)
- *alternative-to* → [dynamic-expert-recruitment](dynamic-expert-recruitment.md)

## References

- (paper) Wang et al., *Mixture-of-Agents Enhances Large Language Model Capabilities*, 2024, <https://arxiv.org/abs/2406.04692>

**Tags:** routing, experts, specialisation
