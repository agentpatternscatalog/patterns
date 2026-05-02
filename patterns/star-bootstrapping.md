# STaR Bootstrapping

**Also known as:** Self-Taught Reasoner, Rationale Bootstrapping

**Category:** Reasoning  
**Status in practice:** emerging

## Intent

Bootstrap a model's reasoning by training it on its own correct chain-of-thought outputs.

## Context

Reasoning tasks where chain-of-thought helps but supervised rationale data is unavailable.

## Problem

Without supervised rationale data, fine-tuning for reasoning is constrained; pure CoT prompting plateaus.

## Forces

- Filter quality determines what 'correct' rationale gets reinforced.
- Wrong rationales that produce right answers can leak in.
- Compute cost of repeated generation + filtering.


## Applicability

**Use when**

- Reasoning task where CoT helps but supervised rationale data is unavailable.
- Ground-truth answers exist so generated rationales can be filtered.
- Fine-tuning the model on rationale + answer pairs is feasible.

**Do not use when**

- No ground-truth answers exist to filter rationales.
- The base model is too weak to produce any correct CoT outputs.
- Quick iteration matters more than the bootstrap-and-train cycle.

## Solution

Prompt the base model with CoT to generate rationale + answer pairs. Keep pairs where the answer matches ground truth. **Rationalization**: when a generated rationale yields the wrong answer, prompt the model with the correct answer as a hint and ask for a rationale that justifies it; add the rationalized example to training. Fine-tune on the kept + rationalized pairs. Repeat: the fine-tuned model generates better rationales next round; iterate.

## Variants

- **Vanilla STaR** — Generate rationale+answer; keep pairs whose answer matches ground truth; fine-tune on those.
- **STaR with rationalisation** — On failure, prompt the model with the correct answer as a hint, accept the resulting rationale, and add it to the training set.
- **Quiet-STaR** — Train the model to generate token-level rationales for every token, not only at problem boundaries (Zelikman et al. 2024).

## Example scenario

A team has a small base model that knows facts but cannot reliably reason. They prompt it with CoT to generate (rationale, answer) pairs across a dataset with ground-truth answers. They keep pairs whose answer is right; for wrong answers they 'rationalize' (give the model the right answer and ask for a rationale). They fine-tune on the kept set, then iterate. After two STaR rounds the model's reasoning capability climbs without any human-written rationales.

## Consequences

**Benefits**

- Self-improvement on reasoning without rationale labels.
- Iterative gains compound.

**Liabilities**

- Spurious-rationale leakage if filtering is too lax.
- Compute-heavy.

## What this pattern constrains

Training data is restricted to filter-passing rationales; ungrounded rationales are not reinforced.

## Known uses

- **STaR paper experiments** — *Available*
- **Influences modern reasoning-distillation pipelines** — *Available*

## Related patterns

- *uses* → [chain-of-thought](chain-of-thought.md)
- *complements* → [self-consistency](self-consistency.md)
- *specialises* → [rest-em](rest-em.md)

## References

- (paper) Zelikman, Wu, Mu, Goodman, *STaR: Bootstrapping Reasoning with Reasoning*, 2022, <https://arxiv.org/abs/2203.14465>

**Tags:** reasoning, training, bootstrapping
