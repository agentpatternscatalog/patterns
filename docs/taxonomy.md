# Taxonomy

Thirteen categories. Each pattern belongs to exactly one. Boundaries are pragmatic: when a pattern straddles two buckets, we pick the one a reader would search first.

The thirteen: **reasoning**, **planning-control-flow**, **tool-use-environment**, **retrieval**, **memory**, **multi-agent**, **verification-reflection**, **safety-control**, **routing-composition**, **governance-observability**, **structure-data**, **streaming-ux**, **anti-patterns**.

## planning-control-flow

How the agent decides what to do next. Single-step, multi-step, sequential, parallel, branching, backtracking. The shape of the loop.

Examples: ReAct (think-act-observe loop), Plan-and-Execute (plan first, run plan), ReWOO (plan as DAG with placeholders), LLMCompiler (parallel DAG), LATS (tree search with backtracking), Planner-Executor-Observer (three-role split).

## tool-use-environment

How the agent reaches outside itself. Tool calls, code execution, protocol layers, environment adapters.

Examples: Tool Use / Function Calling, MCP (Model Context Protocol), Code Execution Sandbox, Translation Layer / Anti-Corruption Layer, Skill Library.

## memory

What the agent remembers, where, and for how long. Short-term, working, episodic, semantic, procedural. Compaction, decay, rehearsal.

Examples: Per-Thread Short-Term Memory, Episodic Summaries, Five-Tier Cascade (sensory → working → short → episodic → long), Hippocampal Rehearsal, Append-Only Thought Stream.

## multi-agent

Two or more agents (or one model worn as multiple roles) coordinating. Supervisors, workers, debate, hierarchy.

Examples: Supervisor, Orchestrator-Workers (Anthropic), Inner Committee (one model, multiple roles), Debate, Hierarchical Agents.

## verification-reflection

Catching the model's mistakes. Self-critique, evaluator loops, deterministic checks bracketing LLM calls.

Examples: Reflection (Frozen Rubric), Evaluator-Optimizer, Deterministic-LLM Sandwich, Self-Consistency at Inference, Verification-and-Grounding Loop, Inner Critic on Self-Modification, Reflexion.

## safety-control

Hard limits on what the agent may do. Constitutional rules, immutable charters, human approval gates, step bounds, cost ceilings.

Examples: Constitutional Charter (Immutable), Human-in-the-Loop, Step Budget, Cost Gating, Per-User Auth Scope, Quorum on Rule Mutation, Kill Switch, Secrets Handling.

## routing-composition

Sending requests to the right specialist. Intent classification, model selection, prompt chaining, parallel branches.

Examples: Routing (Mode Selector), Multi-Model Routing (cheap model for cheap question), Prompt Chaining, Parallelization, Fallback Chain, Provider Fallback.

## governance-observability

Audit, provenance, eval, regulatory traceability. The patterns that let humans trust the agent over time.

Examples: Provenance Ledger, Append-Only Thought Stream, Eval Harness (Champion-Challenger), LLM-as-Judge Regression, Decision Log, Replay/Time-Travel, Cost Observability, Incident Response Runbook.

## structure-data

Shape of inputs, outputs, and stored artefacts. Where typed schemas earn their seat.

Examples: Structured Output (JSON Schema), Polymorphic Record, Schema Extensibility (Reserved + Namespaced), Versioned Envelope, Open Interchange Format.

## streaming-ux

How partial state reaches the user. Streaming, push messages, agent-initiated communication, salience-driven output.

Examples: SSE Typed Events, Bidirectional Impulse Channel, Salience-Triggered Output, Citation Streaming, Stop/Cancel.

## reasoning

How the model reasons before acting. Chain-of-thought, tree search, verification, decomposition.

Examples: Chain of Thought, Tree of Thoughts, Graph of Thoughts, Chain of Verification, Self-Ask, Least-to-Most, Zero-Shot CoT, Test-Time Compute Scaling.

## retrieval

How the agent fetches knowledge from outside parameters. RAG family.

Examples: Naive RAG, Hybrid Search, HyDE, Cross-Encoder Reranking, GraphRAG, Contextual Retrieval, Agentic RAG, Self-RAG, CRAG, RAFT.

## anti-patterns

Failure modes named explicitly with their proper alternatives.

Examples: Hero Agent, Black-Box Opaqueness, Infinite Debate, Perma-Beta, Schema-Free Output, Unbounded Loop, Same-Model Self-Critique, Hallucinated Tools, Hallucinated Citations, Naive-RAG-First, Tool Explosion, Hidden Mode Switching, Tool Output Trusted Verbatim, Prompt Bloat, Unbounded Subagent Spawn.
