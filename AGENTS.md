# AGENTS.md

Guidance for AI coding agents working in this repository. Format per [agents.md](https://agents.md).
For human-facing orientation, read [`README.md`](README.md) first; for the rules a pattern must clear, read [`docs/contributing.md`](docs/contributing.md).

## What this repo is

A machine-readable catalog of agentic design patterns in GoF/POSA form. **Pure data — no application code.** The repo ships JSON (validated against schemas), generated Markdown, and docs. The only executable code that is *tracked* lives under `.github/scripts/` (CI build/lint) and `.github/scripts/*.js`.

## Source of truth vs. derived artifacts

This is the single most important rule. **Edit only the `*-src/` directories. Never hand-edit derived files.**

| Edit these (source of truth)        | Never hand-edit these (derived)                                              |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `patterns-src/` (one shard/category)| `patterns.json`, `patterns.graph.json`, `patterns.compositions.json`         |
| `compositions-src/`                 | `compositions.json`                                                          |
| `methodologies-src/`                | `methodologies.json`                                                         |
| `examples-src/`                     | `examples.json`                                                              |
| `training-src/`, `training-todo-src/`| `training.json`, `training-todo.json`                                        |
| `patterns/<id>.md` (authored pages) | `INDEX.md`, `dist/`                                                          |

After editing any `*-src/` shard, run `make build` so the derived artifacts match. CI fails on drift (committed `INDEX.md` stale vs. a clean rebuild).

## Build & check commands

```
make build     # rebuild derived artifacts at repo root, from source
make lint      # run the catalog linter
make drift     # fail if committed INDEX.md is stale vs a clean rebuild
make check     # lint + drift — this is what CI runs
make publish   # build the dist/ bundle for GitHub Pages
make clean     # remove generated JSON artifacts and dist/
```

Before pushing: run `make check` and validate edited shards against their schema (any JSON Schema draft 2020-12 validator; schemas are in the repo root, e.g. `schema.json`, `compositions.schema.json`, `examples.schema.json`).

## Editing `*-src/` JSON shards

- **Keep the compact formatting.** The shards are stored as compact JSON, not `json.dumps(indent=2)`. For small changes, edit the raw text in place rather than reserializing the whole file — a reformat produces a huge, unreviewable diff.
- Each entry must validate against its schema. Pattern hard-requirements (lint A16 fails the build): `intent`, `example_scenario`, `context`, `problem`, `applicability.use_when`, `applicability.do_not_use_when`, `diagram.mermaid`, `constrains`, and at least one of `consequences.liabilities` / `failure_modes`.
- A new pattern needs: the `patterns-src/<category>.json` entry, the `patterns/<id>.md` page, any related-pattern edges in existing entries, and a `verification-todo.json` entry (aspects start `todo`).
- Code examples live inline as strings in `examples-src/` — there are no separate `.py`/`.ts` files. Use placeholders for secrets (`"sk-..."`); never invent API shapes you can't trace to the example's `source_url`.

## Local tooling convention

Repo-root `*.py` files (e.g. `_lint.py`, `_build_training.py`) are **gitignored, local-only** one-shot helpers, conventionally prefixed with `_`. Do not expect them in CI and do not rely on them being tracked. The tracked, canonical build/lint logic is `.github/scripts/*.py`, invoked through the `Makefile`. `CLAUDE.md` is also gitignored — this `AGENTS.md` is the tracked agent-facing guidance.

## Prose & terminology style

- Sentences over bullet lists in prose slots (Intent, Context, Problem, Solution). Intent is exactly one sentence.
- Write "the model" or "the LLM" — never "the AI."
- No emoji, no hype words. Plain technical English.
- Call them **anti-patterns** — never "named failures" or "common pitfalls."
- Reader-facing fields stay plain English; technical rigour goes in the schema-backed `deep_dive` field where one exists.
- Word substitutions in prose: use "step" (not "rung"), "competitive advantage" (not "moat").

## Commits & pull requests

- Branch off `main`; one PR per logical change. PR titles are short and declarative (`Add Foo Bar pattern`, `Fix references on Cross-Encoder Reranking`).
- **Do not add AI co-author trailers.** All commits are authored solely by Marco Nissen.
- License is [CC BY 4.0](LICENSE); by contributing you license the contribution to match.
