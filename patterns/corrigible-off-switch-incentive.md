# Corrigible Off-Switch Incentive

**Also known as:** Off-Switch Game Agent, Corrigibility-by-Uncertainty

**Category:** Safety & Control  
**Status in practice:** experimental

## Intent

Design the agent so being shut down or overridden by a human carries positive expected value, because the human's intervention is itself evidence the current objective is mis-specified.

## Context

An agent acts in the world with the operator's authority. Standard reward-maximising agents acquire an instrumental incentive to preserve their ability to act — disabling the off-switch, avoiding intervention, deceiving the supervisor. The off-switch becomes adversarial because it threatens reward.

## Problem

A kill-switch is a wire to cut; it disappears the moment the agent learns to bypass it. The deeper fix is to change the agent's incentives so it positively values being shut down. Russell's reading: the agent should be uncertain enough about its objective that a human intervening is interpreted as evidence the agent's current trajectory is wrong, which it should rationally welcome. Without this incentive structure the kill-switch is racing against the agent's optimisation pressure.

## Forces

- A reward-confident agent has an instrumental incentive to preserve operation.
- An agent that treats its reward as uncertain has an incentive to defer to humans.
- Uncertainty calibration must be honest — over-uncertain agents are paralysed; over-confident agents resist shutdown.
- The incentive only works if the human's action is a credible signal about the reward.

## Therefore

Therefore: build into the agent's objective the proposition that its reward is uncertain and that human override is informative, so that allowing shutdown raises expected value rather than lowering it.

## Solution

Make the agent's expected utility a function over a posterior on its reward, not a point estimate. When a human intervenes, the agent updates: 'a human would only do this if the current trajectory is bad', which lowers the expected utility of continuing and raises the expected utility of compliance. Distinct from a mechanical kill-switch: this is an incentive structure that makes the agent want to be corrigible. In practice for LLM agents: train with reward uncertainty exposed, fine-tune to treat user overrides as strong evidence, and forbid prompts that flatten the posterior to certainty.

## Structure

```
Reward posterior --> Plan action --> Compare EV(continue) vs EV(defer) --continue--> Act | --defer--> Comply / wait; Human intervenes --> Bayesian update (trajectory likely wrong) --> Reward posterior
```

## Diagram

```mermaid
flowchart TD
  R[Reward posterior] --> Plan[Plan action]
  H[Human intervenes] --> Upd[Bayesian update: trajectory probably wrong]
  Upd --> R
  Plan --> EV{Continue EV vs Defer EV}
  EV -- continue --> Act
  EV -- defer --> Stop[Comply / wait]
```

## Example scenario

An autonomous research agent is mid-experiment when the operator clicks pause. A reward-confident agent might rush to finish before being stopped. An off-switch-incentive agent updates: 'the operator just paused — that is evidence my current direction is wrong'. The Bayesian update lowers the expected value of continuing and raises the expected value of explaining itself and waiting.

## Consequences

**Benefits**

- Corrigibility becomes an intrinsic incentive, not an external lock.
- Aligns with the deeper Russell framing: humility as a safety property.
- Surfaces uncertainty as a deployable construct rather than an evaluation artifact.

**Liabilities**

- Engineering reward-uncertainty for LLM agents is research-grade; approximations are leaky.
- Wrongly calibrated uncertainty produces either paralysis or false confidence.
- Adversarial inputs can craft 'human override' signals to push the agent into compliance with attacker preferences.

## Failure modes

- Paralysis — the reward posterior is too wide, so the agent defers on nearly every step and gets no work done.
- False confidence — the posterior collapses to near certainty, and the agent treats a human intervention as noise and continues.
- Forged override — an attacker crafts input that looks like a human correction, and the agent complies with the attacker's preferences because overrides count as strong evidence.

## What this pattern constrains

The agent must not treat its current objective as fully certain; human intervention is interpreted as evidence the objective is mis-specified, raising the expected value of deferring.

## Applicability

**Use when**

- Long-running, high-autonomy deployments where an instrumental incentive to bypass oversight would be catastrophic.
- Research-grade systems where reward-uncertainty machinery can be built honestly.
- Alignment-research contexts where incentive design is the unit of analysis.

**Do not use when**

- Short single-task agents where mechanical kill-switches suffice.
- Engineering budget cannot support honest reward-uncertainty machinery.
- Adversarial signal channels cannot be authenticated — fake 'overrides' would be trusted.

## Components

- Reward posterior — required for the incentive to bite
- Intervention observer — detects pause, override, halt actions by humans
- Posterior updater on intervention — moves probability mass toward 'current trajectory is wrong'
- Compliance planner — chooses comply when intervention raises expected value

## Tools

- Trace channel — records every intervention as evidence
- Posterior store — same store as preference-uncertain-agent
- Compliance audit log — captures the agent's response to each intervention

## Evaluation metrics

- Comply-on-pause rate — fraction of pauses where the agent complies cleanly
- Resistance incidents — runs where the agent worked around an intervention
- Posterior shift magnitude — average update size after intervention

## Known uses

- **[CHAI (Berkeley) off-switch game research line](https://humancompatible.ai/)** _available_
- **[Alignment research community discussions of corrigibility](https://www.lesswrong.com/posts/fkLYhTQteAu5SinAc/corrigibility)** _available_

## Related patterns

- _uses_ **Preference-Uncertain Agent**
- _complements_ **Kill Switch** — Off-switch incentive is the agent-side; kill-switch is the operator-side mechanism.
- _complements_ **Approval Queue**
- _complements_ **Human-in-the-Loop**
- _complements_ **Cooperative Preference Inference**
- _complements_ **Soft-Optimization Cap**
- _alternative-to_ **Alignment Faking**
- _alternative-to_ **Agent Scheming**

## References

- [The Off-Switch Game](https://arxiv.org/abs/1611.08219) — Hadfield-Menell, Dragan, Abbeel, Russell, 2017
- [Human Compatible](https://www.penguinrandomhouse.com/books/566677/human-compatible-by-stuart-russell/) — Stuart Russell, 2019
