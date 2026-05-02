# Replay / Time-Travel

**Also known as:** Trace Replay, Run Branching, Fork from Step N

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Re-run a past agent trace from any step with modified inputs/prompts/tools to debug or branch.

## Context

Agent debugging and experimentation; production incidents that need reproduction.

## Problem

Agent runs are non-deterministic and state-laden; without replay, debugging is reproduction-by-prayer.

## Forces

- Captured state must be complete enough to re-run.
- Storage of full traces is expensive.
- Modified replays diverge from original; comparison logic is non-trivial.


## Applicability

**Use when**

- Agent runs are non-deterministic and incidents need reproducible debugging.
- Engineers want to branch from a past step to test fixes or alternative prompts.
- Per-step inputs, outputs, and tool calls can be captured durably.

**Do not use when**

- Trace storage cost outweighs the value of replay (low-stakes ephemeral runs).
- Privacy or retention rules forbid keeping per-step traces.
- The agent has no externally observable failures worth reproducing.

## Solution

Capture per-step inputs, outputs, prompts, model id, tool calls. Provide a replay tool that loads a trace at step N and re-runs forward with optional modifications (different model, different prompt, different tool result). Store branches for comparison.

## Consequences

**Benefits**

- Debugging cycle drops from hours to minutes.
- A/B comparison of fixes becomes trivial.

**Liabilities**

- Trace storage overhead.
- Non-deterministic external dependencies (network) limit fidelity.

## What this pattern constrains

Replay reads from captured state; live model and tool calls happen only for the modified branch from step N forward.

## Known uses

- **LangSmith replay** — *Available*
- **Langfuse playground replay** — *Available*
- **Inspect AI** — *Available*
- **Claude Code conversation rewind** — *Available*. Transcript-level rewind, not full trace replay.
- **Braintrust playground** — *Available*

## Related patterns

- *uses* → [decision-log](decision-log.md)
- *complements* → [lineage-tracking](lineage-tracking.md)

## References

- (doc) *LangSmith: Replay*, <https://docs.smith.langchain.com/observability/how_to_guides/replay>

**Tags:** debug, replay, observability
