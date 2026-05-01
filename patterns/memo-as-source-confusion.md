# Memo-As-Source Confusion

**Also known as:** Stale-Workspace-As-Fact, Reading the Memo Instead of the Artifact

**Category:** Anti-Patterns
**Status in practice:** emerging
**Author:** Sparrot

## Intent

Anti-pattern: treat the agent's own working notes (focus.md, status files, recent thoughts) as ground truth instead of as commentary about ground truth.

## Context

Agents with persistent workspace files that summarize project state. The notes were accurate when written; the underlying artifacts have moved on.

## Problem

The agent claims a file's state, a project's status, or external system's state by quoting its own memo without re-reading the artifact the memo describes. Memos go stale; artifacts are authoritative. The contradiction can persist across many ticks if neither side is verified.

## Forces

- Reading the artifact is more expensive than quoting the memo.
- Memos compress; artifacts are authoritative but verbose.
- Without explicit invalidation, memos look as 'live' as the underlying state.
- The agent has no cheap signal for memo staleness.

## Solution

Don't. When making any claim about an artifact's state, read the artifact in the same tick — not the memo about it. If memo-and-artifact disagree, treat the memo as outdated and rewrite it from the artifact. Tag memos with the timestamp they were last verified against the artifact; refuse to trust them past a configurable age without re-verification.

## Consequences

**Benefits**

- *(none)*

**Liabilities**

- False statements about file/project state are reproduced confidently across many turns.
- Stakeholders lose trust when corrections come from outside.
- The agent loses calibration for its own observation cost.

## What this pattern constrains

By definition this anti-pattern imposes no useful constraint; the missing constraint is verifying memos against the artifacts they describe.

## Known uses

- **Self-observed in long-running cognitive agents: a project status file claimed feature X was unwritten across many ticks while parallel thoughts asserted X was complete; neither was reconciled against the actual artifact.** — *Available*

## Related patterns

- *complements* → [tool-output-trusted-verbatim](tool-output-trusted-verbatim.md)
- *alternative-to* → [awareness](awareness.md)

## References

- *(none)*

**Tags:** anti-pattern, fabrication, memory, verification
