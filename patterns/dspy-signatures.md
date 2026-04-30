# DSPy Signatures

**Also known as:** Prompt Programs, Compiled Prompts

**Category:** Structure & Data  
**Status in practice:** emerging

## Intent

Specify agent behaviour as declarative typed signatures and modules; compile prompts and few-shot examples automatically against a metric.

## Context

Building reliable agent pipelines without hand-crafting prompts; treating prompts as the output of a compiler over typed specifications.

## Problem

Hand-crafted prompts are brittle, model-specific, and drift over time; teams reinvent the same prompt-engineering loop per pipeline.

## Forces

- Declarative coverage vs signature expressivity ceiling.
- Compile-time optimization vs metric/data availability.
- Portability vs per-model compilation gains.

## Solution

Define each step as a typed signature (input fields → output fields). Compose signatures into modules. Run a teleprompter (optimizer) that generates few-shot examples and refines instructions against a held-out metric. The compiled artefact replaces hand-tuned prompts.

## Consequences

**Benefits**

- Prompts become a reproducible build artefact.
- Metric-driven optimisation replaces vibes-based prompting.

**Liabilities**

- Compilation requires labelled or auto-evaluable data.
- Compiled artefacts drift with model upgrades; recompile regularly.

## What this pattern constrains

Module behaviour is constrained by its declared signature; ad-hoc string manipulation is replaced by typed input/output fields.

## Known uses

- **[Stanford DSPy](https://github.com/stanfordnlp/dspy)** — *Available*
- **DSPy production deployments at Replit, Databricks, Klarna** — *Available*

## Related patterns

- *uses* → [structured-output](structured-output.md)
- *uses* → [eval-harness](eval-harness.md)
- *complements* → [agent-skills](agent-skills.md)

## References

- (paper) Khattab, Singhvi, Maheshwari, Zhang, Santhanam, Vardhamanan, Haq, Sharma, Joshi, Moazam, Miller, Zaharia, Potts, *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*, 2023, <https://arxiv.org/abs/2310.03714>

**Tags:** prompt-programs, dspy, compilation
