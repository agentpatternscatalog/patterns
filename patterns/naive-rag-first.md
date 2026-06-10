# Naive-RAG-First

**Also known as:** RAG-By-Default, Vector-Store-First

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: reach for naive RAG before checking whether the knowledge actually needs retrieval.

## Context

A team is starting a new knowledge-grounded agent — a customer-support bot, an internal Q&A assistant, a docs helper — and the field's reference architectures push retrieval-augmented generation (RAG, where the system embeds documents into a vector store and looks up passages by semantic similarity) as the default move. The team builds the vector index before checking where the answer-bearing knowledge actually lives. Often the real source is a database, an internal API, a search service, or a small set of stable documents that would fit in the system prompt.

## Problem

When the knowledge lives in a structured store, semantic retrieval over embeddings is the wrong shape: the agent gets approximate, stale passages where a typed SQL query or a single API call would return an exact, fresh answer. The team pays embedding pipeline cost, vector store cost, and re-indexing cost on every update, and quality drops compared to the simpler design because retrieval is solving the wrong problem. Naive RAG also adds an entire failure surface — chunking, embedding drift, recall holes — that a typed tool call simply does not have.

## Forces

- RAG is on every reference architecture.
- Vector stores feel like a moat.
- Tool use is sometimes harder to build than RAG.


## Applicability

**Use when**

- Never use this; check whether the knowledge belongs in a tool, database, or scoped prompt before adopting RAG.
- Use tool-use when the knowledge lives behind an API or query.
- Adopt naive-rag only when those simpler stores genuinely do not work.

**Do not use when**

- Any project where vector indexes are added by reflex without checking alternatives.
- Any setting where a SQL query, API call, or inlined document would already answer the need.
- Any team treating RAG as a default rather than a deliberate choice.

## Therefore

Therefore: locate where the knowledge actually lives — a database, API, search service, or a small inlined document — before adding a vector index, so that retrieval is shaped to the data rather than reflexed onto it.

## Solution

Don't reach for RAG first. Check whether the knowledge lives in a tool (database, API, search service), a scoped system prompt, or a small inlined document. Only adopt RAG when those genuinely do not work. See tool-use, naive-rag for when it does.

## Example scenario

A team's first move on a new internal Q&A bot is to spin up a vector index over the company wiki. After three weeks they discover that 80 percent of questions are about live ticket status, which is in their helpdesk database, and a vector search over stale wiki pages cannot answer them. They name the failure naive-rag-first: they tear out the index for those queries and route them to a typed helpdesk tool call. RAG stays only for the genuine free-text knowledge questions where the wiki is authoritative.

## Diagram

```mermaid
flowchart TD
  Q[New knowledge need] --> X{Where does it live?}
  X -->|tool / DB / API| T[Use tool-use]
  X -->|small + stable| P[Inline in system prompt]
  X -->|truly external + large| R[Use naive-rag]
  X -.skipped check.-> AP[Anti-pattern: RAG by default]
  AP -.causes.-> Bloat[Index sprawl & latency]
```

## Consequences

**Liabilities**

- Architectural complexity that pays for nothing.
- Retrieval misses that a SQL query would not.
- Embedding maintenance burden.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Common in 2023-2024 enterprise AI projects** — *Available*

## Related patterns

- *conflicts-with* → [naive-rag](naive-rag.md) — RAG is fine; RAG-first is not.
- *alternative-to* → [tool-use](tool-use.md)

## References

- (paper) Gao et al., *Retrieval-Augmented Generation for Large Language Models: A Survey*, 2023, <https://arxiv.org/abs/2312.10997>

**Tags:** anti-pattern, rag, architecture
