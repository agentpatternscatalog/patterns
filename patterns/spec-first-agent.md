# Spec-First Agent

**Also known as:** Specification-Driven Agent, Plan-as-Document

**Category:** Planning & Control Flow  
**Status in practice:** emerging

## Intent

Drive the agent loop from a human-authored specification document rather than free-form prompts.

## Context

A team runs an agent on a task that is well-defined enough to write down — a recurring report, a bug-fix list, a migration plan, a multi-step automation. The team wants the agent's instructions to live in a file that humans can read, review, and edit alongside the code, rather than in a chat history or someone's head. Reviewers should be able to diff changes to the agent's intent the same way they diff changes to the source code.

## Problem

Free-form prompts drift between sessions: the same engineer types subtly different instructions on different days and the agent's behaviour quietly changes. When the spec lives in one engineer's head, nobody else can review it, audit it, or take over when that engineer is away. Without a written target, there is no single source of truth for what "done" means, so the agent may declare success on partial work or keep going past where the team would have stopped. The team needs a written, version-controlled spec without giving up the agent's ability to update its own plan as it learns.

## Forces

- Spec authoring is up-front work.
- The agent must update the spec when learnings invalidate it; uncontrolled spec mutation is dangerous.
- Spec format must be both human- and agent-readable.

## Therefore

Therefore: make a human-authored markdown spec the single source of truth for what 'done' means and let the agent read it each iteration and edit it only under controlled conditions, so that intent is auditable and behaviour drift shows up as a reviewable diff.

## Solution

Write the specification as a markdown file (PROMPT.md, fix_plan.md, or similar). The agent reads the spec at each iteration, executes against it, and may update it under controlled conditions. The spec is the single source of truth for what 'done' means.

## Structure

```
Human author --writes--> Spec file (PROMPT.md / fix_plan.md) --read each iteration--> Agent loop --work only on named goals--> controlled spec updates (reviewed as diffs) --> Spec defines done --> stop
```

## Diagram

```mermaid
flowchart TD
  Author[Human author] -->|writes| Spec[(PROMPT.md / fix_plan.md)]
  Spec --> Agent[Agent loop]
  Agent -->|reads each iter| Spec
  Agent -->|controlled writes| Spec
  Spec --> Done{Spec defines 'done'?}
  Done -->|yes| Stop[Stop loop]
```

## Example scenario

A small team has one engineer who knows the agent's behaviour by heart but the spec lives in their head and is unaudited. They write PROMPT.md as the agent's spec, the agent reads it each iteration and may update it under controlled conditions. New engineers read the markdown to understand intent; reviewers diff spec changes; behaviour drift becomes visible because it shows up as a spec edit rather than a silent prompt change.

## Consequences

**Benefits**

- Inspectable target; reviewable diffs over time.
- Pairs naturally with iterative loops (Ralph).

**Liabilities**

- Spec quality bounds agent quality.
- Spec mutation introduces drift if uncontrolled.

## Failure modes

- Thin spec — the spec leaves out a requirement, and the agent declares done on work that misses it.
- Uncontrolled spec edits — the agent rewrites the spec to match what it built, and the target quietly moves.
- Out-of-scope work — the agent does work not named in the spec, and reviewers cannot trace why it happened.
- Stale spec — the team changes direction in conversation but not in the file, and the agent keeps building the old target.

## What this pattern constrains

The agent acts only against goals named in the spec; out-of-scope work must be added to the spec first.

## Applicability

**Use when**

- The task is well-defined enough to write down as a spec.
- The spec needs to be inspectable, audited, or shared across engineers.
- The agent benefits from a stable target rather than free-form prompts.

**Do not use when**

- Requirements change faster than a spec can be maintained.
- The task is exploratory and a spec would prematurely commit to a path.
- Writing the spec costs more than just doing the work.

## Components

- Human-authored spec — markdown file describing what done means
- Spec reader — agent step that loads the spec at each iteration
- Spec-bound executor — performs work only against goals named in the spec
- Controlled spec mutator — narrow path by which the agent edits the spec
- Reviewer surface — diff-based view of spec changes over time

## Tools

- Markdown file — single source of truth for intent (PROMPT.md, fix_plan.md, etc.)
- LLM API — agent that reads the spec and acts against it
- Version-control system — tracks spec edits as reviewable diffs
- Tool catalogue — actions the agent can take while honouring the spec

## Evaluation metrics

- Out-of-spec action rate — agent steps that did work not named in the spec
- Spec mutation frequency — how often the agent edits the spec versus reading it
- Reviewer round-trip time — turnaround on spec-change PRs
- Drift visibility — fraction of behaviour changes that surfaced as spec diffs
- Spec-quality gap — outcomes the spec failed to constrain that needed re-authoring

## Known uses

- **Ralph Wiggum loop** _available_ — PROMPT.md + fix_plan.md drive the loop.
- **Spec-driven Claude Code workflows** _available_

## Related patterns

- _used-by_ **Spec-Driven Loop**
- _complements_ **Agent Skills**
- _complements_ **SOP-Encoded Multi-Agent Workflow**
- _alternative-to_ **Todo-List-Driven Autonomous Agent**
- _alternative-to_ **Automatic Workflow Search**
- _complements_ **Planner-Generator-Evaluator Harness**
- _alternative-to_ **Visual Workflow Graph**
- _composes-with_ **Pre-Flight Spec Authoring**
- _complements_ **Rigor Relocation**

## References

- [Geoffrey Huntley, Ralph](https://ghuntley.com/ralph/) — 2025
