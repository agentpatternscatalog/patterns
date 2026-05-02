# Constitutional Charter

**Also known as:** Immutable Constitution, Negative Constraints, Robot Laws

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Define rules the agent reads every turn but cannot modify, encoding inviolable boundaries.

## Context

Long-running or self-modifying agents need a fixed point of reference; without one, recursive editing drifts the agent's identity.

## Problem

If the agent can edit everything, it can edit its own values; nothing stays inviolable.

## Forces

- Charter authors must encode hard constraints without paralysing the agent.
- Read-only at the tool layer is enforceable; read-only by exhortation is not.
- Charters age; updating requires human action.

## Solution

A charter file is read into context every turn (or every tick). The tool layer enforces read-only on it; the agent has no write tool that can touch it. Updates go through an explicit operator path. Charters typically express constraints in negative form ('the agent shall not...').

## Consequences

**Benefits**

- Stable identity across long runs and self-modifications.
- Explicit list of inviolable constraints, auditable separately from prompts.

**Liabilities**

- A bad charter codifies bad values.
- Charter prose adds tokens to every turn.

## What this pattern constrains

The agent cannot write the charter; updates require explicit operator action outside the agent loop.

## Known uses

- **Sparrot** — *Available*. charter.md read every tick; read-only at tool layer.
- **Anthropic Constitutional AI** — *Available*

## Related patterns

- *complements* → [quorum-on-mutation](quorum-on-mutation.md)
- *used-by* → [inner-critic](inner-critic.md)
- *used-by* → [refusal](refusal.md)
- *alternative-to* → [prompt-bloat](prompt-bloat.md)
- *complements* → [sovereign-inference-stack](sovereign-inference-stack.md)
- *composes-with* → [world-model-separation](world-model-separation.md)

## References

- (paper) Bai et al., *Constitutional AI: Harmlessness from AI Feedback*, 2022, <https://arxiv.org/abs/2212.08073>

**Tags:** safety, constitution, immutable
