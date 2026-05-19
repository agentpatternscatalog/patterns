# Synthetic Filesystem Overlay

**Also known as:** Virtual Filesystem for Agents, Unified-Tree Data Surface, FS-as-Tool-API

**Category:** Tool Use & Environment
**Status in practice:** emerging

## Intent

Project heterogeneous enterprise data sources into a single navigable Unix-like tree exposed through a small set of filesystem primitives so the agent reuses path semantics it already knows instead of learning a bespoke API per source.

## Context

Enterprise agents that must read across Notion, Slack, Google Drive, GitHub, Linear, Jira, email, and a dozen internal systems. Each source has its own auth, pagination, search dialect, and result shape. Even with MCP, the agent juggles dozens of source-specific tools and incompatible mental models per call.

## Problem

Designing agent-friendly APIs per source (per the Agent-Computer Interface pattern) does not scale — every new source adds a new vocabulary the agent must learn. Vector RAG flattens everything into chunks and loses structure. The agent has strong priors for filesystem navigation (ls, find, cat, grep) from training on Unix-like data, but no native data source matches those semantics. Observations from internal logs show agents spontaneously inventing file-path syntax ("/notion/eng/onboarding.md") even when no filesystem exists, because the abstraction is intuitive.

## Forces

- Each source has unique semantics, but a unified surface must hide them.
- The agent's strongest navigation priors are filesystem operations, not REST.
- Cross-source joins (a Slack thread plus its linked Notion doc plus the related PR) require traversal, not separate tool calls.
- Auth, rate limits, and pagination must remain per-source even when the surface is unified.
- Lazy enumeration matters: listing all of Slack as a directory cannot fetch every message eagerly.

## Therefore

Therefore: build a virtual filesystem that maps each data source under a path prefix (/slack/, /notion/, /drive/) and expose exactly five primitives — list, find, cat, search, locate_in_tree — so the agent traverses cross-source data with semantics it already has.

## Solution

Mount each connector under a deterministic path: /slack/<workspace>/<channel>/<date>/<message>.md, /notion/<workspace>/<page-path>.md, /github/<org>/<repo>/.... Expose five primitives: list (enumerate children, paginated), find (path-pattern matching), cat (fetch a node's content), search (full-text query, optionally scoped to a subtree), and locate_in_tree (resolve an opaque ID to its path). Each primitive translates into source-specific API calls on demand; nodes are virtual until cat. The agent navigates with shell-like idioms — list /slack/eng/, find /notion -name '*onboarding*', search 'incident 2026-05' /slack/eng — and joins results by paths rather than per-source identifiers.

## Structure

```
Agent | Five-primitive interface (list, find, cat, search, locate_in_tree) | Path-routing layer | Per-source adapters (Slack, Notion, Drive, GitHub...) with their own auth and rate-limit governors | Lazy hydration: nodes materialize on cat, not on list.
```

## Example scenario

An on-call engineer asks the assistant to summarize last week's incident. The agent runs find /slack -name '*incident*' -newer 2026-05-12, cats the matching channel transcripts, searches /notion for the linked postmortem template, and lists /github/infra/prs filtered by date. Three sources, one navigation idiom, no per-source SDK calls. The same agent on a new connector (Linear) needs only a new subtree under /linear/ — no new tools, no new prompts.

## Consequences

**Benefits**

- One mental model across all sources; new connectors add a subtree, not a new vocabulary.
- Reuses the model's filesystem priors instead of training new tool affordances.
- Cross-source traversal becomes path concatenation rather than ID translation.
- Small primitive set keeps the tool surface tiny even as data grows.
- Lazy hydration bounds per-call cost.

**Liabilities**

- Source semantics that do not map to trees (graph-heavy data, time-series streams) must be flattened or hidden.
- Path stability becomes a contract — renames in upstream sources can break agent memory of paths.
- Permission systems differ per source; a unified path namespace must still enforce per-source ACLs.
- Full-text search quality depends on each adapter; uneven coverage frustrates the agent.
- Listing very large directories needs careful pagination defaults.

## What this pattern constrains

The agent must access enterprise data only through the five primitives — direct per-source API calls are forbidden once the overlay is mounted. It must treat paths as the canonical identifier and not invent paths that locate_in_tree has not validated.

## Applicability

**Use when**

- Agent must read across many heterogeneous enterprise data sources.
- Cross-source joins are common and ID translation hurts.
- Tool count is climbing past what the model handles cleanly.
- Source data is mostly tree- or document-shaped.

**Do not use when**

- Only one or two data sources exist — overlay is overkill.
- Data is fundamentally graph-shaped (e.g. social network) and trees lose information.
- Per-source APIs already share a clean uniform shape.
- Real-time streaming dominates over snapshot reads.

## Known uses

- **[Dust.tt production agents (Paris)](https://blog.dust.tt/)** — *Available* — Five-primitive synthetic filesystem across Notion, Slack, GitHub, Drive and others. Internal logs documented agents inventing file-path syntax before the FS existed.

## Related patterns

- *alternative-to* → [mcp](mcp.md) — MCP exposes per-source tool surfaces; this overlay collapses them into one filesystem-shaped interface.
- *specialises* → [agent-computer-interface](agent-computer-interface.md) — Inverts ACI: instead of designing agent-friendly APIs per source, design one universal filesystem all sources project into.
- *alternative-to* → [tool-discovery](tool-discovery.md) — Discovery becomes ls/find against a tree rather than runtime tool enumeration.
- *alternative-to* → [knowledge-graph-memory](knowledge-graph-memory.md) — Graph-of-triples vs tree-of-paths — different shapes for the same cross-source navigation problem.
- *alternative-to* → [naive-rag-first](naive-rag-first.md) — Preserves source structure where vector RAG flattens it into chunks.

## References

- (blog) Dust, *Building Deep Dive: Infrastructure for AI Agents That Actually Go Deep*, 2025, <https://blog.dust.tt/>
- (blog) Dust, *How We Taught AI Agents to Navigate Company Data Like a Filesystem*, 2025, <https://blog.dust.tt/>

**Tags:** tool-design, enterprise, data-access, filesystem, unified-interface
