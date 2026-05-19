# Chain-of-Agents Distillation

**Also known as:** 智能体链, Multi-Agent Distillation, AFM Distillation, Collapsed-MAS Model

**Category:** Multi-Agent
**Status in practice:** emerging

## Intent

Internalise a heterogeneous multi-agent system (planner, tool-agent, role-agent, critic) into a single foundation model via trajectory distillation plus agentic reinforcement learning, so one model emulates the collaboration at inference time without orchestration overhead.

## Context

Teams running mature multi-agent systems where a planner, several tool-using role-agents, and a critic produce strong trajectories on hard tasks. Inference cost is dominated by repeated orchestration round-trips and large context payloads passed between agents. The trajectories themselves are reusable supervision: every successful run records the full sequence of role-tagged messages, tool calls, and revisions.

## Problem

A heterogeneous multi-agent topology is expensive to run in production. Each role-agent demands its own context, its own prompt program, and its own model call; the orchestrator pays for the protocol overhead on every step. At the same time, the orchestration logic is brittle: routing rules, role prompts, and hand-offs are hand-tuned and drift out of sync with the underlying model. A single foundation model is cheaper and simpler but loses the role specialisation and the deliberative back-and-forth that made the multi-agent system strong in the first place.

## Forces

- Multi-agent inference cost scales with the number of role-agents and the protocol round-trips between them.
- Role specialisation and inter-agent critique are genuinely load-bearing — naively collapsing them into one prompt loses capability.
- Hand-tuned orchestration logic drifts as the underlying model improves and as task distribution shifts.
- Trajectories from a working multi-agent system are a rich, structured supervision signal that is being thrown away after each run.
- Distilled single-model behaviour must remain steerable and inspectable, or the team loses the ability to debug failures.

## Therefore

Therefore: log role-tagged trajectories from the running multi-agent system, distill them into a single foundation model with supervised fine-tuning, and then close the loop with agentic reinforcement learning against task rewards, so the model emulates planner/role/critic collaboration internally and the orchestrator can be retired at inference time.

## Solution

Stand up the multi-agent system first and let it produce trajectories on representative tasks. Trajectories are recorded with explicit role tags (planner, tool-agent, role-agent, critic) and tool-call structure preserved. A foundation model is then trained in two stages: supervised fine-tuning on the role-tagged trajectories teaches it to emit the inter-agent dialogue end-to-end inside a single context window, and agentic reinforcement learning against task rewards tightens the policy and lets it deviate from the multi-agent system's exact moves where the reward justifies it. At inference the orchestration layer is dropped; the model produces what looks like a multi-agent transcript autoregressively, calling tools where the original role-agents would have. The original multi-agent system is retained as a teacher and as a regression baseline.

## Structure

```
Teacher MAS (planner, role-agents, critic) -> trajectory store with role tags and tool calls -> SFT pass on a base foundation model -> agentic RL pass against task rewards -> single distilled model that, at inference, emits role-tagged collaboration in one autoregressive stream.
```

## Example scenario

A team operates a four-role agent system for long-horizon research tasks: a planner decomposes the query, two tool-agents search and execute code, and a critic re-reads drafts before submission. Inference per task costs several dollars in orchestration round-trips. The team logs role-tagged trajectories for two months, then fine-tunes a 32B base model on them and runs an agentic RL phase against task-success rewards. The resulting single model produces the same role-tagged collaboration inside one context window, and per-task cost drops by roughly an order of magnitude while task scores hold.

## Consequences

**Benefits**

- Inference cost drops sharply by eliminating inter-agent round-trips and duplicated context payloads.
- Role specialisation survives because the training signal is the role-tagged trajectory, not a flattened transcript.
- Agentic RL lets the distilled model improve past the teacher MAS on the reward signal.
- One model is simpler to deploy, monitor, and route to than a fleet of role-agents.

**Liabilities**

- Requires a working multi-agent system first as the teacher; cold-starting from no MAS yields no trajectories.
- Training cost is non-trivial: SFT plus RL on long role-tagged trajectories needs serious compute.
- Debuggability is reduced compared to a real multi-agent system where each role's output is a separate message.
- Distilled behaviour ages with the underlying base model; re-distillation is required when the base is upgraded.

## What this pattern constrains

The distilled model must keep role tags and tool-call structure in its output stream so the trajectory remains inspectable; it must not silently collapse the inter-agent dialogue into a single unstructured monologue, and it must not exceed the teacher MAS's safety envelope on tool-call surface or autonomy.

## Applicability

**Use when**

- A working multi-agent system already produces strong trajectories on representative tasks.
- Inference cost or orchestration latency from the MAS is a real production constraint.
- Role specialisation is load-bearing and a naive single-prompt collapse has measurably failed.

**Do not use when**

- There is no teacher multi-agent system yet — distillation has nothing to distill from.
- Tasks are short and the orchestration overhead is negligible.
- The base foundation model is changing weekly; the distillate will age out faster than it pays back the training cost.

## Known uses

- **[OPPO PersonalAI Lab Agent Foundation Model (AFM)](https://chain-of-agents-afm.github.io/)** — *Available* — Chain-of-Agents distillation from a heterogeneous multi-agent system into a single foundation model; reported large inference-cost reduction versus running the full MAS.

## Related patterns

- *alternative-to* → [agent-as-tool-embedding](agent-as-tool-embedding.md) — Agent-as-tool wraps one sub-agent as a callable; this pattern collapses the entire MAS into one model's weights.
- *alternative-to* → [hierarchical-agents](hierarchical-agents.md) — Hierarchical agents keep the manager/worker tree at runtime; this pattern bakes the tree into a single model.
- *complements* → [self-archaeology](self-archaeology.md) — Self-archaeology synthesises history within one agent; chain-of-agents distillation does it across a multi-agent topology.
- *alternative-to* → [inner-committee](inner-committee.md) — Inner-committee uses prompt-time personas in one model; this pattern trains the multi-role behaviour into weights.

## References

- (paper) *Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL*, 2025, <https://arxiv.org/abs/2508.13167>
- (blog) *Chain-of-Agents project page*, 2025, <https://chain-of-agents-afm.github.io/>
- (blog) *Chain-of-Agents deep read*, 2025, <https://blog.csdn.net/2401_84495872/article/details/151612478>

**Tags:** multi-agent, distillation, agentic-rl, trajectory-supervision, foundation-model
