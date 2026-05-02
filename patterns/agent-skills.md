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

## Example scenario

A customer-support agent now handles refunds, address changes, subscription pauses, and SIM swaps. Cramming every workflow into the system prompt has pushed it past 18k tokens and the agent still skips steps. The team breaks each workflow into an Agent Skill — a markdown file with the procedure plus a few example dialogues — that the agent loads on demand once the user's intent is classified. The base prompt shrinks; only the relevant procedure enters context for that conversation.

## Consequences

**Benefits**

- Workflow knowledge becomes a product surface.
- Versioned, reviewable, sharable.

**Liabilities**

- Discovery / matching overhead.
- Skill rot when not maintained.

## What this pattern constrains

The agent operates within the procedure of the loaded skill; ad-hoc deviation is forbidden when a skill is active.

## Applicability

**Use when**

- You have many distinct procedures and stuffing them all into the system prompt would bloat context.
- Procedures are author-time artefacts that benefit from versioning alongside the agent.
- The agent can reliably classify which procedure applies to the current task.

**Do not use when**

- The agent has only a handful of procedures that fit comfortably in the system prompt.
- Procedures must be authored at runtime by the agent itself (use a runtime skill-library pattern instead).
- On-demand loading adds latency the use case cannot tolerate.

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
