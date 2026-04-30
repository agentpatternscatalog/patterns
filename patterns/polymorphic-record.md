# Polymorphic Record

**Also known as:** Tagged Union, Discriminated Union

**Category:** Structure & Data  
**Status in practice:** mature

## Intent

Represent a family of related entities in a single core schema with type-specific extensions.

## Context

Multiple entity sub-types (yarn / fabric / thread; project / queue / favorite) share most fields but differ in some.

## Problem

Separate schemas per sub-type duplicate work and break clients that do not understand all sub-types; one giant schema with all fields is bloated and unenforceable.

## Forces

- Common fields must stay common; new sub-types must not break old ones.
- Type-specific fields need a clean place to live.
- Validation must be per-sub-type, not just per-record.

## Solution

Define a core schema with the common fields and a discriminator (e.g. `material_type`). Sub-type fields live in a namespaced extension block (e.g. `yarn: {...}` for yarn-specific). Clients that do not understand a sub-type still read the core fields and round-trip the rest without data loss.

## Consequences

**Benefits**

- Forward-compatible: new sub-types don't break old clients.
- One core schema; many specialisations.

**Liabilities**

- Validation logic per sub-type adds complexity.
- Discriminator-driven code paths can be hard to debug.

## What this pattern constrains

Sub-type fields must live under their namespaced extension; they cannot pollute the core.

## Known uses

- **Weft** — *Available*. Material with material_type=yarn / fabric / thread / etc.; Pattern across knitting / crochet / weaving / etc.
- **FHIR resource polymorphism** — *Available*
- **Stripe API discriminated objects** — *Available*
- **JSON-LD @type** — *Available*
- **OpenAPI discriminator/oneOf** — *Available*

## Related patterns

- *complements* → [schema-extensibility](schema-extensibility.md)
- *complements* → [translation-layer](translation-layer.md)

## References

- (book) Martin Kleppmann, *Designing Data-Intensive Applications*, 2017

**Tags:** schema, polymorphism, data
