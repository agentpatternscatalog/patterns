# Context Window Packing

**Also known as:** Context Compression, Token Budget Management, Fit in Context, Token Cost Reduction

**Category:** Memory  
**Status in practice:** mature

## Intent

Choose what fits in the context window each turn given a fixed token budget.

## Context

Agents whose available context (system prompt + history + retrieved chunks + tools + state) exceeds the model's window.

## Problem

Naive concatenation overflows; naive truncation loses critical state.

## Forces

- What to drop is task-dependent.
- Compression has its own LLM cost.
- Reserved budget for the response itself.

## Solution

Define a packing policy. Reserve N tokens for system + tools + response. Allocate the rest across history (compressed), retrieved chunks (top-k after rerank), and current state. Use eviction (drop oldest), summarisation (compress), or selection (relevance-rank) policies. Audit token counts before each call.

## Consequences

**Benefits**

- Predictable behaviour at the window edge.
- Inspectable trade-offs.

**Liabilities**

- Complexity of the packing logic.
- Compression artefacts.

## What this pattern constrains

Total tokens passed to the model must not exceed the window minus the reserved response budget.

## Known uses

- **LangChain ConversationSummaryBufferMemory** — *Available*
- **Most production agent frameworks** — *Available*

## Related patterns

- *uses* → [episodic-summaries](episodic-summaries.md)
- *alternative-to* → [memgpt-paging](memgpt-paging.md)
- *complements* → [dynamic-scaffolding](dynamic-scaffolding.md)
- *used-by* → [todo-list-driven-agent](todo-list-driven-agent.md)
- *used-by* → [reasoning-trace-carry-forward](reasoning-trace-carry-forward.md)
- *alternative-to* → [salience-attention-mechanism](salience-attention-mechanism.md)

**Tags:** context, tokens, budget
