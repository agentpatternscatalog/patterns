# Toolformer

**Also known as:** Self-Supervised Tool Learning

**Category:** Tool Use & Environment  
**Status in practice:** deprecated

## Intent

Train the model to learn when and how to call tools through self-supervised data, without human annotation.

## Context

Tool use deployed at scale where prompt-based function-calling underperforms and human-labelled tool-use traces are unavailable.

## Problem

Prompt-based tool calling is brittle and capability-limited; supervised fine-tuning needs costly human-labelled traces.

## Forces

- Self-supervised data must distinguish helpful from unhelpful tool calls.
- The training-time tool surface diverges from runtime over time.
- Filtering noise dominates training cost.

## Solution

Generate candidate tool calls during training. Insert each into a context. Score whether the resulting completion is improved (perplexity drop on the gold continuation). Keep helpful insertions as training data. Fine-tune the model to emit tool calls in those positions.

## Consequences

**Benefits**

- No human-labelled tool-call data required.
- Model learns when not to call tools, not just when to.

**Liabilities**

- Training pipeline complexity.
- Tool surface drift between train and serve.
- Historical: superseded by RLHF-tuned tool-use in frontier models; not productionised at scale.

## What this pattern constrains

Tool use is bound to positions where self-supervised filtering judged the call helpful; ungrounded tool calls are not reinforced.

## Known uses

- **Toolformer paper baseline** — *Available*
- **Influences modern instruction-tuning of frontier models** — *Available*

## Related patterns

- *specialises* → [tool-use](tool-use.md)
- *complements* → [agent-skills](agent-skills.md)
- *alternative-to* → [tool-discovery](tool-discovery.md)

## References

- (paper) Schick, Dwivedi-Yu, Dessì, Raileanu, Lomeli, Zettlemoyer, Cancedda, Scialom, *Toolformer: Language Models Can Teach Themselves to Use Tools*, 2023, <https://arxiv.org/abs/2302.04761>

**Tags:** tool-use, self-supervised, training
