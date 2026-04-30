# Unbounded Loop

**Also known as:** No Step Cap, Open-Ended Agent, Agent Stuck, Loops Forever

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: run the agent loop without a step budget and let model self-termination decide.

## Context

An agent is implemented as 'while not done' where 'done' is whatever the model says. The model rarely says done.

## Problem

The agent wanders, retries, or loops on errors. Cost is unbounded. User waits.

## Forces

- Caps cut off legitimate work.
- Choosing the cap is empirical.
- Model self-termination feels natural until it fails.

## Solution

Don't. Set max_steps. Add a stop hook. See step-budget, the-stop-hook.

## Consequences

**Liabilities**

- Cost blow-up.
- Silent quality regressions when models drift.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Early autonomous-agent demos (AutoGPT, BabyAGI initial versions)** — *Available*

## Related patterns

- *alternative-to* → [step-budget](step-budget.md)
- *alternative-to* → [stop-hook](stop-hook.md)

**Tags:** anti-pattern, loop, budget
