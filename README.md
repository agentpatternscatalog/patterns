# Agentic Patterns Catalog

A machine-readable reference of agentic design patterns in GoF/POSA form. Pure data — no code, no scripts.

**179 patterns across 13 categories, 850 typed cross-pattern edges.**

## What "agentic" means

An agent is a system that pursues a goal and reaches an action autonomously. Given a user-supplied objective, the LLM decides what to do next, picks tools, observes results, and iterates until the goal is met or a budget is exhausted — without a human stepping through each call.

Three properties separate an agentic system from a one-shot prompt:

- **Goal-directed.** The agent holds an objective across many model calls, not a single response.
- **Autonomous action.** The agent chooses tools and executes them; the host does not script the steps in advance.
- **Loop-bounded.** The agent keeps acting until it terminates itself, hits a step or cost budget, or is interrupted.

The patterns in this catalog are the architectural choices that make agentic systems work in production: how the loop is shaped, what the agent is allowed to remember, which tools it sees, and how it is verified, audited, and stopped.

## Why a pattern catalog for LLM agents

Christopher Alexander, in *A Pattern Language* (1977), defined a pattern as something that "describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in such a way that you can use this solution a million times over, without ever doing it the same way twice." The Gang of Four carried that framing into software in 1994. The result was a shared vocabulary that let teams reason about decisions instead of re-discovering them.

LLM agents need this kind of vocabulary more than most software, not less. The model itself is non-deterministic and drifts across versions; the only thing that stays stable is the architecture around it. Patterns are the architecture around it.

Three reasons a catalog earns its seat:

- **Repeatability against a non-deterministic substrate.** A working production agent gives the model less room than it could fill. Patterns name exactly the constraints — step budgets, frozen rubrics, deterministic-LLM sandwiches, charters — that turn one-off prompt experiments into systems other teams can run, audit, and trust.
- **Reuse across use cases.** ReAct, Plan-and-Execute, evaluator-optimizer loops, contextual retrieval, kill switches: the same shapes recur whether the agent writes code, fills a form, schedules meetings, or runs unattended for weeks. Naming them once means the next product builds on yesterday's lessons.
- **A language for composition.** Real systems compose many patterns. *Modern coding agent* = ReAct + Tool Use + Step Budget + Subagent Isolation + Decision Log + Agent-Computer Interface. *Production RAG* = Hybrid Search + Cross-Encoder Reranking + Contextual Retrieval + Citation Streaming + Eval Harness + Chain of Verification. The catalog's typed edges (`uses`, `composes-with`, `specialises`, `alternative-to`) make those compositions explicit and reviewable.

Every entry in this catalog declares one thing the LLM is *forbidden* to do under that pattern. That constraint-first framing is the through-line: patterns are what you give the model less, so it can be relied on more.

## Browse the catalog

- **[`INDEX.md`](INDEX.md)** — every pattern grouped by category.
- **[`patterns/`](patterns/)** — one Markdown page per pattern.
- **[`patterns-src/`](patterns-src/)** — source of truth: 13 per-category JSON shards, each entry validated against [`schema.json`](schema.json).
- **[`framework-coverage.json`](framework-coverage.json)** — which patterns each agent framework (LangChain, LangGraph, LlamaIndex, AutoGen, CrewAI, DSPy, n8n, Temporal, Vercel AI SDK, Claude Agent SDK, Google ADK, Letta, …) provides as `fully` / `limited` / `none` / `unknown`. Hand-curated, conservative; carries a `last_analysis_date` plus per-row `last_analyzed`.
- **[`recipes.json`](recipes.json)** — named cross-category compositions: *modern coding agent*, *production RAG*, *voice agent stack*, *sovereign deployment*, *long-running autonomous agent*, *multi-agent debate*, *browser & computer-use stack*, *memory architecture*, *multi-agent coordination*, *safety hardening*, *eval & observability*, *structured output stack*, *streaming UX stack*, *planning loops*, *routing & fallback*, *reflection & self-correction*. Each recipe lists pattern members with role (`core`, `hardening`, `optional`).

## Find a pattern

- **By problem:** [`docs/decision-table.md`](docs/decision-table.md) — "I want to... → read first".
- **By stack:** [`docs/recipes.md`](docs/recipes.md) — common compositions (modern coding agent, production RAG, ...).
- **By failure mode:** [`docs/anti-patterns.md`](docs/anti-patterns.md) — anti-pattern → proper alternative.

## Reference

- **Categories:** [`docs/taxonomy.md`](docs/taxonomy.md).
- **Pattern shape & required slots:** [`docs/schema.md`](docs/schema.md).
- **Contribute:** [`docs/contributing.md`](docs/contributing.md).

## License

[CC BY 4.0](LICENSE). All commits authored solely by Marco Nissen — please do not add AI co-author trailers.
