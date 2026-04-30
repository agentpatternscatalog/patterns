# Dynamic Scaffolding

**Also known as:** Adaptive Prompting, Just-in-Time Context

**Category:** Routing & Composition  
**Status in practice:** emerging

## Intent

Inject task-specific scaffolding (examples, hints, schemas) into the prompt only when the task type warrants it.

## Context

Agents handling heterogeneous tasks where always-present scaffolding wastes tokens and sometimes biases outputs.

## Problem

Static prompts either include everything (wasteful, sometimes misleading) or include nothing (under-scaffolded for hard cases).

## Forces

- Detection of when scaffolding helps is itself a problem.
- Scaffolding library curation effort.
- Compositional scaffolding (multiple scaffolds in one prompt) interacts unpredictably.

## Solution

Maintain a library of scaffolds (few-shot examples, schemas, hints) keyed by task type or feature. At runtime, classify the task and inject the matching scaffolds. Audit which scaffolds fired per request.

## Consequences

**Benefits**

- Token efficiency.
- Targeted quality lift on hard cases.

**Liabilities**

- Scaffold library maintenance.
- Misclassification injects wrong scaffolds.

## What this pattern constrains

Scaffolds load only on matching task classification; default tasks see the bare prompt.

## Known uses

- **Avramovic Dynamic Scaffolding pattern** — *Available*
- **DSPy compiled prompts (signature-driven scaffolding)** — *Available*

## Related patterns

- *uses* → [routing](routing.md)
- *complements* → [context-window-packing](context-window-packing.md)
- *complements* → [agent-skills](agent-skills.md)

## References

- (repo) *zeljkoavramovic/agentic-design-patterns*, <https://github.com/zeljkoavramovic/agentic-design-patterns>

**Tags:** prompting, scaffolding, dynamic
