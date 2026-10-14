# Attentive Reasoning Queries

**Also known as:** ARQs, Reasoning Blueprint, Structured Reasoning Queries

**Category:** Reasoning  
**Status in practice:** emerging

## Intent

Replace free-form chain-of-thought with a domain-tailored sequence of structured queries that re-anchor the model's attention to the critical instructions and prior decisions at the exact generation steps where adherence tends to slip.

## Context

A team runs a customer-facing agent that must follow a large body of use-case-specific instructions — eligibility rules, escalation policies, things it must never say — across long multi-turn conversations. The agent reasons before each reply, usually with chain-of-thought. As the conversation grows and the instructions accumulate, the model starts to drift: it forgets a guideline it applied correctly three turns ago, or it asserts a fact under conversational pressure, even though the rule that should have stopped it was in its context the whole time.

## Problem

Free-form chain-of-thought lets the model decide what to reason about, and on long instruction-heavy conversations that freedom is the failure: the steps that matter most — re-checking a guideline, confirming a value the user gave earlier, refusing to assert an unverified fact — are exactly the steps the model is most likely to skip when the context is crowded. Because the reasoning is unstructured prose, there is also no fixed place to check that a given instruction was actually considered; an auditor cannot tell from the trace whether the model weighed the escalation rule or simply never looked at it. The instruction sits in the context window but never becomes a token the model is forced to attend to at the decision point.

## Forces

- The model attends unevenly across a long context, so instructions far from the generation point lose salience.
- Free-form reasoning is flexible but unconstrained, which leaves the critical step optional.
- Hand-authoring a reasoning script per use case is upfront work that generic chain-of-thought avoids.
- A structured trace is machine-checkable, but over-scripting reasoning can suppress the model's own problem-solving.

## Therefore

Therefore: author a domain-specific blueprint of targeted queries that the model must answer in sequence before it acts, reinstating each critical instruction and prior decision at the step where it is needed, so adherence is forced rather than left to the model's discretion.

## Solution

For each decision point, author a blueprint — a fixed sequence of queries, typically emitted and answered as JSON fields — that walks the model through the reasoning the use case requires. Early queries reinstate the instructions and facts that matter here, such as restating the active guideline or recalling a value the customer gave; intermediate queries have the model commit to checkable sub-conclusions, such as whether the case meets the eligibility rule or whether the user has been verified; the final query produces the action conditioned on those answers. The queries fire at the points where the model historically slips, re-anchoring attention to the relevant instruction just before generation. Because every step is a named field, the trace is machine-checkable: a downstream guard can confirm the eligibility query was answered before the approval was emitted. Author blueprints per use case and keep them as narrow as the failure modes demand.

## Structure

```
User turn --> match relevant guidelines --> reasoning blueprint (JSON fields in order): Q1 restate active guideline --> Q2 recall verified facts --> Q3 commit to checkable sub-conclusion --> action gate: required answers present? --no--> withhold or re-query | --yes--> emit action
```

## Diagram

```mermaid
flowchart TD
  Q[User turn] --> M[Match guidelines relevant to this turn]
  M --> B{Reasoning blueprint}
  B --> Q1[Q1 restate active guideline]
  Q1 --> Q2[Q2 recall verified facts]
  Q2 --> Q3[Q3 checkable sub-conclusion]
  Q3 --> G{Action gate: required answers present?}
  G -->|no| H[Withhold or re-query]
  G -->|yes| A[Emit action]
```

*A fixed query sequence re-anchors instructions before the action; a gate releases the action only once the required answers are present.*

## Example scenario

A bank's support agent must verify a customer's identity before discussing account details and must escalate any mention of fraud, across conversations that run dozens of turns. With plain chain-of-thought it occasionally discusses balances before verification or misses a fraud cue buried in a long message, because those checks compete with everything else in its free-form reasoning. The team adds an attentive-reasoning-queries blueprint: before each reply the model answers a fixed sequence — is the customer verified? did this turn mention fraud? which guideline applies here? — as JSON fields, and a guard refuses any account-detail action whose verification field is false. The drift stops, and every reply now carries a checkable record of which rules the model considered.

## Consequences

**Benefits**

- Critical instructions are re-anchored at the decision point, so guideline re-application and instruction-following hold up over long conversations.
- Each reasoning step is a named field, so the trace is machine-checkable and a guard can gate the action on specific answers.
- Targeting queries at known failure points can cost fewer tokens than free-form reasoning over the whole context.
- Hallucination drops when an explicit query forces the model to confirm a fact before asserting it.

**Liabilities**

- Each use case needs a hand-authored blueprint, and that design work does not transfer across domains.
- An over-prescribed blueprint can box the model in, suppressing reasoning the designer did not anticipate.
- Blueprints drift from the instructions they encode as policies change, and a stale query re-anchors the wrong rule.
- The approach assumes the designer can enumerate the decision points where adherence slips; novel failure modes are uncovered until a query is added for them.

## Failure modes

- Stale blueprint — a query re-anchors an instruction that policy has since changed, so the model adheres to the wrong rule
- Over-scripting — the blueprint forecloses reasoning the task needed and the model cannot route around it
- Uncovered failure point — a decision point with no query still drifts, since the blueprint only protects what it names
- Field-without-thought — the model fills a query field with a rote answer it does not actually condition the action on

## What this pattern constrains

The model may not emit the final action until it has answered the blueprint's queries in order; it cannot substitute its own free-form reasoning path for the prescribed one, and a step the blueprint demands cannot be silently skipped.

## Guardrails

- Gate the action on specific query answers — refuse to emit the approval until the eligibility query is answered
- Validate the blueprint output against its field schema before any field is consumed

## Applicability

**Use when**

- The agent must follow many use-case-specific instructions across long multi-turn conversations where free-form reasoning drifts.
- Specific failure points are identifiable — a guideline that gets dropped, a fact that gets hallucinated — and can be targeted with a query.
- The reasoning trace needs to be machine-checkable so a downstream guard can gate the action.
- The domain is stable enough that authoring and maintaining a reasoning blueprint pays off.

**Do not use when**

- The task is one-shot or short, where instruction drift across turns is not the problem.
- The problem space is open-ended and a fixed query sequence would constrain reasoning the model needs to do freely.
- No one can enumerate the decision points that matter, so there is nothing specific to anchor.
- Generic chain-of-thought already meets the reliability bar and the blueprint maintenance cost is not justified.

## Components

- Reasoning blueprint — the authored, ordered set of queries the model must answer for a given decision point
- Query emitter — prompts the model to produce each query's answer, typically as a named structured field
- Instruction reinstatement step — early queries that restate the active guidelines and recalled facts so they regain salience
- Checkable sub-conclusions — intermediate queries whose answers a guard can verify before the action is allowed
- Action gate — releases the final action only after the required queries have been answered

## Tools

- LLM — answers the blueprint queries and produces the final action
- Structured-output decoder — enforces the JSON field schema for each reasoning step
- Guideline matcher — selects the instructions relevant to the current turn that the blueprint should re-anchor, as in Parlant's per-turn matching

## Evaluation metrics

- Instruction-following success rate — share of scenarios where every applicable guideline was honoured, against a chain-of-thought baseline
- Guideline re-application rate — how often a rule applied earlier is correctly re-applied later in the same conversation
- Hallucination rate — fraction of replies asserting a fact the blueprint should have forced the model to confirm
- Query-answer coverage — share of actions emitted only after their required queries were answered
- Token cost per turn — overhead of the blueprint versus free-form reasoning over the full context

## Known uses

- **[Parlant (emcie-co/parlant)](https://github.com/emcie-co/parlant)** _available_ — Open-source framework for reliable customer-facing agents where ARQs originated; the engine matches the guidelines relevant to each turn and walks the model through structured reasoning queries before it generates a response.

## Related patterns

- _alternative-to_ **Chain of Thought** — Chain-of-thought lets the model reason free-form; ARQs prescribe a domain-tailored query sequence that re-anchors attention to the instructions that matter.
- _composes-with_ **Structured Output** — The blueprint's queries are emitted as structured fields, so structured output is the mechanism that makes each reasoning step individually checkable.
- _alternative-to_ **Tree of Thoughts** — Tree-of-thoughts widens reasoning into a search over branches; ARQs narrow it into a prescribed, checkable sequence.
- _composes-with_ **ReAct** — ARQs can structure the reasoning step inside a ReAct loop so each think phase follows the blueprint.
- _complements_ **Standing State Injection** — ARQs re-anchor attention via a fixed query sequence inside the model's reasoning; standing-state-injection re-anchors it via a harness-computed state block placed ahead of reasoning.
- _complements_ **Set-and-Forget System Prompt** — Re-anchors the model's attention on the critical instructions at reasoning time, which is a direct in-model remedy for the decay named here.

## References

- [Attentive Reasoning Queries: A Systematic Method for Optimizing Instruction-Following in Large Language Models](https://arxiv.org/abs/2503.03669) — Karov, Zohar, Marcovitz, 2025
- [Parlant — framework for reliable customer-facing agents](https://github.com/emcie-co/parlant)
