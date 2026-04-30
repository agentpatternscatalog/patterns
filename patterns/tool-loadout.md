# Tool Loadout

**Also known as:** Tool Subset Selection, Per-Task Tool Filtering, Tool Filter, Limit Exposed Tools

**Category:** Tool Use & Environment  
**Status in practice:** mature

## Intent

Select a small task-relevant subset of available tools per request rather than exposing the full registry to the model.

## Context

Agents with large tool registries (MCP, plugin marketplaces, internal tool catalogs) where exposing all tools degrades selection accuracy.

## Problem

Function-calling accuracy degrades past ~20 tools; a 100-tool registry is unusable without per-request filtering.

## Forces

- Filter quality (does the agent get the right tools?).
- Filter cost (one extra model call per request, or rule-based).
- Tool-discovery latency on each request.

## Solution

Before the main loop, classify the request and select N relevant tools (rule-based: by routed lane; or model-based: a quick classifier picks tools). Expose only the selected subset to the agent's main inference call. Tools outside the subset are unavailable for this request.

## Consequences

**Benefits**

- Function-calling accuracy holds up at scale.
- Token budget for tool definitions stays manageable.

**Liabilities**

- Filter mistakes hide capability the agent could have used.
- Filtering adds latency.

## What this pattern constrains

The agent's tool palette is exactly the filtered subset for the current request; tools outside the subset cannot be invoked.

## Known uses

- **Claude Code per-task allowed_tools** — *Available*
- **Cursor contextual tool selection** — *Available*
- **MCP server filtering** — *Available*

## Related patterns

- *complements* → [tool-discovery](tool-discovery.md)
- *uses* → [routing](routing.md)
- *conflicts-with* → [tool-explosion](tool-explosion.md)
- *complements* → [agent-computer-interface](agent-computer-interface.md)

**Tags:** tool-use, loadout, filtering
