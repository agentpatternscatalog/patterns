# Chain of Verification

**Also known as:** CoVe, Factored Verification, Verify Before Answering

**Category:** Reasoning  
**Status in practice:** emerging

## Intent

Reduce hallucination by drafting an answer, generating independent verification questions, answering them in isolation, and revising.

## Context

Long-form factual generation (biographies, summaries, recommendations) where plausible-sounding errors creep into the draft.

## Problem

When the model verifies its own draft in the same context, the draft biases follow-up checks; errors persist.

## Forces

- Verification questions must be independently answerable.
- Joint verification (all questions in one prompt) underperforms factored.
- Verification cost scales with question count.

## Solution

Four-step pipeline. Draft: produce initial answer. Plan: generate verification questions covering claims in the draft. Execute: answer each question in isolation, without seeing the original draft. Revise: rewrite the draft using the verification answers.

## Variants

- **Joint CoVe** — Generate verification questions and answer them in a single prompt; cheapest but lets the draft bias the checks.
- **Two-step CoVe** — Plan questions in one call, answer them in a second call that does not see the draft.
- **Factored CoVe** — Answer each verification question in its own isolated prompt so checks cannot reinforce each other (highest quality).
- **Factor+Revise CoVe** — Factored execution plus an explicit cross-check step that flags inconsistencies between draft and verification answers before revising.

## Consequences

**Benefits**

- Substantial hallucination reduction without retrieval.
- Composes with retrieval naturally (retrieve evidence per question).

**Liabilities**

- 4x baseline cost.
- Verification quality depends on question coverage.

## What this pattern constrains

Verification answers are produced without the draft in context; coupled verification is not permitted.

## Applicability

**Use when**

- The model hallucinates claims when it self-verifies in the same context as the draft.
- Verification questions can be answered in isolation without seeing the draft.
- A revise step can integrate the verification answers back into the final output.

**Do not use when**

- The task has no factual claims to verify (pure stylistic or generative tasks).
- Latency budget cannot absorb four sequential model calls per output.
- Verification questions cannot be answered cheaply or independently.

## Known uses

- **Meta AI implementation** — *Available*

## Related patterns

- *specialises* → [reflection](reflection.md)
- *complements* → [self-consistency](self-consistency.md)
- *composes-with* → [naive-rag](naive-rag.md)
- *alternative-to* → [critic](critic.md)

## References

- (paper) Dhuliawala, Komeili, Xu, Raileanu, Li, Celikyilmaz, Weston, *Chain-of-Verification Reduces Hallucination in Large Language Models*, 2023, <https://arxiv.org/abs/2309.11495>

**Tags:** reasoning, verification, hallucination
