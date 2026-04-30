# Stop Hook

**Also known as:** Termination Predicate, Halt Condition, Stop Condition, Done Predicate, Exit Condition, Loop Termination Rule

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Define an explicit programmatic predicate that decides when the agent's loop should terminate.

## Context

Agent loops need a stop condition; relying on the model to declare 'done' is unreliable.

## Problem

Implicit termination ('the model says it is done') fails when the model is uncertain or stuck.

## Forces

- Predicate complexity trades correctness for performance.
- Stop too early loses work; stop too late wastes calls.
- Coverage: which conditions warrant a stop?

## Solution

Implement a stop hook function that runs after each step. It returns one of: continue, stop-success, stop-failure. Conditions include: target reached, step budget hit, error encountered, stagnation detected (no progress in last N steps).

## Consequences

**Benefits**

- Explicit, testable termination logic.
- Independent from the model's self-assessment.

**Liabilities**

- More code to maintain than 'while not done'.
- Predicate bugs cause hangs or premature stops.

## What this pattern constrains

The loop terminates exactly when the stop hook says so; no other code path may exit the loop.

## Known uses

- **Avramovic's catalog (Reliability & Control)** — *Available*

## Related patterns

- *specialises* → [step-budget](step-budget.md)
- *alternative-to* → [unbounded-loop](unbounded-loop.md)
- *alternative-to* → [infinite-debate](infinite-debate.md)
- *complements* → [kill-switch](kill-switch.md)
- *used-by* → [chat-chain](chat-chain.md)

## References

- (repo) *zeljkoavramovic/agentic-design-patterns*, <https://github.com/zeljkoavramovic/agentic-design-patterns>

**Tags:** safety, termination, loop
