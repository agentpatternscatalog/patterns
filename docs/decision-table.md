# What problem are you solving?

| You want to... | Read first |
|---|---|
| Stop the agent from looping forever | [step-budget](../patterns/step-budget.md), [stop-hook](../patterns/stop-hook.md) |
| Verify the agent's output before it lands | [deterministic-llm-sandwich](../patterns/deterministic-llm-sandwich.md), [chain-of-verification](../patterns/chain-of-verification.md), [evaluator-optimizer](../patterns/evaluator-optimizer.md) |
| Save agent state across restarts or disconnects | [agent-resumption](../patterns/agent-resumption.md), [short-term-memory](../patterns/short-term-memory.md) |
| Make the agent remember things across sessions | [cross-session-memory](../patterns/cross-session-memory.md), [vector-memory](../patterns/vector-memory.md) |
| Fall back when a tool/provider fails | [fallback-chain](../patterns/fallback-chain.md), [provider-fallback](../patterns/provider-fallback.md), [graceful-degradation](../patterns/graceful-degradation.md) |
| Ask the user before acting on risky things | [human-in-the-loop](../patterns/human-in-the-loop.md), [approval-queue](../patterns/approval-queue.md), [cost-gating](../patterns/cost-gating.md) |
| Reduce token cost on a long-running agent | [prompt-caching](../patterns/prompt-caching.md), [context-window-packing](../patterns/context-window-packing.md), [episodic-summaries](../patterns/episodic-summaries.md), [multi-model-routing](../patterns/multi-model-routing.md) |
| Coordinate multiple specialist agents | [supervisor](../patterns/supervisor.md), [orchestrator-workers](../patterns/orchestrator-workers.md), [lead-researcher](../patterns/lead-researcher.md) |
| Defend against prompt injection | [prompt-injection-defense](../patterns/prompt-injection-defense.md), [tool-output-poisoning](../patterns/tool-output-poisoning.md), [input-output-guardrails](../patterns/input-output-guardrails.md) |
| Trace and audit what the agent did | [provenance-ledger](../patterns/provenance-ledger.md), [decision-log](../patterns/decision-log.md), [lineage-tracking](../patterns/lineage-tracking.md) |
| Halt all running agents in an emergency | [kill-switch](../patterns/kill-switch.md) |
| Build a research/scout multi-agent | [lead-researcher](../patterns/lead-researcher.md), [orchestrator-workers](../patterns/orchestrator-workers.md), [subagent-isolation](../patterns/subagent-isolation.md) |
