# Process Reward Model

**Also known as:** PRM, Step-Level Verifier

**Category:** Verification & Reflection  
**Status in practice:** emerging

## Intent

Train a verifier that scores each reasoning step rather than only the final answer.

## Context

Multi-step reasoning tasks where final-answer scoring conflates good reasoning with lucky right answers.

## Problem

Outcome reward models reinforce shortcut reasoning that lands on the right answer through wrong steps; step-level supervision gives finer-grained signal.

## Forces

- Step-level annotation is expensive (humans must label each step).
- Step boundaries vary across tasks.
- PRM and outcome reward sometimes conflict on what counts as 'correct'.


## Applicability

**Use when**

- Outcome-only reward reinforces shortcut reasoning that lands on the right answer the wrong way.
- Step-level labels (correct, neutral, incorrect, hallucination) can be collected at scale.
- Test-time search or fine-tuning can consume step-level scores.

**Do not use when**

- Outcome reward already produces robust generators on the target task.
- Collecting step-level labels at sufficient scale is not feasible.
- Inference-time scoring overhead exceeds the quality gain.

## Solution

Collect step-level labels (correct / neutral / incorrect / hallucination) for chain-of-thought traces. Train a classifier to predict step labels. At inference, score every step; reject candidates whose intermediate steps have low scores. Powers test-time search and fine-tuning of the generator.

## Example scenario

A maths-reasoning agent passes most of the eval set but on inspection many traces have correct final answers reached through wrong intermediate steps — shortcuts the outcome reward model rewarded. The team trains a process-reward-model: human raters label each chain-of-thought step as correct, neutral, incorrect, or hallucinated; a classifier learns step-level scores. At inference, candidates whose intermediate steps score low are rejected even when the final answer happens to match. The agent's reasoning quality, not just its final accuracy, improves.

## Consequences

**Benefits**

- Catches wrong-reasoning-right-answer cases.
- Enables tree-search and best-of-N with finer signal.

**Liabilities**

- Annotation cost.
- PRM calibration shifts with model capability.

## What this pattern constrains

Final answers are accepted only when intermediate steps pass the PRM threshold.

## Known uses

- **OpenAI 'Let's Verify Step by Step' baseline** — *Available*
- **DeepMind reasoning evaluators** — *Available*

## Related patterns

- *uses* → [best-of-n](best-of-n.md)
- *specialises* → [test-time-compute-scaling](test-time-compute-scaling.md)
- *complements* → [lats](lats.md)

## References

- (paper) Lightman, Kosaraju, Burda, Edwards, Baker, Lee, Leike, Schulman, Sutskever, Cobbe, *Let's Verify Step by Step*, 2023, <https://arxiv.org/abs/2305.20050>

**Tags:** verification, reward, step-level
