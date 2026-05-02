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


## Applicability

**Use when**

- Never use this; once the prompt grows past a few hundred lines or tool count exceeds about a dozen, extract specialists.
- Use routing, supervisor, or multi-model-routing to split capability across agents.
- Treat single-prompt sprawl as a smell, not a destination.

**Do not use when**

- Any agent with more than a handful of distinct workflows.
- Any agent where cheap requests must not pay expensive prompt costs.
- Any team that needs independent ownership of separate capabilities.

## Solution

Don't. Once the prompt exceeds a few hundred lines or the tool count exceeds about a dozen, extract specialists. See routing, supervisor, multi-model-routing.

## Example scenario

A startup ships a single 'do-everything' assistant whose system prompt grew to 1800 lines and whose tool list passed forty entries. Latency triples, the model confuses calendar tools with email tools, and the cheapest 'what time is it' request now costs as much as a full research query. They diagnose hero-agent as the named anti-pattern and extract specialists: a small router up front, a calendar agent, a mail agent, a research agent. The monolith stays only as an escape hatch and the prompt shrinks by 80 percent.

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
