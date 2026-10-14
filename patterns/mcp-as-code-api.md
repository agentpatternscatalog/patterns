# MCP-as-Code-API

**Also known as:** Code-Execution-with-MCP, MCP-as-Typed-API, Filesystem-Mirrored Tools, Tools-as-Code-Modules

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Materialize MCP servers as a directory of typed code wrappers so the agent writes code that imports them and large tool outputs flow between calls inside the sandbox without ever entering the model's context window.

## Context

A team is running an agent that is connected to many Model Context Protocol (MCP) servers at once: a Google Drive server, a Slack server, an internal Postgres server, a GitHub server. Each server exposes tens or hundreds of tools with verbose JSON outputs. The agent already has a code-execution sandbox available (a Python or TypeScript runtime it can use as its action channel).

## Problem

Conventional tool calling loads every advertised tool schema into the system prompt and routes every tool result back through the model's context window, even when the model is only going to pass that result straight to the next tool. A single workflow that joins a 5 megabyte spreadsheet with a paginated Slack thread can burn six-figure token counts before any actual reasoning happens, and most of those tokens are plumbing the model never has to read.

## Forces

- Tool schemas are static and discoverable on the filesystem, but model context is scarce and per-turn-priced.
- Intermediate data often flows tool-to-tool with no semantic reasoning in between, yet conventional MCP routes every byte through the model.
- Code execution can manipulate large objects locally for free, but only if tool wrappers exist as callable code.
- Typed wrappers give the model autocomplete-like affordances, but typing every tool by hand does not scale; wrappers must be generated from MCP schemas.
- Security boundaries previously enforced by the model reading tool output now shift to the sandbox; untrusted data may flow without an LLM checkpoint.

## Therefore

Therefore: generate a directory of typed code modules from each MCP server's schema, expose only that filesystem to the agent, and let the agent write code that imports the wrappers — keeping large intermediate results inside the sandbox so only the final summary returns to context.

## Solution

At connection time, walk each MCP server's tool list and emit a file per tool (e.g. servers/gdrive/getDocument.ts, servers/slack/listChannels.ts) with full type signatures derived from the JSON schema. Expose this tree to the agent as a readable filesystem and let it explore via standard list/read primitives rather than loaded schemas. The agent then writes execution code — a short script that imports the wrappers, chains calls, transforms results in-memory, and prints only the final answer. Tool outputs live in sandbox variables; only what the script prints (or saves to a designated output) crosses back into model context. Pair with progressive disclosure: the model reads only the tool files it intends to use.

## Structure

```
Agent <-> Model context (small) | Sandbox runtime executes generated code | Tool wrapper tree (one file per MCP tool, typed) | MCP servers behind wrappers | Large intermediate data stays in sandbox memory; only printed output returns to context.
```

## Diagram

```mermaid
flowchart TD
  A[Agent context<br/>small] -->|writes script| SCR[Generated code]
  SCR --> SAND[Sandbox runtime]
  subgraph FS[Tool wrapper tree on filesystem]
    W1[servers/gdrive/getDocument.ts]
    W2[servers/slack/listChannels.ts]
    W3[servers/.../tool.ts]
  end
  SAND -->|imports| FS
  FS --> MCP[MCP servers]
  MCP --> FS
  FS --> SAND
  SAND -->|only printed / saved output| A
  SAND -.large intermediate data stays in sandbox memory.-> SAND
```

*Tool wrappers live on a readable filesystem; the agent ships code that chains them in the sandbox, so bulk data never enters the context.*

## Example scenario

An assistant must take meeting notes from Google Drive, identify action items, and post them in the right Slack channels. The naive approach pulls the entire transcript into context, then pulls the channel list, then formats messages — burning ~150K tokens. With MCP-as-Code-API, the model writes a short TypeScript that imports gdrive.getDocument and slack.postMessage, filters action items in-process, and prints only a confirmation. Total tokens dropped to ~2K because the transcript never crossed the context boundary.

## Consequences

**Benefits**

- Massive token reduction — Anthropic reports 98.7% on representative workflows.
- Large tool outputs (sheets, transcripts, binaries) never enter context.
- Composition becomes ordinary programming: filters, joins, retries are code, not prompted loops.
- Tool discovery becomes filesystem navigation, reusing well-trained model behaviour.
- Schemas are loaded on demand rather than all upfront.

**Liabilities**

- Requires a working code-execution sandbox with network egress controls.
- Model must be strong at code generation in the chosen runtime.
- Untrusted data flowing through code without LLM checkpoints widens the prompt-injection surface inside the sandbox.
- Wrapper generation must stay in sync with upstream MCP schema changes.
- Debugging failures spans two layers — generated code and tool wrappers — rather than one tool call.

## Failure modes

- Wrapper drift — an upstream MCP schema changes and the generated file still has the old signature, so the agent's script fails on a call that looked valid.
- Invented module — the agent imports a wrapper that was never generated, guessing from tool names instead of reading the file tree.
- Raw output in context — the script prints a whole spreadsheet instead of a summary, and the token saving is lost.
- Unchecked data path — untrusted content moves between tools inside the sandbox with no model checkpoint, and an injected instruction reaches a write tool.

## What this pattern constrains

The model must not request raw tool outputs into context when they exceed a configured size; it must route large outputs through sandbox variables and return only printed summaries. It must not invent wrapper modules — only those materialized on the filesystem from real MCP schemas are callable.

## Applicability

**Use when**

- Workflows chain many MCP tools and intermediate data is large.
- A code-execution sandbox is already part of the agent stack.
- Token cost or latency dominated by tool-output round-tripping.
- Tool surface is too large to fit all schemas in prompt.

**Do not use when**

- Only a handful of tools are used and outputs are small.
- No code sandbox is available or code generation in the runtime is weak.
- Each tool result genuinely requires LLM reasoning before the next call.
- Compliance forbids untrusted data flowing without per-step LLM inspection.

## Components

- Wrapper Generator — walks each MCP server's tool list and emits a typed code file per tool
- Tool Wrapper Tree — filesystem-shaped directory of typed wrappers grouped by server
- Agent — writes execution code that imports wrappers instead of calling tools through the model
- Sandbox Runtime — executes the agent-authored script and routes wrapper calls to MCP servers
- Filesystem Surface — exposes the wrapper tree to the agent via list and read primitives instead of preloaded schemas

## Tools

- JSON-Schema-to-TypeScript (or Python) compiler — generates the typed wrappers from MCP tool schemas
- Sandboxed code runtime (Deno, Node, or Python sandbox) — executes the agent-authored scripts that import wrappers
- MCP client library — carries wrapper calls to the underlying servers

## Evaluation metrics

- Context tokens versus eager-schema baseline — reduction from leaving schemas off the prompt
- Wrapper-discovery hit rate — fraction of needed tools the agent locates via list and read
- Inter-tool data size kept in sandbox — payload that never enters the model context
- Generated-script validity rate — share of authored scripts that parse and run end to end
- End-to-end task success on data-heavy workflows — headline value of moving plumbing into code

## Known uses

- **[Anthropic Claude (engineering blog reference implementation)](https://www.anthropic.com/engineering/code-execution-with-mcp)** _available_ — Reports ~98.7% token reduction on representative MCP workflows.
- **[Cloudflare Code Mode](https://developers.cloudflare.com/agents/api-reference/codemode)** _available_ — Exposes MCP tools as a typed code API the model writes against.

## Related patterns

- _specialises_ **Model Context Protocol** — Materializes the MCP protocol as a typed code surface instead of inline tool calls.
- _composes-with_ **Code-as-Action Agent** — The agent emits code as its action — but the action imports MCP-derived wrappers rather than ad-hoc helpers.
- _complements_ **Tool Search Lazy Loading** — Filesystem layout enables on-demand schema loading: the model reads only the wrapper files for tools it plans to call.
- _alternative-to_ **Tool Loadout** — Loadout pre-selects a static tool subset; MCP-as-Code-API lets the model self-select at code-write time.
- _uses_ **Sandbox Isolation** — Relies on a code sandbox to hold large intermediate state outside model context.
- _alternative-to_ **Tool Explosion** — Avoids the bloat by never loading all schemas into prompt at once.
- _complements_ **MCP Bidirectional Bridge**
- _complements_ **Direct API Wrapper**
- _complements_ **Composite Service**

## References

- [Code execution with MCP: building more efficient AI agents](https://www.anthropic.com/engineering/code-execution-with-mcp) — Anthropic Engineering, 2025
- [Code execution with MCP (annotation)](https://simonwillison.net/2025/Nov/4/code-execution-with-mcp/) — Simon Willison, 2025
- [Model Context Protocol specification](https://modelcontextprotocol.io) — 2024
