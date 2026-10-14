# Stop Hook

**Also known as:** Termination Predicate, Halt Condition, Stop Condition, Done Predicate, Exit Condition, Loop Termination Rule

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Define an explicit programmatic predicate that decides when the agent's loop should terminate.

## Context

A team is operating an agent loop where the agent repeatedly thinks, acts, observes, and decides whether to keep going. The loop needs an explicit stop condition that does not rely on the model itself declaring 'done', because in practice the model's own sense of completion is unreliable — it either stops too early on hard tasks or refuses to stop on easy ones.

## Problem

When termination is left implicit, with the loop ending only when the model says it is finished, the agent stalls in two opposite ways. On uncertain tasks the model will not commit to 'done' and keeps generating one more step indefinitely; on stuck tasks the model will keep trying variations of the same broken approach. Both burn budget and produce poor results. The team needs an explicit programmatic predicate — a stop hook — that decides termination from outside the model, based on observable signals such as goal completion, step count, repeated outputs, or detected errors.

## Forces

- Predicate complexity trades correctness for performance.
- Stop too early loses work; stop too late wastes calls.
- Coverage: which conditions warrant a stop?

## Therefore

Therefore: run a programmatic stop predicate after every step that returns continue, stop-success, or stop-failure on explicit conditions (target, budget, error, stagnation), so that termination is a tested decision rather than the model's opinion.

## Solution

Implement a stop hook function that runs after each step. It returns one of: continue, stop-success, stop-failure. Conditions include: target reached, step budget hit, error encountered, stagnation detected (no progress in last N steps).

## Structure

```
Agent step --> Stop hook predicate --target reached--> stop-success | --budget hit / error / stagnation--> stop-failure | --none--> continue --> next Agent step
```

## Diagram

```mermaid
flowchart TD
  Step[Agent step] --> Hook[Stop hook]
  Hook --> R{Predicate}
  R -->|target reached| OK[stop-success]
  R -->|step budget hit| Halt[stop-failure]
  R -->|error encountered| Halt
  R -->|stagnation detected| Halt
  R -->|none of the above| Cont[continue]
  Cont --> Step
```

## Example scenario

An agent's loop terminates when 'the model says it is done', which fails when the model is uncertain or stuck and the loop runs to budget. The team adds an explicit stop-hook predicate that runs after each step and returns continue, stop-success, or stop-failure based on target reached, step budget, error class, or stagnation detection. Termination becomes a programmatic decision rather than a wish, and unbounded loops become impossible by construction.

## Consequences

**Benefits**

- Explicit, testable termination logic.
- Independent from the model's self-assessment.

**Liabilities**

- More code to maintain than 'while not done'.
- Predicate bugs cause hangs or premature stops.

## Failure modes

- Premature stop — the stagnation check reads a slow but real step as no progress and ends a run that was about to succeed.
- Hang on predicate bug — a condition never evaluates true, so the hook keeps returning continue and the loop runs on.
- Success misread — the target-reached check matches a partial result, and the run reports stop-success on unfinished work.

## What this pattern constrains

The loop terminates exactly when the stop hook says so; no other code path may exit the loop.

## Applicability

**Use when**

- Agent loops need an explicit termination predicate beyond model self-declaration.
- Conditions like budget hit, error, or stagnation can be detected programmatically.
- Costs of an unbounded loop are unacceptable.

**Do not use when**

- The model reliably declares 'done' and termination already works.
- No programmatic stop condition can be defined for the task.
- The loop is naturally bounded by an external trigger.

## Components

- Stop-hook predicate — function returning continue, stop-success, or stop-failure each step
- Target detector — checks whether the goal has been met against an explicit criterion
- Stagnation detector — flags no-progress windows over the last N steps
- Error classifier — categorises step errors as transient or terminal for stop purposes

## Tools

- Loop-state tracker — records per-step outputs and progress signals the predicate consumes
- Goal-completion checker — task-specific oracle or rule comparing state against target

## Evaluation metrics

- Predicate accuracy — how often the predicate's verdict matched a reference human judgement
- Premature-stop rate — runs halted before the task was actually complete
- Late-stop rate — runs that continued past the point useful work stopped
- Hang incidents — runs where the predicate never returned a terminating verdict

## Known uses

- **Avramovic's catalog (Reliability & Control)** _available_

## Related patterns

- _specialises_ **Step Budget**
- _alternative-to_ **Unbounded Loop**
- _alternative-to_ **Infinite Debate**
- _complements_ **Kill Switch**
- _used-by_ **Chat Chain**

## References

- [zeljkoavramovic/agentic-design-patterns](https://github.com/zeljkoavramovic/agentic-design-patterns)
