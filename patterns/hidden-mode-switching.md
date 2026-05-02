# Hidden Mode Switching

**Also known as:** Silent Model Swap, Undisclosed Routing

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: silently swap the underlying model between requests without disclosing the change to users or operators.

## Context

Cost or capacity pressure pushes a product to route some requests to cheaper models; the routing is invisible.

## Problem

Reproducibility breaks; users notice quality changes they cannot diagnose; trust erodes.

## Forces

- Cost arbitrage feels too good to disclose.
- Per-request model disclosure adds UI complexity.
- Hidden routing complicates eval gates.


## Applicability

**Use when**

- Never use this; routing model changes silently undermines reproducibility and trust.
- Use multi-model-routing transparently with the chosen model disclosed per response.
- Make routing decisions inspectable in traces and operator dashboards.

**Do not use when**

- Any user-facing product where quality must be diagnosable.
- Any audit or compliance setting requiring per-request model identity.
- Any environment where users compare outputs across runs.

## Solution

Don't. Disclose model identity per response. Use multi-model-routing transparently. Make routing decisions inspectable.

## Consequences

**Liabilities**

- Trust erosion when users discover the swap.
- Reproducibility broken across requests.
- Eval results become misleading.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **GPT-4 -> GPT-4o auto-router incident, 2024** — *Available*

## Related patterns

- *alternative-to* → [multi-model-routing](multi-model-routing.md)
- *alternative-to* → [lineage-tracking](lineage-tracking.md)
- *alternative-to* → [model-card](model-card.md)

**Tags:** anti-pattern, routing, disclosure
