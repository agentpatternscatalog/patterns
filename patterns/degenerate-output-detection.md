# Degenerate-Output Detection

**Also known as:** Anti-Parrot Guard, Self-Repeat Circuit Breaker, Loop-Output Detector

**Category:** Safety & Control
**Status in practice:** experimental
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

No two consecutive outgoing messages may exceed the similarity threshold without intervention.

## Known uses

- **Sparrot — `webui._detect_dup_reply` + `_LOAD_OVERRIDE_STATE` escalation** — *Available*

## Related patterns

- *complements* → [provider-fallback](provider-fallback.md)
- *alternative-to* → [same-model-self-critique](same-model-self-critique.md)
- *specialises* → [circuit-breaker](circuit-breaker.md)

## References

- *(none)*

**Tags:** safety, anti-loop, provider-routing, self-monitoring
