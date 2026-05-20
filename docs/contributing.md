# Contributing

This catalog is opinionated about what counts as a pattern. Three rules.

## 1. A pattern must name a recurring problem

Not a feature, not a framework, not a library. A problem that shows up across products, frameworks, and years.

If you cannot finish the sentence "this is the pattern for when *...*" without naming a specific vendor, it is probably not yet a pattern. It might be a technique. We are happy to discuss it; it is not in the catalog.

## 2. A pattern must reference at least one of

- a paper (linked, with authors and year),
- a publicly visible product that ships it,
- a working open repository.

No pattern is admitted on speculation alone. The Known Uses slot exists for a reason.

## 3. Every pattern declares what it constrains

The `constrains` slot is required-by-convention even though the schema marks it optional. A pattern that does not constrain the LLM's freedom is decoration. Examples of valid constraints:

- "JSON Schema rejects edits the model invents outside the toolkit."
- "Charter is read-only at the tool layer; the agent cannot rewrite it."
- "Step budget halts the loop after N tool calls regardless of progress."
- "Frozen rubric forbids the reviewer model from inventing new finding categories."

## Where catalog state lives

Four files (or directories) hold all contributor-editable state. Pick the one that matches what you are doing.

- `patterns-src/` — one JSON shard per category. Source of truth for every pattern. Validated against [`schema.json`](../schema.json).
- `patterns/<id>.md` — one Markdown page per pattern, generated alongside the JSON entry.
- `compositions-src/` — one JSON shard per composition family. Holds both `kind: recipe` (abstract design templates) and `kind: framework` (real shipping software, with per-pattern evidence). Validated against [`compositions.schema.json`](../compositions.schema.json).
- `pattern-todo.json` — proposed pattern candidates that have not yet been authored. Validated against [`pattern-todo.schema.json`](../pattern-todo.schema.json).
- `verification-todo.json` — per-aspect verification status for every pattern and composition. Validated against [`verification-todo.schema.json`](../verification-todo.schema.json).

The built artefacts (`patterns.json`, `INDEX.md`, `patterns.graph.json`) are derived from `patterns-src/` and should not be hand-edited.

## Four ways to contribute

### A. Add a new pattern

1. Open an issue (or a draft PR) with a one-paragraph statement of the problem and at least one Known Use.
2. Branch off `main`. Add the entry to the appropriate `patterns-src/<category>.json` shard, validating against `schema.json`.
3. Add the corresponding `patterns/<id>.md` page.
4. Add any new related-pattern edges in existing entries.
5. Add a matching entry in `verification-todo.json` (all aspects start as `todo`).
6. Open a PR. Maintainer review focuses on the three rules above and on naming. We prefer the canonical literature name where one exists, with the alternative as an alias.

### B. Amend an existing pattern or composition

PRs welcome for prose tightening, new Known Uses, corrected references, additional related-pattern edges, and added variants. Branch, commit, PR. Schema changes and category renames go through an issue first.

### C. Suggest a pattern without authoring it yet

If you spotted a candidate while researching a composition but cannot yet write the full entry, append it to `pattern-todo.json`. Required fields: kebab-case `id`, human-readable `name`, `summary`, and `raised_by[]` with at least one composition id and upstream evidence (URL + quote). Status starts at `proposed`, moves to `drafting` when someone is authoring it, and to `authored` (then the candidate is deleted from this file) when the pattern lands in `patterns-src/`. Use `rejected` with a `rejected_reason` if the team decides not to pursue it.

### D. Flag an issue that needs systematic re-checking

`verification-todo.json` is how the catalog stays honest over time. Every pattern carries a fixed set of aspects (intent one sentence, references live, edges correct, …) and every composition carries an aspect set specific to its kind (recipe vs. framework). Aspect values: `todo`, `pass`, `fail`, `na`. Top-level `verified` is true only when every applicable aspect is `pass` or `na`. The full aspect list lives in `verification-todo.json`'s `aspect_definitions` block.

If you check an aspect and find it correct, set it to `pass` and add a dated note. If you find it broken, set it to `fail`, add a dated note explaining what is wrong, and either fix it in the same PR or leave it for someone else to fix. Setting an aspect back to `todo` is fine when an upstream change (a moved URL, a renamed framework) invalidates a previous `pass`.

The `last_analysis_date` field at the top of the file should be bumped whenever the file is edited.

## Workflow

- Branch off `main`. One PR per logical change.
- Validate JSON locally before pushing (any draft 2020-12 validator works; the schemas are in the repo root).
- PR titles are short and declarative (`Add Foo Bar pattern`, `Fix references on Cross-Encoder Reranking`, `Mark 12 patterns verified`).

## Style

- Sentences over bullet lists in the prose slots (Intent, Context, Problem, Solution).
- One sentence in Intent. If you cannot say it in one sentence, the pattern is probably two patterns.
- "The model" or "the LLM" — not "the AI."
- No emoji. No hype words. Plain technical English.
- Anti-patterns are called *anti-patterns*, not "named failures" or "common pitfalls."

## License

By contributing you agree the contribution is licensed under CC BY 4.0, matching the repository. Do not add AI co-author trailers — all commits are authored solely by Marco Nissen.
