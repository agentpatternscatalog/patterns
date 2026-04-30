# Extended Thinking

**Also known as:** Reasoning Tokens, Reasoning Budget

**Category:** Reasoning  
**Status in practice:** mature

## Intent

Spend a configurable budget of internal reasoning tokens before producing a user-visible answer.

## Context

Hard reasoning tasks where extra inference-time compute reliably improves answer quality.

## Problem

Static prompt-based CoT mixes reasoning into the response; reasoning models offer a separate budget meter and opaque internal reasoning the user does not see.

## Forces

- Reasoning tokens cost more than standard tokens on most providers.
- User-visible latency rises with thinking budget.
- Opaque reasoning blocks: harder to inspect and debug.

## Solution

Use the provider's reasoning-mode API (OpenAI o-series reasoning effort, Anthropic Claude extended thinking budget_tokens, Gemini thinking budget). Set budget per request based on task difficulty (cheap for routing, expensive for hard reasoning). Monitor reasoning-token consumption.

## Consequences

**Benefits**

- Quality lift on hard reasoning without prompt rewrites.
- Budget meter is a clean control.

**Liabilities**

- Cost spikes with budget.
- Opaque reasoning blocks are harder to debug than visible CoT.

## What this pattern constrains

Reasoning happens within the declared token budget; exceeding it terminates reasoning and forces an answer.

## Known uses

- **Anthropic Claude extended thinking (budget_tokens)** — *Available*
- **Gemini 2.5 thinking budget** — *Available*
- **DeepSeek-R1** — *Available*
- **OpenAI reasoning effort (o1, o3, o4-mini)** — *Available*. Qualitative low/medium/high control.

## Related patterns

- *complements* → [chain-of-thought](chain-of-thought.md)
- *complements* → [scratchpad](scratchpad.md)
- *complements* → [cost-gating](cost-gating.md)
- *specialises* → [test-time-compute-scaling](test-time-compute-scaling.md)
- *complements* → [reasoning-trace-carry-forward](reasoning-trace-carry-forward.md)

## References

- (doc) *Anthropic: Extended thinking*, <https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking>
- (doc) *OpenAI: Reasoning models*, <https://platform.openai.com/docs/guides/reasoning>

**Tags:** reasoning, budget, tokens
