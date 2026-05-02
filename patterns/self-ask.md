# Self-Ask

**Also known as:** Decompose-Ask, Sub-Question Prompting

**Category:** Reasoning  
**Status in practice:** mature

## Intent

Have the model emit explicit follow-up sub-questions, answer them (optionally via search), then compose the final answer.

## Context

Multi-hop questions where the model knows each single hop but fails to chain hops in one inference.

## Problem

The 'compositionality gap': models know each fact in isolation but fail to combine them into a multi-hop answer.

## Forces

- Sub-question quality bounds the answer quality.
- Sub-question slots invite tool integration but add latency.
- Excessive decomposition wastes calls.


## Applicability

**Use when**

- The task is multi-hop and the model knows each hop in isolation.
- Compositionality gaps cause the model to skip combining facts.
- Sub-questions can be answered by the model or a search tool.

**Do not use when**

- Single-hop questions where decomposition adds latency without lift.
- The sub-questions cannot be answered cleanly and would compound errors.
- Latency budget cannot afford the extra inference per sub-question.

## Solution

Prompt the model to interleave sub-questions and their answers. Each sub-question is either answered by the model directly or by a search tool. The final answer is composed once all sub-questions are answered.

## Variants

- **Self-Ask (model-only)** — Sub-questions are answered by the same model from its parametric memory.
- **Self-Ask + Search** — Each sub-question is delegated to a web/search tool whose answer is spliced back into the trace.
- **Self-Ask + RAG** — Sub-questions are answered by a retrieval pipeline over a private corpus rather than the open web.

## Example scenario

A QA agent fails on multi-hop questions like 'which of the founder's PhD advisors won a Turing Award?' even though it knows each fact. The team prompts it to emit explicit follow-up sub-questions ('who was the founder's PhD advisor?', 'did that person win a Turing Award?'), answer each via search, then compose. Multi-hop accuracy jumps because the compositionality gap is closed by externalising the steps the model otherwise short-circuits.

## Consequences

**Benefits**

- Bridges CoT and tool-using agents naturally.
- Decomposition is lexical and inspectable.

**Liabilities**

- Latency: N sub-question calls per question.
- Sub-questions can drift from the original.

## What this pattern constrains

Sub-question slots are the only insertion point for retrieval or tool calls; the agent cannot retrieve except through a sub-question.

## Known uses

- **Self-Ask + Search** — *Available*

## Related patterns

- *generalises* → [react](react.md)
- *complements* → [least-to-most](least-to-most.md)

## References

- (paper) Press, Zhang, Min, Schmidt, Smith, Lewis, *Measuring and Narrowing the Compositionality Gap in Language Models*, 2022, <https://arxiv.org/abs/2210.03350>

**Tags:** reasoning, decomposition, multi-hop
