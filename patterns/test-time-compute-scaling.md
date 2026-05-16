# Test-Time Compute Scaling

**Also known as:** Inference-Time Scaling, Compute-Time Trade-Off

**Category:** Reasoning  
**Status in practice:** mature

## Intent

Allocate more inference-time compute (samples, search, deeper thinking) instead of scaling parameters to improve quality.

## Context

Frontier of agent capability where parameter scaling has saturated and quality gains come from inference-time techniques.

## Problem

Naive single-pass inference under-uses available compute; many hard tasks have inference-time techniques that beat ever-larger models.

## Forces

- Wall-clock latency rises with compute.
- Cost rises linearly or worse with sample count.
- Best technique (samples / search / deeper thinking) is task-dependent.


## Applicability

**Use when**

- Parameter scaling has saturated and inference-time techniques deliver further lift.
- The task is amenable to a known technique (best-of-N, self-consistency, tree search, extended thinking).
- Compute budget at inference time is available and worth spending for quality.

**Do not use when**

- Latency or cost budgets cannot absorb extra inference-time compute.
- The task does not benefit from any of the inference-time techniques.
- A larger or better model is cheaper than scaling test-time compute.

## Therefore

Therefore: spend more compute at inference (samples, search, deeper thinking) instead of more parameters, so that quality lifts on hard tasks without retraining.

## Solution

Pick the inference-time technique that fits: best-of-N for verifier-amenable tasks, self-consistency for sampling-amenable tasks, tree search for combinatorial tasks, extended thinking for sequential reasoning. Compose techniques where complementary. Tune the compute budget per task class.

## Variants

- **Parallel sampling (best-of-N)** — Draw N independent samples and pick the best by a verifier or majority vote.
- **Sequential revision** — One sample is iteratively revised by the same model conditioned on its previous attempt.
- **Tree / beam search** — Explore a branching search tree with a value model pruning low-promise branches (ToT, LATS, MCTS-style).
- **Compute-optimal routing** — Pick parallel vs sequential vs deeper-thinking per question based on difficulty estimate (Snell et al. 2024).

## Example scenario

A team has a hard math benchmark where their current model underperforms; the obvious move is to wait for a larger model. Instead they apply test-time compute scaling: best-of-N sampling with a verifier for verifier-amenable items, self-consistency for sampling-amenable items, tree search for combinatorial items, extended thinking for sequential reasoning. Per-item cost rises but accuracy on the benchmark beats the next-tier model at lower total cost.


## Diagram

```mermaid
flowchart TD
  Q[Request] --> Class{Task class?}
  Class -->|verifier-amenable| BoN[Best-of-N]
  Class -->|sampling-amenable| SC[Self-consistency]
  Class -->|combinatorial| Tree[Tree search]
  Class -->|sequential| ET[Extended thinking]
  BoN --> Comp[Compose where complementary]
  SC --> Comp
  Tree --> Comp
  ET --> Comp
  Comp --> Out[Answer at tuned compute budget]
```

## Consequences

**Benefits**

- Quality lifts without retraining.
- Compute budget becomes a per-request control.

**Liabilities**

- Latency-sensitive use cases cannot afford much.
- Token cost can dominate.

## What this pattern constrains

Each request specifies its compute budget; over-budget requests are cut off.

## Known uses

- **OpenAI o-series scaling-with-effort** — *Available*
- **DeepMind AlphaCode/AlphaProof scaling** — *Available*

## Related patterns

- *generalises* → [extended-thinking](extended-thinking.md)
- *generalises* → [best-of-n](best-of-n.md)
- *generalises* → [self-consistency](self-consistency.md)
- *generalises* → [lats](lats.md)
- *generalises* → [process-reward-model](process-reward-model.md)

## References

- (paper) Snell, Lee, Xu, Kumar, *Scaling LLM Test-Time Compute Optimally Can Be More Effective Than Scaling Model Parameters*, 2024, <https://arxiv.org/abs/2408.03314>
- (paper) Brown, Juravsky, Ehrlich, Clark, Le, Ré, Mirhoseini, *Large Language Monkeys: Scaling Inference Compute with Repeated Sampling*, 2024, <https://arxiv.org/abs/2407.21787>

**Tags:** reasoning, scaling, compute
