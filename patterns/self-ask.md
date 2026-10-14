# Self-Ask

**Also known as:** Decompose-Ask, Sub-Question Prompting

**Category:** Reasoning  
**Status in practice:** mature

## Intent

Have the model emit explicit follow-up sub-questions, answer them (optionally via search), then compose the final answer.

## Context

A team is using a model on questions whose answer requires chaining several known facts together. For example, 'which of the founder's PhD advisors won a Turing Award?' depends on first knowing who founded the organisation, then who that person's PhD advisors were, then which awards each of those advisors won. The model can answer each individual hop correctly when asked in isolation, but when the question is posed as a single sentence it tends to return the wrong endpoint.

## Problem

Knowing each fact and being able to chain those facts together inside a single inference are different skills; this gap between them is the so-called compositionality gap. Without scaffolding, the model collapses the chain into a single step and either invents an answer or returns the wrong endpoint. Plain chain-of-thought helps a little, but the reasoning steps are not framed as questions, so the model cannot offload any of them to a search tool, and a human reader cannot easily inspect where in the chain the model went wrong.

## Forces

- Sub-question quality bounds the answer quality.
- Sub-question slots invite tool integration but add latency.
- Excessive decomposition wastes calls.

## Therefore

Therefore: have the model interleave explicit follow-up sub-questions and their answers before composing the final answer, so that decomposition is visible and each step is independently tool-able.

## Solution

Prompt the model to interleave sub-questions and their answers. Each sub-question is either answered by the model directly or by a search tool. The final answer is composed once all sub-questions are answered.

## Structure

```
Top question --> Model --> Sub-question 1 --answer directly or via search--> Answer 1 --> Sub-question 2 --> Answer 2 --> ... --> compose final answer from sub-answers
```

## Diagram

```mermaid
flowchart TD
  Q[Top question] --> M[Model]
  M --> SQ1[Sub-question 1]
  SQ1 -->|answer directly<br/>or via search| A1[Answer 1]
  A1 --> SQ2[Sub-question 2]
  SQ2 -->|answer| A2[Answer 2]
  A2 --> Comp[Compose final answer]
```

## Example scenario

A QA agent fails on multi-hop questions like 'which of the founder's PhD advisors won a Turing Award?' even though it knows each fact. The team prompts it to emit explicit follow-up sub-questions ('who was the founder's PhD advisor?', 'did that person win a Turing Award?'), answer each via search, then compose. Multi-hop accuracy jumps because the compositionality gap is closed by externalising the steps the model otherwise short-circuits.

## Consequences

**Benefits**

- Bridges CoT and tool-using agents naturally.
- Decomposition is lexical and inspectable.

**Liabilities**

- Latency: N sub-question calls per question.
- Sub-questions can drift from the original.

## Failure modes

- Drifting sub-questions — the sub-questions wander away from the original question, and the composed answer addresses something else.
- Unanswered gap — the model answers a sub-question from memory when it should have searched, and the invented fact feeds the final answer.
- Latency stack — many sub-questions, each with a search call, make simple questions slow.
- Wrong endpoint — every sub-answer is right, but the final composition picks the wrong one as the answer.

## What this pattern constrains

Sub-question slots are the only insertion point for retrieval or tool calls; the agent cannot retrieve except through a sub-question.

## Applicability

**Use when**

- The task is multi-hop and the model knows each hop in isolation.
- Compositionality gaps cause the model to skip combining facts.
- Sub-questions can be answered by the model or a search tool.

**Do not use when**

- Single-hop questions where decomposition adds latency without lift.
- The sub-questions cannot be answered cleanly and would compound errors.
- Latency budget cannot afford the extra inference per sub-question.

## Components

- LLM — emits the follow-up sub-questions and the final composed answer
- Sub-question parser — detects the 'Follow up:' / 'Intermediate answer:' markers in the trace
- Answer router — sends each sub-question to the model, a search tool, or a retrieval pipeline
- Composer step — assembles the final answer once no more follow-ups are needed

## Tools

- LLM API — one call per sub-question plus the final compose call
- Search or retrieval tool — optional backend that resolves a sub-question against the open web or a private corpus

## Evaluation metrics

- Multi-hop accuracy lift — gain over direct prompting on compositional questions
- Sub-question count per query — depth of decomposition needed to close the gap
- Sub-question drift rate — fraction of follow-ups that wander from the top question, sample-audited
- Tool-grounded share — proportion of sub-questions answered by search or retrieval rather than parametric memory
- End-to-end latency at p95 — wall-clock cost of N sequential sub-question calls

## Known uses

- **Self-Ask + Search** _available_

## Related patterns

- _generalises_ **ReAct**
- _complements_ **Least-to-Most Prompting**
- _complements_ **Socratic Questioning Agent**
- _complements_ **Query-Decomposition Agent**

## References

- [Measuring and Narrowing the Compositionality Gap in Language Models](https://arxiv.org/abs/2210.03350) — Press, Zhang, Min, Schmidt, Smith, Lewis, 2022
