# Agent Skills

**Also known as:** Author-Time Procedures, Slash Commands, Agent Rules

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Package author-time procedures (markdown + optional resources) the agent loads on demand for specific task types.

## Context

Production agent products where common workflows benefit from authored procedures the agent can pick up.

## Problem

Stuffing every workflow into the system prompt bloats context; ad-hoc prompt files are unmanaged. Distinct from the runtime skill-library (which the agent itself authors).

## Forces

- Discovery: how does the agent know which skill applies?
- Versioning of authored procedures.
- Skill quality bounds agent quality on the relevant workflow.

## Solution

Package each procedure as a markdown file (and optional companion resources) under a known directory. The agent loads relevant skills on demand based on the current task. Skills are author-time artefacts versioned with the agent.

## Consequences

**Benefits**

- Workflow knowledge becomes a product surface.
- Versioned, reviewable, sharable.

**Liabilities**

- Discovery / matching overhead.
- Skill rot when not maintained.

## What this pattern constrains

The agent operates within the procedure of the loaded skill; ad-hoc deviation is forbidden when a skill is active.

## Known uses

- **Anthropic Claude Skills** — *Available*
- **Claude Code slash commands** — *Available*
- **Cursor rules / .cursorrules** — *Available*
- **Continue prompts** — *Available*

## Related patterns

- *alternative-to* → [skill-library](skill-library.md) — Author-time vs agent-authored skills.
- *complements* → [dynamic-scaffolding](dynamic-scaffolding.md)
- *complements* → [spec-first-agent](spec-first-agent.md)
- *complements* → [toolformer](toolformer.md)
- *complements* → [dspy-signatures](dspy-signatures.md)
- *alternative-to* → [prompt-bloat](prompt-bloat.md)

## References

- (doc) *Anthropic: Skills*, <https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview>

**Tags:** skills, authoring, procedures
