# Infinite Debate

**Also known as:** Stuck Multi-Agent, Convergence Failure, Agents Stuck Talking, Multi-Agent Loop

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: launch multi-agent debate without a termination rule and watch the agents loop forever.

## Context

Debate or consensus patterns are added without explicit halt conditions; the agents argue until the cost cap kicks in.

## Problem

Debate without termination converges only by accident. Real cost grows linearly while progress stalls.

## Forces

- Consensus heuristics are easy to game.
- Round caps cut off legitimate convergence.
- Judge agents become the new bottleneck.

## Solution

Don't. Add a round cap and a termination predicate. Pair debate with a judge or aggregator. See debate, step-budget, the-stop-hook.

## Consequences

**Liabilities**

- Cost blow-up.
- User-visible non-termination.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Early multi-agent demos in 2023-2024** — *Available*

## Related patterns

- *alternative-to* → [debate](debate.md)
- *alternative-to* → [step-budget](step-budget.md)
- *alternative-to* → [stop-hook](stop-hook.md)
- *conflicts-with* → [communicative-dehallucination](communicative-dehallucination.md)

## References

- (repo) *ai-standards/ai-design-patterns (Infinite Debate)*, <https://github.com/ai-standards/ai-design-patterns>

**Tags:** anti-pattern, multi-agent, termination
