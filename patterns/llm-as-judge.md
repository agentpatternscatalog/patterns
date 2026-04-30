# LLM-as-Judge

**Also known as:** Model Grading, Auto-Evaluator

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Use an LLM to score open-ended outputs against rubric criteria when no exact-match metric applies.

## Context

Free-form outputs (summaries, code, prose) defy exact-match scoring; human grading is too slow for CI.

## Problem

Without an automated grader, regression detection on free-form outputs requires human eyes on every run.

## Forces

- Judges have biases (length, position, model-family preference).
- Calibration against human judgement is its own dataset.
- Same-model judging is suspect when the candidate is from the same family.

## Solution

Define a rubric. Prompt a judge model with the input, candidate output, and rubric. Receive a structured score plus rationale. Calibrate periodically against human-graded samples. Use a different model family for judge vs candidate where possible.

## Consequences

**Benefits**

- Scales free-form evaluation.
- Rationales are debugging breadcrumbs.

**Liabilities**

- Judge biases skew scores in subtle ways.
- Cost: every eval is now N x judge calls.

## What this pattern constrains

Scores are advisory unless calibrated against human judgement at known intervals.

## Known uses

- **MT-Bench / AlpacaEval** — *Available*
- **Ragas / DeepEval / Langfuse** — *Available*

## Related patterns

- *used-by* → [eval-harness](eval-harness.md)
- *used-by* → [evaluator-optimizer](evaluator-optimizer.md)
- *generalises* → [agent-as-judge](agent-as-judge.md)
- *used-by* → [shadow-canary](shadow-canary.md)

## References

- (paper) Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, 2023, <https://arxiv.org/abs/2306.05685>

**Tags:** eval, judge, scoring
