# Chat Chain

**Also known as:** Phased Multi-Agent Pipeline, Sequential Role-Pair Chats, Communicative Phase Chain

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Decompose a long, multi-disciplinary task into ordered phases; within each phase, run a paired-role chat between two agents until the phase artefact is signed off; pass the artefact to the next phase.

## Context

A task (build a small program, write a brief, prepare a report) requires several disciplines in sequence and is too long for a single agent loop or a flat multi-agent broadcast.

## Problem

A single agent loop loses focus; broadcast multi-agent chat produces tangled context; flat prompt-chaining cannot host the back-and-forth a discipline needs.

## Forces

- Each discipline benefits from focused two-agent dialogue.
- Context windows blow up if every agent sees every chat.
- Phase-to-phase hand-off needs a clean artefact contract.
- Termination of a phase has to be explicit, not vibes-based.

## Solution

Define an ordered chain of phases. Each phase has (a) a defined input artefact, (b) two role-paired agents (e.g. designer + coder, coder + tester), (c) a phase-specific completion predicate, (d) a defined output artefact. Within a phase, the two agents converse multi-turn; the completion predicate ends the phase; the artefact moves to the next phase. The chain is the macro-control; the chat is the micro-control.

## Structure

```
Phase_1 (Role_A <-> Role_B) -> artefact_1 -> Phase_2 (Role_B <-> Role_C) -> artefact_2 -> ... -> final_artefact.
```

## Consequences

**Benefits**

- Clear macro-progression with chat-level flexibility inside each phase.
- Keeps each phase's context tight; only the artefact crosses the boundary.
- Auditable artefact trail per phase.

**Liabilities**

- Designing the chain (phases + completion predicates) is the architecture problem.
- Sequential by construction; parallelism inside a phase requires extra design.
- Wrong phase decomposition forces agents into awkward role pairings.

## What this pattern constrains

Agents may not skip phases or address agents outside the current phase; phase output must satisfy the completion predicate before transition.

## Known uses

- **[ChatDev](https://github.com/OpenBMB/ChatDev)** — *Available*. Software-development chain: design → coding → testing → documentation, each as a paired-role chat.

## Related patterns

- *generalises* → [prompt-chaining](prompt-chaining.md) — Prompt chaining is a single-agent special case.
- *complements* → [sop-encoded-multi-agent](sop-encoded-multi-agent.md)
- *alternative-to* → [supervisor](supervisor.md)
- *uses* → [pipes-and-filters](pipes-and-filters.md)
- *uses* → [stop-hook](stop-hook.md) — Phase completion predicate is a stop hook scoped to a phase.

## References

- (paper) Qian et al., *ChatDev: Communicative Agents for Software Development*, 2023, <https://arxiv.org/abs/2307.07924>

**Tags:** multi-agent, pipeline, china-origin, chatdev
