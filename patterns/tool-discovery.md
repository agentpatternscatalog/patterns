# Tool Discovery

**Also known as:** Capability Advertisement, Dynamic Tool Loading

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Let the agent discover available tools at runtime rather than hardcoding the tool list at agent build time.

## Context

Tool palettes evolve; new tools land without redeploying the agent. MCP and similar protocols make discovery feasible.

## Problem

Hardcoded tool palettes force a redeploy for every new capability; dynamic environments need dynamic palettes.

## Forces

- Discovery latency adds to every cold start.
- Tool quality varies; not every advertised tool should be exposed.
- Versioning of advertised tools.


## Applicability

**Use when**

- Tool palettes evolve and redeploys per new capability are a drag.
- A registry (MCP server, internal directory) advertises tools with typed schemas.
- The agent can refresh its palette safely at runtime.

**Do not use when**

- The tool set is fixed and small enough to hardcode.
- Dynamic discovery introduces unacceptable latency or trust risk.
- No registry exists and building one is more cost than benefit.

## Solution

On startup (or periodically), the agent queries a tool registry (MCP server, internal directory). The registry returns advertised tools with typed schemas. The agent loads them into its palette. Optionally cached and refreshed.

## Consequences

**Benefits**

- Capability expansion without agent redeploy.
- Multiple agents can share an evolving tool layer.

**Liabilities**

- Discovery failure modes (registry down).
- Trust: should the agent use any advertised tool?

## What this pattern constrains

The agent's tool palette at any moment is exactly the discovered set; off-registry tools are forbidden.

## Known uses

- **MCP server discovery** — *Available*
- **OpenAI plugin manifests (deprecated)** — *Available*

## Related patterns

- *uses* → [mcp](mcp.md)
- *specialises* → [tool-use](tool-use.md)
- *complements* → [awareness](awareness.md)
- *alternative-to* → [toolformer](toolformer.md)
- *complements* → [tool-loadout](tool-loadout.md)
- *generalises* → [app-exploration-phase](app-exploration-phase.md)
- *complements* → [wasm-skill-runtime](wasm-skill-runtime.md)

## References

- (doc) *Model Context Protocol Specification*, <https://modelcontextprotocol.io/specification>

**Tags:** discovery, tool-use, registry
