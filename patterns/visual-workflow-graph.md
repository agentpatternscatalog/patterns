# Visual Workflow Graph

**Also known as:** Typed-Node Canvas, Drag-and-Drop Workflow Builder, Low-Code Agent Canvas

**Category:** Planning & Control Flow  
**Status in practice:** mature

## Intent

Express agentic logic as a visual graph of typed nodes connected on a canvas with Start and End nodes so non-coding stakeholders can read and edit the flow.

## Context

A team is building on a low-code or no-code platform — Dify, Coze, n8n, Flowise, Langflow, FastGPT, Bisheng — or in an IDE-embedded workflow editor, where the same product surface is used both by developers and by non-developers such as business users or operations teams. The workflow itself is the artefact those users will edit and review, not the code behind it.

## Problem

Procedural agentic code is dense and unfamiliar for non-coders, and review-heavy even for developers because the orchestration logic is buried inside source files. The graph topology — which nodes feed which, which branches gate which — is the part that most needs to be inspectable, but in a procedural codebase that topology has to be reconstructed by reading code. The platform needs a graph-shaped representation of the workflow as the primary artefact, with code only behind the individual nodes that need it.

## Forces

- Visual editing lowers the bar for non-developer contributors but raises the bar for version control and merge.
- A typed-node vocabulary (LLM, retrieval, tool, conditional, iteration, code) lets the canvas validate connections statically.
- The graph must round-trip with the runtime — what runs is what is drawn.
- Conditional and iteration nodes need to compose without becoming visually unreadable.
- Agent nodes inside the graph blur the line between deterministic workflow and agentic loop.

## Therefore

Therefore: model the workflow as a typed-node graph with explicit Start and End nodes, validate connections by node-type contract, and execute the graph as drawn, so that topology is the source of truth and the canvas is what runs.

## Solution

Define a small vocabulary of node types — Start, End, LLM, Retrieval, Tool, Conditional, Iteration (see iteration-node), Code, Agent — each with a typed input/output schema. Build the workflow on a drag-and-drop canvas connecting nodes by edges; the editor validates connections by type. Persist the graph as a serialisable artefact (JSON/YAML) that the runtime executes directly. Pair with iteration-node (the per-element subgraph construct), pluggable execution semantics for Agent nodes, and policy-as-code-gate for guarded edges. Treat the canvas as a UI projection of the artefact, not the source of truth alone — diffs and reviews work on the artefact.

## Structure

```
Canvas (drag-and-drop UI) ↔ Graph artefact (JSON/YAML, version-controlled) ↔ Workflow runtime that executes the graph.
```

## Diagram

```mermaid
flowchart TD
  Start([Start]) --> QC[Question Classifier]
  QC -->|billing| KB1[Retrieval: billing]
  QC -->|tech| KB2[Retrieval: tech]
  QC -->|other| KB3[Retrieval: general]
  KB1 --> LLM[LLM: draft reply]
  KB2 --> LLM
  KB3 --> LLM
  LLM --> Cond{confidence >= 0.85?}
  Cond -- yes --> Send[Tool: send]
  Cond -- no --> Hum[Human review queue]
  Send --> End1([End])
  Hum --> End2([End])
```

## Example scenario

A customer-success team wants to build a triage workflow that classifies incoming messages, retrieves relevant docs, drafts a reply, and routes high-confidence drafts to send while low-confidence drafts go to human review. Their engineering team uses Dify: a Start node receives the message; a Question Classifier routes by category; a Knowledge Retrieval node fetches docs per category; an LLM node drafts the reply; a Conditional node splits on confidence; one branch ends in Send, the other in Human Review. The whole workflow is one canvas. When customer success wants to add a new category, they edit the canvas; the engineering team reviews the artefact diff in the PR.

## Consequences

**Benefits**

- Topology is inspectable at a glance.
- Non-developers can read and propose edits.
- Typed-node contracts catch wiring errors before execution.
- Iteration, conditional, and agent nodes compose without leaving the canvas.
- The graph artefact is auditable and reviewable.

**Liabilities**

- Version-controlling visual diffs is harder than text diffs without good artefact-level diffing.
- Large graphs become visually unreadable — modularisation (subflows) is mandatory at scale.
- Lowest-common-denominator node vocabulary may not cover bespoke logic; Code escape-hatch nodes appear and bypass the canvas's safety.
- Cross-graph refactoring is harder than across-code refactoring.

## Failure modes

- Code-node escape — bespoke logic moves into Code nodes, and the canvas shows a simple flow while the real behaviour hides inside them.
- Unreadable canvas — a large graph is kept on one canvas without subflows, and reviewers can no longer follow its paths.
- Diff blindness — changes are reviewed on the canvas only, and a moved edge goes unnoticed without an artefact-level diff.
- Graph-runtime mismatch — the runtime executes a path that is not in the stored artefact, and the canvas stops describing what runs.

## What this pattern constrains

All workflow logic must be expressed through typed nodes connected on the canvas; the runtime is not allowed to execute paths that do not appear in the graph artefact.

## Applicability

**Use when**

- Non-developer stakeholders must read, review, or edit the workflow.
- Topology inspectability is a stronger requirement than code-level concision.
- Iteration, conditional, and agent constructs need to compose visibly.
- The runtime can execute a serialised graph artefact directly.

**Do not use when**

- The workflow is mostly bespoke logic that the typed-node vocabulary cannot express cleanly.
- The team has no good story for diffing and reviewing the graph artefact.
- Latency budgets are so tight that node-by-node execution overhead is the bottleneck.
- The product needs LLM-driven dynamic plans rather than predefined topology.

## Components

- Typed-node vocabulary — Start, End, LLM, Retrieval, Tool, Conditional, Iteration, Code, Agent
- Drag-and-drop canvas — UI editor for connecting nodes
- Graph artefact — serialisable JSON or YAML representation of the workflow
- Type validator — checks node-to-node connection contracts statically
- Workflow runtime — executes the graph artefact directly

## Tools

- Low-code platform — Dify, Coze, n8n, Flowise, Langflow, FastGPT, or Bisheng
- LLM API — invoked inside LLM and Agent nodes
- Tool catalogue — registered functions exposed to Tool nodes
- Version-control system — tracks graph-artefact diffs for review

## Evaluation metrics

- Non-developer edit rate — share of changes contributed without code edits
- Type-validation catch rate — wiring errors caught before execution
- Artefact-diff review quality — reviewer ability to read the diff versus reconstructing intent
- Code escape-hatch share — fraction of nodes that bypass the typed vocabulary via Code nodes
- Subflow modularisation depth — at what graph size readability collapses without it

## Known uses

- **[Dify](https://github.com/langgenius/dify)** _available_ — Dify's headline feature is a visual canvas for building and testing AI workflows.
- **[Coze](https://www.coze.com/)** _available_ — Coze workflows expose a typed-node canvas with Start/End nodes and full agent/tool/conditional vocabulary.
- **[n8n](https://docs.n8n.io/)** _available_ — n8n's visual node canvas hosts AI Agent and Chain root nodes alongside conventional automation nodes.
- **[Flowise / Langflow](https://flowiseai.com/)** _available_ — LangChain-family visual workflow builders with typed-node canvases.
- **[FastGPT / Bisheng](https://github.com/dataelement/bisheng)** _available_ — Chinese-ecosystem visual workflow platforms with the same canvas shape.

## Related patterns

- _uses_ **Iteration Node**
- _complements_ **Event-Driven Agent**
- _complements_ **Policy-as-Code Gate**
- _complements_ **Agent-as-Tool Embedding**
- _alternative-to_ **Spec-First Agent**
- _complements_ **Iteration Node**

## References

- [Dify](https://github.com/langgenius/dify) — LangGenius
- [n8n — AI nodes](https://docs.n8n.io/) — n8n
