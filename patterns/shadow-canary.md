# Shadow Canary

**Also known as:** Shadow Agent, Canary Deployment

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Run a candidate agent version in shadow alongside the champion, comparing outputs without affecting users.

## Context

Agent changes are non-deterministic and prompt-sensitive; CI tests cover correctness, not field behaviour.

## Problem

Releases without field comparison miss regressions visible only on real traffic.

## Forces

- Shadow runs cost money for output never shown.
- Comparison logic for free-form outputs is non-trivial.
- Shadow latency must not affect the user-visible path.

## Solution

Route a fraction of real traffic through both champion and challenger. Champion's output reaches the user. Challenger's output is logged. Diff the outputs on agreed metrics (judge model, exact match on tool calls, latency, cost). Promote on lift; revert on regression.

## Consequences

**Benefits**

- Field-quality regression detection.
- Confidence to roll out non-deterministic changes.

**Liabilities**

- 2x cost during shadow window.
- Diff-noise on free-form outputs is hard to attribute.

## What this pattern constrains

Challenger output is not user-visible during shadow; only logging.

## Known uses

- **Standard practice in ML/agent platforms** — *Available*

## Related patterns

- *complements* → [eval-harness](eval-harness.md)
- *uses* → [llm-as-judge](llm-as-judge.md)
- *alternative-to* → [perma-beta](perma-beta.md)
- *complements* → [eval-as-contract](eval-as-contract.md)
- *complements* → [prompt-versioning](prompt-versioning.md)

**Tags:** governance, shadow, release
