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

The `constrains` slot in the schema is required-by-convention even though the schema marks it optional. A pattern that does not constrain the LLM's freedom is decoration. Examples of valid constraints:

- "JSON Schema rejects edits the model invents outside the toolkit."
- "Charter is read-only at the tool layer; the agent cannot rewrite it."
- "Step budget halts the loop after N tool calls regardless of progress."
- "Frozen rubric forbids the reviewer model from inventing new finding categories."

## How to propose a pattern

1. Open an issue with a one-paragraph statement of the problem and at least one Known Use.
2. If accepted, open a PR adding:
   - an entry in `patterns.json` validating against `schema.json`,
   - a `patterns/<id>.md` page generated from the entry,
   - any new related-pattern edges in existing entries.
3. Maintainer review focuses on the three rules above and on naming. We prefer the canonical literature name where one exists, with the alternative as an alias.

## How to amend an existing pattern

PRs welcome. Schema changes and category renames go through an issue first.

## Style

- Sentences over bullet lists in the prose slots (Intent, Context, Problem, Solution).
- One sentence in Intent. If you cannot say it in one sentence, the pattern is probably two patterns.
- "The model" or "the LLM" — not "the AI."
- No emoji. No hype words. Plain technical English.

## License

By contributing you agree the contribution is licensed under CC BY 4.0 (content) and MIT (schema/tooling), matching the repository.
