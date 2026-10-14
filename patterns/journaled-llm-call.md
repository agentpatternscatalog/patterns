# Journaled LLM Call

**Category:** Governance & Observability  
**Status in practice:** emerging

## Intent

Record the output of every non-deterministic step on first execution and replay that recorded value during crash-recovery instead of re-invoking the model.

## Context

A team runs an agent on a durable-execution engine that survives crashes by replaying the workflow from a recorded history. The workflow drives non-deterministic steps: LLM calls, tool results, timestamps, and random draws. The engine reconstructs in-memory state after a restart by re-running the workflow code up to the point it died, then resuming. For that reconstruction to be correct, every step the workflow code re-executes during replay must yield the same value it produced on the original run.

## Problem

An LLM call is not a pure function: the same prompt returns a different completion on the next invocation, and a timestamp or random draw changes every time. If the durable engine re-invokes the model during replay, the recovered run diverges from the original — a tool gets called with arguments the first run never produced, a branch is taken that never happened, and the workflow history no longer matches reality. This replay divergence corrupts state silently and is hard to detect, because each individual call looks valid. Re-invoking also pays the model cost and latency a second time for work that already completed.

## Forces

- Replay correctness demands that re-executed steps return identical values, but model calls are non-deterministic by construction.
- A recorded LLM response may be stale relative to the world, yet a fresh response breaks determinism.
- Re-invoking the model on every recovery doubles token cost and latency for work already done.
- Journaling adds storage and a write on the hot path of each non-deterministic step.

## Therefore

Therefore: wrap each non-deterministic step as a recorded side-effect — execute it once, persist its output to the workflow journal, and on every subsequent replay return the journaled value without calling the model, clock, or RNG again.

## Solution

Classify every step as deterministic workflow logic or non-deterministic effect. Run each effect — LLM call, tool invocation, timestamp read, random draw — exactly once and append its result to an append-only journal keyed by step position. On crash-recovery the engine replays the workflow code from the start; deterministic logic recomputes freely, but each effect call short-circuits to its journaled output instead of re-invoking the underlying resource. The model is queried only the first time a given step is reached; thereafter the recorded response stands in for it. This trades a possibly-stale recorded answer for deterministic, fault-tolerant replay and avoids paying the call cost twice.

## Structure

```
Non-deterministic step (LLM call / tool / time / random) --> Effect wrapper --> Journal entry for this step? --no, first run--> Invoke resource --> Append output to step-keyed journal --> Use output / --yes, replay--> Read journaled output --> Use output --> Deterministic workflow logic --> Next step
```

## Diagram

```mermaid
flowchart TD
  Step[Non-deterministic step<br/>LLM / tool / time / random] --> Q{Journal entry<br/>for this step?}
  Q -- No, first run --> Inv[Invoke model/resource] --> Rec[Append output to journal] --> Use[Use output]
  Q -- Yes, replay --> Read[Read journaled output] --> Use
  Use --> Det[Deterministic workflow logic] --> Next[Next step]
```

## Example scenario

A durable research agent calls an LLM to pick a search query, runs the search as a tool, then summarises. The worker crashes after the summary tool call but before persisting the next step. On recovery the engine replays the workflow: without journaling it would re-prompt the model, get a different query, and summarise the wrong results. With journaled calls the engine returns the original query and search result from the journal, recomputes only the deterministic control flow, and resumes exactly where it left off.

## Consequences

**Benefits**

- Replay is deterministic: recovered runs follow the identical path the original took.
- Each model call is paid for once; recovery reuses the recorded output instead of re-billing.
- The journal doubles as an audit trail of every non-deterministic decision the workflow made.

**Liabilities**

- A journaled response can be stale: replay reuses a value the world has since changed.
- Forgetting to wrap one non-deterministic step reintroduces divergence that is hard to spot.
- The append-only journal grows with every effect and must be stored and garbage-collected.
- Changing workflow code between original run and replay can invalidate journaled step positions.

## Failure modes

- Unwrapped effect — one timestamp read or random draw is left outside the effect wrapper, and replay takes a different branch from the original run.
- Stale replayed answer — recovery reuses a journaled model response about data that has since changed, and the workflow acts on it.
- Shifted step positions — the workflow code changes between run and replay, journal keys no longer line up with steps, and the wrong output is fed to a step.
- Unbounded journal — every effect is appended and nothing is garbage-collected, so journal storage grows with every long-running workflow.

## What this pattern constrains

On replay the workflow must not re-invoke the model, clock, or RNG; the journaled output is replayed in place of a fresh call.

## Applicability

**Use when**

- The agent runs on a durable-execution engine that recovers by replaying workflow code from a recorded history.
- The workflow contains non-deterministic steps — LLM calls, tool results, timestamps, or random draws.
- A recovered run must follow the same path the original took, and re-invoking the model on recovery is unacceptable on cost or correctness grounds.

**Do not use when**

- The agent keeps no durable history and simply restarts from scratch on failure.
- Every step is already deterministic and pure, so replay is naturally faithful.
- Replay deliberately wants fresh model outputs, as in trace re-runs with modified inputs.

## Components

- Effect Wrapper — marks an LLM call, tool, timestamp, or RNG draw as a recorded side-effect rather than inline workflow logic
- Step-Keyed Journal — append-only log mapping each step position to the output produced on first execution
- Replay Resolver — on recovery, intercepts each effect call and returns the journaled value instead of invoking the resource
- Determinism Checker — flags workflow-code changes or unwrapped non-determinism that would break replay
- Journal Store — durable backend (event history, database, or log) that persists and garbage-collects entries

## Tools

- Temporal — durable-execution engine that records Activity results in event history and replays them
- DBOS — checkpoints step outputs to a database and returns the checkpoint instead of re-executing on recovery
- Restate — durable execution runtime that journals handler results for deterministic replay

## Evaluation metrics

- Replay divergence incidents — recovered runs whose path differed from the original per million recoveries
- Journal hit rate on replay — share of effect calls served from the journal versus re-invoked
- Recovery model-cost saved — token/latency cost avoided by replaying recorded outputs instead of re-calling
- Unwrapped-non-determinism findings — steps the determinism checker flags as not journaled
- Journal storage growth — bytes of journal written per workflow run

## Known uses

- **[Temporal](https://docs.temporal.io/workflow-definition)** _available_ — Non-deterministic work runs in Activities whose results are written to event history and reused when the workflow replays.
- **[Restate](https://www.restate.dev/blog/resilient-serverless-agents)** _available_
- **[DBOS](https://docs.dbos.dev/architecture)** _available_ — Step outputs are checkpointed to a database; on recovery a step with a checkpoint returns the recorded output instead of executing.
- **[Inngest](https://www.inngest.com/uses/durable-workflows)** _available_
- **[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)** _available_

## Related patterns

- _complements_ **Durable Workflow Snapshot**
- _complements_ **Agent Resumption**
- _alternative-to_ **Replay / Time-Travel**
- _complements_ **Determinism-Tiered Replay Gate** — Journaling records each non-deterministic step so a run can be replayed at all; this pattern measures whether such replays converge and gates deployment on the result.
- _complements_ **Replay Divergence** — Journaled-llm-call is the remedy for the crash-recovery case — record the output and replay it instead of re-invoking; this anti-pattern names the broader hazard, including model-version re-derivation that journaling deliberately cannot fix.
- _complements_ **As-Of Information-Set Pinning** — Journaling replays one recorded model output for crash recovery and says nothing about the corpus or reference data the call read; pinning fixes that surrounding input set.
- _complements_ **Harness-Native Rollout Capture** — Both record model calls at the same boundary, but the journal exists so a durable workflow can resume without re-invoking the model, while this record exists so a trainer can compute a gradient over the exact tokens.

## References

- [Agent Workflows Are Rediscovering Durable Execution](https://nittikkin.medium.com/agent-workflows-are-rediscovering-durable-execution-be110661ed8c)
- [Trustworthy AI Agents: Deterministic Replay](https://www.sakurasky.com/blog/missing-primitives-for-trustworthy-ai-part-8/)
- [Temporal: Workflow Definition and Determinism](https://docs.temporal.io/workflow-definition)
- [DBOS Architecture: Steps and Checkpointing](https://docs.dbos.dev/architecture)
