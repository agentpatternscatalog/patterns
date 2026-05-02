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


## Applicability

**Use when**

- The tool registry is large (MCP, plugins, internal catalog) and exposing all degrades selection.
- A classifier or rule can pick the relevant subset per request cheaply.
- Function-calling accuracy is a release-gate metric.

**Do not use when**

- The tool set is small and a static palette already works well.
- Per-request classification adds latency that is not earned back in accuracy.
- Subsetting would frequently exclude the tool the agent actually needs.

## Solution

Before the main loop, classify the request and select N relevant tools (rule-based: by routed lane; or model-based: a quick classifier picks tools). Expose only the selected subset to the agent's main inference call. Tools outside the subset are unavailable for this request.

## Example scenario

A general-purpose agent has access to a 100-tool registry and selection accuracy is poor because the model cannot keep that many tool descriptions in working attention. The team adds a quick classifier ahead of the main loop that picks N relevant tools per request (rule-based by routed lane, or model-based). The agent's main loop now sees only the curated subset; selection accuracy and latency both improve.

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
