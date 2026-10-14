# Process Reward Model

**Also known as:** PRM, Step-Level Verifier

**Category:** Verification & Reflection  
**Status in practice:** emerging

## Intent

Train a verifier that scores each reasoning step rather than only the final answer.

## Context

A team trains or evaluates a model on multi-step reasoning tasks such as mathematics word problems, multi-hop question answering, or chains of logical deduction. The model produces a chain of intermediate steps and a final answer, and the team has been training or selecting candidates using an outcome reward model (a verifier that only scores whether the final answer is right). They also have, or could collect, human labels at the level of individual reasoning steps.

## Problem

Outcome-only scoring cannot tell the difference between reasoning that got to the right answer correctly and reasoning that got to the right answer by lucky shortcuts, cancelled errors, or fabricated intermediate facts. Reinforcing on outcome alone rewards those shortcuts, so the model becomes more confident in chains of thought that contain wrong intermediate steps. Later, on harder problems where the shortcut does not exist, the same kinds of wrong intermediate steps lead to wrong final answers. The team needs a feedback signal that can reject a candidate because step three is wrong, even when step five happens to land on the right number.

## Forces

- Step-level annotation is expensive (humans must label each step).
- Step boundaries vary across tasks.
- PRM and outcome reward sometimes conflict on what counts as 'correct'.

## Therefore

Therefore: label and score reasoning steps individually rather than only the final answer, so that bad intermediate hops can be rejected before they propagate into a confidently wrong conclusion.

## Solution

Collect step-level labels (correct / neutral / incorrect / hallucination) for chain-of-thought traces. Train a classifier to predict step labels. At inference, score every step; reject candidates whose intermediate steps have low scores. Powers test-time search and fine-tuning of the generator.

## Structure

```
Reasoning trace -> split into steps -> process reward model scores each step (correct / neutral / incorrect / hallucination) -> any step below threshold -> reject candidate; all steps above -> accept final answer
```

## Diagram

```mermaid
flowchart TD
  CoT[Reasoning trace] --> S1[Step 1] --> S2[Step 2] --> S3[Step 3] --> Ans[Final answer]
  S1 --> PRM[Process reward model]
  S2 --> PRM
  S3 --> PRM
  PRM -->|low score| Reject[Reject candidate]
  PRM -->|all high| Accept[Accept]
```

## Example scenario

A maths-reasoning agent passes most of the eval set but on inspection many traces have correct final answers reached through wrong intermediate steps — shortcuts the outcome reward model rewarded. The team trains a process-reward-model: human raters label each chain-of-thought step as correct, neutral, incorrect, or hallucinated; a classifier learns step-level scores. At inference, candidates whose intermediate steps score low are rejected even when the final answer happens to match. The agent's reasoning quality, not just its final accuracy, improves.

## Consequences

**Benefits**

- Catches wrong-reasoning-right-answer cases.
- Enables tree-search and best-of-N with finer signal.

**Liabilities**

- Annotation cost.
- PRM calibration shifts with model capability.

## Failure modes

- Calibration lag — the generator improves, the PRM was trained on older traces, and its step scores no longer track step quality.
- Label noise — step-level annotations are inconsistent, and the PRM learns to reward a writing style rather than correct steps.
- Rejecting valid unusual steps — a correct but unfamiliar step scores low, and a good candidate is thrown away.
- Annotation cost cut — too few labelled traces are collected, and the PRM is weak on exactly the harder problems where it matters.

## What this pattern constrains

Final answers are accepted only when intermediate steps pass the PRM threshold.

## Applicability

**Use when**

- Outcome-only reward reinforces shortcut reasoning that lands on the right answer the wrong way.
- Step-level labels (correct, neutral, incorrect, hallucination) can be collected at scale.
- Test-time search or fine-tuning can consume step-level scores.

**Do not use when**

- Outcome reward already produces robust generators on the target task.
- Collecting step-level labels at sufficient scale is not feasible.
- Inference-time scoring overhead exceeds the quality gain.

## Components

- Generator — model emitting chain-of-thought traces with step boundaries
- Step segmenter — splits the trace into discrete steps the verifier can score
- Process reward model — classifier predicting correct/neutral/incorrect/hallucination per step
- Step-level annotation pipeline — human labellers producing the training data for the PRM
- Inference-time selector — rejects candidates with low intermediate-step scores

## Tools

- Step-label annotation interface — human raters tag each reasoning step
- Classifier training pipeline — fine-tunes the PRM on labelled step-level data
- LLM API — generator and inference-time scoring calls
- Tree-search or best-of-N harness — consumes per-step scores at inference time

## Evaluation metrics

- Step-level accuracy of the PRM — agreement with held-out human labels per step
- Wrong-reasoning-right-answer catch rate — share of lucky-shortcut traces the PRM rejects
- Final-answer accuracy lift over outcome-only reward — net gain from step-level scoring
- Annotation cost per percentage point of lift — economic shape of the PRM investment
- PRM calibration drift across model versions — when the PRM stops matching the new generator

## Known uses

- **OpenAI 'Let's Verify Step by Step' baseline** _available_
- **DeepMind reasoning evaluators** _available_
- **[Sparrot](https://marco-nissen.com/sparrot/)** _available_ — A thought-scoring pass scores individual reasoning steps along multiple axes (salience, conceptual fit, others) rather than only judging the final answer, so weak intermediate moves can be re-routed.

## Related patterns

- _uses_ **Best-of-N Sampling**
- _specialises_ **Test-Time Compute Scaling**
- _complements_ **Language Agent Tree Search**
- _complements_ **Adaptive Compute Allocation**
- _alternative-to_ **Reward Hacking**
- _complements_ **Checklist Partial-Credit Scoring** — A process reward model is a learned step-level verifier steering search or training inside the agent loop; this is a scoring rule for an evaluation report, authored per task rather than trained.

## References

- [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) — Lightman, Kosaraju, Burda, Edwards, Baker, Lee, Leike, Schulman, Sutskever, Cobbe, 2023
