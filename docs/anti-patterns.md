# Anti-pattern → use this instead

| Anti-pattern | Replace with |
|---|---|
| [Hero Agent](../patterns/hero-agent.md) | [routing](../patterns/routing.md), [supervisor](../patterns/supervisor.md), [multi-model-routing](../patterns/multi-model-routing.md) |
| [Black-Box Opaqueness](../patterns/black-box-opaqueness.md) | [provenance-ledger](../patterns/provenance-ledger.md), [decision-log](../patterns/decision-log.md), [lineage-tracking](../patterns/lineage-tracking.md) |
| [Infinite Debate](../patterns/infinite-debate.md) | [step-budget](../patterns/step-budget.md), [stop-hook](../patterns/stop-hook.md) |
| [Perma-Beta](../patterns/perma-beta.md) | [eval-harness](../patterns/eval-harness.md), [eval-as-contract](../patterns/eval-as-contract.md), [shadow-canary](../patterns/shadow-canary.md) |
| [Schema-Free Output](../patterns/schema-free-output.md) | [structured-output](../patterns/structured-output.md), [tool-use](../patterns/tool-use.md) |
| [Unbounded Loop](../patterns/unbounded-loop.md) | [step-budget](../patterns/step-budget.md), [stop-hook](../patterns/stop-hook.md) |
| [Same-Model Self-Critique](../patterns/same-model-self-critique.md) | [evaluator-optimizer](../patterns/evaluator-optimizer.md), [llm-as-judge](../patterns/llm-as-judge.md), [self-refine](../patterns/self-refine.md) |
| [Hallucinated Tools](../patterns/hallucinated-tools.md) | [tool-use](../patterns/tool-use.md), [structured-output](../patterns/structured-output.md) |
| [Hallucinated Citations](../patterns/hallucinated-citations.md) | [citation-streaming](../patterns/citation-streaming.md), [naive-rag](../patterns/naive-rag.md) |
| [Naive-RAG-First](../patterns/naive-rag-first.md) | [tool-use](../patterns/tool-use.md) (when knowledge lives in a database/API) |
| [Tool Explosion](../patterns/tool-explosion.md) | [tool-loadout](../patterns/tool-loadout.md) |
| [Hidden Mode Switching](../patterns/hidden-mode-switching.md) | [multi-model-routing](../patterns/multi-model-routing.md), [lineage-tracking](../patterns/lineage-tracking.md) |
| [Tool Output Trusted Verbatim](../patterns/tool-output-trusted-verbatim.md) | [tool-output-poisoning](../patterns/tool-output-poisoning.md), [structured-output](../patterns/structured-output.md) |
| [Prompt Bloat](../patterns/prompt-bloat.md) | [agent-skills](../patterns/agent-skills.md), [constitutional-charter](../patterns/constitutional-charter.md) |
| [Unbounded Subagent Spawn](../patterns/unbounded-subagent-spawn.md) | [step-budget](../patterns/step-budget.md), [cost-gating](../patterns/cost-gating.md), [kill-switch](../patterns/kill-switch.md) |
