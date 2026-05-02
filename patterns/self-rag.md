# Self-RAG

**Also known as:** Self-Reflective RAG

**Category:** Retrieval & RAG  
**Status in practice:** emerging

## Intent

Fine-tune the model to emit reflection tokens that decide when to retrieve, evaluate retrieved relevance, and assess generated support.

## Context

Retrieval-augmented generation where the model needs to reason about whether to retrieve, whether retrieved evidence is relevant, and whether the generation is supported.

## Problem

Static retrieve-then-generate retrieves regardless of need and generates regardless of evidence quality; both wastes calls and admits hallucination.

## Forces

- Token vocabulary expansion adds training complexity.
- Reflection tokens must be enforced at inference, not just trained.
- Self-evaluation correlates with the model's blind spots.


## Applicability

**Use when**

- Retrieval-augmented generation needs to decide when to retrieve and whether evidence is relevant.
- Static retrieve-then-generate wastes calls or admits hallucination.
- Fine-tuning the model with reflection tokens is feasible.

**Do not use when**

- A simpler RAG pipeline meets quality targets.
- Fine-tuning the generator on reflection tokens is not feasible.
- Latency or cost of inline reflection tokens is unacceptable.

## Solution

A critic model is first trained to label data with reflection tokens. The generator is then fine-tuned on the labeled data to emit four reflection tokens inline at inference: [Retrieve], [IsRel] (is retrieved evidence relevant?), [IsSup] (is generation supported?), [IsUse] (is generation useful?). The host enforces the reflection grammar and uses tokens to control flow.

## Consequences

**Benefits**

- Adaptive retrieval: skip when not needed.
- Inline self-evaluation grounds generation.

**Liabilities**

- Requires fine-tuning; not zero-shot.
- Reflection-token quality bounded by training data.

## What this pattern constrains

Generation steps are gated by the reflection grammar; the model cannot generate freely without emitting the appropriate reflection tokens.

## Known uses

- **Self-RAG paper baseline** — *Available*

## Related patterns

- *specialises* → [agentic-rag](agentic-rag.md)
- *uses* → [reflection](reflection.md)

## References

- (paper) Asai, Wu, Wang, Sil, Hajishirzi, *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*, 2023, <https://arxiv.org/abs/2310.11511>

**Tags:** rag, self-reflection, fine-tuning
