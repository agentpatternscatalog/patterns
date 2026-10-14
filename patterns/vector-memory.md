# Vector Memory

**Also known as:** Embedding-Indexed Memory, Vector Store Memory

**Category:** Memory  
**Status in practice:** mature

## Intent

Store memories as embeddings in a vector index and retrieve the most semantically similar items at query time.

## Context

A long-running agent accumulates facts and observations over time, and on each step it needs to find the small subset of past items that is relevant to the current situation. Relevance is best judged by semantic similarity rather than by exact term match or chronological recency: 'find the past notes whose meaning is close to what is happening now'.

## Problem

An append-only log of everything the agent has seen grows unboundedly and quickly becomes too large to search by linear scan. Without a semantic retrieval layer, the agent has no way to find the relevant past, because keyword search misses paraphrase and chronological recency misses older but topically relevant items. The team needs a memory store that supports similarity queries against an embedding of the current context, so that the agent can pull back exactly the items it should be thinking about now.

## Forces

- Embedding choice constrains retrieval quality.
- Index updates have non-trivial latency.
- Forgetting is achieved by deletion or decay; both have failure modes.

## Therefore

Therefore: embed every memory item and retrieve the top-k most similar at query time, so that recall is driven by semantic match instead of exact keys or scrollback position.

## Solution

Each memory item is embedded and indexed. At query time, embed the query (or a summary of current state), retrieve top-k most similar memories, prepend to context. Optional decay (boost recent, age old) and salience weighting.

## Structure

```
New memory item --embed--> Vector index; Query / current state --embed--> Top-k similarity search over index --decay / salience weighting--> Prepend to context
```

## Diagram

```mermaid
flowchart TD
  Mem[New memory item] --> Emb[Embed]
  Emb --> Idx[(Vector index)]
  Q[Query / current state] --> QEmb[Embed]
  QEmb --> Top[Retrieve top-k similar]
  Idx --> Top
  Top --> Decay[Apply decay / salience weighting]
  Decay --> Ctx[Prepend to context]
```

## Example scenario

A long-running personal agent's append-only thought log grows past a million entries; finding relevant past becomes hopeless and dumping it all into context is impossible. The team embeds each memory item, indexes it in a vector store, and at query time retrieves top-k semantically similar items (plus optional recency boost). Now 'what did I decide about latency three months ago' returns the actual right entries rather than the most recent or none, and prompt size stays bounded as memory grows.

## Consequences

**Benefits**

- Semantically relevant past surfaces automatically.
- Scales to memory stores too large for context.

**Liabilities**

- Misses purely temporal queries ('what did I do yesterday?').
- Embedding drift on schema changes.

## Failure modes

- Temporal blind spot — a question like what happened yesterday returns similar items from any date, not the recent ones.
- Embedding drift — the embedding model changes, and old vectors no longer match new queries well.
- Near-miss retrieval — the top-k items share wording with the query but not its meaning, and the agent reasons from the wrong memories.
- Decay mistuned — aging is too strong and older relevant items never surface, or too weak and stale items crowd out new ones.

## What this pattern constrains

The agent reads memory only through the retriever; full-store scans are not part of the loop.

## Applicability

**Use when**

- Long-running agents accumulate facts whose relevance is best judged by similarity.
- Append-only logs would otherwise grow unboundedly without retrieval.
- An embedding model and vector index can be deployed and maintained.

**Do not use when**

- Memory is small and a typed key-value store would serve better.
- Recency or exact-match retrieval matters more than semantic similarity.
- Vector index maintenance cost outweighs the retrieval benefit.

## Components

- Embedding model — produces a vector for each memory item at write time and for the query at read time
- Vector index — persistent ANN store holding (id, vector, payload) tuples for similarity search
- Writer — embeds new memory items and upserts them into the index
- Retriever — embeds the query or current state, fetches top-k nearest neighbours, returns payloads
- Decay/salience weighter — adjusts neighbour scores with recency boost or salience to break ties on raw similarity

## Tools

- Vector database — Pinecone, Weaviate, Chroma, FAISS, or pgvector for the index itself
- Embedding model — OpenAI text-embedding-3, Cohere embed-v3, or a local bge model
- Optional reranker — cross-encoder pass over the top-k to lift retrieval quality before context injection

## Evaluation metrics

- Recall@k of golden memories — fraction of labelled relevant items that appear in the top-k for matching queries
- Retrieval latency p95 — wall-clock for embed+query+rerank on a typical store size
- Embedding-drift incidents — count of breakages caused by changing the embedding model without reindexing
- Temporal-query miss rate — fraction of 'what did I do yesterday' style questions where similarity alone fails
- Storage and index cost per million items — the operational floor under which the pattern stops paying off

## Known uses

- **[MemGPT / Letta archival memory](https://docs.letta.com/)** _available_
- **Generative Agents memory stream (Park et al.)** _available_
- **LangChain VectorStoreRetrieverMemory** _available_
- **[Sparrot](https://marco-nissen.com/sparrot/)** _available_ — Embedding-indexed memory sits alongside the Markdown corpus so semantically similar items can be retrieved from a query, not just keyword matches.

## Related patterns

- _used-by_ **MemGPT-Style Paging**
- _specialises_ **Naive RAG** — Vector Memory is RAG over the agent's own past.
- _alternative-to_ **Knowledge Graph Memory**
- _used-by_ **Self-Archaeology**
- _used-by_ **Co-Located Memory Surfacing**
- _complements_ **Salience Attention Mechanism**
- _complements_ **Self-Corpus Vocabulary**
- _used-by_ **Semantic Memory**
- _used-by_ **Episodic Memory**
- _composes-with_ **Agentic Memory**
- _complements_ **Memory-Type Storage Specialization**
- _used-by_ **CDC-Driven Vector Sync**
- _used-by_ **Streaming Feature Pipeline**
- _used-by_ **FTI LLM Pipeline Split**

## References

- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) — Park et al., 2023
