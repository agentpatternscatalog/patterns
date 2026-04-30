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

## Consequences

**Benefits**

- Substantial hallucination reduction without retrieval.
- Composes with retrieval naturally (retrieve evidence per question).

**Liabilities**

- 4x baseline cost.
- Verification quality depends on question coverage.

## What this pattern constrains

Verification answers are produced without the draft in context; coupled verification is not permitted.

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
