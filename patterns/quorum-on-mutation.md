# Quorum on Mutation

**Also known as:** Two-Tick Confirmation, Distributed Consensus (Single Agent)

**Category:** Safety & Control  
**Status in practice:** experimental

## Intent

Require multiple consecutive ticks (or runs) to agree before a mutation to durable state lands.

## Context

A long-running agent proposes changes to its own rules or persistent memory; one-shot proposals can encode transient confusion as permanent state.

## Problem

A single-tick edit can capture momentary confusion as a lasting rule.

## Forces

- More ticks = slower change; legitimate improvements are delayed.
- Coordination across ticks needs a proposal / approval state machine.
- User override should always be available for legitimate fast paths.

## Solution

Mutation proposals are written to a holding area. A subsequent tick must confirm the proposal (still endorses it given fresh context). After K consecutive confirms, the mutation lands. Explicit user approval bypasses the wait.

## Consequences

**Benefits**

- Reduces transient-confusion mutations.
- Surfaces hesitation: K-1 confirms then a withdrawal is itself signal.

**Liabilities**

- Latency on legitimate changes.
- Implementation complexity in the agent's state machine.

## What this pattern constrains

A mutation cannot land on a single tick's say-so; it requires K consecutive endorsements.

## Known uses

- **Sparrot** — *Available*. rules/*.md changes require two consecutive ticks to agree, or explicit user approval.

## Related patterns

- *complements* → [constitutional-charter](constitutional-charter.md)
- *complements* → [inner-critic](inner-critic.md)

**Tags:** safety, consensus, mutation
