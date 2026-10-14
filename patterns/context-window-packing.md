# Context Window Packing

**Also known as:** Context Compression, Token Budget Management, Fit in Context, Token Cost Reduction

**Category:** Memory  
**Status in practice:** mature

## Intent

Choose what fits in the context window each turn given a fixed token budget.

## Context

An agent's available context for the next model call — the system prompt, conversation history, retrieved chunks, tool definitions, current state, and any other information the model needs — has grown to the point where it exceeds the model's maximum context window. The team has to decide what goes in and what stays out for every single call.

## Problem

Naively concatenating everything overflows the window and the call fails. Naively truncating from the start or the end drops information that may be critical (the original task, the most recent tool result, the system prompt itself). A first-fit packing strategy leaves the model with a different subset on every call, which makes behaviour unpredictable. The team needs a deliberate policy for what is preserved, what is summarised, what is retrieved on demand, and what is dropped — and that policy has to be applied consistently across calls.

## Forces

- What to drop is task-dependent.
- Compression has its own LLM cost.
- Reserved budget for the response itself.

## Therefore

Therefore: budget the window explicitly across system, tools, history, retrieval, and response before each call, so that nothing important is silently truncated and nothing wasteful is silently included.

## Solution

Define a packing policy. Reserve N tokens for system + tools + response. Allocate the rest across history (compressed), retrieved chunks (top-k after rerank), and current state. Use eviction (drop oldest), summarisation (compress), or selection (relevance-rank) policies. Audit token counts before each call.

## Structure

```
Token budget T --reserve N--> System + tools + reply slot; remainder --packing policy--> {compressed history, top-k reranked chunks, current state} --token audit--> Context window --> Model call
```

## Diagram

```mermaid
flowchart TD
  B[Token budget T] --> R[Reserve N for system + tools + reply]
  R --> P[Packing policy]
  P --> H[History compressed]
  P --> K[Top-k retrieved chunks<br/>after rerank]
  P --> S[Current state]
  H --> CW[Context window]
  K --> CW
  S --> CW
```

## Example scenario

A long-running support agent has a 200k window and a thirty-turn conversation full of tool outputs, two 80-page attached PDFs, and the system charter. Naive concatenation overflows; truncating from the back loses the original ticket; truncating from the front loses the latest turn. The team builds a Context-Window Packing step: each turn it scores items by recency, relevance, and pinned-status, then fits a budgeted subset, replacing the rest with summaries. The window stops overflowing and critical state stays visible.

## Consequences

**Benefits**

- Predictable behaviour at the window edge.
- Inspectable trade-offs.

**Liabilities**

- Complexity of the packing logic.
- Compression artefacts.

## Failure modes

- Reserve too small — the packer fills the window right up to the limit and the reply is cut off mid-answer.
- Task eviction — a drop-oldest rule removes the original instruction, and the model drifts from the goal.
- Summary distortion — compressed history loses a key detail and the model acts on a wrong version of earlier turns.
- Count mismatch — the packer counts tokens with a different tokenizer than the model, and calls fail at the window edge.

## What this pattern constrains

Total tokens passed to the model must not exceed the window minus the reserved response budget.

## Applicability

**Use when**

- Naive concatenation overflows the context window for realistic inputs.
- Some context (system, tools, response reservation) is fixed and the rest must be allocated dynamically.
- You can audit token counts before each call and adjust the policy.

**Do not use when**

- Inputs are small and always fit comfortably in the window.
- There is no measurable quality difference between packing policies and the work is overhead.
- An external memory or retrieval layer already controls what reaches the model.

## Components

- Token budgeter — pre-call accountant that reserves slots for system, tools, response, and remaining slack
- Packing policy — declares allocation across history, retrieved chunks, current state, and pins
- Eviction or summarisation step — applies the policy by dropping, compressing, or relevance-ranking content
- Pre-call auditor — counts tokens against the model's window and fails loudly when the policy overshoots
- Reranker — orders retrieved chunks so the top-k that survive the budget cut are the most useful ones

## Tools

- Tokeniser — tiktoken, Anthropic token counting endpoint, or model-native counter used before every call
- Summarisation LLM — secondary model call that compresses older turns into a few sentences
- Reranker — bge-reranker or Cohere Rerank to score retrieved chunks before the budget cut

## Evaluation metrics

- Overflow rate — fraction of calls that would have exceeded the window before pre-call audit
- Critical-fact retention — task-level checks that load-bearing facts (original goal, key constraints) stayed in the window
- Compression cost per turn — tokens and money spent on summarisation per packed call
- Behaviour drift across packing strategies — answer-quality delta when policies change, held against a fixed eval set
- Reserved-response saturation — how often the reply fills the reserved budget and gets truncated

## Known uses

- **[LangChain ConversationSummaryBufferMemory](https://python.langchain.com/api_reference/langchain/memory/langchain.memory.summary_buffer.ConversationSummaryBufferMemory.html)** _available_
- **Most production agent frameworks** _available_
- **[Sparrot](https://marco-nissen.com/sparrot/)** _available_ — Prompt-cache management and a context-packer fit the per-tick prompt into the model's window deliberately (stable prefix, recent ledger, current workspace, active variant) rather than relying on the provider to truncate.

## Related patterns

- _complements_ **Dynamic Scaffolding**
- _uses_ **Episodic Summaries**
- _alternative-to_ **MemGPT-Style Paging**
- _used-by_ **Reasoning Trace Carry-Forward**
- _alternative-to_ **Salience Attention Mechanism**
- _complements_ **Self-Archaeology**
- _used-by_ **Todo-List-Driven Autonomous Agent**
- _complements_ **Tool Search Lazy Loading**
- _complements_ **Sleep-Time Compute**
- _complements_ **Context Window Dumb-Zone Cap**
- _complements_ **Landmark Attention**
- _complements_ **Information Chunking for Agent Memory**
- _alternative-to_ **Lost in the Middle (Positional Bias)**
- _complements_ **Context Compaction** — Compaction condenses what packing has placed into the window once it fills.
- _complements_ **Tool-Result Eviction** — Packing decides what enters the window; eviction decides what leaves it once consumed.

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) — Liu, Lin, Hewitt, Paranjape, Bevilacqua, Petroni, Liang, 2023
