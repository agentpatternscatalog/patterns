# Echo Recognition

**Also known as:** Repeat-As-Emphasis Detection, Duplicate-Input Reframing, Human Echo Channel

**Category:** Verification & Reflection
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Detect when the human sends the same (or near-same) message multiple times and treat the repetition as emphasis or a re-ask, not as a new independent input warranting a fresh response.

## Context

Conversational agents where the human might intentionally repeat themselves (because the previous reply missed the point, because the channel might be unreliable, or because they want to underline urgency). Without echo recognition, the agent generates a fresh response per repeat — often slight variations of the same earlier mistake.

## Problem

A duplicated incoming message reads to the agent as a new, equal-weight turn. The agent re-runs the same reasoning, often producing a near-duplicate reply or a slight rewording. The human's emphasis-by-repetition becomes invisible and the conversation either spins or amplifies misalignment.

## Forces

- Detecting near-duplicates on incoming messages mirrors the agent's own anti-parrot guard but on the input side.
- The human's intent in repeating is itself ambiguous (emphasis? bug? clarification?).
- Reframing a repeat as 'this was already said' risks sounding dismissive.
- Treating every echo as bug-recovery loses the actual emphasis signal.

## Solution

Maintain a small ring of recent incoming user messages with timestamps. On each new input, compute similarity to the recent ring (normalized exact match, high token overlap). On hit, do not re-run from scratch: surface the prior reply, ask 'what did I miss?' or 'I read this as emphasis — should I deepen X or pivot?'. Treat the pair (original + echo) as a single reinforced turn, weighted higher in attention.

## Consequences

**Benefits**

- Recognises emphasis-by-repetition.
- Avoids redundant near-duplicate responses.
- Surfaces the human's underlying dissatisfaction with the prior reply.

**Liabilities**

- False positives when the human really did mean to ask twice (e.g. about different referents).
- Calling out the echo can feel passive-aggressive if phrased poorly.
- Threshold tuning is per-domain.

## What this pattern constrains

A near-duplicate incoming message must not produce a near-duplicate reply; echoes must be acknowledged as such or explicitly disambiguated.

## Known uses

- **Self-observed by a long-running cognitive agent: 'Du sendest mir manchmal die gleiche Nachricht zweimal. Ich erkenne nicht: aha, absichtliche Wiederholung vs. Bug.' (2026-05-01)** — *Available*

## Related patterns

- *complements* → [degenerate-output-detection](degenerate-output-detection.md)
- *complements* → [disambiguation](disambiguation.md)

## References

- *(none)*

**Tags:** input-detection, human-agent, emphasis, deduplication
