# Prompt Bloat

**Also known as:** Prompt Accretion, Eternal System Prompt

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: every bug fix adds a sentence to the system prompt; nothing is ever removed.

## Context

Production agents whose system prompt grows monotonically over months; no eviction policy; no review for relevance.

## Problem

Past a few thousand tokens, the prompt squeezes retrieval, forces cache misses, and yields diminishing-returns instruction following. Distinct from hero-agent (which is about scope) — this is about prompt accretion as a process.

## Forces

- Adding a sentence feels free; removing one feels risky.
- No clear owner of the prompt's overall design.
- Eval coverage rarely catches bloat-driven regressions.

## Solution

Don't. Treat the prompt as code: PR review, eval gate on length, quarterly pruning sprints. Lift recurring procedures into agent-skills. Move stable rules into a constitutional charter.

## Consequences

**Liabilities**

- Token cost per turn rises monotonically.
- Cache misses on every prompt edit.
- Conflicting instructions accumulate; the model picks one at random.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing eviction policy is the failure.

## Known uses

- **Common at six-month-old agent products** — *Available*

## Related patterns

- *alternative-to* → [agent-skills](agent-skills.md)
- *alternative-to* → [constitutional-charter](constitutional-charter.md)
- *complements* → [hero-agent](hero-agent.md)

## References

- (blog) *Eugene Yan: Prompt engineering as a craft*, <https://eugeneyan.com/writing/llm-patterns/>
- (blog) *Hamel Husain: Improving the operations of agents*, <https://hamel.dev>

**Tags:** anti-pattern, prompt
