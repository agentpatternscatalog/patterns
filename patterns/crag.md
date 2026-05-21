# CRAG

**Also known as:** Corrective RAG

**Category:** Retrieval & RAG  
**Status in practice:** emerging

## Intent

Add a lightweight retrieval evaluator that grades each retrieved document and triggers corrective web search on poor retrievals.

## Context

A team is running a retrieval-augmented system in production over a corpus where retrieval quality varies request by request. Sometimes the top chunks are exactly right; sometimes they are tangentially related; sometimes they miss the answer entirely. The team cannot guarantee that every query gets a clean retrieval, and the cost of a hallucinated or confidently wrong answer is high enough that they need an explicit recovery path.

## Problem

A naive retrieve-then-generate pipeline passes every retrieval — good or bad — straight into the generator without judging it. When the retrieval is poor, the generator either ignores it and falls back to parametric knowledge that may itself be wrong, or it incorporates it and produces an answer corrupted by irrelevant chunks. Either way, the user sees no signal that the retrieval was weak, and the system has no correction step that could fall back to a web search, refine the query, or refuse to answer when the evidence is insufficient.

## Forces

- Evaluator quality bounds correction accuracy.
- Web fallback adds latency and external dependency.
- Three-way grading (correct / ambiguous / incorrect) needs calibration.

## Therefore

Therefore: insert a lightweight evaluator after retrieval and let its three-way grade trigger pass-through, web search, or rejection, so that bad retrievals are caught before they reach the generator.

## Solution

After retrieval, a lightweight evaluator (T5-based or similar) grades each document as Correct, Ambiguous, or Incorrect. Correct documents go forward as-is. Ambiguous documents trigger a web search for additional evidence. Incorrect documents are discarded and replaced via web search. The generator receives the corrected document set.

## Variants

- **Three-grade CRAG** — Evaluator labels each retrieval Correct / Ambiguous / Incorrect; only Ambiguous and Incorrect trigger fallback (the canonical paper recipe).
- **Binary CRAG** — Simplified two-grade variant (good / bad) used when a calibrated three-way evaluator is unavailable.
- **Decompose-and-recompose CRAG** — For Correct documents, additionally strip irrelevant strips and recompose only the relevant strips before passing to the generator.

## Example scenario

A RAG-powered legal assistant retrieves three statutes for a question about export controls; one of them is from the wrong jurisdiction. Naive RAG would hand all three to the generator and the wrong statute would corrupt the answer. The team layers in CRAG: a lightweight evaluator grades each retrieved document for relevance, the wrong-jurisdiction one falls below threshold, and the system triggers a corrective web search before generation. The final answer is grounded in two strong retrievals plus one fresh source instead of one bad one.

## Diagram

```mermaid
flowchart TD
  Q[Query] --> R[Retrieve docs]
  R --> E[Evaluator grades each doc]
  E --> C{Grade}
  C -- Correct --> G[Generate]
  C -- Ambiguous --> W[Web search<br/>augment]
  C -- Incorrect --> W
  W --> G
  G --> A[Answer]
```

## Consequences

**Benefits**

- Robustness to poor retrievals.
- Plug-and-play with existing RAG.

**Liabilities**

- Two-stage retrieval increases latency.
- Web fallback has its own correctness questions.

## What this pattern constrains

The generator sees only retrieval-graded-Correct documents, optionally augmented with corrective-search results.

## Applicability

**Use when**

- Naive RAG passes bad retrievals through to the generator and corrupts outputs.
- A lightweight evaluator (e.g. T5-class) can grade documents as Correct, Ambiguous, or Incorrect cheaply.
- Web search is available as a corrective fallback for ambiguous or incorrect retrievals.

**Do not use when**

- Retrieval quality is already high enough that the evaluator step adds no measurable lift.
- No corrective fallback (e.g. web search) is available, so the evaluator's verdict has no recovery path.
- Latency budget cannot absorb the extra evaluator and fallback hops.

## Known uses

- **CRAG paper baseline** — *Available*
- **LangGraph Corrective-RAG tutorial** — *Available*

## Related patterns

- *specialises* → [agentic-rag](agentic-rag.md)
- *uses* → [evaluator-optimizer](evaluator-optimizer.md)

## References

- (paper) Yan, Gui, Xiao, Mei, Liu, Shang, Sun, Wang, *Corrective Retrieval Augmented Generation*, 2024, <https://arxiv.org/abs/2401.15884>

**Tags:** rag, corrective, evaluator
