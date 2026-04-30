# Reflection

**Also known as:** Self-Critique, Single-Pass Self-Review

**Category:** Verification & Reflection  
**Status in practice:** mature

## Intent

Have the model review its own output and produce a revised version in one or more passes.

## Context

First-pass model outputs contain mistakes a second look would catch; the cost of an extra pass is acceptable.

## Problem

One-shot generation underuses the model; a second pass focused on critique often fixes errors at modest cost.

## Forces

- Same-model self-critique misses correlated blind spots.
- Free-form review drifts; the model invents new criteria each time.
- Termination: when does the loop stop?

## Solution

After producing an output, the model is prompted (often as a critic persona) to find issues. The original output and critique go back into a revision step. Repeat until a stop condition (no new issues, max iterations).

## Consequences

**Benefits**

- Catches surface errors cheaply.
- Pairs naturally with structured outputs.

**Liabilities**

- Diminishing returns after one or two passes.
- Self-reinforced confidence on wrong answers (Reflexion replication studies).

## What this pattern constrains

The reviewer may only critique against criteria fixed by the surrounding system; free-form criteria invention is forbidden when the pattern is used at a correctness boundary.

## Known uses

- **Knitting-DSL Pipeline (Stash2Go)** — *Available*. scopedLlmReviewer.js runs a frozen 6-item rubric.
- **Self-Refine paper** — *Available*

## Related patterns

- *generalises* → [frozen-rubric-reflection](frozen-rubric-reflection.md)
- *specialises* → [evaluator-optimizer](evaluator-optimizer.md)
- *generalises* → [reflexion](reflexion.md)
- *used-by* → [agentic-rag](agentic-rag.md)
- *generalises* → [chain-of-verification](chain-of-verification.md)
- *generalises* → [self-refine](self-refine.md)
- *alternative-to* → [same-model-self-critique](same-model-self-critique.md)
- *generalises* → [critic](critic.md)
- *used-by* → [self-rag](self-rag.md)

## References

- (paper) Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback*, 2023, <https://arxiv.org/abs/2303.17651>

**Tags:** reflection, self-critique
