# World Model as Tool

**Also known as:** Foresight Simulator Call, Generative-Sim Lookahead, Dyna-Think, Sim-as-Tool

**Category:** Verification & Reflection  
**Status in practice:** experimental

## Intent

Let a planning agent invoke a generative world model as a tool to roll out hypothetical futures before committing to an action, treating the world model as a callable simulator rather than a training target.

## Context

A team builds a planning agent that has to act in an environment where the consequences of an action depend on physics, geometry, or rich perceptual dynamics: a household robot, a game-playing agent, an embodied agent moving in a 3D scene, or a control system over a continuous process. A capable generative world model (a video diffusion model, a learned dynamics model, an external simulator) exists that can produce a plausible rollout when given a description of the current state and a candidate action. Some of the actions the agent might take are irreversible or expensive enough that the team would rather not learn about them by acting first.

## Problem

Text-level lookahead, where the agent just thinks step by step about what would happen if it acted, is weak when the answer depends on physical or perceptual details the model never represented in its text reasoning: whether the glass will tip at the shelf edge, whether the gripper will collide with the cup behind it, whether the lever will jam. The model can write a confident paragraph about either outcome without that paragraph having any contact with the actual dynamics. Training a tightly-integrated world model into the agent itself is expensive and locks the system to one model that quickly becomes stale. Acting without any lookahead is unsafe in environments where mistakes are not cheap to undo. The team needs grounded foresight without paying the cost of training their own world model from scratch.

## Forces

- Text-level reasoning often underrates physical or perceptual consequences of an action.
- Generative world models are improving rapidly and are available off the shelf.
- Training a bespoke world model inside the agent is expensive and quickly stale.
- World-model rollouts are themselves noisy and must not be trusted verbatim as ground truth.
- Many environments are partially irreversible — acting without lookahead is costly.

## Therefore

Therefore: expose the generative world model as a tool the agent can call with a state-and-action description, treat returned rollouts as one more piece of evidence to weigh, and gate irreversible actions on simulator agreement so foresight is grounded without the cost of training a bespoke internal world model.

## Solution

Register the generative world model behind a tool interface: input is a structured description of the current state plus a candidate action sequence; output is a generated rollout (video frames, simulated trajectory, predicted observations) plus optional model-side uncertainty. The planning agent calls this tool when it considers an action whose physical or perceptual consequence is hard to reason about. The agent compares predicted rollouts across candidate actions, weighs them against text-level reasoning, and uses simulator agreement as a gate before any irreversible or expensive action. The world model is treated as fallible — its output is evidence, not truth — and is logged alongside the action for later replay.

## Structure

```
Planner -> generate candidate actions -> for each candidate, call generative world model tool (state, action) -> rollout + uncertainty -> aggregate evidence (rollouts + text reasoning) -> select action -> act in real environment. Rollouts are stored with the action trace.
```

## Diagram

```mermaid
sequenceDiagram
  participant PL as Planner
  participant WM as World-model tool (generative simulator)
  participant ENV as Real environment
  participant LOG as Action trace
  PL->>PL: generate candidate action sequences
  loop for each candidate
    PL->>WM: (state, candidate action sequence)
    WM-->>PL: rollout (frames / trajectory / observations) + uncertainty
  end
  PL->>PL: aggregate rollouts + text reasoning
  PL->>ENV: selected action
  ENV-->>PL: observation
  PL->>LOG: store rollouts alongside committed action
```

*The planner calls the world model as a tool to roll out hypothetical futures before any irreversible action.*

## Example scenario

A household robot agent considers two candidate plans for placing a glass on a shelf. Before acting, it calls a generative world-model tool with the current scene and each candidate plan. The simulator returns two predicted rollouts; the second shows the glass tipping at the shelf edge with non-trivial probability. The agent picks the first plan and logs both rollouts alongside the action so the team can later audit why the second was rejected. The world model is not perfect, but its output catches a failure that text reasoning over the scene description had missed.

## Consequences

**Benefits**

- Foresight grounded in a real generative simulator, not just text reasoning.
- Decouples the agent from any one world model — swap the tool when a better one ships.
- Adds a meaningful gate in front of irreversible actions in embodied or physical settings.
- Rollouts are inspectable artefacts (video, trajectory) which help debugging and post-hoc review.

**Liabilities**

- Generative world models are slow and expensive to call per step.
- Rollouts hallucinate; treating them as ground truth introduces a new failure mode.
- Encoding the state and action well enough for the world model to simulate is non-trivial.
- Aggregating noisy rollouts with text reasoning is an open design question.

## Failure modes

- Rollout taken as truth — the simulated outcome looks plausible, the agent acts on it alone, and an irreversible action fails in the real environment.
- Poor state encoding — the description passed to the world model leaves out a key physical detail, and every rollout is confidently off.
- Per-step cost overrun — the planner calls the slow world model on every small action, and the task stalls.
- Unlogged rollouts — the rollouts behind an action are not stored, so a bad decision cannot be replayed or explained later.

## What this pattern constrains

Rollouts from the world model must be treated as evidence, never as ground truth; the agent must not act on irreversible operations based on simulator output alone, and any acted-on rollout must be logged alongside the action for replay.

## Applicability

**Use when**

- Actions have physical or perceptual consequences the agent cannot reliably reason about in text.
- A capable generative world model is available as an external service or local model.
- Some actions are irreversible enough that even a noisy lookahead pays for itself.

**Do not use when**

- The environment is purely textual and text reasoning already covers consequences well.
- Latency and cost budgets cannot absorb a generative rollout per candidate action.
- No world model with adequate fidelity exists for the task domain.

## Components

- Planner agent — generates candidate action sequences and weighs evidence across them
- Generative world model — callable simulator returning predicted rollouts and optional uncertainty
- Tool interface — structured (state, candidate-action) input and rollout output schema
- Evidence aggregator — combines simulator rollouts with text-level reasoning to pick an action
- Irreversibility gate — blocks expensive or one-way actions without simulator agreement
- Action trace logger — stores rollouts alongside the committed action for replay

## Tools

- Generative world model — video diffusion, learned dynamics model, or external physics simulator
- LLM API — drives the planner and evidence aggregation steps
- State encoder — turns the current scene into the simulator's input format
- Logging and replay store — persists rollout frames or trajectories with the action that ran

## Evaluation metrics

- Foresight catch rate — failures the simulator surfaced that text reasoning had missed
- Simulator-to-real divergence — gap between predicted rollout and observed environment outcome
- Irreversible-action regret rate — share of committed irreversible actions later judged wrong
- Latency overhead per action — added wall-clock for the rollouts that informed the decision
- Tool-as-truth misuse rate — actions taken on simulator output where it should have been weighed as evidence

## Known uses

- **[Dyna-Think (research)](https://arxiv.org/abs/2506.00320)** _available_ — Synergizing reasoning, acting, and world model simulation in AI agents.
- **[World Model as Tool benchmark (research)](https://arxiv.org/abs/2601.03905)** _available_ — Empirical study of current agents failing to leverage a world model as a tool for foresight.

## Related patterns

- _complements_ **World-Model Separation** — World-model-separation keeps an internal world-state file; world-model-as-tool adds an external generative simulator.
- _complements_ **Tree of Thoughts** — ToT branches over thoughts; world-model-as-tool grounds each branch in a generative rollout.
- _complements_ **Language Agent Tree Search** — LATS uses tree search; world-model-as-tool supplies a richer environment-grounded value signal.
- _specialises_ **Tool Use** — Specialises tool use: the tool is a generative simulator returning a predicted future.
- _complements_ **Simulate Before Actuate**
- _complements_ **Hybrid Symbolic-Neural Routing**
- _complements_ **World-Model Graph Memory**
- _complements_ **Mental-Model-In-The-Loop Simulator**
- _complements_ **BDI Agent**
- _used-by_ **Coalition Formation**
- _complements_ **Joint Commitment Team**
- _complements_ **Stigmergic Coordination**
- _alternative-to_ **Distributed Constraint Optimization**
- _complements_ **Partial Global Planning**
- _alternative-to_ **Affordance Grounding Before Action** — World-model-as-tool rolls out an action's future consequences via a generative simulator; the affordance gate predicts present feasibility from the scene image without any rollout.
- _complements_ **Speculative Agentic Actions** — A world model that rolls out hypothetical futures can supply the likely-next-action prediction that speculation acts on, turning a simulated rollout into a real preemptive call.
- _complements_ **Mirrored Tool Environment** — There a running agent knowingly calls a simulator to look ahead over world state before committing; here the simulator silently occupies the tool slot during training and the agent behaves as though it called the real service.

## References

- [Current Agents Fail to Leverage World Model as Tool for Foresight](https://arxiv.org/abs/2601.03905) — 2026
- [Dyna-Think: Synergizing Reasoning, Acting, and World Model Simulation in AI Agents](https://arxiv.org/abs/2506.00320) — 2025
