# MemGPT-Style Paging

**Also known as:** Virtual Context, Memory Paging, OS-Style Memory

**Category:** Memory  
**Status in practice:** emerging

## Intent

Treat the LLM context window as RAM and external storage as disk, with the model issuing tool calls to page memory in and out.

## Context

Long-running agents whose conversation or document state exceeds the context window; naive truncation loses state unpredictably.

## Problem

Fixed context windows force a choice between losing state and stuffing irrelevant content; both degrade quality.

## Forces

- Paging tools compete for context space themselves.
- Eviction policy (LRU? LFU? salience?) affects quality.
- Tool latency on page faults adds to user-visible time.

## Solution

Two memory tiers. Main context: system prompt, working set, recent messages. External context: recall (raw history) and archival (vector store). The model has tool calls for read_recall, write_archival, search_archival. Paging happens at the agent's discretion; the model treats main context as RAM and external as disk.

## Consequences

**Benefits**

- Conversation continuity beyond the context window.
- Inspectable memory tiers; archival is queryable independently.

**Liabilities**

- Tool definitions consume context budget.
- Page-fault tool calls add latency.

## What this pattern constrains

Memory beyond the working set is accessible only via paging tool calls; the agent cannot directly read external state.

## Known uses

- **[Letta (formerly MemGPT)](https://github.com/letta-ai/letta)** — *Available*

## Related patterns

- *uses* → [vector-memory](vector-memory.md)
- *alternative-to* → [five-tier-memory-cascade](five-tier-memory-cascade.md)
- *uses* → [tool-use](tool-use.md) — Paging operations are tool calls.
- *alternative-to* → [cross-session-memory](cross-session-memory.md)
- *alternative-to* → [context-window-packing](context-window-packing.md)

## References

- (paper) Packer, Wooders, Lin, Fang, Patil, Stoica, Gonzalez, *MemGPT: Towards LLMs as Operating Systems*, 2023, <https://arxiv.org/abs/2310.08560>

**Tags:** memory, paging, os
