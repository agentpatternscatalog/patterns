# Hierarchical Tool Selection

**Also known as:** Tool Tree, Categorised Tool Catalog, Two-Stage Tool Routing

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Organise tools into a tree of categories so the agent first picks a branch and then a specific tool within it.

## Context

An agent has access to dozens or hundreds of tools — every public API the company exposes, every micro-action across many domains (billing, identity, scheduling, search, code, files). Presenting them all in the system prompt blows up the context window and overloads the model's selection step.

## Problem

A flat tool list collapses in two ways past roughly 30 tools. Token cost grows linearly in description length × tool count. Selection error rises non-linearly as the model confuses similar tools or misses the right one entirely. Worse, permissions and ownership are flat too — there is no scope at which a team can say 'these are the billing tools, this team owns them'. The agent ends up either under-tooled (some tools dropped) or unreliable (the model picks wrong).

## Forces

- Token cost of tool descriptions scales with catalog size.
- Model selection accuracy degrades past a few dozen choices.
- Permissions, ownership, and audit naturally group by domain.
- The first-stage choice (category) must be cheap enough not to cost what was saved.

## Therefore

Therefore: organise tools into a tree of categories and have the agent first pick a category, then pick a specific tool within it, so token cost and selection error scale sub-linearly with catalog size.

## Solution

Group tools into named categories (billing, identity, scheduling, search, code, files). At the top level the agent sees only the category names with one-line descriptions. After it picks a category, it sees the tools in that branch. Permissions can scope per branch (this user can read but not write billing tools). For very large catalogs nest the tree further. The cost is one extra decoding step at the top; the saving is paying full tool descriptions only for the chosen branch.

## Structure

```
Prompt (category names only) --> Agent picks category --> Tools in chosen branch (billing / identity / scheduling ...) --> Agent picks tool --> Tool call
```

## Diagram

```mermaid
flowchart TD
  P[Prompt: category names only] --> Pick1[Agent picks category]
  Pick1 --> Bil[Billing tools]
  Pick1 --> Idn[Identity tools]
  Pick1 --> Sch[Scheduling tools]
  Bil --> Pick2[Agent picks billing tool]
  Pick2 --> Call[Tool call]
```

## Example scenario

An ops agent has 180 tools spanning eight domains. The system prompt presents only the eight category names. After picking 'billing' the agent receives the 24 billing tools. End-to-end latency is one extra decode at the top; total tokens drop ~80% on average and selection accuracy on a 200-trace eval rises from 64% to 91%.

## Consequences

**Benefits**

- Token cost stays bounded as the catalog grows.
- Selection accuracy improves because the model picks among few items at each level.
- Permissions and ownership map onto the tree naturally.

**Liabilities**

- An extra step per call adds latency and one more decoding decision.
- Categories that don't carve nature at the joints (a tool that spans two domains) need duplication or compromise.
- Wrong top-level pick produces a dead-end where the right tool is in a different branch.

## Failure modes

- Wrong branch — the agent picks the billing category when the needed tool sits under identity, and it reaches a dead end with no way to see the right tool.
- Straddling tool — a tool that belongs to two domains is placed in only one, and the agent never finds it from the other side.
- Vague category names — one-line descriptions at the top level do not separate branches clearly, so the first pick is close to a guess.
- Extra hop on hot paths — a simple, frequent call pays the category step every time and adds latency the flat list did not have.

## What this pattern constrains

A large tool catalog must not be presented as a flat list to the model; tools are organised into named categories and the agent first picks a category before seeing tool-level descriptions.

## Applicability

**Use when**

- Tool catalog exceeds roughly 30 tools.
- Tools naturally cluster into domain categories.
- Permissions or ownership can scope per category.

**Do not use when**

- Catalog is small enough to present flat.
- Tools span domains so heavily that categorisation is arbitrary.
- Latency budget cannot absorb the extra top-level decode.

## Components

- Tool tree — categories at the top, tools at the leaves
- Category-description block — short prompt content for top level
- Branch loader — fetches tool descriptions for the chosen branch only
- Permission scoping — applies per-branch access policy

## Tools

- Tool registry — holds the tree definition and per-branch descriptions
- Prompt builder — assembles top-level vs branch-level prompts

## Evaluation metrics

- Token cost per tool call — tokens spent presenting tools
- Selection accuracy — fraction of tool picks reviewers judge correct
- Dead-end rate — share where wrong top-level pick blocks the right tool

## Known uses

- **[Building Applications with AI Agents (Albada) — Hierarchical Tool Selection](https://www.oreilly.com/library/view/building-applications-with/9781098176495/ch04.html)** _available_
- **[MCP-Zero hierarchical semantic routing (arXiv 2506.01056)](https://arxiv.org/abs/2506.01056)** _available_

## Related patterns

- _complements_ **Tool Use**
- _complements_ **Agent Skills**
- _complements_ **Model Context Protocol**
- _complements_ **MCP Bidirectional Bridge**
- _complements_ **Agent-Computer Interface**
- _composes-with_ **Tool Transition Fusion**
- _alternative-to_ **One Tool, One Agent**
- _complements_ **Composite Service**
- _alternative-to_ **Dependency-Aware Skill Retrieval** — Hierarchical selection narrows a flat catalog by category tree; here the structure followed is the dependency graph, not a topical hierarchy.

## References

- [Building Applications with AI Agents](https://www.oreilly.com/library/view/building-applications-with/9781098176495/ch04.html) — Michael Albada, 2025
- [MCP-Zero: Active Tool Discovery for Autonomous LLM Agents](https://arxiv.org/abs/2506.01056) — 2025
