# Distributed Constraint Optimization

**Also known as:** DCOP, ADOPT, Distributed Constraint Reasoning

**Category:** Planning & Control Flow  
**Status in practice:** experimental

## Intent

A group of agents jointly assigns values to shared variables to minimise (or maximise) a global cost defined by inter-agent constraints, exchanging only the messages needed.

## Context

Several agents each hold private variables and constraints — meeting scheduling across users who don't want to expose calendars, resource allocation across teams that don't share budgets, sensor coordination across nodes that can't centralise. The global cost depends on all variables, but no single agent has the right to see them all.

## Problem

Centralising the whole problem is the easy answer but often illegal, expensive, or politically infeasible. Each agent solving locally produces solutions that violate global constraints. Without a distributed coordination algorithm that respects information boundaries, the team cannot find a global-cost-minimising assignment without surrendering privacy or autonomy.

## Forces

- Information cannot or should not be fully centralised.
- Local optima may violate global constraints.
- Message-passing has cost; communication must be bounded.
- Some algorithms guarantee global optimum (ADOPT) at high message cost; others are heuristic and faster.

## Therefore

Therefore: cast the joint assignment as a DCOP and solve with a distributed algorithm that exchanges only the messages needed, so global cost is minimised without centralising private variables or constraints.

## Solution

Cast the problem as a DCOP (Distributed Constraint Optimisation Problem): each agent owns variables; constraints are factored across agents. Run a distributed solver — ADOPT (Asynchronous Distributed OPTimisation) for a guaranteed optimum, or DPOP, Max-Sum, or local-search heuristics for cheaper approximate solutions. Each agent communicates only with constraint-neighbours. The algorithm terminates with each agent holding an assignment that is consistent with the others and minimises (or approximately minimises) global cost. For LLM-agent applications, the LLM may serve as a propose-and-evaluate step at each agent, with a small DCOP-like backbone enforcing global consistency.

## Structure

```
Each agent (own variables + local constraints) <--messages to constraint-neighbours only (ADOPT / DPOP / Max-Sum)--> neighbour agents --> termination detector --> consistent, low-cost global assignment
```

## Diagram

```mermaid
flowchart LR
  A1[Agent 1: vars + local constraints] <--> A2[Agent 2: vars + local constraints]
  A2 <--> A3[Agent 3: vars + local constraints]
  A1 <--> A3
  A1 --> Sol[Assignment consistent + low cost]
  A2 --> Sol
  A3 --> Sol
```

## Example scenario

Five team-calendar agents schedule a recurring cross-team meeting without exposing individual calendars. Each agent owns a variable (proposed slot) constrained by no-overlap with its team's commitments. They run Max-Sum: each agent proposes locally, exchanges aggregate cost messages with neighbours, and converges on a slot that minimises total conflict across teams without anyone seeing another team's calendar.

## Consequences

**Benefits**

- Global optimisation without centralising private data.
- Information boundaries respected by construction.
- Algorithm choice tunes communication cost vs solution quality.

**Liabilities**

- Optimal algorithms (ADOPT) have exponential worst-case message complexity.
- Constraint factorisation is itself a design problem.
- Heuristic solvers may stall in local optima.

## Failure modes

- Message blow-up — an exact solver such as ADOPT meets a dense constraint graph, and message traffic grows until the run cannot finish in time.
- Local-optimum stall — a heuristic solver settles on an assignment where no single agent can improve, while the global cost is still high.
- Bad factorisation — constraints are split across agents in the wrong way, so the solver optimises a problem that does not match the real one.
- Quiet centralisation — to get a result faster, agents send their full local state to one node, breaking the information boundary the pattern was meant to keep.

## What this pattern constrains

Joint problems must not be centralised when information boundaries forbid it; agents exchange only the messages a distributed solver requires.

## Applicability

**Use when**

- Several agents hold variables/constraints that cannot be centralised.
- Global cost depends on the joint assignment.
- Some algorithm in the DCOP family fits the cost/quality budget.

**Do not use when**

- Centralising is legal, cheap, and politically fine.
- Constraints cannot be factored across agents — DCOP needs factorisation.
- Communication cost dominates any optimisation benefit.

## Components

- Local variables — owned by each agent
- Local constraints — owned by each agent
- Message protocol — algorithm-specific (ADOPT, DPOP, Max-Sum)
- Termination detector — recognises when assignment is final

## Tools

- DCOP solver library — implements the algorithm family
- Message bus — neighbour-to-neighbour exchange
- Trace log — captures the message trace

## Evaluation metrics

- Solution quality vs centralised optimum (where measurable)
- Message count to convergence
- Wall-clock convergence time

## Known uses

- **[Multiagent Systems (Weiss) — Distributed Constraint Reasoning (Yokoo & Ishida chapter)](https://mitpress.mit.edu/9780262731317/multiagent-systems/)** _available_
- **[Sensor-network scheduling, distributed meeting scheduling research deployments](https://arxiv.org/abs/1602.06347)** _available_

## Related patterns

- _complements_ **Partial Global Planning**
- _alternative-to_ **Blackboard**
- _alternative-to_ **Supervisor**
- _complements_ **Contract Net Protocol**
- _alternative-to_ **World Model as Tool**
- _alternative-to_ **Stigmergic Coordination**
- _alternative-to_ **Solver-Ready Formulation Handoff** — That solves a constraint problem across many agents holding shared variables because information boundaries forbid centralising it; here one centralised exact solver decides and the agents only write the model.

## References

- [Multiagent Systems, 2nd ed.](https://mitpress.mit.edu/9780262731317/multiagent-systems/) — Gerhard Weiss (ed.), 2013
- [Distributed constraint optimization](https://en.wikipedia.org/wiki/Distributed_constraint_optimization)
