# Agent-as-Tool Embedding

**Also known as:** Sub-Agent as Function, Nested Agent, Agent Wrapped in a Tool Signature

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Wrap a sub-agent (with its own loop, prompt, and tool palette) behind a single function-shaped tool signature, so the parent agent calls it like any other tool and never sees the sub-agent's internal turns.

## Context

A parent agent that benefits from delegating bounded sub-tasks ("search the web for X and summarise", "plan a multi-day itinerary") to a specialised loop without inheriting the sub-agent's turn-level context.

## Problem

Letting the parent observe the sub-agent's turns either bloats parent context or couples parent reasoning to sub-agent intermediate state. Hand-rolled multi-agent broadcast bus is over-engineering for this case.

## Forces

- Nested loops add abstraction; parent shouldn't care about how sub solves it.
- The function-shaped tool signature is already the agent's native composition unit.
- Sub-agent failure has to surface cleanly to the parent.
- Cost attribution across nesting depth is non-trivial.

## Solution

Define the sub-agent as `def sub_agent(task: str, ...) -> Result`. The parent calls it like any other tool. Inside the function: a fresh agent loop with its own model, tool palette, and step budget runs to completion or failure, returning a structured result. Parent context records only the call and the return value. Step budget and timeout are enforced by the wrapper, not by the sub-agent's prompt.

## Example scenario

A travel-planning agent needs to research hotel options, which itself takes ten or twenty turns of search and filtering. Putting all those turns into the parent's transcript bloats context and entangles the planner with hotel-search internals. The team wraps the hotel sub-agent behind a single function-shaped tool: the parent calls research_hotels(criteria) and gets back a structured shortlist. The sub-agent's internal turns stay sealed behind that signature.

## Structure

```
Parent agent -> tool_call(sub_agent, task) -> [hidden: sub-agent loop] -> Result -> Parent agent.
```

## Consequences

**Benefits**

- Composition without ad-hoc multi-agent infrastructure.
- Parent context stays small and stable.
- Sub-agent can be replaced or upgraded behind the same signature.

**Liabilities**

- Hidden costs: sub-agent failures or timeouts surprise the parent.
- Debugging requires traceability across the boundary (parent sees only the return).
- Recursive nesting can spiral cost if the sub-agent itself spawns more.

## What this pattern constrains

The parent may not access the sub-agent's intermediate turns; only the return value crosses the boundary.

## Applicability

**Use when**

- A sub-task is well-scoped enough that the parent should see only its result, not its turns.
- Putting the sub-agent's intermediate state into parent context would bloat tokens or couple parent reasoning to sub-agent internals.
- The sub-agent has its own model, tool palette, or step budget that should not leak into the parent loop.

**Do not use when**

- The parent must observe and steer sub-agent steps in real time.
- Sub-agent failures need to be diagnosable from the parent context without a separate trace.
- The sub-task is one or two model calls — function-style tool wrapping is cheaper than spawning an agent loop.

## Known uses

- **[Hugging Face Transformers Agents (multi-agent)](https://huggingface.co/docs/transformers/v4.47.1/agents_advanced)** — *Available*. ReactCodeAgent embeds sub-agents as callable Python functions.
- **smolagents** — *Available*. Same pattern; sub-agents exposed as ordinary tool functions to a CodeAgent.
- **OpenAI Agents SDK / handoffs** — *Available*. Adjacent pattern with explicit handoff semantics rather than function-call nesting.

## Related patterns

- *specialises* → [orchestrator-workers](orchestrator-workers.md)
- *complements* → [subagent-isolation](subagent-isolation.md)
- *specialises* → [hierarchical-agents](hierarchical-agents.md)
- *uses* → [tool-use](tool-use.md)
- *complements* → [step-budget](step-budget.md)

## References

- (doc) *Hugging Face Transformers — Agents Advanced (Multi-Agents)*, <https://huggingface.co/docs/transformers/v4.47.1/agents_advanced>

**Tags:** multi-agent, composition, france-origin, huggingface, smolagents
