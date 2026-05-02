# WebAssembly Skill Runtime

**Also known as:** Wasm Cognitive Skills, Polyglot Skill Sandbox, Capability-Sandboxed Tool Plane

**Category:** Tool Use & Environment  
**Status in practice:** experimental

## Intent

Package each agent skill or tool as a WebAssembly module with an explicit capability manifest, run it inside a Wasm runtime that enforces those capabilities, so untrusted or third-party skills can run in the agent's tool plane without weakening the host's sandbox.

## Context

An enterprise agent platform that must accept user-authored or partner-authored skills written in different languages (Rust, Python compiled, TypeScript, Go) while enforcing per-skill resource and IO limits.

## Problem

Plain-process tools share the host's privileges, language-specific sandboxes (e.g. Python sandbox) are not robust, and per-skill containers are heavy; the agent can't safely run third-party skills at request rate.

## Forces

- Skills authored by partners cannot be trusted with host privileges.
- Per-request container start-up is too slow and too expensive.
- Polyglot authoring is a real requirement; Python-only is restrictive.
- Capability declarations have to be checkable, not advisory.


## Applicability

**Use when**

- Enterprise platforms must accept user- or partner-authored skills in multiple languages.
- Per-skill capabilities (filesystem, network, env, syscalls) must be enforced.
- Per-call container overhead is too heavy for request-rate execution.

**Do not use when**

- All skills are first-party and trusted.
- Wasm tooling for the target languages is not mature enough for the workload.
- A simpler sandbox already meets the threat model.

## Solution

Define a Wasm Component Model interface for skills: each skill compiles to a Wasm module and ships with a manifest declaring (filesystem paths, network hosts, env vars, syscalls) it needs. The host runtime instantiates a fresh sandbox per call with only those capabilities. Skills can be authored in any language compiling to Wasm. The host treats the manifest as the contract; missing-capability calls fail at the boundary.

## Structure

```
Host runtime { capability gate } -> Wasm sandbox(skill_module, manifest) -> deterministic IO -> result.
```

## Consequences

**Benefits**

- Polyglot skill ecosystem with one runtime.
- Strong capability isolation; manifest is the audit surface.
- Wasm cold-start is fast enough to run per request.

**Liabilities**

- Wasm ecosystem maturity per language varies (Rust strong, Python heavier).
- Capability manifest design is the real engineering problem.
- Some workloads (GPU, large data) don't fit Wasm well.

## What this pattern constrains

A skill may not exercise any capability not declared in its manifest; manifest drift is detected at load time.

## Known uses

- **[Aleph Alpha PhariaEngine](https://github.com/Aleph-Alpha/pharia-engine)** — *Available*. Cognitive Business Units (Skills) compile to Wasm and run inside the engine's sandboxed runtime.

## Related patterns

- *specialises* → [sandbox-isolation](sandbox-isolation.md)
- *complements* → [skill-library](skill-library.md)
- *complements* → [tool-discovery](tool-discovery.md)
- *complements* → [secrets-handling](secrets-handling.md)
- *complements* → [code-execution](code-execution.md)

## References

- (repo) *Aleph-Alpha/pharia-engine — Serverless AI powered by WebAssembly*, <https://github.com/Aleph-Alpha/pharia-engine>

**Tags:** tool-use, sandbox, germany-origin, wasm, aleph-alpha
