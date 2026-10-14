# Adaptive Branching Tree Search

**Also known as:** AB-MCTS, 適応的分岐モンテカルロ木探索, TreeQuest, Multi-LLM AB-MCTS

**Category:** Planning & Control Flow  
**Status in practice:** experimental

## Intent

At each node of an inference-time search tree, use Thompson sampling to decide whether to deepen an existing answer or branch a fresh attempt, optionally choosing per-node which underlying LLM to invoke.

## Context

A team is using a large language model to attack problems whose outputs can be scored — running code against tests, checking a math answer, or grading an abstract-reasoning puzzle. They have a fixed budget of model calls to spend at inference time and want to spend it better than a flat sampling pass would. Several models with different strengths may be available at once, and the controller can choose which to call at each step.

## Problem

Existing inference-time search schemes commit to a fixed shape. Monte Carlo Tree Search over language-model rollouts uses a fixed branching factor and treats every node the same; tree-of-thoughts expands at a fixed width; best-of-N is flat and never refines anything. None of these adapt the trade-off between trying more fresh attempts and refining a promising one based on what the scores are actually telling the controller, and none can pick a different model for a hard node. On difficult problems this leaves a lot of compute on payoff-poor branches.

## Forces

- Width (more fresh attempts) and depth (refining existing ones) compete for the same budget.
- The right width/depth balance differs per node and is not known in advance.
- Multiple LLMs have complementary failure modes; picking the right one per node is itself a search axis.
- Thompson sampling is principled but adds bookkeeping over plain MCTS.
- Inference-time compute is expensive; wasted rollouts hurt directly.

## Therefore

Therefore: at each tree node sample from a Thompson-sampling posterior over the actions "deepen this branch" versus "branch a fresh attempt" (and optionally "with model M"), so the search adaptively allocates width, depth, and model-choice based on observed payoffs rather than fixed branching parameters.

## Solution

Each node in the search tree maintains posterior estimates over the value of its possible actions. Actions are: refine the current candidate (deepen), generate a fresh sibling (branch), and — in the multi-LLM variant — which model to call. At each step the controller draws a Thompson sample from the per-action posterior and picks the highest sampled value; the resulting rollout's score updates the posterior. Over many rollouts the tree concentrates compute on the branches and models that are paying off. The score function must be either verifiable (compiler, test, oracle) or a trusted evaluator. The framework runs until a budget or success threshold is hit.

## Structure

```
Root -> per-node {posterior over (deepen | branch | choose-model)} -> Thompson sample -> rollout via chosen LLM -> score -> posterior update.
```

## Diagram

```mermaid
flowchart TD
  ROOT[Search tree root] --> PICK[Pick a node]
  PICK --> POST[Per-node posterior over actions:<br/>deepen / branch / choose-model]
  POST --> TS[Thompson sample]
  TS --> ACT{Sampled action}
  ACT -->|deepen| DEEP[Refine current candidate]
  ACT -->|branch| BR[Generate fresh sibling]
  ACT -->|choose-model| MOD[Select LLM M]
  DEEP --> RO[Rollout via chosen LLM]
  BR --> RO
  MOD --> RO
  RO --> SC[Score: verifier / tests / oracle]
  SC --> UPD[Update posterior at node]
  UPD --> BUD{Budget hit?}
  BUD -->|no| PICK
  BUD -->|yes| OUT[Return best candidate]
```

*Each node samples width vs depth (and optionally LLM) from a Thompson posterior, updated by rollout scores.*

## Example scenario

A team tackles ARC-AGI-2 puzzles with three different LLMs. They drop the puzzles into TreeQuest, which builds a search tree where each node decides via Thompson sampling whether to refine the current candidate program, generate a fresh sibling, and which of the three models to use. After a fixed compute budget the tree has concentrated rollouts on the branches that scored well — and on the model that turned out to handle that puzzle family best — producing higher pass rates than flat best-of-N at the same cost.

## Consequences

**Benefits**

- Adaptive width/depth balance outperforms fixed-shape search on hard problems.
- Per-node model choice exploits complementary strengths of multiple LLMs.
- Thompson sampling gives a principled exploration-exploitation trade-off.
- Compute concentrates on payoff-rich branches automatically.

**Liabilities**

- Requires a usable score function; without one, the posteriors are noise.
- Bookkeeping is heavier than plain MCTS or best-of-N.
- Inference cost is still high; the pattern reduces waste but does not make search cheap.
- Multi-LLM variant adds operational complexity (different APIs, latencies, pricing).

## Failure modes

- Noisy score posteriors — the score function is a weak judge, so the posteriors track noise and the tree deepens branches that only looked good by chance.
- Budget burn on hard nodes — the controller keeps drawing samples on a difficult problem and spends the full budget without reaching the success threshold.
- Bypassed sampler — a hand-coded shortcut picks a favoured branch directly, and the search loses its balance between deepening and branching.
- Multi-model drift — the multi-LLM variant routes hard nodes to a model with different latency or pricing, and run cost and timing become hard to predict.

## What this pattern constrains

The controller must update posteriors from observed rollout scores before drawing the next sample; node expansion must not exceed the declared budget; the agent itself cannot bypass the Thompson sample to pick a favoured branch directly.

## Applicability

**Use when**

- A reliable score function (verifier, tests, oracle) is available.
- The task benefits from a mix of refinement and fresh attempts.
- Multiple LLMs are available and their strengths differ across the input distribution.

**Do not use when**

- No usable score function exists; the posteriors collapse to noise.
- Latency budgets forbid multi-rollout search.
- A single best-of-N pass already saturates the score.

## Components

- Search tree — nodes hold partial candidates and per-action posteriors
- Thompson sampler — draws an action (deepen, branch, choose-model) per visit
- Rollout LLM(s) — generates the candidate refinement or fresh sibling
- Score function — verifier, test suite, or oracle that returns a reward
- Posterior updater — folds the score back into the node's per-action belief

## Tools

- LLM API (potentially several) — rollout policy invoked per chosen model per node
- Verifier or test harness — produces the scalar reward that drives posteriors
- Search-tree state store — persists nodes, posteriors, and visit counts across rollouts

## Evaluation metrics

- Pass rate at fixed compute budget — quality lift over flat best-of-N at the same cost
- Compute concentration on payoff-rich branches — fraction of rollouts spent on the eventual best subtree
- Per-model contribution share — how often each LLM wins the Thompson draw on hard nodes
- Posterior collapse rate — fraction of runs where the score function is too noisy to discriminate actions
- Wall-clock to first passing candidate — how quickly the tree finds a winner versus flat sampling

## Known uses

- **[Sakana AI TreeQuest](https://sakana.ai/ab-mcts-jp/)** _available_ — Open-source (Apache 2.0) framework implementing AB-MCTS and Multi-LLM AB-MCTS; benchmarked on ARC-AGI-2.

## Related patterns

- _specialises_ **Language Agent Tree Search** — AB-MCTS replaces LATS's fixed-branching MCTS with adaptive Thompson-sampled width/depth.
- _alternative-to_ **Tree of Thoughts** — ToT uses fixed branching; AB-MCTS adapts branching to payoffs.
- _generalises_ **Best-of-N Sampling** — Best-of-N is the flat zero-depth case of this pattern.
- _specialises_ **Test-Time Compute Scaling** — A specific scheme for spending inference-time compute.
- _complements_ **Self-Consistency** — Self-consistency provides a voting score function that AB-MCTS can drive search against.
- _complements_ **Multi-Path Plan Generator**
- _uses_ **Forkable Agent Sandbox** — Adaptive branching decides how wide to go at each node, which is only affordable when a branch costs a delta rather than a rebuilt environment.

## References

- [AB-MCTS: 推論時の試行錯誤を効率化する新たなAIアルゴリズム](https://sakana.ai/ab-mcts-jp/) — Sakana AI, 2025
- [Sakana AIが新アルゴリズムAB-MCTSを発表](https://gihyo.jp/article/2025/07/sakana-ai-ab-mcts-algorithm) — gihyo.jp, 2025
- [Sakana AIの新アルゴリズム](https://wired.jp/article/sakana-ai-new-algorithm/) — WIRED Japan, 2025
