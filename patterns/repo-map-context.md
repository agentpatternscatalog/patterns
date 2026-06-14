# Repo Map

**Also known as:** Repository Map, Structural Code Context

**Category:** Retrieval & RAG  
**Status in practice:** emerging

## Intent

Give the agent a compact, ranked map of the codebase's symbols and their dependencies so it orients on what matters before reading any files.

## Context

A coding agent must work in a repository far larger than its context window — thousands of files, deep dependency chains, conventions spread across modules. It cannot read everything, and keyword search finds matching text but says nothing about which symbols are important or how they connect. Dumping whole files wastes the window on code the task never touches.

## Problem

Without a structural overview the agent explores blindly: it greps, opens files at random, and misses the few symbols that actually govern the change, while burning context on irrelevant code. It needs a high-signal summary of the repository's structure — which symbols exist and how they depend on each other — small enough to fit the window yet ranked so the important parts survive truncation.

## Forces

- A repository never fits the context window, but blind keyword search is structure-blind and whole-file dumps are wasteful.
- A static structural map costs precompute and goes stale as the agent edits the code.
- Ranking by importance keeps the map small, but the ranking signal must be cheap to compute over a large graph.

## Therefore

Therefore: parse the repository into a symbol-and-dependency graph, rank it by importance (for example PageRank over the call and import edges), and hand the agent a compact map of the top symbols so it orients before opening files.

## Solution

Parse the repository with a language-aware parser such as tree-sitter into symbols (functions, classes, methods) and the call and import edges between them. Run a centrality measure like PageRank over that graph to score each symbol's importance, optionally biased toward files the current task mentions. Render the top-ranked symbols and their signatures as a compact text map and place it in the agent's context as orientation, refreshing it as the working tree changes. The agent reads the map first, then opens only the files the map points to.

## Structure

```
Repo files -> tree-sitter parse -> symbol + dependency graph -> PageRank rank -> compact top-N map -> agent context
```

## Diagram

```mermaid
flowchart TD
  repo[Repository files] --> parse[tree-sitter parse]
  parse --> graph[Symbol + dependency graph]
  graph --> rank[PageRank by importance]
  rank --> map[Compact ranked map]
  map --> ctx[Agent context]
  ctx --> open[Open only mapped files]
```

*The repository is parsed and ranked into a compact map that orients the agent before it opens files.*

## Example scenario

An agent is asked to add rate limiting to an API server with 800 source files. Instead of searching for the word 'limit', it first reads a repo map that ranks Server.handle, Router.dispatch, and Middleware.apply as the most central symbols. The map shows that requests flow through Middleware.apply, so the agent opens just that file and its two callers, makes the change, and never loads the other 795 files.

## Consequences

**Benefits**

- The agent orients on the few load-bearing symbols instead of searching blindly.
- Context spend shifts from whole files to a small ranked summary, leaving room for the actual task.
- Importance ranking degrades gracefully: when the map is truncated, the most central symbols survive.

**Liabilities**

- Building and ranking the graph costs precompute before any query is served.
- The map goes stale as the agent edits; it must be rebuilt or it misleads.
- Languages without a good parser get a weaker map.

## Failure modes

- Stale map — edits during the session make the map describe a repository that no longer exists.
- Mis-ranking — the centrality measure elevates utility code over the symbols the task actually needs.
- Map bloat — too high a top-N pushes the map past the budget it was meant to save.

## What this pattern constrains

The agent does not browse the repository blind; it must consult the ranked structural map first and may only open files the map surfaces as relevant, rather than dumping whole files or relying on keyword search alone.

## Applicability

**Use when**

- The agent works in a codebase far larger than its context window.
- A language-aware parser can extract symbols and dependency edges for the repository.
- Orienting on structure before reading files would cut wasted context and missed-symbol errors.

**Do not use when**

- The codebase is small enough to fit in context or has no meaningful structure.
- The working tree changes so fast that a map cannot be kept current.
- Plain similarity retrieval over code already gives adequate orientation.

## Components

- Parser — extracts symbols and call/import edges from the repository (for example tree-sitter)
- Dependency graph — nodes are symbols, edges are calls and imports
- Ranker — scores symbol importance with a centrality measure such as PageRank
- Map renderer — emits the top-ranked symbols and signatures as a compact text block
- Refresher — rebuilds the map as the working tree changes so it does not go stale

## Tools

- Tree-sitter or an equivalent AST parser — turns source into a symbol-and-edge graph across languages
- Graph centrality library — computes PageRank over the dependency graph
- Coding agent context window — receives the rendered map as orientation

## Evaluation metrics

- Files opened per task vs a blind-search baseline — how much the map narrows exploration
- Context tokens spent on orientation vs whole-file dumps — the budget the map saves
- Edit-localisation accuracy — whether the agent lands the change in the symbols the map surfaced
- Map staleness rate — how often the map describes code that has since changed

## Known uses

- **[Aider repo map](https://aider.chat/docs/repomap.html)** _available_ — Builds a PageRank-weighted tree-sitter map of the repository and sends it to the model as orientation with each request.
- **[Inside the Scaffold (coding-agent taxonomy)](https://arxiv.org/abs/2604.03515)** _available_ — Catalogs 'Repo map (static analysis)' as a distinct context-retrieval paradigm used across coding agents (Aider, Cline).

## Related patterns

- _alternative-to_ **Hierarchical Retrieval** — Hierarchical retrieval cascades coarse-to-fine by content similarity; a repo map ranks by code structure (call/import centrality).
- _alternative-to_ **GraphRAG** — GraphRAG builds an entity-relation graph over prose; a repo map builds a symbol-dependency graph over code.
- _complements_ **Filesystem as Context** — The map is a ranked index over the same working tree the agent reads files from.
- _complements_ **Code-as-Action Agent**

## References

- [Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures](https://arxiv.org/abs/2604.03515) — 2026
- [Aider: Repository map](https://aider.chat/docs/repomap.html) — Aider, 2024
