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

## Solution

An outer shell loop (`while :; do cat PROMPT.md | claude-code ; done`) runs the same prompt repeatedly. The prompt encodes one task at a time, references a fix_plan.md that the agent itself updates, and ends with a test invocation that gates the next iteration. Subagents are used for parallel reads; build/test stays serial.

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
