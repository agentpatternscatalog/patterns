# Subagent Isolation

**Also known as:** Worktree Subagent, Parallel Subagent, Isolated Worker

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Run subagents in isolated workspaces so their writes do not collide and parallelism is safe.

## Context

Coding agents that delegate to multiple subagents for parallel work; without isolation, subagents fight over the same files.

## Problem

Subagents writing to the same workspace race each other; one's edits are clobbered by another's.

## Forces

- Isolation has setup cost (new worktree, branch, container).
- Reconciling work back to the main workspace is its own problem.
- Excessive isolation prevents subagents from seeing each other's progress when that would help.

## Solution

Each subagent runs in its own workspace (git worktree, container, branch, sandbox). The supervisor reconciles results back to the main workspace on completion (merge, cherry-pick, replay). Only one workspace can land changes at a time.

## Consequences

**Benefits**

- True parallelism without write collisions.
- Failed subagents leave their workspace as evidence.

**Liabilities**

- Setup latency.
- Reconciliation conflicts.

## What this pattern constrains

Subagents may only write to their own isolated workspace; cross-workspace writes are forbidden.

## Known uses

- **Claude Code subagent + git worktree** — *Available*
- **Devin sessions** — *Available*
- **Cursor parallel agents** — *Available*
- **OpenHands** — *Available*

## Related patterns

- *specialises* → [orchestrator-workers](orchestrator-workers.md)
- *composes-with* → [sandbox-isolation](sandbox-isolation.md)
- *composes-with* → [llm-compiler](llm-compiler.md)
- *complements* → [agent-as-tool-embedding](agent-as-tool-embedding.md)

## References

- (blog) *Mastering Git Worktrees with Claude Code*, 2025, <https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe>

**Tags:** multi-agent, isolation, parallel
