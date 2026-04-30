# Chain of Thought

**Also known as:** CoT, Step-by-Step Prompting

**Category:** Reasoning  
**Status in practice:** mature

## Intent

Elicit multi-step reasoning by prompting the model to produce intermediate steps before its final answer.

## Context

The task is compositional, arithmetic, or otherwise requires working through several inferences a human would write down.

## Problem

LLMs given only (input, output) exemplars fail at problems whose answers depend on a sequence of intermediate inferences.

## Forces

- Longer outputs cost more.
- Wrong reasoning chains can produce confidently wrong answers.
- Few-shot exemplars are dataset-specific; zero-shot triggers generalise but lose accuracy.

## Solution

Prompt the model with exemplars showing intermediate reasoning, or use a zero-shot trigger ('Let's think step by step') before answering. The reasoning trace is visible and parseable.

## Consequences

**Benefits**

- Substantial accuracy gains on reasoning benchmarks.
- Reasoning trace is inspectable for debugging.

**Liabilities**

- Single linear trace; no branching or self-correction.
- Cost scales with trace length.

## What this pattern constrains

The model is required to emit reasoning before the final answer; one-shot answer-only generation is forbidden by prompt design.

## Known uses

- **OpenAI Reasoning prompts** — *Available*
- **Most production agents (CoT inside system prompts)** — *Available*

## Related patterns

- *complements* → [self-consistency](self-consistency.md)
- *generalises* → [tree-of-thoughts](tree-of-thoughts.md)
- *alternative-to* → [least-to-most](least-to-most.md)
- *complements* → [extended-thinking](extended-thinking.md)
- *generalises* → [zero-shot-cot](zero-shot-cot.md)
- *used-by* → [scratchpad](scratchpad.md)
- *used-by* → [star-bootstrapping](star-bootstrapping.md)

## References

- (paper) Wei, Wang, Schuurmans, Bosma, Ichter, Xia, Chi, Le, Zhou, *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*, 2022, <https://arxiv.org/abs/2201.11903>
- (paper) Kojima, Gu, Reid, Matsuo, Iwasawa, *Large Language Models are Zero-Shot Reasoners*, 2022, <https://arxiv.org/abs/2205.11916>

**Tags:** reasoning, cot, prompting
