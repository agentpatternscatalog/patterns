# Tool Transition Fusion

**Also known as:** Tool Pair Fusion, Composite Tool Synthesis, Telemetry-Driven Tool Composition

**Category:** Tool Use & Environment  
**Status in practice:** experimental

## Intent

Mine tool-call telemetry for high-probability X-then-Y transitions and fuse those pairs into a single composite tool, shrinking the planner's step count.

## Context

An agent has been running long enough to accumulate substantial tool-call telemetry: which tool was called, then which tool followed, and how often. Each tool call is a model-decoding decision that can fail or cost tokens; the planner is also paying per-step latency.

## Problem

Many tool sequences are nearly deterministic. After a search, the agent almost always fetches one of the top results; after a database lookup, it almost always formats and writes a row. These transitions are paid for over and over: each step is a model call, each decision an opportunity for the planner to mis-pick. The agent's intermediate decoding errors and per-step latency dominate the trajectory cost even though the team could see, from the telemetry alone, that the transition was effectively fixed.

## Forces

- Frequent X-then-Y pairs are visible from logs but require periodic mining to detect.
- Fusing into a composite tool removes the per-step decoding decision and one step of latency.
- Over-fusion hides flexibility — sometimes the agent does need to deviate from the common path.
- Composite tool surface must stay legible to the planner and to humans reviewing traces.

## Therefore

Therefore: mine telemetry for tool transitions above a fixed probability threshold and fuse them into named composite tools, shrinking the planner's step count along the dominant trajectory.

## Solution

Sweep tool-call telemetry for transitions P(Y|X) above a threshold (e.g. 0.8). Wrap qualifying X-then-Y pairs in a composite tool whose signature is X's input and Y's output. Add the composite to the catalog; leave X and Y available for edge cases. Re-run the sweep periodically as task mix shifts. Document why each composite exists so a later reviewer understands the fusion was telemetry-driven, not author intuition.

## Structure

```
Tool-call telemetry --> Sweep P(Y|X) --(>= threshold)--> Compose X then Y into one tool --> Add to tool catalog --> Planner; --(< threshold)--> Keep X and Y separate
```

## Diagram

```mermaid
flowchart LR
  Tel[Tool-call telemetry] --> Sweep[Sweep P(Y|X)]
  Sweep --> Thr{>= threshold?}
  Thr -- yes --> Fuse[Compose X∘Y]
  Fuse --> Cat[Add to tool catalog]
  Cat --> Planner
  Thr -- no --> Keep[Keep X, Y separate]
```

## Example scenario

A code-review agent's telemetry shows that after `read_file(path)` it calls `parse_python(content)` on 94% of trajectories. The team adds a composite `read_and_parse(path)` tool; the planner now makes one call where it used to make two. End-to-end latency drops noticeably and a class of bug where the model occasionally called `parse_json` instead of `parse_python` disappears.

## Consequences

**Benefits**

- Cuts one step (and one decoding decision) per fused pair.
- Removes a recurring failure mode where the model picks the wrong follow-up.
- Reusing telemetry instead of author intuition keeps the catalog grounded.

**Liabilities**

- Composite tools hide the X/Y boundary from anyone reading a trace.
- Over-fusion entrenches the dominant path and slows divergence when task mix shifts.
- Threshold choice is a judgment call; too low fuses noise, too high yields nothing.

## Failure modes

- Noise fused — the threshold is set too low, a pair that only sometimes follows is merged, and the composite does the wrong second step on the other cases.
- Entrenched path — the task mix shifts but the sweep is not re-run, and the planner keeps reaching for a composite that no longer fits.
- Hidden boundary — a failure inside the composite shows up as one opaque call in the trace, and the reviewer cannot tell whether X or Y broke.
- Intuition fusion — a pair is fused because it looked obvious to an author, with no telemetry behind it, and the composite is rarely the right choice.

## What this pattern constrains

Tools must not be fused merely on author intuition; fusion is gated on observed transition probability above a documented threshold from real telemetry.

## Applicability

**Use when**

- Sufficient tool-call telemetry exists to estimate transition probabilities.
- Per-step latency or decoding-error rate is a measurable cost driver.
- A clear majority transition (>0.8 conditional probability) recurs across many sessions.

**Do not use when**

- Tool catalog churn is high; composites rot before they earn their keep.
- The X/Y pair is logically separable but operationally diverse — fusion hides legitimate branching.
- No telemetry exists; intuition-only fusion is forbidden by this pattern.

## Components

- Telemetry store — captures every tool call and its successor
- Transition mining job — computes P(Y|X) over the window and flags pairs above threshold
- Composite tool generator — wraps the X-then-Y pair as a single tool exposing X's input and Y's output
- Catalog updater — registers the composite and keeps X, Y available for edge cases

## Tools

- Tool-call log warehouse — durable store of every (tool, args, result) event
- Mining job runner — periodic batch computing transition probabilities
- Tool catalog registry — surface the agent loads each session

## Evaluation metrics

- Step reduction — average steps per task before vs after fusion.
- Composite hit rate — fraction of composite calls that follow the dominant path (should stay high).
- Divergence rate — fraction of tasks where the original X without Y still fires.

## Known uses

- **Production agents with periodic tool-catalog pruning from logs** _available_
- **[AI Engineering (Huyen) — agent-design discussion of transition mining](https://huyenchip.com/2025/01/07/agents.html)** _available_

## Related patterns

- _complements_ **Agent-Computer Interface**
- _complements_ **Agent Skills**
- _alternative-to_ **Compound Error Degradation** — Shrinking step count is one mitigation for multiplicative error.
- _complements_ **Tool Use**
- _composes-with_ **Hierarchical Tool Selection**

## References

- [Agents — Chip Huyen](https://huyenchip.com/2025/01/07/agents.html) — Chip Huyen, 2025
