# ReST-EM

**Also known as:** Reinforced Self-Training, Self-Training Loop

**Category:** Reasoning  
**Status in practice:** emerging

## Intent

Iterate generate → reward-filter → fine-tune to bootstrap reasoning capabilities without human-labelled data.

## Context

Reasoning tasks where the model is partially competent and a reward signal (correct answer, executable test, formal verifier) exists.

## Problem

Pure prompting plateaus; full RL with PPO is unstable and expensive; supervised data is unavailable.

## Forces

- Reward filter quality bounds learning quality.
- Iteration count vs cost.
- Distribution drift across iterations.

## Solution

EM-style loop. (E-step) Generate many responses per problem. Filter by reward (correctness against ground truth or executable test). (M-step) Fine-tune on the filtered set. Iterate. Variants: ReST (DeepMind, RL-shaped), ReST-EM (Singh et al., expectation-maximisation framing).

## Consequences

**Benefits**

- Strong gains without human-labelled rationales.
- Stable; converges in a few iterations.

**Liabilities**

- Compute-heavy.
- Reward gaming possible.

## What this pattern constrains

Training data is restricted to filter-passing samples; ungrounded samples are not reinforced.

## Known uses

- **DeepMind ReST** — *Available*
- **Singh et al. ReST-EM** — *Available*

## Related patterns

- *generalises* → [star-bootstrapping](star-bootstrapping.md)
- *uses* → [best-of-n](best-of-n.md)

## References

- (paper) Gulcehre et al., *Reinforced Self-Training (ReST) for Language Modeling*, 2023, <https://arxiv.org/abs/2308.08998>
- (paper) Singh, Co-Reyes, Agarwal, Anand, Patil, Garcia, Liu, Harrison, Lee, Xu, Parisi, Kumar, Alemi, Rizkowsky, Nova, Adlam, Bohnet, Elsayed, Sedghi, Mordatch, Simpson, Gur, Snoek, Pfaff, Brown, Roy, Mustafa, Hoffman, Botvinick, Faust, Larochelle, Hadsell, Schuurmans, Faruqui, *Beyond Human Data: Scaling Self-Training for Problem-Solving with Language Models*, 2023, <https://arxiv.org/abs/2312.06585>

**Tags:** reasoning, self-training, rl
