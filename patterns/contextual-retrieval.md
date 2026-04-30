# Contextual Retrieval

**Also known as:** Chunk Contextualisation, Anthropic Contextual Embeddings

**Category:** Retrieval & RAG  
**Status in practice:** emerging

## Intent

Prepend a short LLM-generated description to each chunk before embedding so the chunk carries its situating context.

## Context

Chunks that lose context at split boundaries (pronouns, 'the company', time references) embed far from queries that name the entity explicitly.

## Problem

Naive chunking destroys context; queries that name entities by full name miss chunks that refer to them by pronoun.

## Forces

- An LLM call per chunk is expensive.
- Prompt caching of the parent document amortises the cost.
- Context generation must be deterministic enough to keep the index stable.

## Solution

For each chunk, prompt an LLM with the parent document and the chunk; receive a short description that situates the chunk. Prepend that description to the chunk. Embed the prepended chunk. Store BM25 over both prepended chunks (Contextual BM25) and dense vectors (Contextual Embeddings). Compose with reranking for further gains.

## Consequences

**Benefits**

- Reported retrieval-failure reductions: 35% (embeddings), 49% (+BM25), 67% (+reranking).
- Fully compatible with existing RAG pipelines.

**Liabilities**

- Indexing cost per chunk; only worth it for stable corpora.
- Chunk re-indexing required when context model changes.

## What this pattern constrains

Chunks enter the index only after contextualisation; raw chunks are not indexed.

## Known uses

- **[Anthropic Contextual Retrieval blog post](https://www.anthropic.com/news/contextual-retrieval)** — *Available*

## Related patterns

- *specialises* → [naive-rag](naive-rag.md)
- *composes-with* → [hybrid-search](hybrid-search.md)
- *composes-with* → [cross-encoder-reranking](cross-encoder-reranking.md)
- *uses* → [prompt-caching](prompt-caching.md)
- *alternative-to* → [raft](raft.md)

## References

- (blog) Anthropic, *Introducing Contextual Retrieval*, 2024, <https://www.anthropic.com/news/contextual-retrieval>

**Tags:** rag, contextual, anthropic
