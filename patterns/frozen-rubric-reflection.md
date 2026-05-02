# Frozen Rubric Reflection

**Also known as:** Scoped Self-Review, Closed-Set Critic

**Category:** Verification & Reflection  
**Status in practice:** emerging

## Intent

Constrain reflection to a fixed, hand-authored rubric of criteria so the reviewer cannot invent new ones each run.

## Context

Open-ended reflection drifts pattern over pattern; the reviewer's criteria change with the wind, making outputs hard to compare across runs or users.

## Problem

Free-form 'review your work' produces inconsistent reviews because the model invents categories on each call.

## Forces

- Authoring a good rubric is non-trivial up-front work.
- Rubric drift over time is a separate problem from per-call drift.
- Some defects fall outside the rubric and go unflagged.

## Solution

A fixed rubric file (or schema) lists exactly the categories the reviewer may flag. The reviewer prompt includes the rubric and a JSON Schema enforcing it. Temperature is zero. Output validates against the schema; new finding categories are rejected.

## Consequences

**Benefits**

- Consistent reviews across runs and users.
- Rubric is the single load-bearing artefact; iteration is in one place.

**Liabilities**

- Hard ceiling on what the reviewer can catch.
- Rubric authorship is its own engineering discipline.

## What this pattern constrains

The reviewer cannot output finding categories outside the rubric; the JSON schema rejects them.

## Known uses

- **Knitting-DSL Pipeline (Stash2Go)** — *Available*. Six-item rubric in scopedLlmReviewer.js: duplicate NOTEs, finishing order, construction voice, prose omissions, prose inventions, pattern name sanity.

## Related patterns

- *specialises* → [reflection](reflection.md)
- *uses* → [structured-output](structured-output.md)
- *composes-with* → [deterministic-llm-sandwich](deterministic-llm-sandwich.md)
- *complements* → [dream-consolidation-cycle](dream-consolidation-cycle.md)

## References

- (blog) *Marco Nissen, Working with the models*, 2026

**Tags:** reflection, rubric, structured-output
