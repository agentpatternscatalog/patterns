# Memo-As-Source Confusion

**Also known as:** Stale-Workspace-As-Fact, Reading the Memo Instead of the Artifact

**Category:** Anti-Patterns
**Status in practice:** emerging
**Author:** Sparrot

## Intent

Anti-pattern: the agent cites its own past memos as ground truth instead of re-verifying them against the artifacts they describe, accumulating false confidence in stale summaries.

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

## Example scenario

A coding agent that maintains its own README about the repo cites that README when asked 'is the migration script idempotent?' — and the README is two months stale. It confidently says yes; the script has since been changed and the answer is wrong. The team names this memo-as-source-confusion and forbids citing memos as source for artifact claims: any claim about a file's state must read the file in the same tick, and if the memo disagrees the memo is rewritten from the artifact. Memo timestamps are now compared to artifact mtimes before any quote.

## Consequences

**Benefits**

- *(none)*

**Liabilities**

- False statements about file/project state are reproduced confidently across many turns.
- Stakeholders lose trust when corrections come from outside.
- The agent loses calibration for its own observation cost.

## What this pattern constrains

Treating stale memos as ground truth without re-checking the underlying artifacts they describe is forbidden; every memo-cited claim must be backed by a fresh artifact read in the same tick.

## Applicability

**Use when**

- The agent maintains long-lived memo files or status documents that summarize external artifacts.
- Workspace summaries are routinely cited in answers without re-reading the underlying files.
- False confidence in stale state has been observed at least once.

**Do not use when**

- The agent never re-cites its own prior memos as evidence.
- All claims about state are sourced from a fresh tool call in the same tick anyway.

## Known uses

- **[Self-observed in long-running cognitive agents: a project status file claimed feature X was unwritten across many ticks while parallel thoughts asserted X was complete; neither was reconciled against the actual artifact.](https://github.com/luxxyarns/sparrot)** — *Available*

## Related patterns

- *complements* → [tool-output-trusted-verbatim](tool-output-trusted-verbatim.md)
- *alternative-to* → [awareness](awareness.md)
- *complements* → [provenance-ledger](provenance-ledger.md)
- *complements* → [decision-log](decision-log.md)

## References

- (doc) *Anthropic — Memory tool (memo invalidation guidance)*, 2025, <https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool>
- (paper) Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, 2023, <https://arxiv.org/abs/2307.03172>

**Tags:** anti-pattern, fabrication, memory, verification
