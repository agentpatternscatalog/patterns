# Model Context Protocol

**Also known as:** MCP, Open Tool Protocol

**Category:** Tool Use & Environment  
**Status in practice:** mature

## Intent

Standardise how agents discover and call tools so that a tool written once is usable by any conformant agent.

## Context

Multiple agents (vendor clients, IDEs, custom hosts) want to share a tool layer; rewriting tool adapters per host is wasteful and creates drift.

## Problem

Tool definitions are vendor-specific; the same capability is re-implemented per agent host with diverging behaviour.

## Forces

- Agents need a stable contract; tool authors need freedom to evolve the implementation.
- Local (stdio) and hosted (HTTP) deployments have different operational shapes but should expose the same surface.
- Auth must travel without leaking host credentials to every tool.

## Solution

Tools live behind a server speaking a common protocol. Hosts list available tools, call them with typed arguments, and receive typed results. The protocol covers discovery, invocation, errors, and (in some implementations) prompts and resources alongside tools.

## Consequences

**Benefits**

- Write a tool once, expose it to Claude Desktop, Claude Code, Cursor, custom hosts.
- Protocol-level auth (bearer-wrapped per-user tokens) keeps multi-tenancy out of each tool.

**Liabilities**

- Adds a process boundary; latency and operational surface increase.
- Schema versioning across servers and clients is a real concern as the protocol evolves.
- Long-lived SSE connections need server-side keep-alives and per-tool timeouts; connection drops mid-tool-call leave orphaned operations whose results are never reconciled.
- Streaming-tool backpressure: slow consumers can fill server buffers when the model lags behind the tool's stream output.

## What this pattern constrains

Agents can only see tools advertised by an MCP server; servers can only advertise tools matching the protocol's typed shape.

## Known uses

- **[Weft](https://github.com/luxxyarns/weft)** — *Available*. Node.js MCP server exposing Ravelry through the WEFT JSON format; stdio + HTTP entry points.
- **Anthropic Claude Desktop / Claude Code** — *Available*
- **Cursor MCP integration** — *Available*
- **OpenAI Agents SDK** — *Available*
- **Windsurf** — *Available*
- **Zed** — *Available*
- **GitHub Copilot** — *Available*

## Related patterns

- *generalises* → [tool-use](tool-use.md)
- *composes-with* → [translation-layer](translation-layer.md)
- *used-by* → [tool-discovery](tool-discovery.md)
- *complements* → [inter-agent-communication](inter-agent-communication.md)
- *complements* → [tool-output-poisoning](tool-output-poisoning.md)
- *complements* → [secrets-handling](secrets-handling.md)
- *used-by* → [cross-domain-agent-network](cross-domain-agent-network.md)

## References

- (doc) *Model Context Protocol*, <https://modelcontextprotocol.io>
- (blog) *Anthropic: Introducing the Model Context Protocol*, 2024, <https://www.anthropic.com/news/model-context-protocol>

**Tags:** mcp, protocol, interop
