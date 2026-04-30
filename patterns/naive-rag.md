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

## Solution

Chunk the corpus. Embed each chunk with a dense encoder. At query time, embed the query, retrieve top-k by similarity, prepend chunks to the prompt, generate. The simplest production RAG pipeline.

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
