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

## Solution

Prompt the model to interleave sub-questions and their answers. Each sub-question is either answered by the model directly or by a search tool. The final answer is composed once all sub-questions are answered.

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
