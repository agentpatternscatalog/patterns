# Inter-Agent Communication

**Also known as:** A2A, Agent-to-Agent Protocol

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Define a protocol for agents to exchange tasks, capabilities, and results across process or vendor boundaries.

## Context

Agents from different teams or vendors need to cooperate but speak different internal shapes.

## Problem

Bespoke point-to-point integrations do not scale; each new agent pair requires fresh glue.

## Forces

- Capability discovery: how does agent A know what agent B can do?
- Auth and trust across organisational boundaries.
- Versioning: protocols evolve faster than legacy agents.


## Applicability

**Use when**

- Multiple agents must exchange tasks, capabilities, or results across process or vendor boundaries.
- Bespoke point-to-point integrations are starting to multiply.
- A protocol like MCP or A2A is available and acceptable to the operating environment.

**Do not use when**

- All agents run in one process and direct function calls suffice.
- Capability advertisement and discovery are not actually needed.
- Adopting a cross-vendor protocol would add governance burden without payoff.

## Solution

Adopt a protocol (Google A2A, Anthropic MCP, in-house equivalents) that covers capability advertisement, task delegation, result return, and auth. Agents advertise capabilities; clients discover and invoke; results round-trip in typed envelopes.

## Example scenario

An enterprise has agents from three vendors — a legal review agent from one, an HR agent from another, an internal IT agent — and every cross-agent integration is bespoke glue maintained by a different team. They adopt MCP as the inter-agent-communication protocol: each agent advertises its capabilities in a typed envelope, clients discover and invoke without knowing the implementation, and auth flows through one shared mechanism. Adding a fourth vendor's procurement agent now takes a day instead of a quarter.

## Consequences

**Benefits**

- Cross-team and cross-vendor reuse.
- Capability inventory becomes inspectable.

**Liabilities**

- Protocol overhead.
- Schema versioning becomes everyone's problem.

## What this pattern constrains

Agents may only invoke each other through the advertised protocol; out-of-band calls are forbidden.

## Known uses

- **Google A2A Protocol** — *Available*

## Related patterns

- *complements* → [mcp](mcp.md)
- *composes-with* → [handoff](handoff.md)
- *complements* → [supervisor](supervisor.md)
- *complements* → [orchestrator-workers](orchestrator-workers.md)
- *used-by* → [communicative-dehallucination](communicative-dehallucination.md)
- *used-by* → [cross-domain-agent-network](cross-domain-agent-network.md)

## References

- (doc) *Google A2A Protocol*, 2025, <https://google.github.io/A2A/>

**Tags:** a2a, protocol, interop
