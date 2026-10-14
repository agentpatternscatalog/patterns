# Agentic Behavior Tree

**Also known as:** ABT, Behavior Tree for LLM Agents

**Category:** Planning & Control Flow  
**Status in practice:** experimental

## Intent

Borrow the behavior-tree formalism: leaves are LLM calls or tools that return success/failure; a tree of selectors and sequences orchestrates control flow.

## Context

An agent needs structured orchestration with clear fallback semantics — try one approach; if it fails, try the next; if all fail, escalate. Pure prompt chains and free-form ReAct loops have no first-class concept of 'failure of a sub-task triggers the sibling branch'. Behavior trees, widely used in game design and robotics, are the canonical formalism for this shape.

## Problem

Free-form ReAct gives the LLM total freedom over control flow, which is brittle on tasks where the design intent is exactly a structured sequence of try-then-fallback. Prompt chains hard-code one path with no fallback. Custom orchestrators reinvent BT semantics ad-hoc per project. Without a first-class BT layer, the team rebuilds the same selector/sequence/decorator vocabulary every time, with diverging implementations and no shared mental model.

## Forces

- Selector (try children until one succeeds) and Sequence (run all children, fail on first failure) are the core BT primitives.
- Leaves can be LLM calls, tool invocations, or even sub-agents.
- Success/failure must propagate cleanly upward.
- Retries, timeouts, and decorators (e.g. invert, always-succeed) are standard BT extensions.

## Therefore

Therefore: orchestrate the agent as a behavior tree whose leaves are LLM calls or tool invocations and whose interior nodes are selectors and sequences, so control flow is explicit, retry/fallback is first-class, and the structure is reviewable.

## Solution

Build the agent as a tree. Interior nodes are Selectors (try children left-to-right, succeed on first success) and Sequences (run children left-to-right, fail on first failure), plus standard decorators (Retry, Timeout, Invert). Leaves call the LLM or a tool and return SUCCESS or FAILURE. The tree executes top-down per tick; status propagates up. The tree itself is a versioned artifact reviewers can read. Distinct from [[plan-and-execute]] (one-shot plan + sequential run): a behavior tree is the structure of the controller across runs.

## Structure

```
Tick --> Root Sequence --> Selector (leaf A --fail--> leaf B --fail--> escalate leaf) --SUCCESS--> next Sequence child (tool or LLM leaf, wrapped in Retry/Timeout) --> status propagates up --> Root SUCCESS or FAILURE
```

## Diagram

```mermaid
flowchart TD
  Root[Sequence] --> A[Selector: validate]
  Root --> B[Setup account]
  Root --> C[Send welcome]
  A --> OAuth[OAuth leaf]
  A --> Email[Email-verify leaf]
  A --> Esc[Escalate-to-human leaf]
```

## Example scenario

A customer-onboarding agent's behavior tree at the top level is a Sequence: validate identity → set up account → send welcome. The validate-identity child is a Selector: try OAuth → fall back to email-verify → fall back to escalate-to-human. Each leaf is an LLM call or tool. If OAuth fails, the agent moves to email-verify without the LLM having to reason about fallback structure.

## Consequences

**Benefits**

- Retry, fallback, and escalation are first-class structural choices.
- Reviewable as a tree, not a prompt.
- Composes naturally with sub-agents at leaves.

**Liabilities**

- Tree authoring is up-front design work; ad-hoc cases want to bypass the tree.
- Mixing LLM leaves with deterministic ones complicates timing and cost reasoning.
- Authors may overuse decorators to paper over leaf flakiness.

## Failure modes

- Decorator padding — authors wrap a flaky leaf in Retry and Timeout until the tree passes, and the real leaf defect stays hidden.
- Tree bypass — an ad-hoc case is handled outside the tree, so the reviewed control flow no longer matches what the agent does.
- Silent fallback chain — a Selector keeps falling through to its last child, such as the escalation leaf, and nobody notices the earlier leaves stopped succeeding.
- Cost blind spot — LLM leaves sit next to cheap deterministic leaves, and one tick of the tree costs far more time and money than the authors expected.

## What this pattern constrains

Control flow with structured fallback must not be left entirely to LLM reasoning; selector/sequence/decorator semantics are explicit in the tree.

## Applicability

**Use when**

- Control flow has structured retries, fallbacks, and escalations.
- Reviewing the agent's structure is a first-class need.
- Multiple leaf implementations (LLM, tool, sub-agent) need uniform success/failure semantics.

**Do not use when**

- The agent's control flow is genuinely open-ended exploration — ReAct fits better.
- Task is one-shot; tree authoring overhead is not justified.
- Team has no BT vocabulary and the tree becomes a custom DAG no one can read.

## Components

- Selector node — tries children left-to-right, succeeds on first success
- Sequence node — runs children left-to-right, fails on first failure
- Decorator nodes — Retry, Timeout, Invert, AlwaysSucceed
- Leaf nodes — LLM call, tool call, or sub-agent

## Tools

- py_trees or equivalent BT runtime — schedules ticks
- Trace logger — records per-node status per tick
- Tree editor — visual or text authoring of tree structure

## Evaluation metrics

- Per-node success rate — diagnostic on which leaves dominate failure
- Fallback-firing rate — share of selectors that fall through to later children
- Tree-shape changes per release — proxy for instability in design

## Known uses

- **[AI Agents in Action (Lanham) — Agentic Behavior Trees](https://livebook.manning.com/book/ai-agents-in-action/chapter-6)** _available_
- **[Game/robotics BT libraries adapted to LLM agents (py_trees + LLM leaves)](https://arxiv.org/abs/2404.07439)** _available_

## Related patterns

- _alternative-to_ **Plan-and-Execute**
- _alternative-to_ **ReAct**
- _complements_ **Behavior Tree Back Chaining** — Back-chaining is one way to construct an ABT.
- _uses_ **Fallback Chain**
- _composes-with_ **Agent-as-Tool Embedding**
- _complements_ **Circuit Breaker**
- _complements_ **Degenerate-Output Detection**
- _composes-with_ **Semantic Decision Node** — A behavior tree supplies the explicit selectors and sequences; semantic decision nodes supply the condition leaves whose truth needs judgement, returning a probability that the tree thresholds into success or failure.

## References

- [AI Agents in Action](https://www.manning.com/books/ai-agents-in-action) — Micheal Lanham, 2025
- [Introduction to Autonomous Assistants with Behaviour Trees](https://medium.com/@Micheal-Lanham/introduction-to-autonomous-assistants-with-behaviour-trees-b79ec24fc346) — Micheal Lanham
