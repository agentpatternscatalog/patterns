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

## Solution

Adopt a protocol (Google A2A, Anthropic MCP, in-house equivalents) that covers capability advertisement, task delegation, result return, and auth. Agents advertise capabilities; clients discover and invoke; results round-trip in typed envelopes.

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
