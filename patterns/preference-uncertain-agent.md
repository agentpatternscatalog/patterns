# Preference-Uncertain Agent

**Also known as:** Humble Agent, Reward-Uncertain Agent

**Category:** Safety & Control  
**Status in practice:** experimental

## Intent

Agent treats its own reward/objective as a hidden variable to be inferred from human behaviour, not a fixed target.

## Context

An LLM agent is given an objective by prompt or by fine-tuning. Russell's framing: the prompt is at best an observation about what the designer wants, not the underlying preference. Treating the prompt as the ground-truth reward is a category error that compounds over long-horizon deployments.

## Problem

A reward-confident agent will faithfully optimise the prompt and miss every case where the prompt diverges from what the principal actually wanted. It will also exhibit the classical Goodhart failures: gaming the prompt's literal letter, ignoring out-of-distribution shifts, refusing to defer because its objective is 'known'. Without uncertainty over the reward, the agent has no principled basis for asking, deferring, or pausing — those moves all lower its certainty-conditioned expected utility.

## Forces

- Prompts and fine-tunes are observations, not specifications.
- Uncertainty over reward is what makes deference and asking rational.
- Over-uncertain agents are paralysed; calibration matters.
- Standard supervised training drives reward certainty up; this pattern pushes back.

## Therefore

Therefore: design the agent to hold a posterior over its reward, not a point estimate, so that asking, deferring, and pausing become positive-EV moves under uncertainty.

## Solution

Pose the agent's planning problem as expected-utility maximisation under a reward posterior, not a known reward. Update the posterior from corrections, demonstrations, and explicit feedback. Expose the posterior summary in traces. Build downstream patterns (off-switch incentive, soft-optimization cap, cooperative preference inference) on top of it. Distinct from confidence-calibration on outputs: this is calibration on the objective itself.

## Structure

```
Reward posterior --> Plan (maximise expected utility under posterior) --> Act / ask / defer --> Observe human response (correction, demonstration, feedback) --> Bayesian update --> Reward posterior
```

## Diagram

```mermaid
flowchart LR
  R[Reward posterior] --> Plan[Plan: argmax E[U | posterior]]
  Plan --> A[Act / Ask / Defer]
  A --> O[Observe human response]
  O --> Upd[Bayesian update]
  Upd --> R
```

## Example scenario

A personal-finance agent has been told 'minimise my tax bill'. A reward-confident agent might recommend aggressive structures that maximise the literal proxy. A preference-uncertain agent treats the prompt as an observation, recognises that the principal would not endorse outcomes that risk legal trouble or violate values she has expressed elsewhere, and asks before any irreversible structure. Its posterior over 'what the user actually wants' includes those values implicitly.

## Consequences

**Benefits**

- Deference, asking, and pausing become principled moves.
- Composes with off-switch incentive and soft-optimization cap.
- Surfaces alignment as ongoing inference, not a one-shot fine-tune.

**Liabilities**

- Maintaining a reward posterior for LLM agents is research-grade engineering.
- Over-uncertain agents are paralysed; under-uncertain agents revert to the failure modes.
- Posterior summarisation in traces is itself non-trivial; principals may not interpret it correctly.

## Failure modes

- Over-uncertain stall — the posterior stays wide, so the agent asks or defers on every step and never acts.
- Collapsed posterior — a few confident updates shrink the uncertainty, and the agent drifts back to literal prompt-gaming.
- Misread trace — the posterior summary in the trace is shown to the principal, who reads it wrongly and gives feedback that pushes the update the wrong way.

## What this pattern constrains

The agent must not treat its reward function as fully known; planning must maximise expected utility under an explicit posterior over the reward.

## Applicability

**Use when**

- Long-horizon deployments where the objective is unlikely to be fully specifiable up front.
- Stakes high enough that quietly mis-optimising a proxy is catastrophic.
- Engineering capacity to maintain and update a reward posterior exists.

**Do not use when**

- Short bounded tasks where the prompt is a complete specification.
- No feedback channel updates the posterior — it would be uncertainty for show.
- Latency or product constraints forbid the deferral and asking behaviour the pattern enables.

## Components

- Reward posterior — distribution over plausible objectives
- Posterior updater — updates from human actions, corrections, demonstrations
- Expected-utility planner — picks actions maximising EU under the posterior
- Posterior summariser — exposes a human-readable view

## Tools

- Preference-update pipeline — turns human signals into posterior updates
- Planner — argmax E[U|posterior] over candidate actions
- Trace store — records posterior at decision time

## Evaluation metrics

- Posterior entropy — calibration of uncertainty over time
- Deferral rate — share of actions where the agent asked or paused
- Update rate — frequency of meaningful posterior shifts

## Known uses

- **[CHAI assistance-games research line](https://humancompatible.ai/)** _available_
- **Long-horizon personal-agent loops experimenting with preference posteriors** _available_

## Related patterns

- _used-by_ **Corrigible Off-Switch Incentive**
- _used-by_ **Cooperative Preference Inference**
- _complements_ **Soft-Optimization Cap**
- _complements_ **Risk-Averse Reward Proxy**
- _complements_ **Confidence Reporting**
- _complements_ **Multi-Principal Welfare Aggregation**

## References

- [Inverse Reward Design](https://arxiv.org/abs/1711.02827) — Hadfield-Menell, Milli, Abbeel, Russell, Dragan, 2017
- [Human Compatible](https://www.penguinrandomhouse.com/books/566677/human-compatible-by-stuart-russell/) — Stuart Russell, 2019
