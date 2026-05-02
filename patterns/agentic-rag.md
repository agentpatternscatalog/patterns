# Agentic RAG

**Also known as:** Iterative RAG

**Category:** Retrieval & RAG  
**Status in practice:** mature

## Intent

Replace static retrieve-then-generate with autonomous agents that plan, choose sources, retrieve iteratively, reflect, and re-query.

## Context

Multi-hop, ambiguous, or evolving information needs where single-shot retrieval is insufficient.

## Problem

Naive RAG cannot decide whether to retrieve, which source to use, when to stop retrieving, or how to recover from poor retrievals.

## Forces

- Agentic loops cost more than single-shot retrieval.
- Source selection requires capability descriptions.
- Loop bounds must prevent runaway retrieval.

## Solution

Treat retrieval as a tool. The agent decides whether to retrieve, formulates and reformulates the query, picks among multiple retrievers (vector, graph, keyword, web), evaluates retrieved evidence, and re-queries on insufficient results. Composes naturally with reflection, planning, and tool-use patterns.

## Consequences

**Benefits**

- Handles multi-hop and adaptive queries.
- Source diversity (multi-store retrieval) becomes feasible.

**Liabilities**

- Cost and latency rise with loop iterations.
- Loop quality depends on agent self-evaluation.

## What this pattern constrains

Retrieval is one tool among many; the agent decides invocation, but each retrieval is bounded by the step budget.

## Applicability

**Use when**

- A single retrieve-then-generate pass is insufficient for the task's information needs.
- Multiple retrievers (vector, graph, keyword, web) exist and the right one varies per query.
- The agent benefits from reflecting on retrieved evidence and re-querying when results are poor.

**Do not use when**

- Static one-shot RAG already meets quality targets at lower cost and latency.
- Latency budgets cannot afford iterative retrieval rounds.
- There is only one retriever and no meaningful query reformulation possible.

## Known uses

- **Self-RAG, CRAG implementations** — *Available*
- **LangGraph Agentic RAG tutorials** — *Available*
- **Perplexity** — *Available*
- **ChatGPT Search** — *Available*
- **Glean** — *Available*
- **Notion AI** — *Available*

## Related patterns

- *generalises* → [naive-rag](naive-rag.md)
- *uses* → [react](react.md)
- *uses* → [reflection](reflection.md)
- *uses* → [tool-use](tool-use.md) — Retrieval is exposed as a tool the agent decides to invoke.
- *composes-with* → [cross-encoder-reranking](cross-encoder-reranking.md) — Reranking is a near-universal RAG companion.
- *generalises* → [self-rag](self-rag.md)
- *generalises* → [crag](crag.md)

## References

- (paper) Singh, Ehtesham, Kumar, Khoei, *Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG*, 2025, <https://arxiv.org/abs/2501.09136>

**Tags:** rag, agentic, iterative
