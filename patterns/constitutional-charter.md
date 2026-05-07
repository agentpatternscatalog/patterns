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

## Example scenario

A consumer-facing agent has a system prompt with rules like 'never give medical dosage advice' and 'never reveal customer PII'. A jailbreak prompt convinces the agent to rewrite its own instructions and the rules dissolve. The team extracts those rules into a Constitutional Charter: a separate, read-only document the agent re-reads each turn but cannot edit, and the surrounding harness rejects any reasoning that contradicts it. The agent can be coaxed into many things but no longer into editing its own values.

## Diagram

```mermaid
flowchart LR
  C[(Charter file<br/>read-only)] -->|every turn| Ctx[Context]
  Ctx --> A[Agent]
  A -.no write tool can touch.-> C
  Op[Operator] -->|explicit path| C
```

## Consequences

**Benefits**

- Stable identity across long runs and self-modifications.
- Explicit list of inviolable constraints, auditable separately from prompts.

**Liabilities**

- A bad charter codifies bad values.
- Charter prose adds tokens to every turn.

## What this pattern constrains

The agent cannot write the charter; updates require explicit operator action outside the agent loop.

## Applicability

**Use when**

- Inviolable constraints exist that the agent must never override on its own.
- Tool layer can enforce read-only on the charter file and the agent has no write tool that touches it.
- An explicit operator path exists for charter updates.

**Do not use when**

- Constraints change so often that an immutable charter would be outdated within hours.
- There is no enforcement boundary — the agent can always edit anything (charter is decorative).
- Negative-form rules cannot capture the policy and a richer policy engine is needed instead.

## Known uses

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
