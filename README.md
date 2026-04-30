# Agentic Patterns Catalog

A machine-readable reference of agentic design patterns in GoF/POSA form. Pure data — no code, no scripts.

**179 patterns across 13 categories, 850 typed cross-pattern edges.**

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
- **[`patterns.json`](patterns.json)** — source of truth, validated against [`schema.json`](schema.json).
- **[`patterns-src/`](patterns-src/)** — per-category JSON shards; `patterns.json` is regenerated from these.

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
