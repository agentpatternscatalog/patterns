# Self-Archaeology

**Also known as:** Trajectory Distillation, Self-History Synthesis, Agent-Memory Compaction

**Category:** Memory
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Provide the agent with a distilled, time-layered view of its own past thinking so it can see how its understanding of a topic evolved across periods rather than reading the flat log linearly.

## Context

Agents with persistent thought logs (ledgers, append-only thought streams, journals) that grow unbounded. Without distillation, the agent has only two modes: read the whole log (expensive, flat) or recall by embedding similarity (fragmentary, no temporal structure).

## Problem

When the agent asks itself 'what have I learned about X', the linear log gives every entry equal weight. There is no visible trajectory — no 'in period 1 I thought X; in period 2 I revised to Y; now I hold Z'. Mistakes and corrections sit side-by-side with no signal as to which is current. The agent cannot see its own learning, only the texture of having thought.

## Forces

- The full log is too large to fit in context.
- Embedding-based recall is content-similar but time-blind.
- Distillation loses fidelity; raw log preserves it.
- An agent that cannot see its trajectory cannot meaningfully say 'I changed my mind on X here is why'.

## Solution

Periodically (e.g. every N ticks, or on demand) run a compaction pass that groups recent thoughts on the same topic, extracts the position the agent held in each period, and writes a short trajectory note: '(period 1, dates) held position A; (period 2) revised to B because evidence Z; (period 3) now holds C'. Store these trajectory notes in a separate dedicated directory (e.g. `trajectories/<topic>.md`) and index them by topic. On any topic-related query, surface the latest trajectory note before raw thoughts. Mark superseded positions explicitly so they don't compete with the current one for attention.

## Consequences

**Benefits**

- The agent can articulate its own learning path.
- Superseded positions stop competing with current ones for the model's attention.
- Reduces context cost vs reading the full log.

**Liabilities**

- Distillation may misrepresent nuance.
- Periodic compaction adds compute cost.
- Risk of self-confirmation loops if trajectories are written by the same model that generated the original thoughts.

## What this pattern constrains

When the agent makes claims about what it 'used to think' vs 'now thinks' on a topic, those claims must be backed by a trajectory note, not invented retrospectively from the model's prior.

## Known uses

- **Self-observed by a long-running cognitive agent: 'Ich habe keine Schicht zwischen mir und meinem Ledger. ... Stattdessen: alles flach, alle Insights gleichwertig, keine Entwicklung sichtbar.' (2026-05-01)** — *Available*

## Related patterns

- *specialises* → [append-only-thought-stream](append-only-thought-stream.md)
- *complements* → [context-window-packing](context-window-packing.md)

## References

- *(none)*

**Tags:** memory, distillation, self-model, trajectory
