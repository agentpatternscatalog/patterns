# Schema

Every entry in `patterns.json` validates against `schema.json` (JSON Schema draft 2020-12).

## Required slots

| Slot | Shape | Notes |
|---|---|---|
| `id` | kebab-case string | Stable identifier; also the `patterns/<id>.md` filename |
| `name` | string | Canonical human-readable name |
| `aliases` | string[] | Synonyms / Also-Known-As — covers vocabulary from neighbour catalogs |
| `category` | enum | One of the 13 buckets in [taxonomy.md](taxonomy.md) |
| `intent` | string | One sentence stating what the pattern accomplishes |
| `context` | string | The situation in which the problem recurs |
| `problem` | string | The recurring problem the pattern solves |
| `forces` | string[] | Competing constraints that make the problem hard |
| `solution` | string | How the pattern resolves the forces, recipe-level |
| `consequences` | { benefits, liabilities } | Trade-offs |
| `constrains` | string | What the pattern *forbids* the LLM from doing |
| `known_uses` | array | Systems shipping the pattern, each with status |
| `related` | array | Typed cross-pattern edges |
| `references` | array | Papers, blogs, docs, repos |
| `status_in_practice` | enum | `mature` / `emerging` / `experimental` / `deprecated` |

## Known-use status

- `available` — running in production today
- `planned` — on the immediate roadmap
- `pure-future` — interesting on paper, not on the roadmap
- `not-pursued` — deliberate non-choice

## Related-edge relations

`uses`, `used-by`, `specialises`, `generalises`, `complements`, `alternative-to`, `composes-with`, `conflicts-with`.

Inverses are kept symmetric: if A `specialises` B, then B `generalises` A. The catalog is post-processed so every directional edge has its inverse on the target.

## Constraint-first framing

Every pattern declares what it *forbids* the LLM from doing. A pattern that does not constrain the model is decoration. Examples:

- **Tool Use:** "The model cannot affect state except through a registered tool with a typed signature."
- **Frozen Rubric Reflection:** "The reviewer cannot output finding categories outside the rubric."
- **Constitutional Charter:** "The agent cannot write the charter; updates require explicit operator action."
- **Step Budget:** "The loop terminates after N iterations regardless of agent's own opinion."
