# Initializer Agent

**Also known as:** Bootstrap Session, One-Shot Scaffolder, Pre-Work Scaffold Agent

**Category:** Planning & Control Flow
**Status in practice:** emerging

## Intent

Run one specialised agent session whose only job is to expand a vague user prompt into a durable on-disk scaffold (feature list, init script, progress notes, initial commit) that all subsequent agent sessions read on boot.

## Context

Long-running coding-agent harnesses where many short sessions accumulate to deliver one large outcome. The first session has the freshest understanding of the user's intent but also the least committed work; later sessions inherit whatever state is on disk.

## Problem

Without a dedicated bootstrap step, every later session re-derives the plan from the same vague prompt, often inconsistently. Asking the same agent that writes code to also scaffold the workspace conflates two very different prompts and frequently produces half-finished plans, missing init scripts, or no initial commit to roll back to. A separate session with a different system prompt — explicitly scoped to scaffolding only — produces cleaner, more durable artefacts that downstream sessions can trust.

## Forces

- The first session has the freshest read on the user's intent but the smallest budget for direct work.
- Downstream sessions need a stable, machine-readable plan they did not author.
- Scaffolding work (init scripts, feature lists, initial commit) is qualitatively different from coding work.
- Re-scaffolding mid-run is expensive and destabilising; the scaffold must be right once.

## Therefore

Therefore: dedicate a single one-shot agent session with a scaffolding-only prompt to produce a durable on-disk artefact (feature list, init script, progress note, initial commit) before any coding agent is invoked, so that every later session boots from a stable shared workspace.

## Solution

The harness launches an Initializer with a prompt restricted to scaffolding: expand the user request into a feature-list.json, write an init.sh that brings a fresh checkout up to a working state, drop a progress.md with the run's intent and constraints, and make an initial git commit. The Initializer is forbidden from writing application code or running long tool sequences; its exit condition is the presence of the four artefacts. Subsequent coding agents start every session by reading the scaffold, never by re-deriving it. The Initializer itself is single-shot — if its scaffold is wrong, a human or a higher-level driver re-runs it, not the coding agent.

## Structure

```
Initializer (single session) -> {feature-list.json, init.sh, progress.md, initial commit}. Coding agents (many sessions) -> read scaffold, write code, never re-scaffold.
```

## Example scenario

A user asks for "a new internal status dashboard". Instead of the coding agent starting immediately, the harness launches an Initializer. It writes feature-list.json with eight chunks, init.sh that installs dependencies and seeds a database, progress.md restating the user's intent, and commits the empty scaffold. Over the next two days a dozen coding-agent sessions boot, each reading feature-list.json and progress.md, none re-deriving the plan from the original prompt.

## Consequences

**Benefits**

- Downstream sessions share a stable understanding of the job.
- Scaffolding and coding prompts can each be tuned independently.
- Initial commit provides a clean rollback point.
- Fresh-context coding sessions are smaller because the plan lives on disk, not in prompt.

**Liabilities**

- Adds an explicit first step to every run.
- A bad scaffold poisons every downstream session until re-run.
- Two different prompt styles to maintain.
- Over-scaffolding for tiny jobs is wasted overhead.

## What this pattern constrains

The Initializer must not write application code, must not start the coding work, and must terminate as soon as the scaffold artefacts exist; coding sessions must not modify the feature list without going back through the Initializer or a higher-level driver.

## Applicability

**Use when**

- Many downstream sessions will inherit state from a single starting point.
- The user prompt is vague enough that re-deriving the plan would be inconsistent across sessions.
- There is a clear scaffold artefact set (feature list, init script, progress note) the team agrees on.

**Do not use when**

- The job fits in one session; scaffolding is overhead.
- The workspace is already populated by a previous run; resume directly.
- There is no agreement on what the scaffold should contain.

## Known uses

- **[Anthropic harness for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)** — *Available* — Initializer session pattern described in Anthropic's effective-harnesses post.
- **[Anthropic harness-design-long-running-apps guidance](https://www.anthropic.com/engineering/harness-design-long-running-apps)** — *Available* — Bootstrap step formalised as part of the harness architecture.

## Related patterns

- *complements* → [spec-first-agent](spec-first-agent.md) — The Initializer's feature-list is a lightweight spec.
- *complements* → [todo-list-driven-agent](todo-list-driven-agent.md) — Initializer produces the durable todo list that later sessions execute against.
- *complements* → [agent-resumption](agent-resumption.md) — Initializer's commit provides the resumption anchor.
- *composes-with* → [planner-generator-evaluator-harness](planner-generator-evaluator-harness.md) — Initializer often runs ahead of a three-role harness.

## References

- (blog) Anthropic Engineering, *Effective harnesses for long-running agents*, 2025, <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
- (blog) Anthropic Engineering, *Harness design for long-running application development*, 2026, <https://www.anthropic.com/engineering/harness-design-long-running-apps>

**Tags:** bootstrap, scaffold, harness, one-shot, long-running
