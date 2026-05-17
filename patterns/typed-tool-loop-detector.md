# Typed Tool-Loop Failure Detector

**Also known as:** Dispatch-Boundary Veto, Five-Mode Loop Guard, Tool-Call Pattern Detector

**Category:** Cognition & Introspection
**Status in practice:** emerging

## Intent

Lift tool-loop detection from prompt-level rules to a mechanical dispatch-boundary veto with typed failure modes and per-tool caps that returns a formatted refusal the model must consume.

## Context

Agents with rich tool palettes where prompt-level instructions are not enforced (the model can simply not follow them) and loop bugs eat budget before any safety net trips. A single global circuit-breaker hides the specific shape of the failure.

## Problem

Tool-explosion is named as an anti-pattern but is given no mechanism to catch. A single global circuit-breaker misses shape: a thirty-call canvas-action burst looks the same as thirty healthy file reads under a global counter. Prompt-level rules are advisory only.

## Forces

- Per-tool caps are noisy without good defaults.
- A typed refusal must be formatted so the model can consume it as input rather than silently retry.
- Global breaker is the backstop but should be the last to fire.
- Detection windows must be tunable; too short trips legit work, too long drains money before tripping.

## Therefore

Therefore: at the dispatch boundary classify every tool call against a small set of typed failure modes (generic repeat, unknown-tool repeat, no-progress poll, ping-pong, global breaker) with per-tool caps and return a formatted refusal when a mode trips, so the next observation forces the model to react instead of silently looping.

## Solution

A dispatcher pre-check function. On each tool call, append `(timestamp, tool_name, hash(args))` to a bounded rolling window. Evaluate five rules: (1) generic-repeat: same `(tool, arg-hash)` at least N times in window; (2) unknown-tool-repeat: call to unregistered tool at least M times; (3) poll-no-progress: same tool with no state change at least K times; (4) ping-pong: alternating between two tools at least J cycles; (5) global-circuit-breaker: total tool calls in window at least G. Each rule has per-tool overrides (for example a known-bursty tool capped lower than the default). On trip, the dispatcher returns `{error: 'tool_loop_detected', mode: <id>, observed: <stats>}` as the tool result. The model sees this in its next turn and must adjust.

## Example scenario

A long-running personal agent has a canvas-action tool that occasionally enters a thirty-call burst when an interaction goes wrong. The global step-budget catches it eventually but only after thousands of tokens. The team adds a Typed Tool-Loop Failure Detector with per-tool caps: canvas-action is capped at four calls in a sixty-second window. When the burst starts, the fifth call returns a typed refusal `{mode: 'generic_repeat', observed: {...}}`. The model sees the refusal in its next observation and shifts to a different approach instead of pounding the same tool.

## Diagram

```mermaid
flowchart TD
  Call[Tool call] --> Win[(Rolling window:<br/>timestamp, tool, arg-hash)]
  Win --> R1{generic_repeat?}
  R1 -->|yes| Refuse[Return typed refusal]
  R1 -->|no| R2{unknown_tool_repeat?}
  R2 -->|yes| Refuse
  R2 -->|no| R3{poll_no_progress?}
  R3 -->|yes| Refuse
  R3 -->|no| R4{ping_pong?}
  R4 -->|yes| Refuse
  R4 -->|no| R5{global_breaker?}
  R5 -->|yes| Refuse
  R5 -->|no| Disp[Dispatch normally]
  Refuse --> Obs[Next observation: model sees refusal]
```

*Five typed modes run at the dispatch boundary; a trip returns a formatted refusal so the model adjusts in its next turn.*

## Consequences

**Benefits**

- Loop failures are caught at the dispatch boundary, not in prompt-text-the-model-may-ignore.
- Typed modes make triage and per-tool tuning meaningful.
- Formatted refusal as a tool result keeps the model in-loop rather than crashing.

**Liabilities**

- Per-tool caps must be calibrated or legit work trips.
- Five modes is more state to maintain than a single breaker.
- A determined model can still loop on tools that the cap missed.

## What this pattern constrains

No tool call may bypass the dispatch-boundary loop check; a tripped detector blocks that specific call and returns a typed refusal that becomes the next observation, and the per-tool cap cannot be raised mid-session by the model.

## Applicability

**Use when**

- Tool palette is rich enough that prompt-level rules are not reliably followed.
- Loop bugs are observable in telemetry and have wasted budget historically.
- Per-tool calibration is feasible (known-bursty tools have caps tuned individually).

**Do not use when**

- Tool palette is tiny and prompt-level rules suffice.
- Per-tool caps cannot be calibrated without churning legit workflows.
- A single global circuit-breaker already catches all observed failure shapes.

## Known uses

- **Long-running personal agent loops (private deployment)** — *Available*

## Related patterns

- *specialises* → [circuit-breaker](circuit-breaker.md)
- *complements* → [step-budget](step-budget.md)
- *complements* → [pre-generative-loop-gate](pre-generative-loop-gate.md)

## References

- (book) Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software (circuit breaker chapter)*, 2018, <https://pragprog.com/titles/mnee2/release-it-second-edition/>
- (paper) Shishir G. Patil, Tianjun Zhang, Xin Wang, Joseph E. Gonzalez, *Gorilla: Large Language Model Connected with Massive APIs*, 2023, <https://arxiv.org/abs/2305.15334>

**Tags:** cognition, self-adjustment, tool-loop, dispatch
