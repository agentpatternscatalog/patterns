# Evaluator-Optimizer

**Also known as:** Generator-Critic Loop, LLM-as-Judge Refinement

**Category:** Verification & Reflection  
**Status in practice:** mature

## Intent

One LLM generates; another evaluates and feeds back; loop until criteria are met.

## Context

Tasks with measurable evaluation criteria where iterative refinement beats single-pass generation.

## Problem

Single-shot generation tops out below what an evaluator-corrected loop achieves.

## Forces

- The evaluator must be calibrated; a bad judge teaches bad lessons.
- Loop budget caps cost.
- Generator and evaluator can collude (especially if same model, same prompt family).

## Solution

Generator produces a candidate. Evaluator scores it against criteria with feedback. Generator revises with the feedback. Loop until evaluator passes or max iterations.

## Consequences

**Benefits**

- Quality climbs predictably with iterations.
- Evaluator can be reused as an offline regression suite.

**Liabilities**

- Cost = (generator + evaluator) x iterations.
- Convergence is not guaranteed.

## What this pattern constrains

Generator outputs are accepted only after the evaluator passes; an unbounded loop is forbidden by the iteration cap.

## Known uses

- **Anthropic Building Effective Agents (Workflow #5)** — *Available*
- **Cursor auto-fix loops** — *Available*
- **Cline auto-iterate** — *Available*
- **Aider lint-then-fix loop** — *Available*

## Related patterns

- *generalises* → [reflection](reflection.md)
- *alternative-to* → [best-of-n](best-of-n.md)
- *composes-with* → [planner-executor-observer](planner-executor-observer.md)
- *uses* → [llm-as-judge](llm-as-judge.md)
- *conflicts-with* → [same-model-self-critique](same-model-self-critique.md)
- *alternative-to* → [self-refine](self-refine.md)
- *used-by* → [crag](crag.md)
- *used-by* → [dynamic-expert-recruitment](dynamic-expert-recruitment.md)

## References

- (blog) *Anthropic: Building Effective Agents*, 2024, <https://www.anthropic.com/research/building-effective-agents>

**Tags:** evaluator, loop, judge
