# Plan-and-Execute

**Also known as:** Plan-Then-Execute, Outline-Then-Run

**Category:** Planning & Control Flow  
**Status in practice:** mature

## Intent

Plan all the steps once with a strong model, then execute each step with a cheaper model under the plan.

## Context

A team runs an agent on a task that decomposes into several mostly-known steps — book a venue, then a restaurant, then send invitations — and a strong, expensive model is available alongside a cheaper, faster one. The team would like to use the strong model where its judgment matters (deciding the steps and their order) and the cheaper model where it does not (typing each step's tool call). The world is stable enough that a plan written once is still good a few minutes later.

## Problem

A ReAct loop (reason-act-observe) runs the strong model on every single step, including trivial ones where the next action is obvious, so it pays full price for routine execution. Hand-coding the workflow gives up the agent's ability to handle small surprises. Without an inspectable plan emitted before any tool fires, reviewers cannot see what the agent intends to do until it has already partially done it, and a wrong assumption near the start cannot be caught until the run produces a bad result.

## Forces

- Planning quality depends on context the planner has at planning time.
- Execution may discover the plan was wrong; replan-versus-fail is a real choice.
- Cheaper model may not faithfully execute the plan.

## Therefore

Therefore: pay the strong model once to produce an inspectable ordered plan and then walk it with a cheaper executor, replanning only on surprise, so that token cost shifts off routine steps without giving up plan visibility.

## Solution

Two-stage loop. Planner: produce an ordered list of steps with explicit dependencies. Executor: run each step (often with tools) and accumulate results. On failure or surprise, replan with the new evidence in context.

## Structure

```
Planner -> [Step_1, Step_2, ..., Step_N] -> Executor -> Result. On failure, return to Planner.
```

## Diagram

```mermaid
sequenceDiagram
  participant User
  participant Planner
  participant Executor
  participant Tool
  User->>Planner: goal
  Planner->>Planner: decompose into ordered steps
  Planner-->>Executor: plan
  loop per step
    Executor->>Tool: action
    Tool-->>Executor: result
  end
  Executor-->>User: outcome
```

*Plan-and-Execute commits to a plan up front; the executor walks the steps and only loops back to the planner on failure.*

## Example scenario

An office-assistant agent is told, 'Book a team offsite in Barcelona for ten people next month, find a restaurant for dinner, and email everyone the schedule.' Up front it writes a five-step plan: search venues, pick one, search restaurants, pick one, send emails. The executor walks the plan in order. Because the venue list does not depend on what restaurants exist, planning once is cheaper than re-thinking every step.

## Consequences

**Benefits**

- Plan is inspectable before execution starts.
- Cost shifts to the cheap model for routine steps.

**Liabilities**

- Plans can be brittle when the world differs from the planner's mental model.
- Replans add latency and complicate debugging.

## Failure modes

- Plan-world mismatch — the plan assumes a file, field or tool state that does not exist, and early steps fail on facts the planner never checked.
- Silent deviation — the executor skips or reorders steps without raising a replan request, and the plan no longer explains the run.
- Replan loop — each surprise triggers a new plan, latency stacks up, and the trace is hard to debug across plan versions.
- Weak executor — the cheaper model cannot carry out a step that needed more judgement, and returns a plausible but wrong result.

## What this pattern constrains

The executor cannot deviate from the current plan without raising a replan request.

## Applicability

**Use when**

- The task decomposes cleanly into mostly-independent steps.
- The world is stable enough that a plan made once is still good to execute.
- Cost of replanning per step would dominate the run.

**Do not use when**

- Each step's outcome materially changes what the next step should be — ReAct fits.
- The task is a single step; planning is overhead.
- Steps are tightly interdependent and a DAG with placeholders fits better — see ReWOO or LLMCompiler.

## Components

- Planner — strong model that emits the ordered step list once
- Plan artefact — inspectable list of steps with dependencies
- Executor — cheaper model that walks each step under the plan
- Replan trigger — path back to the planner on failure or surprise
- Result accumulator — collects per-step outputs into the final answer

## Tools

- Strong LLM API — used once for the plan, where judgement matters
- Cheaper LLM API — used per step for routine execution
- Tool catalogue — what the executor calls per step
- Plan store — persists the plan so reviewers can inspect before execution starts

## Evaluation metrics

- Cost shift to cheap model — fraction of run tokens executed below the strong model
- Replan frequency — how often plans had to be revised mid-run
- Plan-step success rate — fraction of planned steps that executed without failure
- Plan inspectability lag — time between plan emission and first tool firing
- Brittleness rate — runs that completed the plan but produced wrong output

## Known uses

- **Bobbin (Stash2Go)** _available_ — Explicit planner + screen_executor nodes in the agent lane.
- **LangChain Plan-and-Execute** _available_

## Related patterns

- _alternative-to_ **ReAct**
- _generalises_ **ReWOO**
- _generalises_ **Planner-Executor-Observer**
- _complements_ **Step Budget**
- _complements_ **Structured Output**
- _alternative-to_ **Orchestrator-Workers**
- _complements_ **Least-to-Most Prompting**
- _complements_ **Replan on Failure**
- _generalises_ **Goal Decomposition**
- _generalises_ **Outer-Inner Agent Loop**
- _complements_ **Passive Goal Creator**
- _complements_ **Pre-Flight Spec Authoring**
- _uses_ **Control-Flow Integrity**
- _alternative-to_ **Hybrid HTN + Generative Agent**
- _complements_ **Single-Path Plan Generator**
- _alternative-to_ **BPMN/DMN Deterministic Shell Around Agent**
- _alternative-to_ **Incremental Model Querying**
- _generalises_ **Planner-Executor-Verifier (PEV)**
- _complements_ **BDI Agent**
- _alternative-to_ **Agentic Behavior Tree**
- _alternative-to_ **Behavior Tree Back Chaining**
- _alternative-to_ **Partial Global Planning**
- _alternative-to_ **Query-Decomposition Agent**
- _alternative-to_ **Advisor Consult** — Plan-and-execute uses the strong model once, before the run; the advisor is consulted in the middle of the run, when the executor has met the problems the plan did not foresee.

## References

- [Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models](https://arxiv.org/abs/2305.04091) — Wang, Xu, Lan, Hu, Lan, Lee, Lim, 2023
- [LangChain: Plan-and-Execute Agents](https://blog.langchain.com/planning-agents/) — 2023
- [Agent design pattern catalogue: A collection of architectural patterns for foundation model based agents](https://doi.org/10.1016/j.jss.2024.112278) — Yue Liu, Sin Kit Lo, Qinghua Lu, Liming Zhu, Dehai Zhao, Xiwei Xu, Stefan Harrer, Jon Whittle, 2025
