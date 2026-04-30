# Reflexion

**Also known as:** Cross-Episode Lesson Writing, Verbal Reinforcement Learning

**Category:** Verification & Reflection  
**Status in practice:** experimental

## Intent

Have the agent write linguistic lessons from past failures and consult them in future episodes.

## Context

The same agent attempts similar tasks repeatedly; without memory across attempts, mistakes recur.

## Problem

Stateless agents repeat the same errors; full RL fine-tuning is too expensive for most settings.

## Forces

- Lesson quality is bounded by the model's self-critique ability.
- Lesson retrieval (which lesson applies?) is a search problem.
- Lesson rot: outdated lessons may misguide once the world changes.

## Solution

After each episode, the agent reflects on success/failure and writes a verbal lesson. Lessons are stored in long-term memory keyed by task type. Future episodes retrieve relevant lessons and prepend them to context.

## Consequences

**Benefits**

- Improvement without fine-tuning weights.
- Lessons are human-readable and editable.

**Liabilities**

- Single-agent reflexion repeats blind spots because the same model writes and reads the lessons.
- Lesson stores grow; without curation they become noise.

## What this pattern constrains

Lessons are appended, not overwritten; old lessons are explicitly retired rather than silently deleted.

## Known uses

- **Sparrot** — *Available*. Reflection cycle: chunks -> insights -> rule proposals.
- **Bobbin (Stash2Go)** — *Pure future*. Per-user lesson schema not yet built.

## Related patterns

- *complements* → [episodic-summaries](episodic-summaries.md)
- *specialises* → [reflection](reflection.md)

## References

- (paper) Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao, *Reflexion: Language Agents with Verbal Reinforcement Learning*, 2023, <https://arxiv.org/abs/2303.11366>

**Tags:** memory, reflection, learning
