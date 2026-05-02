# Naive RAG

**Also known as:** Retrieval-Augmented Generation, Top-K Retrieve-and-Stuff

**Category:** Retrieval & RAG  
**Status in practice:** mature

## Intent

Condition the generator on top-k chunks retrieved from an external dense index so knowledge lives outside parameters.

## Context

The agent needs information that lives in a corpus too large to fit in context, and that may change without retraining.

## Problem

Parametric LMs hallucinate, cannot cite, and cannot be updated without retraining; query-time external knowledge is needed.

## Forces

- Chunk size trades context loss for retrieval recall.
- Embedding choice constrains retrieval quality.
- Single-shot retrieval misses multi-hop questions.


## Applicability

**Use when**

- Knowledge lives outside the model and must be conditioned on at query time.
- Citations must be tied to retrieved sources, not invented from parameters.
- A simple chunk-and-embed pipeline meets the recall and quality bar.

**Do not use when**

- The needed knowledge is already in a tool, database, or scoped system prompt (see naive-rag-first).
- Global, corpus-wide questions need GraphRAG or hierarchical retrieval instead.
- Chunk-level retrieval is the wrong shape for the queries you actually serve.

## Solution

Chunk the corpus. Embed each chunk with a dense encoder. At query time, embed the query, retrieve top-k by similarity, prepend chunks to the prompt, generate. The simplest production RAG pipeline.

## Variants

- **Dense-only naive RAG** — Single dense vector index; top-k by cosine similarity (the canonical Lewis 2020 / DPR shape).
- **Sparse-only naive RAG** — BM25 / keyword index without embeddings; cheap and strong on exact-term queries.
- **Hybrid naive RAG** — Run both dense and BM25 retrieval, fuse with RRF, pass top-k to the generator.

## Example scenario

A startup ships a support assistant whose knowledge changes weekly — release notes, pricing, integration guides. Bake-it-into-the-prompt does not scale and fine-tuning on every release is impractical. They adopt naive-rag: chunk the docs, embed with a dense encoder, index, and at query time retrieve top-k and prepend to the prompt. The pipeline is the simplest possible and ships in a week. Knowledge updates now flow by re-indexing the docs, not by retraining or redeploying the model.

## Consequences

**Benefits**

- Knowledge updates without retraining.
- Citations become possible.

**Liabilities**

- Chunk boundaries destroy context.
- Top-k retrieval is recall-oriented; precision suffers without reranking.
- No iterative retrieval; multi-hop fails.

## What this pattern constrains

The generator may use only retrieved chunks plus its parametric memory; the retrieval set is the boundary.

## Known uses

- **LangChain / LlamaIndex default RAG** — *Available*
- **Most enterprise document-QA deployments** — *Available*

## Related patterns

- *generalises* → [hyde](hyde.md)
- *composes-with* → [cross-encoder-reranking](cross-encoder-reranking.md)
- *generalises* → [contextual-retrieval](contextual-retrieval.md)
- *alternative-to* → [graphrag](graphrag.md)
- *specialises* → [agentic-rag](agentic-rag.md)
- *conflicts-with* → [naive-rag-first](naive-rag-first.md) — Naive RAG is fine; treating it as the only answer is the anti-pattern.
- *composes-with* → [chain-of-verification](chain-of-verification.md)
- *generalises* → [vector-memory](vector-memory.md)
- *complements* → [citation-streaming](citation-streaming.md)
- *generalises* → [raft](raft.md)
- *generalises* → [hybrid-search](hybrid-search.md)
- *alternative-to* → [hallucinated-citations](hallucinated-citations.md)
- *used-by* → [app-exploration-phase](app-exploration-phase.md)

## References

- (paper) Lewis, Perez, Piktus, Petroni, Karpukhin, Goyal, Küttler, Lewis, Yih, Rocktäschel, Riedel, Kiela, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, 2020, <https://arxiv.org/abs/2005.11401>

**Tags:** rag, retrieval, vector
