# CRAG

**Also known as:** Corrective RAG

**Category:** Retrieval & RAG  
**Status in practice:** emerging

## Intent

Add a lightweight retrieval evaluator that grades each retrieved document and triggers corrective web search on poor retrievals.

## Context

Production RAG where retrieval quality varies and the system must recover gracefully from low-quality retrievals.

## Problem

Naive RAG passes every retrieval into the generator; bad retrievals corrupt outputs without any correction step.

## Forces

- Evaluator quality bounds correction accuracy.
- Web fallback adds latency and external dependency.
- Three-way grading (correct / ambiguous / incorrect) needs calibration.

## Solution

After retrieval, a lightweight evaluator (T5-based or similar) grades each document as Correct, Ambiguous, or Incorrect. Correct documents go forward as-is. Ambiguous documents trigger a web search for additional evidence. Incorrect documents are discarded and replaced via web search. The generator receives the corrected document set.

## Consequences

**Benefits**

- Robustness to poor retrievals.
- Plug-and-play with existing RAG.

**Liabilities**

- Two-stage retrieval increases latency.
- Web fallback has its own correctness questions.

## What this pattern constrains

The generator sees only retrieval-graded-Correct documents, optionally augmented with corrective-search results.

## Known uses

- **CRAG paper baseline** — *Available*
- **LangGraph Corrective-RAG tutorial** — *Available*

## Related patterns

- *specialises* → [agentic-rag](agentic-rag.md)
- *uses* → [evaluator-optimizer](evaluator-optimizer.md)

## References

- (paper) Yan, Gui, Xiao, Mei, Liu, Shang, Sun, Wang, *Corrective Retrieval Augmented Generation*, 2024, <https://arxiv.org/abs/2401.15884>

**Tags:** rag, corrective, evaluator
