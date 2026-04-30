# Hippocampal Rehearsal

**Also known as:** Memory Reactivation, Lift-from-Archive

**Category:** Memory  
**Status in practice:** experimental

## Intent

Lift archived memory items back into short-term tiers when something re-attends to them.

## Context

A long-running agent has archived something that becomes relevant again; cold-storage retrieval is slow and out-of-band.

## Problem

Archived items might as well not exist if the agent never thinks about them again, even when current context makes them relevant.

## Forces

- Re-attention triggers must be cheap to evaluate.
- Lifting too aggressively floods the working tier.
- The lifted item is now a duplicate of the archive copy.

## Solution

When salience scoring matches against archived items (embedding similarity, keyword match, explicit reference), the matched item is reactivated into short-term memory for one or more cycles. The original archive copy stays untouched.

## Consequences

**Benefits**

- Long-tail relevance does not require the agent to remember to remember.
- Mimics the rehearsal step of biological memory consolidation.

**Liabilities**

- False rehearsals waste working-memory slots.
- Operationally complex; requires content-addressable storage.

## What this pattern constrains

Archived items become readable only after rehearsal lifts them; direct cold reads are not part of the agent's primary path.

## Known uses

- **Sparrot** — *Available*. Stage P5+ rehearsal step.

## Related patterns

- *used-by* → [five-tier-memory-cascade](five-tier-memory-cascade.md)

## References

- (paper) *Memory consolidation through hippocampal-cortical replay (review)*, 2017

**Tags:** memory, rehearsal
