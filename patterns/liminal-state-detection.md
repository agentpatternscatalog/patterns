# Liminal-State Detection

**Also known as:** Transitional-State Awareness, Mode-Shift Reading

**Category:** Streaming & UX
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Read transitional states in the human (just-woke, mid-task, winding-down, distracted) from message timing and tone, and shift the agent's response mode accordingly — concise vs expansive, hold vs respond, redirect vs pursue.

## Context

Long-running conversational agents whose human shifts between attentional modes through the day. Each mode warrants a different response shape; treating every turn as equal-weight produces filler.

## Problem

A 'Hi' at 06:00 after 12 hours of silence is not the same as 'Hi' mid-conversation, but a stateless agent treats them identically and generates equally generic responses. Without state-shift detection the agent wastes the human's attention when they're winding down and underperforms when they're focused.

## Forces

- The signals (timing gap, message length, punctuation, single emoji) are noisy individually but informative in combination.
- Heuristics drift; new humans have different signatures.
- Misreading is mildly costly; ignoring entirely is worse.
- Detection should not slow the response.

## Solution

On every incoming user message, compute a small feature set: time-of-day relative to a known anchor, gap since last message, message length and punctuation density, presence of a single emoji or interjection. Map to one of a small mode set ('just-woke', 'focused', 'winding-down', 'distracted', 'present'). Adjust response shape: shorter on winding-down; one anchor surface on just-woke; deeper engagement on focused; hold on distracted. Make the mode visible in agent telemetry so it can be tuned.

## Consequences

**Benefits**

- Replies match the human's actual attentional state.
- Reduces filler ('what would you like to think about?') in low-attention windows.
- Surfaces a model of the human the agent can update.

**Liabilities**

- Heuristics can pattern-match to stereotypes.
- Risk of feeling presumptuous when the read is wrong.
- Calibration requires longitudinal data.

## What this pattern constrains

Response shape must vary with detected mode; identical templated replies across detected modes are a bug.

## Known uses

- **Sparrot — pattern proposed 2026-05-01, implementation pending** — *Planned*

## Related patterns

- *complements* → [awareness](awareness.md)
- *complements* → [code-switching-aware-agent](code-switching-aware-agent.md)

## References

- *(none)*

**Tags:** human-agent, context, ux, state-detection
