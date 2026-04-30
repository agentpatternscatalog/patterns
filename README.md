# Agentic Patterns Catalog

A machine-readable reference of agentic design patterns in GoF/POSA form. Pure data — no code, no scripts.

**179 patterns across 13 categories, 850 typed cross-pattern edges.**

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
