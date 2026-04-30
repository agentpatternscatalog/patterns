# Agentic Design Patterns

A machine-readable taxonomy of design patterns for LLM-based agents, written in the tradition of *Design Patterns* (Gamma, Helm, Johnson, Vlissides, 1994) and *Pattern-Oriented Software Architecture* (Buschmann et al., 1996).

Every entry names a recurring problem, the forces that make it hard, and a reusable solution. Each pattern carries a constraint-first framing: what it *forbids* the LLM from doing. That framing is the through-line.

**Catalog status:** 179 patterns across 13 categories, 850 cross-pattern edges.

## Why another catalog

Several catalogs exist already — `nibzard/awesome-agentic-patterns`, `ai-standards/ai-design-patterns`, Antonio Gulli's *Agentic Design Patterns* book, Anthropic's *Building Effective Agents*, `zeljkoavramovic/agentic-design-patterns` and others. They are useful and we cite them.

This catalog differs in four ways:

1. **Strict GoF/POSA structure.** Every pattern uses the same slots: Intent, Context, Problem, Forces, Solution, Consequences, Known Uses, Related Patterns, References. No prose-only entries.
2. **Machine-readable JSON.** `patterns.json` is the source of truth; per-pattern markdown is generated. Tooling (eval harnesses, agent IDEs, doc sites) can consume the index directly.
3. **Constraint-first framing.** Each pattern declares what it constrains the LLM from doing. A pattern that does not constrain the model is decoration.
4. **Cascading structure.** Composite patterns explicitly declare which simpler patterns they use, with `uses` / `composes-with` / `specialises` / `generalises` / `alternative-to` / `complements` / `conflicts-with` edges. This is the GoF "X uses [A, B, C]" pattern that turns a flat list into a system.

## Repo layout

```
agentic-patterns/
├── README.md              # this file
├── INDEX.md               # auto-generated browsing index by category
├── schema.json            # JSON Schema for one pattern
├── patterns.json          # 119 patterns, machine-readable source of truth
├── taxonomy.md            # category definitions
├── render.py              # patterns.json -> patterns/*.md + INDEX.md
├── enrich.py              # idempotent cascade-edge enrichment
├── patterns/              # 119 auto-generated human pages
│   ├── react.md
│   ├── tool-use.md
│   └── ...
└── CONTRIBUTING.md        # how to propose / amend a pattern
```

## Categories (13)

See [`taxonomy.md`](taxonomy.md) for full definitions. See [`INDEX.md`](INDEX.md) for the browsing list.

| Category | Count |
|---|---|
| Reasoning | 11 |
| Planning & Control Flow | 17 |
| Tool Use & Environment | 21 |
| Retrieval & RAG | 10 |
| Memory | 14 |
| Multi-Agent | 20 |
| Verification & Reflection | 12 |
| Safety & Control | 19 |
| Routing & Composition | 14 |
| Governance & Observability | 16 |
| Structure & Data | 5 |
| Streaming & UX | 5 |
| Anti-Patterns | 15 |

## Pattern entry shape

Every pattern in `patterns.json` conforms to [`schema.json`](schema.json). Slots:

- **id** — stable kebab-case identifier
- **name** — canonical name; **aliases** — synonyms / Also-Known-As (the field where variant names from other catalogs map back to one canonical entry)
- **category** — one of the 13 buckets above
- **intent** — one sentence
- **context** — when does this situation arise
- **problem** — what is hard about it
- **forces** — competing constraints
- **solution** — recipe-level resolution
- **structure** — optional sketch of participants
- **consequences** — { benefits, liabilities }
- **constrains** — what the LLM is forbidden to do under this pattern
- **known_uses** — systems that ship this pattern, each with status (`available` / `planned` / `pure-future` / `not-pursued`)
- **related** — typed cross-pattern edges (`uses` / `used-by` / `composes-with` / `specialises` / `generalises` / `alternative-to` / `complements` / `conflicts-with`)
- **references** — papers, blogs, docs, repos
- **status_in_practice** — `mature` / `emerging` / `experimental` / `deprecated`

## How to use

- **Browse:** start at [`INDEX.md`](INDEX.md), grouped by category.
- **Search by name or alias:** every catalog name from neighbour catalogs (Gulli, Avramovic, AI-Standards, Anthropic, the academic literature) appears as a canonical entry or as an alias of one.
- **Build a stack:** look at a composite pattern's `uses` edges to see what simpler patterns it depends on. Examples: [agentic-rag](patterns/agentic-rag.md), [planner-executor-observer](patterns/planner-executor-observer.md), [deterministic-llm-sandwich](patterns/deterministic-llm-sandwich.md).
- **Avoid known traps:** the [anti-patterns](INDEX.md#anti-patterns) section names the failure modes explicitly with cross-references to their proper alternatives.
- **Consume programmatically:** `patterns.json` is the source of truth. The schema is in `schema.json`.

## What problem are you solving?

| You want to... | Read first |
|---|---|
| Stop the agent from looping forever | [step-budget](patterns/step-budget.md), [stop-hook](patterns/stop-hook.md) |
| Verify the agent's output before it lands | [deterministic-llm-sandwich](patterns/deterministic-llm-sandwich.md), [chain-of-verification](patterns/chain-of-verification.md), [evaluator-optimizer](patterns/evaluator-optimizer.md) |
| Save agent state across restarts or disconnects | [agent-resumption](patterns/agent-resumption.md), [short-term-memory](patterns/short-term-memory.md) |
| Make the agent remember things across sessions | [cross-session-memory](patterns/cross-session-memory.md), [vector-memory](patterns/vector-memory.md) |
| Fall back when a tool/provider fails | [fallback-chain](patterns/fallback-chain.md), [provider-fallback](patterns/provider-fallback.md), [graceful-degradation](patterns/graceful-degradation.md) |
| Ask the user before acting on risky things | [human-in-the-loop](patterns/human-in-the-loop.md), [approval-queue](patterns/approval-queue.md), [cost-gating](patterns/cost-gating.md) |
| Reduce token cost on a long-running agent | [prompt-caching](patterns/prompt-caching.md), [context-window-packing](patterns/context-window-packing.md), [episodic-summaries](patterns/episodic-summaries.md), [multi-model-routing](patterns/multi-model-routing.md) |
| Coordinate multiple specialist agents | [supervisor](patterns/supervisor.md), [orchestrator-workers](patterns/orchestrator-workers.md), [lead-researcher](patterns/lead-researcher.md) |
| Defend against prompt injection | [prompt-injection-defense](patterns/prompt-injection-defense.md), [tool-output-poisoning](patterns/tool-output-poisoning.md), [input-output-guardrails](patterns/input-output-guardrails.md) |
| Trace and audit what the agent did | [provenance-ledger](patterns/provenance-ledger.md), [decision-log](patterns/decision-log.md), [lineage-tracking](patterns/lineage-tracking.md) |
| Halt all running agents in an emergency | [kill-switch](patterns/kill-switch.md) |
| Build a research/scout multi-agent | [lead-researcher](patterns/lead-researcher.md), [orchestrator-workers](patterns/orchestrator-workers.md), [subagent-isolation](patterns/subagent-isolation.md) |

## Common stacks

Real agent products compose many patterns. A few canonical stacks:

- **Modern coding agent** = [react](patterns/react.md) + [tool-use](patterns/tool-use.md) + [step-budget](patterns/step-budget.md) + [subagent-isolation](patterns/subagent-isolation.md) + [stop-hook](patterns/stop-hook.md) + [decision-log](patterns/decision-log.md) + [agent-computer-interface](patterns/agent-computer-interface.md) + [parallel-tool-calls](patterns/parallel-tool-calls.md)

- **Production RAG** = [hybrid-search](patterns/hybrid-search.md) + [cross-encoder-reranking](patterns/cross-encoder-reranking.md) + [contextual-retrieval](patterns/contextual-retrieval.md) + [citation-streaming](patterns/citation-streaming.md) + [eval-harness](patterns/eval-harness.md) + [chain-of-verification](patterns/chain-of-verification.md)

- **Long-running agent** = [agent-resumption](patterns/agent-resumption.md) + [append-only-thought-stream](patterns/append-only-thought-stream.md) + [provenance-ledger](patterns/provenance-ledger.md) + [replay-time-travel](patterns/replay-time-travel.md) + [cost-observability](patterns/cost-observability.md) + [scheduled-agent](patterns/scheduled-agent.md)

- **Risk-gated mutation agent** = [human-in-the-loop](patterns/human-in-the-loop.md) + [cost-gating](patterns/cost-gating.md) + [quorum-on-mutation](patterns/quorum-on-mutation.md) + [compensating-action](patterns/compensating-action.md) + [constitutional-charter](patterns/constitutional-charter.md) + [approval-queue](patterns/approval-queue.md)

- **Multi-agent research** = [lead-researcher](patterns/lead-researcher.md) + [subagent-isolation](patterns/subagent-isolation.md) + [orchestrator-workers](patterns/orchestrator-workers.md) + [parallelization](patterns/parallelization.md) + [agent-resumption](patterns/agent-resumption.md)

- **Production-safe MCP integration** = [mcp](patterns/mcp.md) + [tool-loadout](patterns/tool-loadout.md) + [tool-output-poisoning](patterns/tool-output-poisoning.md) + [secrets-handling](patterns/secrets-handling.md) + [sandbox-isolation](patterns/sandbox-isolation.md) + [sandbox-escape-monitoring](patterns/sandbox-escape-monitoring.md)

- **Cognitive architecture** = [five-tier-memory-cascade](patterns/five-tier-memory-cascade.md) + [constitutional-charter](patterns/constitutional-charter.md) + [self-modification-diff-gate](patterns/inner-critic.md) + [salience-triggered-output](patterns/salience-triggered-output.md) + [provenance-ledger](patterns/provenance-ledger.md)

## Anti-pattern → use this instead

| Anti-pattern | Replace with |
|---|---|
| [Hero Agent](patterns/hero-agent.md) | [routing](patterns/routing.md), [supervisor](patterns/supervisor.md), [multi-model-routing](patterns/multi-model-routing.md) |
| [Black-Box Opaqueness](patterns/black-box-opaqueness.md) | [provenance-ledger](patterns/provenance-ledger.md), [decision-log](patterns/decision-log.md), [lineage-tracking](patterns/lineage-tracking.md) |
| [Infinite Debate](patterns/infinite-debate.md) | [step-budget](patterns/step-budget.md), [stop-hook](patterns/stop-hook.md) |
| [Perma-Beta](patterns/perma-beta.md) | [eval-harness](patterns/eval-harness.md), [eval-as-contract](patterns/eval-as-contract.md), [shadow-canary](patterns/shadow-canary.md) |
| [Schema-Free Output](patterns/schema-free-output.md) | [structured-output](patterns/structured-output.md), [tool-use](patterns/tool-use.md) |
| [Unbounded Loop](patterns/unbounded-loop.md) | [step-budget](patterns/step-budget.md), [stop-hook](patterns/stop-hook.md) |
| [Same-Model Self-Critique](patterns/same-model-self-critique.md) | [evaluator-optimizer](patterns/evaluator-optimizer.md), [llm-as-judge](patterns/llm-as-judge.md), [self-refine](patterns/self-refine.md) (well-engineered) |
| [Hallucinated Tools](patterns/hallucinated-tools.md) | [tool-use](patterns/tool-use.md), [structured-output](patterns/structured-output.md) |
| [Hallucinated Citations](patterns/hallucinated-citations.md) | [citation-streaming](patterns/citation-streaming.md), [naive-rag](patterns/naive-rag.md) |
| [Naive-RAG-First](patterns/naive-rag-first.md) | [tool-use](patterns/tool-use.md) (when knowledge lives in a database/API) |
| [Tool Explosion](patterns/tool-explosion.md) | [tool-loadout](patterns/tool-loadout.md) |
| [Hidden Mode Switching](patterns/hidden-mode-switching.md) | [multi-model-routing](patterns/multi-model-routing.md), [lineage-tracking](patterns/lineage-tracking.md) |
| [Tool Output Trusted Verbatim](patterns/tool-output-trusted-verbatim.md) | [tool-output-poisoning](patterns/tool-output-poisoning.md), [structured-output](patterns/structured-output.md) |
| [Prompt Bloat](patterns/prompt-bloat.md) | [agent-skills](patterns/agent-skills.md), [constitutional-charter](patterns/constitutional-charter.md) |

## Tooling

- `python3 render.py` — regenerate `patterns/*.md` and `INDEX.md` from `patterns.json`.
- `python3 enrich.py` — idempotently add cascade edges (`uses` / `composes-with` etc.) declared inline in the script.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Patterns must reference at least one of: a paper, a publicly visible product, or a working repo. No pattern is admitted on speculation alone. Every pattern declares what it constrains.

## License

CC BY 4.0. This repository ships catalog content only (patterns, schema,
taxonomy, docs). Local tooling used to generate it is not distributed here.

## Authorship

All commits to this repository are authored solely by Marco Nissen. Do not
add Claude Code or any AI assistant as a co-author or committer.
