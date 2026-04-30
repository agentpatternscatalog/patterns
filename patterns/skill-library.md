# Skill Library

**Also known as:** Tool-Creating Agent, Meta-Tool Use, Self-Authored Tools

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Let the agent grow its own toolkit by writing reusable skills that subsequent runs can call.

## Context

Patterns of tool use repeat; the agent re-derives the same routine across runs and pays for it each time.

## Problem

Without a place to crystallise repeated work, every run starts from scratch.

## Forces

- New skills can be wrong or unsafe.
- The library must be loadable without restart in a long-running agent.
- Skill discovery (which skill applies?) is itself a retrieval problem.

## Solution

A directory (often `skills/*.py` or `skills/*.md`) where the agent can write new modules. A loader (importlib in Python, dynamic import in JS) makes them callable. A critic gates additions. Old skills are versioned, not overwritten silently.

## Consequences

**Benefits**

- Compounding capability over time.
- Skills are reviewable and removable, unlike weights.

**Liabilities**

- Skill-name collisions and silent shadowing.
- Library quality decays without periodic review.

## What this pattern constrains

New skills enter the library only after passing the critic; they cannot mutate existing skills without quorum.

## Known uses

- **Sparrot** — *Available*. skills/*.py loaded via importlib on startup and after restart_self.
- **Voyager (Minecraft agent)** — *Available*. Skill library that grows through self-play.

## Related patterns

- *uses* → [inner-critic](inner-critic.md)
- *composes-with* → [code-execution](code-execution.md)
- *complements* → [exploration-exploitation](exploration-exploitation.md)
- *alternative-to* → [agent-skills](agent-skills.md)
- *complements* → [app-exploration-phase](app-exploration-phase.md)
- *complements* → [wasm-skill-runtime](wasm-skill-runtime.md)

## References

- (paper) Wang et al., *Voyager: An Open-Ended Embodied Agent with Large Language Models*, 2023, <https://arxiv.org/abs/2305.16291>

**Tags:** skill-library, self-modification
