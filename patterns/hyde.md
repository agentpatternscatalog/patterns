# HyDE

**Also known as:** Hypothetical Document Embeddings

**Category:** Retrieval & RAG  
**Status in practice:** emerging

## Intent

Have the LLM write a hypothetical answer document, embed it, and use it as the retrieval query.

## Context

Short or underspecified queries embed far from long-form passages in dense vector space; supervised relevance data is absent.

## Problem

Query-document length and style asymmetry hurts dense retrieval recall on short queries.

## Forces

- Hallucinated documents that miss the topic redirect retrieval badly.
- Adds an LLM call per query.
- Often paired with reranking to recover from off-topic hallucinations.


## Applicability

**Use when**

- Short user queries underperform on dense retrieval against long documents.
- An LLM call to draft a hypothetical answer fits the latency and cost budget.
- Recall on the first stage of RAG is the current bottleneck.

**Do not use when**

- Naive query embedding already retrieves the right chunks.
- Drafting hypothetical answers introduces unacceptable latency.
- The corpus or query distribution makes hallucinated drafts misleading anchors.

## Solution

On query: prompt the LLM to draft a hypothetical answer to the query. Embed the hypothetical answer. Retrieve top-k by similarity to that embedding (not the original query). Pass the retrieved chunks into normal RAG.

## Consequences

**Benefits**

- Zero-shot improvement; no encoder fine-tuning.
- Particularly strong on short, underspecified queries.

**Liabilities**

- Off-topic hallucinations cause retrieval drift.
- One extra LLM call per query.

## What this pattern constrains

Retrieval queries the index with the hypothetical answer's embedding, not the user query's embedding.

## Known uses

- **LangChain HyDE retriever** — *Available*

## Related patterns

- *specialises* → [naive-rag](naive-rag.md)
- *composes-with* → [cross-encoder-reranking](cross-encoder-reranking.md)

## References

- (paper) Gao, Ma, Lin, Callan, *Precise Zero-Shot Dense Retrieval without Relevance Labels*, 2022, <https://arxiv.org/abs/2212.10496>

**Tags:** rag, retrieval, embedding
