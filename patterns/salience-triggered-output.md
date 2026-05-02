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


## Applicability

**Use when**

- The agent runs on a tick or always-on loop and emits too often or too seldom.
- An internal salience signal can be defined from novelty, goal-relevance, and recency.
- Users tolerate occasional silence in exchange for less noise.

**Do not use when**

- The agent is request-driven and emits exactly when asked.
- Missing a low-salience event is unacceptable (compliance, safety telemetry).
- No reliable salience signal can be constructed.

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
