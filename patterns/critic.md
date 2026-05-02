# Tool-Augmented Self-Correction

**Also known as:** Tool-Interactive Self-Correction, CRITIC

**Category:** Verification & Reflection  
**Status in practice:** emerging

## Intent

Self-correct LLM outputs by interactively critiquing them with external tools (search, code execution, calculator).

## Context

Generation tasks where errors can be detected and corrected by grounded checks (factual claims by search, code by execution, math by calculator).

## Problem

Self-critique without external tools recycles the model's blind spots; tools provide grounded ground-truth signals.

## Forces

- Tool selection per critique step.
- Critique cost adds to generation cost.
- Tools may themselves be wrong or limited.

## Solution

After draft generation, the model emits a critique that names suspected errors and queries tools to verify. Tool results inform the revised output. Iterate until tools find no more issues or budget exhausted.

## Consequences

**Benefits**

- Grounded self-correction beats ungrounded reflection.
- Tool invocations during critique are auditable.

**Liabilities**

- Latency and cost per turn.
- Tool selection itself is a learning problem.

## What this pattern constrains

The critic may revise outputs only when an external tool corroborates a defect; ungrounded edits are forbidden.

## Applicability

**Use when**

- The model has external tools (search, code, calculator) that can produce grounded ground-truth signals.
- Self-critique without tools recycles the model's blind spots and fails to catch real errors.
- Iteration to convergence (or a budget cap) is acceptable in the latency model.

**Do not use when**

- No external tools exist that meaningfully verify the model's claims.
- Latency budget allows only one model call per output.
- Critique-and-revise loops collapse to no change and add cost without gain.

## Known uses

- **CRITIC paper baselines** — *Available*

## Related patterns

- *specialises* → [reflection](reflection.md)
- *alternative-to* → [chain-of-verification](chain-of-verification.md)
- *uses* → [tool-use](tool-use.md)

## References

- (paper) Gou, Shao, Gong, Shen, Yang, Duan, Chen, *CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing*, 2023, <https://arxiv.org/abs/2305.11738>

**Tags:** reflection, tool-grounded, self-correction
