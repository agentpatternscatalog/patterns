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

## Example scenario

A long-running support agent has a 200k window and a thirty-turn conversation full of tool outputs, two 80-page attached PDFs, and the system charter. Naive concatenation overflows; truncating from the back loses the original ticket; truncating from the front loses the latest turn. The team builds a Context-Window Packing step: each turn it scores items by recency, relevance, and pinned-status, then fits a budgeted subset, replacing the rest with summaries. The window stops overflowing and critical state stays visible.

## Consequences

**Benefits**

- Predictable behaviour at the window edge.
- Inspectable trade-offs.

**Liabilities**

- Complexity of the packing logic.
- Compression artefacts.

## What this pattern constrains

Total tokens passed to the model must not exceed the window minus the reserved response budget.

## Applicability

**Use when**

- Naive concatenation overflows the context window for realistic inputs.
- Some context (system, tools, response reservation) is fixed and the rest must be allocated dynamically.
- You can audit token counts before each call and adjust the policy.

**Do not use when**

- Inputs are small and always fit comfortably in the window.
- There is no measurable quality difference between packing policies and the work is overhead.
- An external memory or retrieval layer already controls what reaches the model.

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
