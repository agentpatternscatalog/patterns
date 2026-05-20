# Agentic Patterns Catalog

A machine-readable reference of agentic design patterns in GoF/POSA form. Pure data — no code, no scripts. Organised by category, with typed cross-pattern edges (`uses`, `composes-with`, `specialises`, `alternative-to`).

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
- **[`patterns-src/`](patterns-src/)** — source of truth: one JSON shard per category, each entry validated against [`schema.json`](schema.json).
- **[`compositions-src/`](compositions-src/)** — single source of truth for *compositions*: named combinations of patterns with roles. Each entry is either `kind: recipe` (abstract design template: *modern coding agent*, *production RAG*, *voice agent stack*, *sovereign deployment*, …) or `kind: framework` (real shipping software: LangChain, LangGraph, LlamaIndex, AutoGen, CrewAI, DSPy, n8n, Temporal, Vercel AI SDK, Claude Agent SDK, Google ADK, Letta, …). Frameworks carry per-pattern evidence (URL + quote); each entry validated against [`compositions.schema.json`](compositions.schema.json).

## Find a pattern

- **By problem:** [`docs/decision-table.md`](docs/decision-table.md) — "I want to... → read first".
- **By stack:** [`docs/recipes.md`](docs/recipes.md) — common compositions (modern coding agent, production RAG, ...).
- **By failure mode:** [`docs/anti-patterns.md`](docs/anti-patterns.md) — anti-pattern → proper alternative.

## Reference

- **Categories:** [`docs/taxonomy.md`](docs/taxonomy.md).
- **Pattern shape & required slots:** [`docs/schema.md`](docs/schema.md).

## Contribute

See [`docs/contributing.md`](docs/contributing.md) for the rules a pattern must clear before it enters the catalog. There are four ways to contribute, matching the four files that hold catalog state:

- **Add or amend a pattern.** Edit the relevant shard in [`patterns-src/`](patterns-src/) (validated against [`schema.json`](schema.json)) and, for new entries, add the corresponding [`patterns/<id>.md`](patterns/) page. Cut a branch, commit, open a pull request.
- **Add or amend a composition.** Edit the relevant shard in [`compositions-src/`](compositions-src/) (validated against [`compositions.schema.json`](compositions.schema.json)). Recipes are abstract templates; frameworks are real shipping software and require per-pattern evidence (URL + quote).
- **Suggest a pattern without authoring it yet.** Append an entry to [`pattern-todo.json`](pattern-todo.json) (validated against [`pattern-todo.schema.json`](pattern-todo.schema.json)) naming the candidate, the composition that raised it, and the upstream evidence. Candidates graduate from `proposed` → `drafting` → `authored` as they are written into `patterns-src/`.
- **Flag something that needs systematic re-checking.** Add or update an entry in [`verification-todo.json`](verification-todo.json) (validated against [`verification-todo.schema.json`](verification-todo.schema.json)). Each pattern and composition carries per-aspect statuses (`todo` / `pass` / `fail` / `na`) — intent length, references live, edges correct, evidence quoted — so the catalog can be re-verified item-by-item over time.

## License

[CC BY 4.0](LICENSE). All commits authored solely by Marco Nissen — please do not add AI co-author trailers.
