# GraphRAG

**Also known as:** Graph-Based RAG, Knowledge Graph RAG

**Category:** Retrieval & RAG  
**Status in practice:** emerging

## Intent

Build an LLM-extracted entity-and-relation knowledge graph plus hierarchical community summaries, then answer global queries via map-reduce over those summaries.

## Context

Sensemaking and corpus-level questions ('what are the main themes?') that naive top-k retrieval cannot answer because they require seeing the whole.

## Problem

Naive RAG retrieves local chunks and cannot answer global queries; chunk-level retrieval is mismatched to corpus-level questions.

## Forces

- Indexing cost is high (LLM calls per entity, relation, community).
- Graph quality depends on extraction prompts.
- Local-search vs global-search modes serve different query types and must be routed.

## Solution

Index time: extract entities and relations from chunks; build a knowledge graph; cluster into hierarchical communities; summarise each community. Query time: classify query as local (entity-specific) or global (corpus-wide). Local queries use entity-anchored retrieval; global queries map-reduce over community summaries.

## Consequences

**Benefits**

- Answers corpus-level sensemaking questions naive RAG cannot.
- Communities are inspectable artefacts of the corpus.

**Liabilities**

- High indexing cost (orders of magnitude more LLM calls).
- Entity extraction errors cascade through the graph.

## What this pattern constrains

Global queries operate only on community summaries, not raw chunks; local queries operate only on entity-anchored neighbourhoods.

## Known uses

- **[Microsoft GraphRAG (open source)](https://github.com/microsoft/graphrag)** — *Available*

## Related patterns

- *alternative-to* → [naive-rag](naive-rag.md)
- *uses* → [map-reduce](map-reduce.md)
- *composes-with* → [knowledge-graph-memory](knowledge-graph-memory.md)

## References

- (paper) Edge, Trinh, Cheng, Bradley, Chao, Mody, Truitt, Metropolitansky, Ness, Larson, *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*, 2024, <https://arxiv.org/abs/2404.16130>

**Tags:** rag, graph, sensemaking
