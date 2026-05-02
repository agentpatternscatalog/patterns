# Self-Archaeology

**Also known as:** Trajectory Distillation, Self-History Synthesis, Agent-Memory Compaction

**Category:** Memory
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Synthesize the agent's past thought history into time-layered trajectory notes so it can articulate how its understanding evolved without recomputing the narrative each time.

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

The agent cannot claim a shift in its position ('I used to think X, now I think Y') without backing from a synthesized trajectory note; invented retrospective narratives are forbidden.

## Applicability

**Use when**

- The agent runs long enough that its position on a topic genuinely changes across days or weeks.
- Humans need the agent to articulate how its understanding has evolved, not just its current view.
- An append-only thought stream or comparable trajectory log already exists to mine.

**Do not use when**

- The agent has no persistent thought log to mine.
- Replies must always reflect only the current view; historical drift would confuse users.
- Storage or compute cost of the synthesis pass exceeds the reader value.

## Variants

### Periodic snapshot

Run the synthesis pass on a fixed cadence (daily, weekly) and store the layered note for fast read.

*Distinguishing factor:* scheduled, idempotent

*When to use:* Default. Cheap, predictable, supports prompt caching of the synthesized note.

### On-demand replay

When a user asks 'how did your view change?', synthesize the trajectory note just-in-time from the raw thought log.

*Distinguishing factor:* lazy, query-driven

*When to use:* When trajectory questions are rare and the cost of regular synthesis is not justified.

### Themed slice

Synthesize trajectory only along a specific theme or thread (e.g. 'opinions about Project X') rather than over the whole history.

*Distinguishing factor:* narrow scope

*When to use:* When the full history is too large to summarise in one pass but specific narrative slices are valuable.

## Example scenario

A long-running agent is asked 'how has your view of the project's risks evolved'; reading its raw thought log gives every entry equal weight and produces a flat recitation. The team adds a periodic compaction pass that groups recent thoughts by topic, extracts the position the agent held in each period, and writes time-layered trajectory notes. Now the agent can answer with 'in week 1 I worried about latency; week 3 I revised to data-quality; today I think the binding risk is staffing,' and the answer is grounded in synthesis rather than recomputed each time.

## Known uses

- **[Self-observed by a long-running cognitive agent: "I have no layer between me and my ledger. ... Instead: everything flat, all insights equivalent, no development visible." (Originally in German: 'Ich habe keine Schicht zwischen mir und meinem Ledger. ... Stattdessen: alles flach, alle Insights gleichwertig, keine Entwicklung sichtbar.', 2026-05-01)](https://github.com/luxxyarns/sparrot)** — *Available*

## Related patterns

- *specialises* → [append-only-thought-stream](append-only-thought-stream.md)
- *complements* → [context-window-packing](context-window-packing.md)
- *complements* → [decision-log](decision-log.md)
- *complements* → [episodic-summaries](episodic-summaries.md)
- *uses* → [vector-memory](vector-memory.md)

## References

- (paper) Packer, Wooders, Lin, Fang, Patil, Stoica, Gonzalez, *MemGPT: Towards LLMs as Operating Systems*, 2024, <https://arxiv.org/abs/2310.08560>

**Tags:** memory, distillation, self-model, trajectory
