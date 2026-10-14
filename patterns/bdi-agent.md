# BDI Agent

**Also known as:** Belief-Desire-Intention Agent, Rao-Georgeff Agent, PRS-Style Agent

**Category:** Cognition & Introspection  
**Status in practice:** mature

## Intent

Agent maintains explicit Beliefs about the world, Desires (goals), and Intentions (committed plans), and reasons by reconciling the three.

## Context

An LLM agent runs across many model calls, observes the world through tool outputs, has goals it accumulates and abandons, and commits to multi-step plans. By default all of this lives implicitly in the prompt context: the agent's beliefs, goals, and commitments are tangled in one prose blob the next prompt assembles.

## Problem

Implicit BDI is brittle. The agent loses track of which beliefs are current vs stale, which goals are still active vs satisfied, and which intentions it has committed to vs merely entertained. A new prompt can silently abandon a committed plan because the commitment was not represented as a typed thing. Without explicit BDI structures the agent has no vocabulary for 'I currently believe X, my goal is Y, and I am pursuing plan Z' that survives across prompts.

## Forces

- Beliefs change as observations arrive; staleness must be representable.
- Desires (goals) can be in conflict; the agent needs a rule for which to pursue.
- Intentions (committed plans) should not be silently abandoned.
- Updates to beliefs may invalidate intentions; the reconciliation step is non-trivial.

## Therefore

Therefore: represent the agent's mental state as three typed stores — Beliefs, Desires, Intentions — and reconcile them on each tick, so commitments persist across prompts and the agent has explicit language for what it believes, wants, and is doing.

## Solution

Maintain three typed stores: Beliefs (propositions about the world with currency timestamps), Desires (active goals with priorities), Intentions (committed plans with status and rationale). On each tick the agent (a) updates Beliefs from new observations, (b) re-evaluates Desires given new Beliefs, (c) checks Intentions for continued viability (still consistent with Beliefs and aligned with Desires), and (d) commits new Intentions or abandons existing ones explicitly. Each transition writes a trace entry. Distinct from a plain scratchpad: BDI structures are typed.

## Structure

```
Observation --update--> Beliefs --re-evaluate--> Desires --commit or abandon (traced)--> Intentions --act on current intention--> Environment --> Observation; Beliefs -.invalidate.-> Intentions
```

## Diagram

```mermaid
flowchart TD
  Obs[Observation] --> B[Beliefs]
  B --> D[Desires]
  D --> I[Intentions]
  B -.invalidate.-> I
  I --> Act[Act on current intention]
  Act --> Obs
```

## Example scenario

A long-running ops agent maintains Beliefs (current cluster state, last-known costs), Desires (keep p95 latency under 200ms, keep monthly cost under $X), and Intentions (currently scaling out replica set 3). When a new observation arrives showing replica set 3 already scaled, the agent reconciles: belief updates, Intention is satisfied and retired with rationale, Desires re-evaluated, new Intention possibly committed.

## Consequences

**Benefits**

- Commitments survive across prompts because Intentions are first-class.
- Stale beliefs become surfaceable rather than hidden in prose.
- Goal abandonment becomes an explicit move with a rationale.

**Liabilities**

- Three stores plus reconciliation is heavy machinery for simple agents.
- BDI gives no help with how to set priorities — the conflict-resolution rule still needs design.
- Typed stores can drift away from what the prompt actually shows the model.

## Failure modes

- Stale beliefs — beliefs are not updated from new observations, so intentions stay marked viable after the world has changed.
- Silent abandonment — a new prompt pulls the agent onto other work, but the old intention is never explicitly dropped, and it lingers half-committed in the store.
- Priority deadlock — two desires conflict and no rule decides between them, so the agent keeps re-evaluating without committing to either.
- Store and prompt drift — the typed stores say one thing while the prompt the model actually sees says another, and the model acts on the prompt.

## What this pattern constrains

The agent's mental state must not be entirely implicit in the prompt blob; Beliefs, Desires, and Intentions are typed stores that the agent reconciles on each tick.

## Applicability

**Use when**

- Long-running agent across many prompts where commitments must persist.
- Goal conflicts and goal abandonment are common and need explicit treatment.
- Operators need a vocabulary for the agent's beliefs, goals, and plans.

**Do not use when**

- Short single-turn agent where BDI machinery is overkill.
- Goals and commitments are externally tracked (ticket system, workflow engine).
- Engineering capacity cannot keep typed stores in sync with the prompt.

## Components

- Belief store — propositions about the world with currency timestamps
- Desire store — active goals with priorities
- Intention store — committed plans with status and rationale
- Reconciliation step — runs on each tick to update beliefs, re-evaluate desires, validate intentions

## Tools

- Typed-record store — schema for B, D, I records
- Trace logger — captures every transition
- Reconciliation runner — scheduled or event-triggered tick

## Evaluation metrics

- Stale-belief rate — share of beliefs older than freshness bar at decision time
- Goal-abandonment trace coverage — share of dropped desires with explicit rationale
- Intention persistence — fraction of intentions that survive their natural lifetime

## Known uses

- **[Classical BDI architectures (PRS, JACK, Jason)](https://en.wikipedia.org/wiki/Belief%E2%80%93desire%E2%80%93intention_software_model)** _available_
- **[Multiagent Systems (Weiss, MIT Press) — BDI chapter](https://mitpress.mit.edu/9780262731317/multiagent-systems/)** _available_
- **[LLM-agent reimplementations exposing typed beliefs/goals/intentions](https://arxiv.org/abs/2511.17162)** _available_

## Related patterns

- _complements_ **Commitment Tracking**
- _complements_ **Hypothesis Tracking**
- _complements_ **Goal Decomposition**
- _complements_ **World Model as Tool**
- _alternative-to_ **Scratchpad**
- _complements_ **Plan-and-Execute**
- _composes-with_ **Joint Commitment Team**

## References

- [Multiagent Systems, 2nd ed.](https://mitpress.mit.edu/9780262731317/multiagent-systems/) — Gerhard Weiss (ed.), 2013
- [Belief-desire-intention software model](https://en.wikipedia.org/wiki/Belief%E2%80%93desire%E2%80%93intention_software_model)
