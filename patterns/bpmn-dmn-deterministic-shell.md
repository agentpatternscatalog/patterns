# BPMN/DMN Deterministic Shell Around Agent

**Also known as:** BPMN-Spine LLM-Leaf, Workflow-Engine-Grounded Agent

**Category:** Routing & Composition  
**Status in practice:** emerging

## Intent

BPMN (Business Process Model and Notation) processes and DMN (Decision Model and Notation) decision tables form the deterministic spine; LLM-driven agents are invoked only at explicit 'unstructured problem' nodes inside the process.

## Context

An enterprise has existing BPMN workflows and DMN decision tables. Adding agents directly replaces some workflow steps, breaking the existing observability and governance built around workflow engines.

## Problem

Pure-agent replacement of workflow steps loses BPMN observability (which step is running, how long did it take), DMN auditability (which decision rule fired), and existing operator tooling. Hybrid solutions where the agent runs *outside* the workflow lose the integration. Differs from existing hybrid-symbolic-neural-routing by being specifically workflow-engine-grounded — BPMN/DMN as the surrounding shell.

## Forces

- BPMN/DMN engines are mature; adding agent invocations is integration work.
- Some steps are genuinely unstructured and benefit from agent flexibility.
- Workflow engines vary in their support for asynchronous and long-running steps.

## Therefore

Therefore: BPMN/DMN remain the orchestration spine; agents are invoked as specialized service tasks at nodes labeled 'unstructured problem'; agent outputs feed back into BPMN flow.

## Solution

Model the end-to-end process as BPMN. Decision points use DMN rules where possible. At nodes that need LLM-driven flexibility (free-form input handling, summarization, classification with judgement), invoke an agent as a BPMN service task; the agent runs, returns structured output to the workflow engine, BPMN flow continues. Pair with deterministic-control-flow-not-prompt, hybrid-symbolic-neural-routing, plan-and-execute.

## Structure

```
Start --> DMN decision --> BPMN step --> Agent service task (unstructured-problem node) --> Output adapter --structured result--> DMN decision --> BPMN step --> End; BPMN engine owns all orchestration
```

## Diagram

```mermaid
flowchart LR
  Start[Start] --> D1[DMN decision]
  D1 --> S1[BPMN step]
  S1 --> Agent[Agent service task]
  Agent --> D2[DMN decision]
  D2 --> S2[BPMN step]
  S2 --> End[End]

```

## Example scenario

A claim-processing BPMN: 'receive claim' → 'classify (DMN rule)' → 'extract fields (agent service task)' → 'verify (DMN rule)' → 'approve (DMN rule)' → 'notify'. The 'extract fields' node is an agent because claim documents are unstructured. Everything else is deterministic BPMN/DMN. Auditors see the full process in the existing BPMN dashboard; the agent invocation is one labeled service task.

## Consequences

**Benefits**

- BPMN observability and DMN auditability preserved.
- Agent invocation localized to nodes where flexibility is genuinely needed.
- Operator tooling (BPMN dashboards, DMN editors) continues to work.

**Liabilities**

- Two paradigms (workflow engine + agent runtime) to operate.
- BPMN engine must support agent invocation as a service task.
- Agent service-task outputs must conform to BPMN flow expectations.

## Failure modes

- Off-contract agent output — the agent service task returns text or fields the BPMN flow does not expect, and the next gateway or DMN table fails or takes the wrong branch.
- Orchestration creep — routing decisions slip into agent prompts, and the BPMN model no longer shows how the process really runs.
- Agent at a structured node — an agent task is placed where a DMN table would do, and an auditable decision becomes an untraceable one.
- Long-running task mismatch — the engine handles slow or asynchronous agent calls poorly, and process instances time out or hang at the agent node.

## What this pattern constrains

The BPMN engine is the orchestrator; agents are invoked as service tasks at explicitly-labeled unstructured-problem nodes; orchestration logic does not live in agent prompts.

## Applicability

**Use when**

- Enterprise with mature BPMN/DMN governance.
- Process has both deterministic and unstructured steps.
- Workflow engine supports agent invocation as service task.

**Do not use when**

- No existing BPMN/DMN infrastructure.
- Process is end-to-end unstructured.
- Workflow engine cannot integrate agent invocations.

## Components

- BPMN workflow engine — orchestration spine
- DMN decision tables — deterministic decisions
- Agent service task — invoked at unstructured-problem nodes
- Output adapter — agent output → BPMN-compatible structure

## Tools

- BPMN workflow engine
- DMN decision-table engine
- Agent service-task adapter

## Evaluation metrics

- Agent-task latency within BPMN flow
- BPMN observability coverage — share of process visible
- DMN-vs-agent decision split

## Known uses

- **[it-daily.net (German): KI-Agenten in der Produktion 2026 — Prozessstandard](https://www.it-daily.net/it-management/ki/ki-agenten-in-der-produktion-2026-vom-prototyp-zum-prozessstandard)** _available_

## Related patterns

- _complements_ **Hybrid Symbolic-Neural Routing**
- _complements_ **Deterministic Control Flow, Not Prompt**
- _alternative-to_ **Plan-and-Execute**
- _complements_ **Agent-as-Tool Embedding**
- _complements_ **Policy-Gated Agent Action (KRITIS)**
- _complements_ **Agent-to-Rule Distillation** — The shell is the destination structure — a deterministic spine with agent nodes for unstructured problems; distillation is the lifecycle loop that grows the spine by migrating stabilised agent solutions into it.

## References

- [KI-Agenten in der Produktion 2026: Vom Prototyp zum Prozessstandard](https://www.it-daily.net/it-management/ki/ki-agenten-in-der-produktion-2026-vom-prototyp-zum-prozessstandard) — 2026
