# Eval Harness

**Also known as:** Golden Dataset Suite, Champion-Challenger, Regression Suite

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Run a held-out dataset against agent versions to detect regressions and measure improvement.

## Context

Agents are non-deterministic and prompt-sensitive; without an eval harness, every change is a guess.

## Problem

A change that 'feels better' often isn't; without measurement, the system regresses silently.

## Forces

- Dataset construction is expensive and ages.
- Judging open-ended outputs needs a metric or judge.
- Champion-challenger is fairer but doubles cost.

## Solution

Build a golden dataset of (input, expected output) pairs. Run candidate versions against the dataset; score each. Compare champion (current) against challenger (proposed). Promote on quality lift, blocked on regression. Re-run on every meaningful change.

## Consequences

**Benefits**

- Quality becomes measurable, comparable, and trendable.
- Releases gain a quantitative gate.

**Liabilities**

- Dataset bias means high scores can hide real-world failures.
- LLM-as-judge has its own calibration cost.

## What this pattern constrains

Releases are blocked if the harness flags a regression beyond tolerance.

## Known uses

- **Bobbin (Stash2Go)** — *Planned*. Eval harness flagged as the explicit next step; in beta because of this gap.
- **Sparrot** — *Planned*
- **Ragas, DeepEval, Langfuse Evals** — *Available*

## Related patterns

- *uses* → [llm-as-judge](llm-as-judge.md)
- *generalises* → [eval-as-contract](eval-as-contract.md)
- *complements* → [shadow-canary](shadow-canary.md)
- *alternative-to* → [perma-beta](perma-beta.md)
- *used-by* → [dspy-signatures](dspy-signatures.md)
- *complements* → [model-card](model-card.md)
- *used-by* → [agent-as-judge](agent-as-judge.md)
- *used-by* → [automatic-workflow-search](automatic-workflow-search.md)

## References

- (repo) *explodinggradients/ragas*, <https://github.com/explodinggradients/ragas>
- (doc) *Anthropic: Building Effective Agents (eval section)*, 2024

**Tags:** eval, regression, harness
