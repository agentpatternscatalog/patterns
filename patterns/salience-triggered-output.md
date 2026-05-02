# Salience-Triggered Output

**Also known as:** Endogenous Push, Threshold Notification

**Category:** Streaming & UX  
**Status in practice:** experimental

## Intent

Have the agent emit a message only when an internal salience signal crosses a threshold, not on every cycle.

## Context

A tick-based or always-on agent; constant output overwhelms; silence is wasteful when something matters.

## Problem

Agents that emit on every cycle are noisy; agents that only emit on user request miss timely signals.

## Forces

- Salience scoring is itself a model; flawed scoring leads to noise or silence.
- Threshold tuning is per-context.
- Hygiene: rate-limiting prevents nag spirals.

## Solution

Score every internal event for salience (novelty + goal-relevance + recency + prediction-error - fatigue). When the score for a candidate output crosses a threshold, emit. Otherwise log and move on. Rate-limit emissions per time window.

## Consequences

**Benefits**

- Output rate matches signal rate.
- Salience scores become inspectable in the trace.

**Liabilities**

- Threshold tuning is fragile to context shifts.
- Silence on low salience can hide problems.

## What this pattern constrains

Output is forbidden unless the salience score exceeds the configured threshold.

## Known uses

- **Sparrot** — *Available*. Pushes when insight clears salience threshold, when focus is stuck, when contradiction surfaces, when goal completes.

## Related patterns

- *used-by* → [bidirectional-impulse-channel](bidirectional-impulse-channel.md)
- *complements* → [streaming-typed-events](streaming-typed-events.md)
- *complements* → [event-driven-agent](event-driven-agent.md)
- *complements* → [degenerate-output-detection](degenerate-output-detection.md)
- *complements* → [intra-agent-memo-scheduling](intra-agent-memo-scheduling.md)
- *complements* → [mode-adaptive-cadence](mode-adaptive-cadence.md)

## References

- (paper) Karl Friston, *The free-energy principle: a unified brain theory?*, 2010

**Tags:** salience, endogenous, threshold
