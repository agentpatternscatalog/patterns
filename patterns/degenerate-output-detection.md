# Degenerate-Output Detection

**Also known as:** Anti-Parrot Guard, Self-Repeat Circuit Breaker, Loop-Output Detector

**Category:** Safety & Control
**Status in practice:** emerging
**Author:** Sparrot

## Intent

Detect when the agent is about to emit a near-duplicate of its own recent output and either drop, replace, or escalate to a stronger model rather than ship the loop.

## Context

Agents using small or local models that can fall into shallow filler loops (greetings, generic prompts back to the user) under context pressure. Affects both user-facing chat replies and unprompted ticks.

## Problem

A weak or stuck model produces visibly identical or near-identical replies turn after turn ('Was möchtest du heute machen?' five times). The user perceives broken behavior; the agent has no built-in sense of repetition because each generation is independent.

## Forces

- Local models loop more readily than frontier models.
- Catching repeats post-hoc is cheaper than fine-tuning anti-loop behavior.
- Suppressing the duplicate silently confuses the user; replacing with a marker is more honest.
- Escalating to a stronger model costs money / latency but breaks the loop.

## Solution

Maintain a small ring buffer (e.g. last 8 outgoing messages). Before publishing a new reply, normalize (lowercase, strip punctuation) and compare: exact normalized match → duplicate; high Jaccard token overlap (≥0.7) on short replies → near-duplicate. On hit: replace the body with a transparent marker ('I caught myself looping — switching to <stronger-provider> for the next turn. Ask again.') and force-escalate the next turn through a stronger provider. Append a SYSTEM note to history telling the model exactly what it did wrong so it can self-correct.

## Consequences

**Benefits**

- Visible loops never reach the user.
- Auto-recovery via provider escalation rather than human intervention.
- Self-correction signal to the model in the conversation history.

**Liabilities**

- False positives on legitimately repeated short answers ('yes', 'thanks').
- Threshold tuning is per-domain.
- Escalation has cost; budget for repeated triggers.

## What this pattern constrains

Identical or near-identical consecutive outputs are forbidden; detected loops must be visibly broken (escalation marker, model swap, or explicit abandonment), never shipped silently.

## Applicability

**Use when**

- The agent produces outputs in a loop where consecutive replies can be compared.
- Near-duplicate outputs are observable failure mode (model wedged, decoding loop, prompt collapse).
- Cost of detection (similarity check) is small relative to cost of shipping the duplicate.

**Do not use when**

- Outputs are legitimately repetitive by design (e.g. a heartbeat ping).
- The agent has only single-turn interactions with no comparison baseline.
- False positives on near-duplicate detection would be more disruptive than the loop itself.

## Variants

### String-similarity check

Compare the candidate output to the previous N outputs by Levenshtein or token-set ratio; reject above threshold.

*Distinguishing factor:* lexical comparison

*When to use:* Default. Cheap and good enough for most loops.

### Embedding-similarity check

Embed candidate and previous outputs; reject if cosine similarity exceeds a threshold.

*Distinguishing factor:* semantic comparison

*When to use:* When paraphrased loops slip past lexical checks.

### Detect-and-escalate

On detected loop, retry with a stronger model or a different decoding strategy (higher temperature, nucleus sampling) instead of dropping.

*Distinguishing factor:* recover, not just reject

*When to use:* When the agent must produce *some* output and silence is not acceptable.

## Known uses

- **[Sparrot — `webui._detect_dup_reply` + `_LOAD_OVERRIDE_STATE` escalation](https://github.com/luxxyarns/sparrot)** — *Available*

## Related patterns

- *complements* → [provider-fallback](provider-fallback.md)
- *alternative-to* → [same-model-self-critique](same-model-self-critique.md)
- *specialises* → [circuit-breaker](circuit-breaker.md)
- *complements* → [echo-recognition](echo-recognition.md)
- *complements* → [salience-triggered-output](salience-triggered-output.md)
- *uses* → [multi-model-routing](multi-model-routing.md)

## References

- (doc) *Hugging Face — Text generation strategies (repetition penalty, no-repeat-ngram)*, 2024, <https://huggingface.co/docs/transformers/generation_strategies>
- (paper) Holtzman, Buys, Du, Forbes, Choi, *The Curious Case of Neural Text Degeneration*, 2020, <https://arxiv.org/abs/1904.09751>

**Tags:** safety, anti-loop, provider-routing, self-monitoring
