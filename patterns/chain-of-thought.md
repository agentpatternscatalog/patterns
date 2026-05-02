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

## Variants

- **Few-shot CoT** — Provide exemplars with full reasoning traces in the prompt; the model imitates the trace format on the new instance (Wei et al. 2022).
- **Zero-shot CoT** — Skip exemplars; trigger reasoning with a phrase like 'Let's think step by step' (Kojima et al. 2022).
- **Self-consistency CoT** — Sample many CoT traces at temperature, then take the majority-vote answer rather than the first trace (Wang et al. 2023).
- **Auto-CoT** — Automatically construct exemplars by clustering questions and generating zero-shot CoT for each cluster representative (Zhang et al. 2022).

## Example scenario

A maths-tutoring assistant keeps blurting wrong answers to multi-step word problems because it tries to jump straight from 'Maria has...' to a single number. The team adds Chain-of-Thought prompting with a few worked exemplars, asking the model to write out each intermediate quantity before stating the final answer. Accuracy on the same problem set improves substantially because the answer now depends on reasoning steps the model can attend to one at a time, instead of being collapsed into a single output token.

## Consequences

**Benefits**

- Substantial accuracy gains on reasoning benchmarks.
- Reasoning trace is inspectable for debugging.

**Liabilities**

- Single linear trace; no branching or self-correction.
- Cost scales with trace length.

## What this pattern constrains

The model is required to emit reasoning before the final answer; one-shot answer-only generation is forbidden by prompt design.

## Applicability

**Use when**

- The task requires multi-step reasoning that single-shot answers fail at.
- Either exemplars with reasoning traces or a zero-shot trigger ('think step by step') are easy to add.
- The reasoning trace is useful as a debug or audit artefact.

**Do not use when**

- The task is direct lookup or pattern completion where reasoning steps add no quality.
- Latency or token budget cannot absorb the longer outputs.
- A reasoning model is in use that already runs internal chain-of-thought (use extended-thinking instead).

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
