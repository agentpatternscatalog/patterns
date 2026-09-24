# Contributing

Thanks for considering a contribution. This repository is **data, not code**: you edit JSON shards and Markdown pages, and CI validates them against a JSON Schema and a catalog linter.

This page is the short front door. The full rules live in **[`docs/contributing.md`](docs/contributing.md)**. If you are working through an AI coding agent, point it at **[`AGENTS.md`](AGENTS.md)**.

## The one rule that breaks most first pull requests

**Edit only the `*-src/` directories. Never hand-edit the derived files at the repo root.**

| Edit these (source of truth)          | Never hand-edit these (derived)                                      |
| ------------------------------------- | -------------------------------------------------------------------- |
| `patterns-src/` (one shard/category)  | `patterns.json`, `patterns.graph.json`, `patterns.compositions.json` |
| `compositions-src/`                   | `compositions.json`                                                  |
| `examples-src/`                       | `examples.json`                                                      |
| `methodologies-src/`                  | `methodologies.json`                                                 |
| `training-src/`, `training-todo-src/` | `training.json`, `training-todo.json`                                |
| `patterns/<id>.md` (authored pages)   | `INDEX.md`, `dist/`                                                  |

After editing any shard, run `make build` so the derived artifacts match. CI fails if a committed `INDEX.md` is stale against a clean rebuild.

Keep the **compact JSON formatting** in `*-src/` shards. Edit the raw text in place; do not reserialize a whole file with an indenting formatter, because that produces a diff nobody can review.

## What counts as a pattern

Three rules decide whether an entry enters the catalog. All three are checked at review time.

1. **It names a recurring problem** — not a feature, a framework, or a library. If you cannot finish "this is the pattern for when ..." without naming a specific vendor, it is a technique, not yet a pattern.
2. **It cites real evidence** — a linked paper with authors and year, a publicly visible product that ships it, or a working open repository. Nothing is admitted on speculation.
3. **It declares what it constrains** — the `constrains` slot names the one thing the model is forbidden to do under this pattern. A pattern that does not constrain the model's freedom is decoration.

Required slots (linter rule A16 fails the build without them): `intent`, `example_scenario`, `context`, `problem`, `applicability.use_when`, `applicability.do_not_use_when`, `diagram.mermaid`, `constrains`, and at least one entry across `consequences.liabilities` / `failure_modes`.

## Quick start

```sh
git switch -c my-change          # branch off main; one pull request per logical change
# edit the relevant *-src/ shard, plus patterns/<id>.md for a new pattern
make build                       # rebuild derived artifacts from source
make check                       # lint + drift — this is exactly what CI runs
```

`make check` must be green before you push. It needs Python 3.12+ and `pip install jsonschema`.

## Four ways to contribute

Each maps to a file that holds catalog state. Pick the one that matches what you are doing; [`docs/contributing.md`](docs/contributing.md) covers each in full.

- **Add a new pattern.** Add the entry to `patterns-src/<category>.json`, add the `patterns/<id>.md` page, add reciprocal related-pattern edges on the entries you link to, and add a `verification-todo.json` row with every aspect set to `todo`.
- **Amend a pattern, composition, or code example.** Prose tightening, new known uses, corrected references, extra edges, and added variants are all welcome without an issue first. Schema changes and category renames need an issue first.
- **Suggest a pattern without authoring it.** Append a candidate to `pattern-todo.json` naming the id, the name, and `raised_by[]` evidence. Someone can author it later.
- **Flag something for re-checking.** Set the affected aspect in `verification-todo.json` to `fail` (or back to `todo`) with a dated note, so the catalog can be re-verified item by item.

Not ready to open a pull request? Open an issue instead — the [pattern proposal form](https://github.com/agentpatternscatalog/patterns/issues/new?template=1-pattern-proposal.yml) collects the same fields a maintainer needs, and a proposal with good evidence is genuinely useful even if you never write the entry.

## Style

- Sentences over bullet lists in the prose slots (Intent, Context, Problem, Solution). Intent is exactly one sentence.
- Write "the model" or "the LLM" — never "the AI." The linter enforces this (A8).
- Plain, simple language in every reader-facing section: short sentences, one idea each, the common word over the specialist one. Rule A17 fails the build on AI-slop and overcomplex wording (`utilize`, `holistic`, `delve`, `streamline`, `it's not just X, it's Y`, sentence-initial `Moreover`/`Furthermore`, and similar).
- No emoji. No hype words.
- Call them **anti-patterns** — never "named failures" or "common pitfalls."

## Pull requests

Short, declarative titles: `Add Foo Bar pattern`, `Fix references on Cross-Encoder Reranking`, `Mark 12 patterns verified`. The [pull request template](.github/pull_request_template.md) carries the pre-flight checklist.

**Do not add AI co-author trailers.** All commits are authored solely by Marco Nissen. If you used an agent to help draft a contribution, that is fine — just leave the trailers out.

## License

[CC BY 4.0](LICENSE). By contributing you license your contribution to match.
