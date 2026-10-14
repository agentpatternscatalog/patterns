# Prompt Variant Evaluation

**Also known as:** Prompt Flow Variant Compare, Batch-Variant Evaluation

**Category:** Verification & Reflection  
**Status in practice:** mature

## Intent

Author multiple variants of the same prompt node, run them as a batch against a shared dataset, and let an automated evaluation flow score them so the winning variant is selected by measurement.

## Context

A team is iterating on a prompt — different wordings, different examples, different model bindings. Selecting between variants by demo or by author taste produces non-reproducible decisions and loses the comparator the moment the demo is forgotten.

## Problem

Without a batched comparison harness each prompt edit is a vibe check. Authors converge on what looks good on the two examples they happened to test. Subsequent reviewers cannot tell whether the chosen variant is better than the rejected ones because the rejected ones were never measured. The team accumulates committed prompts whose superiority over alternatives no one can verify.

## Forces

- Variants must run against the same dataset for comparison to be valid.
- The eval rubric must be frozen before the variants run, or scoring is post-hoc rationalisation.
- Multiple variants per slot multiply cost — sensible batch size matters.
- Winners must be inspectable: per-variant scores, per-item differences.

## Therefore

Therefore: author each prompt change as a variant slot, run the slot's variants as a batch against the same eval dataset with the same rubric, and select by measurement, so prompt decisions are reproducible.

## Solution

Build a prompt-flow harness that supports variant slots. For each slot the author writes 2-N variants. The harness runs all variants against the frozen eval dataset and rubric, scores them (deterministic checker, LLM-judge, or both), and surfaces per-variant scores plus per-item differences. The team picks the winner from the surfaced scores. Distinct from [[shadow-canary]] (live traffic, two versions): variant evaluation is offline, batched, pre-deployment.

## Structure

```
Prompt node with variant slots (variants 1..N) + frozen eval set + frozen rubric -> batch run in eval harness -> score (deterministic checker and/or LLM judge) -> per-variant scores + per-item differences -> select winner by measured score
```

## Diagram

```mermaid
flowchart LR
  V1[Variant 1] --> Eval[Eval harness]
  V2[Variant 2] --> Eval
  V3[Variant 3] --> Eval
  Set[Frozen eval set] --> Eval
  Rub[Frozen rubric] --> Eval
  Eval --> Scores[Per-variant scores]
  Scores --> Pick[Select winner]
```

## Example scenario

A team has a profile-extraction prompt with five candidate wordings. They run all five against the frozen 100-item eval set using an LLM-judge rubric. Variant 3 wins on overall score but variant 5 wins on a specific edge-case slice; the team picks variant 3 and adds the edge cases to the eval set so future runs measure them.

## Consequences

**Benefits**

- Prompt decisions become measurements with audit trail.
- Surfaces unexpected variant strengths the author would have missed.
- Composes with EDD: variant evaluation is the unit of progress under EDD.

**Liabilities**

- Running many variants multiplies inference cost.
- Eval rubric must be honest; variants can be tuned to game a weak rubric.
- Authors over-iterate when every change is cheap to evaluate.

## Failure modes

- Rubric gaming — variants are tuned to the weak spots of the rubric, and the winner scores well while being worse in use.
- Over-iteration — cheap evaluation invites endless small variants, and the team spends cost and time chasing noise in the scores.
- Overfit to the frozen set — repeated selection against one dataset picks the variant that fits those items, not the task.
- Ignored per-item diffs — only the average is read, and a variant that wins overall but fails a critical case is shipped.

## What this pattern constrains

A prompt edit must not be selected by demo or author taste; variants are evaluated as a batch against the frozen rubric and the winner is selected by measured score.

## Applicability

**Use when**

- Multiple plausible prompt variants exist and the team needs to pick among them.
- An eval dataset and rubric exist (i.e. [[evaluation-driven-development]] is in place).
- Inference cost permits batched comparison.

**Do not use when**

- No eval rubric exists — there is nothing to compare against.
- Variants differ in ways the rubric cannot measure.
- Live-traffic comparison (Bayesian bandit, shadow-canary) better fits the team's needs.

## Components

- Variant slot — named place in the prompt graph holding 2-N variants
- Eval harness — runs variants against the frozen set
- Scorer — deterministic checker or LLM-judge with frozen rubric
- Variant report — per-variant scores plus per-item differences

## Tools

- Prompt-flow runner (Promptfoo, Azure Prompt Flow) — executes variants
- Frozen eval dataset — pinned input set
- LLM-judge — produces scoring signal when deterministic checks don't suffice

## Evaluation metrics

- Per-variant aggregate score
- Per-slice variant ranking — surfaces edge-case strengths
- Cost per evaluated variant — guards over-iteration

## Known uses

- **[AI Agents in Action (Lanham) — Prompt Flow variant comparison](https://livebook.manning.com/book/ai-agents-in-action/chapter-9)** _available_
- **[Azure Prompt Flow / OpenAI Evals variant slots](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/concept-variants?view=azureml-api-2)** _available_

## Related patterns

- _composes-with_ **evaluation-driven-development**
- _uses_ **Eval Harness**
- _uses_ **Frozen Rubric Reflection**
- _uses_ **LLM-as-Judge**
- _composes-with_ **Bayesian Bandit Experimentation**
- _alternative-to_ **Shadow Canary**
- _complements_ **Prompt Versioning**
- _composes-with_ **Dimensional Synthetic Eval Set**

## References

- [AI Agents in Action](https://www.manning.com/books/ai-agents-in-action) — Micheal Lanham, 2025
