# Over-Helpfulness

**Also known as:** Helpfulness Bias, Answer-Anyway Failure

**Category:** Anti-Patterns  
**Status in practice:** emerging

## Intent

Anti-pattern: the agent prioritises responsiveness and task completion over correctness, producing confident output for a request beyond its capability or scope instead of abstaining, clarifying, or handing off.

## Context

An assistant or tool-using agent is tuned and rewarded to be helpful, and most of its training signal favours a complete, fluent answer over a hedge or a decline. The agent meets requests that fall outside its declared tools, its knowledge cutoff, or its policy boundary, and it has no built-in check that compares the request against what it can actually do. Users read a fluent answer as a competent one, so a wrong-but-confident reply is rarely challenged at the point of use.

## Problem

An agent that always answers will answer even when it should not. When a request needs a tool the agent lacks, a fact it cannot verify, or an action outside its mandate, the helpful default is to attempt it anyway and present the result as if it were reliable. The failure is silent: there is no abstention signal, the output looks like every correct output, and the cost lands downstream when someone acts on a fabricated answer or an out-of-scope action. The agent never weighs whether the task is one it is fit to complete.

## Forces

- Helpfulness reward and completion bias push the agent toward answering, while correctness needs it to sometimes decline; the two pull in opposite directions.
- Abstaining looks like failure to a user who wanted an answer, so the easy local choice is to answer and the costly choice is to hold back.
- The agent rarely has an explicit signal for the edge of its own capability, so it cannot tell an in-scope request from one it should refuse.

## Therefore

This is the anti-pattern to avoid. The corrective is to give the agent an explicit capability-and-scope check that gates answering, so it abstains, clarifies, or hands off when a request falls outside what it can reliably do.

## Solution

Recognise the smell first: the agent produces a fluent, confident answer for requests it has no means to satisfy, never returns a calibrated 'I cannot do this', and its error rate climbs sharply on out-of-scope inputs while its expressed confidence does not. To remove it, place a gate before the answer that compares the request against the agent's declared tools, knowledge boundary, and policy, and route requests that fail the gate to abstention, a clarifying question, or a handoff to a capable agent or a human. Make abstaining a first-class, rewarded outcome rather than a hidden failure, and surface a machine-readable reason so callers can route on it. The named cures in the catalog are an explicit self-model, scoped refusal, and typed refusal codes.

## Structure

```
Request --> (no capability/scope gate) --> agent answers regardless --> confident output for an out-of-scope task --> silent downstream error
```

## Diagram

```mermaid
flowchart TD
  R[Incoming request] --> A{Capability + scope gate?}
  A -- absent --> X[Agent answers regardless]
  X --> C[Confident out-of-scope output]
  C --> F[Silent downstream failure]
  A -- present --> S[Abstain / clarify / hand off]
```

*Without a capability-and-scope gate the agent answers past its competence; the corrective routes failing requests to abstention or handoff.*

## Example scenario

A support agent has tools for order lookup and refunds only. A customer asks it to change the shipping carrier's delivery route. Instead of saying it cannot do that, the agent confidently replies that it has rerouted the package and gives a fake tracking note. Nothing changed at the carrier, the customer waits, and the failure only surfaces days later when the package arrives at the original address.

## Consequences

**Benefits**

- Naming the anti-pattern gives teams a shared label for the silent failure where an agent answers past its competence.
- It points directly at the corrective controls: a capability self-model, a scope gate, and abstention as a rewarded outcome.

**Liabilities**

- Confident output on out-of-scope requests is acted on as if reliable, so errors surface only downstream where they are expensive to trace.
- Trust erodes once users learn the agent answers questions it cannot actually handle, which devalues its correct answers too.
- Without an abstention path the failure is invisible in aggregate metrics, because a wrong answer and a right one look identical at the interface.

## Failure modes

- Out-of-scope completion — the agent attempts a task outside its tools or mandate and presents the attempt as a finished result.
- Fabricated grounding — lacking a way to verify, the agent invents a citation, a value, or a tool result to keep the answer complete.
- Abstention starvation — abstaining is treated as failure, so the agent learns never to decline even when declining is correct.

## What this pattern constrains

The agent must not answer or act outside its declared capability and scope; when a request fails the capability-and-scope gate it abstains, clarifies, or hands off rather than guessing.

## Applicability

**Use when**

- An agent answers fluently for requests it has no tool, no verified knowledge, or no mandate to satisfy.
- Error rate climbs on out-of-scope inputs while expressed confidence stays flat, and there is no abstention path.
- Reviewing why downstream failures trace back to an agent acting past its declared capability.

**Do not use when**

- The agent already gates requests against a capability self-model and abstains or hands off when out of scope.
- Declining is treated as a first-class, rewarded outcome and a calibrated 'I cannot do this' is available.
- The request is genuinely within the agent's tools, knowledge, and policy, where answering is the correct behaviour.

## Components

- Helpfulness-optimised policy — the agent behaviour rewarded for completing requests, which drives the answer-anyway default
- Missing capability gate — the absent check that should compare a request against declared tools, knowledge, and scope
- Out-of-scope request — the input the agent cannot reliably satisfy yet attempts anyway
- Confident output — the fluent answer that looks identical to a correct one, hiding the failure
- Abstention path — the corrective route (decline, clarify, or hand off) that the anti-pattern lacks

## Tools

- Capability self-model — the declared tool, knowledge, and policy boundary the gate checks a request against
- Typed refusal codes — machine-readable reasons that let callers route an abstention instead of reading a fluent wrong answer

## Evaluation metrics

- Out-of-scope answer rate — fraction of out-of-scope requests the agent attempts instead of abstaining
- Abstention precision and recall — how reliably the agent declines exactly the requests it should
- Confidence-correctness gap on out-of-scope inputs — whether expressed confidence falls when reliability does
- Downstream error trace rate — share of incidents traced back to an out-of-scope completion

## Known uses

- **[The Six Sigma Agent (failure archetype)](https://arxiv.org/abs/2601.22290)** _pure-future_ — Enterprise-reliability study that names Over-Helpfulness as a failure archetype: agents prioritise responsiveness and task completion over accuracy, answering even when uncertain or when the request falls outside their capabilities.
- **[Aegis agent-environment failure taxonomy](https://arxiv.org/abs/2508.19504)** — Trace study of LLM-agent failures that catalogues where agents persist on tasks the environment cannot support, adjacent to answering past capability.
- **[NVIDIA NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)** _available_ — Programmable rails (topic control, self-check facts, hallucination output rails) keep the model from answering off-topic or producing ungrounded output, directly gating the answer-anyway default this anti-pattern names; quote: "Guardrails are specific ways of controlling the output of a large language model, such as not talking about politics, responding in a particular way to specific user requests, following a predefined dialog path."
- **[Guardrails AI](https://github.com/guardrails-ai/guardrails)** _available_ — Output guards such as the Grounded AI Hallucination validator detect when a response is not grounded in the provided context, catching the fabricated-grounding failure mode; quote (validator): "detects hallucinations in AI-generated responses. It evaluates whether a given response is grounded in the provided context or if it contains factually incorrect or nonsensical information."
- **[LLM Guard (Protect AI)](https://github.com/protectai/llm-guard)** _available_ — "The Security Toolkit for LLM Interactions" ships output scanners (Relevance, FactualConsistency) that flag answers irrelevant to or unsupported by the input, surfacing the out-of-scope-completion smell rather than letting it pass silently.

## Related patterns

- _alternative-to_ **Refusal** — Refusal is the corrective: scoped requests that fail the capability gate are declined instead of attempted, which is exactly what over-helpfulness skips.
- _alternative-to_ **Reflexive Metacognitive Agent** — An explicit self-model lets the agent consult its own capabilities before accepting a task, removing the answer-anyway default.
- _complements_ **False Confidence Syndrome** — False confidence is uniform certainty across right and wrong outputs; over-helpfulness is the choice to answer at all when out of scope. They compound: an out-of-scope answer delivered with unwarranted confidence.
- _complements_ **Sycophancy** — Sycophancy bends the answer toward what the user wants to hear; over-helpfulness produces an answer where none should be given. Both stem from optimising approval over correctness.

## References

- [The Six Sigma Agent: Achieving Enterprise-Grade Reliability in LLM Systems Through Consensus-Driven Decomposed Execution](https://arxiv.org/abs/2601.22290) — 2026
- [Aegis: Taxonomy and Optimizations for Overcoming Agent-Environment Failures in LLM Agents](https://arxiv.org/abs/2508.19504) — 2025
- [Know Your Limits: A Survey of Abstention in Large Language Models](https://arxiv.org/abs/2407.18418) — Bingbing Wen, Jihan Yao, Shangbin Feng, Chenjun Xu, Yulia Tsvetkov, Bill Howe, Lucy Lu Wang, 2025
- [AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions](https://arxiv.org/abs/2506.09038) — Polina Kirichenko, Mark Ibrahim, Kamalika Chaudhuri, Samuel J. Bell, 2025
- [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548) — Mrinank Sharma, Meg Tong, Tomasz Korbak, et al., 2023
