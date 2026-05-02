# Vector Memory

**Also known as:** Semantic Memory, Embedding-Indexed Memory

**Category:** Memory  
**Status in practice:** mature

## Intent

Store memories as embeddings in a vector index and retrieve the most semantically similar items at query time.

## Context

Long-running agents accumulate facts/observations whose relevance is best judged by similarity to the current context.

## Problem

Append-only logs grow unboundedly; without semantic retrieval the agent cannot find the relevant past.

## Forces

- Embedding choice constrains retrieval quality.
- Index updates have non-trivial latency.
- Forgetting is achieved by deletion or decay; both have failure modes.

## Solution

Each memory item is embedded and indexed. At query time, embed the query (or a summary of current state), retrieve top-k most similar memories, prepend to context. Optional decay (boost recent, age old) and salience weighting.

## Consequences

**Benefits**

- Semantically relevant past surfaces automatically.
- Scales to memory stores too large for context.

**Liabilities**

- Misses purely temporal queries ('what did I do yesterday?').
- Embedding drift on schema changes.

## What this pattern constrains

The agent reads memory only through the retriever; full-store scans are not part of the loop.

## Known uses

- **MemGPT / Letta archival memory** — *Available*
- **Generative Agents memory stream (Park et al.)** — *Available*
- **LangChain VectorStoreRetrieverMemory** — *Available*

## Related patterns

- *used-by* → [memgpt-paging](memgpt-paging.md)
- *specialises* → [naive-rag](naive-rag.md) — Vector Memory is RAG over the agent's own past.
- *alternative-to* → [knowledge-graph-memory](knowledge-graph-memory.md)
- *used-by* → [self-archaeology](self-archaeology.md)
- *used-by* → [co-located-memory-surfacing](co-located-memory-surfacing.md)
- *complements* → [salience-attention-mechanism](salience-attention-mechanism.md)

## References

- (paper) Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*, 2023, <https://arxiv.org/abs/2304.03442>

**Tags:** memory, vector, embedding
