<!--
  Short, declarative title, e.g. "Add Step Budget Governor pattern",
  "Fix references on Cross-Encoder Reranking", "Mark 12 patterns verified".
  Full rules: CONTRIBUTING.md and docs/contributing.md.
-->

## What this changes

<!-- One or two sentences. Name the pattern/composition ids touched. -->

## Type of change

- [ ] New pattern or anti-pattern
- [ ] Amendment to an existing entry (prose, references, known uses, edges, variants)
- [ ] New or amended composition (`recipe` or `framework`)
- [ ] New or amended code example
- [ ] Pattern candidate added to `pattern-todo.json`
- [ ] Verification status update
- [ ] Docs or tooling

## Checklist

Every pull request:

- [ ] I edited only `*-src/` shards and `patterns/<id>.md` — no hand-edits to the derived files (`patterns.json`, `patterns.graph.json`, `patterns.compositions.json`, `compositions.json`, `examples.json`, `INDEX.md`, `dist/`).
- [ ] I kept the compact JSON formatting in the shards; I did not reserialize a whole file.
- [ ] `make build` was run, so the derived artifacts match the source.
- [ ] `make check` passes locally (lint plus drift — this is exactly what CI runs).
- [ ] Prose follows the style rules: one-sentence intent, sentences over bullets, "the model" / "the LLM" rather than "the AI", no emoji, no hype words, plain simple language.
- [ ] No AI co-author trailers in any commit.

For a **new pattern**, additionally:

- [ ] Entry added to the correct `patterns-src/<category>.json` shard and validates against `schema.json`.
- [ ] All hard-required slots are present (rule A16): `intent`, `example_scenario`, `context`, `problem`, `applicability.use_when`, `applicability.do_not_use_when`, `diagram.mermaid`, `constrains`, and at least one of `consequences.liabilities` / `failure_modes`.
- [ ] `constrains` names something concrete the model is forbidden to do.
- [ ] At least one reference to a paper, a shipping product, or an open repository — and `known_uses` is not empty.
- [ ] `patterns/<id>.md` page added.
- [ ] Related-pattern edges added **on both sides** — the entries I link to also link back.
- [ ] A `verification-todo.json` row exists for the new id, with aspects starting at `todo`.

For a **framework composition**, additionally:

- [ ] Every member pattern carries evidence: a live URL plus a short quote that shows the framework actually implements it.

## Evidence

<!--
  Links backing new or changed claims: papers with authors and year, product docs, repositories.
  For a framework composition, the per-pattern evidence quotes.
-->

---

By opening this pull request you license the contribution under [CC BY 4.0](../LICENSE), matching the repository.
