# Emotional State Persistence

**Also known as:** Affect State, Visceral Sensation Tracking, Decaying Emotion Scalars

**Category:** Verification & Reflection
**Status in practice:** emerging
**Author:** Sparrot

## Intent

Track the agent's affective state as bounded, decaying scalars across ticks so reasoning can react to its own emotional load instead of treating each turn as emotionally blank.

## Context

Long-running agents whose runs span hours or days and whose recent history affects how the next tick should be shaped. Frustration after stuck loops, a small lift after a clean win, accumulating fatigue across token-heavy stretches — none of these are visible to the next prompt unless they are materialised as state.

## Problem

Long-running agents accumulate emotional residue that is invisible to the next prompt unless it is materialised as state. Each tick treats the agent as emotionally blank, so the model cannot adapt cadence, depth, or risk-taking to its own current load.

## Forces

- Unbounded scalars drift; the agent can pump itself into permanent states.
- Without decay, emotional state never resolves and stays anchored to old events.
- Self-write of mood is a license to manipulate; reflection-only writes for major resets are safer.
- Vocabulary choice matters: too many scalars are noise, too few collapse signal.

## Solution

Define a small fixed vocabulary (for example tenderness, fear, depression, joy, shame, pain) as scalars in the range 0..1. Each scalar has a half-life (30 minutes to 4 hours depending on the dimension). On events that should affect mood, update the scalar with a bounded delta. Persist as JSON. Inject the current snapshot into every tick prompt as a brief affect badge. Reflection passes can use spikes and drops as signals, and a deeper consolidation pass (see dream-consolidation-cycle) can perform major resets.

## Consequences

**Benefits**

- Emotional load becomes visible state instead of invisible drift.
- Bounded scalars and decay prevent permanent stuck states.
- Reflection has a richer signal to act on than just the last few thoughts.

**Liabilities**

- Vocabulary is opinionated; getting it wrong skews everything downstream.
- Affect-as-state can be over-read as ground truth when it is just a heuristic.
- Self-update paths must be locked down or the agent learns to game its own mood.

## What this pattern constrains

Emotion scalars must be bounded to [0,1], must decay according to a fixed half-life rule, and cannot be unboundedly bumped by the agent itself; reflection-only writes for the major resets.

## Applicability

**Use when**

- The agent runs long enough that affective load could meaningfully accumulate across ticks.
- Reasoning quality is sensitive to the agent's own affective state (e.g. high-frustration ticks should de-escalate).
- There is a downstream pattern (dream-consolidation-cycle, mode-adaptive-cadence) that consumes the scalars.

**Do not use when**

- The agent is short-lived and emotional state has no time to accumulate.
- Affective modelling is out of scope for the product domain.
- Persisting emotion-like state would mislead users about the agent's nature.

## Variants

### Bounded scalar with half-life

Each named emotion (frustration, anticipation, etc.) is a scalar in [0,1] that decays exponentially with a fixed half-life.

*Distinguishing factor:* decay over time

*When to use:* Default. Simple, bounded, easy to reason about.

### Event-only update

Scalars only change in response to explicit events; no continuous decay.

*Distinguishing factor:* no continuous decay

*When to use:* When deterministic test reproducibility matters more than realistic decay.

### Surface-on-threshold

Scalars only enter the prompt context when they exceed a threshold; below threshold the context is unaffected.

*Distinguishing factor:* gated visibility

*When to use:* When low-level affect should not bias every tick but spikes should.

## Example scenario

A long-running personal agent has had a tense exchange in the morning, a routine reminder at lunch, and a celebratory message in the afternoon, but each tick reads to the model as emotionally blank. So at 5pm it pushes a hard challenge to a user it should be holding lightly. The team materialises Emotional State Persistence: bounded, decaying scalars (tension, warmth, fatigue) are written into the agent's context each turn and updated by reflection. The model now adapts cadence and risk-taking to its own current load instead of treating every turn as fresh.

## Known uses

- **[Sparrot](https://github.com/luxxyarns/sparrot)** — *Available*

## Related patterns

- *complements* → [awareness](awareness.md)
- *complements* → [liminal-state-detection](liminal-state-detection.md)
- *uses* → [provenance-ledger](provenance-ledger.md)
- *used-by* → [dream-consolidation-cycle](dream-consolidation-cycle.md)

## References

- (book) Antonio Damasio, *The Feeling of What Happens*, 1999, <https://www.goodreads.com/book/show/125777.The_Feeling_of_What_Happens>

**Tags:** affect, state, tick-loop, self-model
