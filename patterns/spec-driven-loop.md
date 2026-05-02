# Spec-Driven Loop

**Also known as:** Naive Iterative Loop, Ralph Wiggum Loop, Ralph Loop

**Category:** Planning & Control Flow  
**Status in practice:** emerging

## Intent

Run the same prompt against a fixed spec in a deterministic outer loop until the spec is satisfied.

## Context

A greenfield task with a clear (or improvable) specification where each iteration can improve the codebase incrementally.

## Problem

Agents that try to plan an entire feature in one go are brittle; agents that wander without a spec drift.

## Forces

- The spec must be good or the loop polishes the wrong artefact.
- Tests gate progress; without them the loop has no error signal.
- Cost per iteration must be tolerable for hundreds of runs.


## Applicability

**Use when**

- A task has a clear (or improvable) spec and incremental iteration adds value.
- Each iteration's output can be gated by a test or check.
- An outer shell loop can run the same prompt repeatedly without supervision.

**Do not use when**

- The task has no spec and cannot be incrementally improved.
- There is no test gate and the loop cannot tell when to stop.
- Unsupervised loops would consume cost without convergence.

## Solution

An outer shell loop (`while :; do cat PROMPT.md | claude-code ; done`) runs the same prompt repeatedly. The prompt encodes one task at a time, references a fix_plan.md that the agent itself updates, and ends with a test invocation that gates the next iteration. Subagents are used for parallel reads; build/test stays serial.

## Example scenario

A team is fixing a long-tail bug list across a large repo. A free-form chat session wanders, plans become stale, and progress is hard to measure. They write a deterministic outer loop (`while :; do cat PROMPT.md | claude-code; done`) where the prompt names one task, references a fix_plan.md the agent itself updates, and exits when the spec is satisfied. Progress becomes legible: tasks tick off, the loop terminates, and resuming after interruption is a no-op.


## Diagram

```mermaid
flowchart TD
  Start[Outer shell loop] --> Read[Read PROMPT.md + fix_plan.md]
  Read --> Run[Run agent on one task]
  Run --> Edit[Agent updates fix_plan.md]
  Edit --> Test[Run test suite]
  Test --> Gate{Spec satisfied?}
  Gate -- no --> Start
  Gate -- yes --> Done[Exit loop]
```

## Consequences

**Benefits**

- Brutally simple. No orchestration framework required.
- Self-improving in practice: the agent updates the spec as it learns.

**Liabilities**

- Easy to burn tokens on the wrong shape.
- Hard to share state between iterations beyond what the agent writes to disk.

## What this pattern constrains

Each loop iteration is constrained by the spec and the test gate; the agent cannot expand scope without editing the spec first.

## Known uses

- **[Geoffrey Huntley's Ralph](https://ghuntley.com/ralph/)** — *Available*. The canonical write-up.

## Related patterns

- *uses* → [spec-first-agent](spec-first-agent.md)
- *complements* → [step-budget](step-budget.md)
- *alternative-to* → [scheduled-agent](scheduled-agent.md)

## References

- (blog) Geoffrey Huntley, *Ralph Wiggum as a 'software engineer'*, 2025, <https://ghuntley.com/ralph/>

**Tags:** loop, spec, iterative
