# Hero Agent

**Also known as:** Mega-Prompt Agent, God Agent

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: stuff every capability into one agent with one giant prompt.

## Context

An agent product grows; new capabilities are added by appending to the system prompt and the tool palette of a single agent.

## Problem

The agent's prompt becomes a monolith. Tools conflict. The model is confused about which path to take. Cheap requests pay expensive prices.

## Forces

- Specialisation requires routing or multi-agent infrastructure that does not yet exist.
- Splitting feels like premature optimisation.
- One-prompt is fastest to ship and slowest to maintain.

## Solution

Don't. Once the prompt exceeds a few hundred lines or the tool count exceeds about a dozen, extract specialists. See routing, supervisor, multi-model-routing.

## Consequences

**Liabilities**

- Quality regressions on each new capability.
- Cost ballooning.
- Debugging the agent becomes archaeology.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Common in early-stage AI products** — *Available*

## Related patterns

- *alternative-to* → [routing](routing.md)
- *alternative-to* → [supervisor](supervisor.md)
- *alternative-to* → [multi-model-routing](multi-model-routing.md)
- *complements* → [tool-explosion](tool-explosion.md)
- *complements* → [prompt-bloat](prompt-bloat.md)
- *alternative-to* → [sop-encoded-multi-agent](sop-encoded-multi-agent.md)
- *alternative-to* → [cross-domain-agent-network](cross-domain-agent-network.md)

## References

- (repo) *ai-standards/ai-design-patterns (Hero Agent)*, <https://github.com/ai-standards/ai-design-patterns>

**Tags:** anti-pattern, monolith
