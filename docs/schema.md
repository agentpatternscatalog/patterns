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
| `therefore` | string | One-sentence Alexandrian bridge from forces to solution |
| `solution` | string | How the pattern resolves the forces, recipe-level |
| `consequences` | { benefits, liabilities } | Trade-offs |
| `constrains` | string | What the pattern *forbids* the LLM from doing |
| `example_scenario` | string | 2-4 sentence plain-English narrative of a concrete situation where this pattern fits |
| `applicability` | { use_when[], do_not_use_when[] } | Decision-style bullets for when (not) to reach for this pattern |
| `diagram` | { type, mermaid } | Mermaid source rendered by Pages and natively on GitHub |
| `known_uses` | array | Systems shipping the pattern, each with status |
| `related` | array | Typed cross-pattern edges |
| `references` | array | Papers, blogs, docs, repos |
| `status_in_practice` | enum | `mature` / `emerging` / `experimental` / `deprecated` |

## Optional reader-view slots (backfill in progress)

These slots feed sections 6, 7, and 10 of the [reader-view template](#reader-view-10-section-template). They are optional in the schema but enforced as count-based gaps by lint rule A16; the catalog is being backfilled over time.

| Slot | Shape | Renders as | Notes |
|---|---|---|---|
| `components` | string[] | Section 6 — Components | One named participant per item ("Planner — produces a numbered plan"). Falls back to `solution` prose when absent. |
| `tools` | string[] | Section 7 — Tools | External APIs / capabilities the agent uses under this pattern. Empty for patterns that don't involve tools. |
| `guardrails` | string[] | Section 8 — Guardrails (secondary) | Secondary checks alongside the primary `constrains` statement (input validation, output filters, kill switches). |
| `failure_modes` | string[] | Section 9 — Failure Modes | Explicit failure-mode catalogue; merged with `consequences.liabilities[]` at render time. |
| `evaluation_metrics` | string[] | Section 10 — Evaluation Metrics | How to measure the pattern is working in production. |

## Reader-view (10-section) template

The Pages site renders every pattern as a fixed 10-section reader view. The numbered headers are deliberately plain — no GoF/POSA jargon — so a reader can scan any pattern the same way. The canonical JSON entry still uses the Alexandrian slot names (`intent`, `context`, `forces`, `therefore`, `solution`, `consequences`, `constrains`, ...) — the reader view is a projection of those slots, not a replacement.

| # | Section | Source slot(s) |
|---|---|---|
| 1 | Pattern Name | `name` (H1) + `intent` and `example_scenario` as the lede (no header) |
| 2 | Problem | `context` + `problem` (+ `forces[]` if present) |
| 3 | When to Use | `applicability.use_when[]` |
| 4 | When Not to Use | `applicability.do_not_use_when[]` |
| 5 | Architecture Diagram | `diagram.mermaid` (rendered) — `structure` ASCII fallback |
| 6 | Components | `components[]` (named participants); falls back to `solution` prose when not yet enumerated |
| 7 | Tools | `tools[]` (external APIs / capabilities the agent uses) |
| 8 | Guardrails | `constrains` (the primary restriction, highlighted) + `therefore` + optional `guardrails[]` |
| 9 | Failure Modes | `failure_modes[]` + `consequences.liabilities[]` (merged) |
| 10 | Evaluation Metrics | `evaluation_metrics[]` |

Below the 10 sections, the rendered page carries an *appendix* (smaller, de-emphasised) with the canonical end matter: expected benefits, variants, known uses, related patterns, references.

Sections 1–5 and 8–9 are hard requirements enforced by lint rule A16. Sections 6, 7, and 10 are backfill-in-progress: lint reports a count-per-section gap rather than per-pattern violations, so the report stays readable while the catalog catches up.

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
