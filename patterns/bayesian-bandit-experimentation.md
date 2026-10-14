# Bayesian Bandit Experimentation

**Also known as:** Multi-Armed Bandit for Prompt Variants, Bandit-Based Agent Rollout

**Category:** Governance & Observability  
**Status in practice:** emerging

## Intent

Replace fixed-split A/B tests between agent variants with a bandit that dynamically reallocates traffic toward better-performing variants based on observed reward, bounding regret from bad variants.

## Context

An agent team has multiple variants in play: two prompt templates, three model choices, two retrieval strategies. They want to learn which performs best on production traffic without exposing many users to the worse variants for the full length of a classical A/B test.

## Problem

A fixed 50/50 (or N-way uniform) split between variants pays regret on every losing variant for the entire experiment window. With multiple simultaneous variants the regret compounds. Worse, the experiment cannot be stopped early without invalidating the statistics; teams keep losing variants live for weeks because the rollout calendar said so. A static split is wrong as a learning policy when the team genuinely cares about user outcomes during the experiment.

## Forces

- Some variants are clearly worse early; continuing uniform allocation pays regret.
- Some variants need many trials to reveal their advantage; aggressive exploitation kills them.
- Reward signals (task success, user satisfaction, cost) arrive with delay and noise.
- Operators need to be able to read off 'which variant is winning' at any point.

## Therefore

Therefore: route traffic to variants by a bandit policy that updates from observed reward, so allocation shifts toward winners as evidence accumulates and regret on losers is bounded.

## Solution

Treat each variant as a bandit arm. After each request, record the variant chosen and (when it arrives) the reward (task success, satisfaction, cost). A Thompson sampler or upper-confidence-bound policy decides allocation for the next request. Run for a budget of requests or until posterior separation crosses a threshold; promote the winner. Surface posterior means and credible intervals in the experiment dashboard.

## Structure

```
Incoming request --> Bandit policy (Thompson sampling / UCB) --> Variant A | B | C --> Observe reward (success, satisfaction, cost) --> Update per-arm posteriors --> Bandit policy; posteriors --> Allocation dashboard; separation threshold or budget reached --> promote winner
```

## Diagram

```mermaid
flowchart TD
  Req[Incoming request] --> Pol[Bandit policy]
  Pol --> V1[Variant A]
  Pol --> V2[Variant B]
  Pol --> V3[Variant C]
  V1 --> R[Observe reward]
  V2 --> R
  V3 --> R
  R --> Upd[Update posteriors]
  Upd --> Pol
```

## Example scenario

A support-agent team has four candidate prompt templates and two candidate models. They run all eight (template × model) combinations as bandit arms with Thompson sampling over downstream user-rating reward. By day three two arms have collected enough credible evidence to promote; the bandit allocates >70% of traffic to them and continues exploring the rest at low rate.

## Consequences

**Benefits**

- Regret on losing variants is bounded; allocation tracks evidence.
- Many simultaneous variants can be experimented over without combinatorial regret.
- Operators see a live posterior rather than waiting for a fixed window to close.

**Liabilities**

- Variants the bandit prunes early can be the slow-burn winners; tune exploration carefully.
- Delayed reward complicates the update; naive bandits over-allocate to fast-response variants.
- Stat-stoppage at posterior-separation introduces optional-stopping bias if undisciplined.

## Failure modes

- Early pruning of a slow winner — the policy starves a variant whose reward only shows up after a few days, and the better variant never gets enough traffic to prove itself.
- Fast-reward bias — reward for some variants arrives late, so the naive update favours whichever variant reports outcomes first.
- Peeking at separation — operators stop the experiment the first time the posteriors look apart, and the promoted winner is a product of optional stopping.
- Mis-specified reward — the reward signal tracks cost or speed only, and the bandit shifts traffic toward a cheaper variant that solves fewer tasks.

## What this pattern constrains

Variant allocation must not be a fixed-fraction split when reward can be observed online; the policy must update from observed reward and shift allocation accordingly.

## Applicability

**Use when**

- Multiple variants are live and reward can be observed online with reasonable delay.
- User-outcome regret on losing variants is a real cost.
- Operators want a live posterior rather than a fixed test window.

**Do not use when**

- Reward is unobservable or arrives only after weeks; bandit cannot learn.
- Variants must be tested at equal sample size for regulatory or scientific reasons.
- Allocation cannot be dynamic — only one variant can be in production at a time.

## Components

- Bandit policy — Thompson sampling or UCB over arms
- Reward observer — captures outcome signal per request
- Posterior store — per-arm reward posterior
- Allocation dashboard — surfaces live posteriors and traffic share

## Tools

- Reward logging pipeline — pushes outcome signal to posterior updater
- Experiment registry — tracks arms, durations, and posterior thresholds
- Eval-harness — used to compute reward signal on tasks

## Evaluation metrics

- Cumulative regret — total reward gap vs always-best.
- Time to credible separation — how fast posteriors diverge.
- Variant survival curve — share of arms still receiving traffic at time t.

## Known uses

- **[Building Applications with AI Agents (Albada) — Bayesian Bandits in improvement loops](https://www.oreilly.com/library/view/building-applications-with/9781098176495/)** _available_
- **[OpenAI Evals and major-lab prompt-eval pipelines using bandit-based variant selection](https://github.com/openai/evals)** _available_

## Related patterns

- _alternative-to_ **Shadow Canary** — Shadow is parallel; bandit reallocates live traffic.
- _uses_ **Eval Harness**
- _complements_ **Evaluator-Optimizer**
- _complements_ **evaluation-driven-development**
- _specialises_ **Exploration vs Exploitation**
- _composes-with_ **Prompt Variant Evaluation**
- _alternative-to_ **Trust and Reputation Routing**
- _complements_ **Learnability-Frontier Task Sampling** — The same allocation reasoning at a different layer: the bandit reallocates production traffic across agent variants, while here one policy reallocates rollout budget across training tasks.

## References

- [Building Applications with AI Agents](https://www.oreilly.com/library/view/building-applications-with/9781098176495/) — Michael Albada, 2025
