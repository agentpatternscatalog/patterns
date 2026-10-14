# Schema Extensibility

**Also known as:** Reserved Fields, Namespaced Extensions

**Category:** Structure & Data  
**Status in practice:** mature

## Intent

Build schemas that evolve without breaking old clients via reserved namespaces and extension blocks.

## Context

A team owns a data format that lives for years and is read by clients of different ages — exported files, API payloads, event records in a queue. New fields show up regularly because the product evolves, and the team cannot reasonably upgrade every client at the same moment a new field is added. They need a way to add fields, and to let vendors add their own extensions, without forcing a coordinated release.

## Problem

A rigid schema that lists exactly which fields are allowed will reject any payload that contains a new field, which means every addition becomes a breaking change for every existing client. The obvious workaround — accepting anything and validating nothing — turns the schema into mush, lets typos through, and makes it impossible to tell deliberate extensions apart from accidents. The team has to choose between cascading breaking changes and losing the schema's value as a contract, and neither is acceptable for a long-lived format.

## Forces

- Old clients should ignore new fields, not error.
- New fields should be discoverable, not hidden.
- Versioning policy must be agreed upfront.

## Therefore

Therefore: wrap payloads in a versioned envelope with reserved extension namespaces, so that old clients ignore new fields and `schema_version` becomes the only breaking-change signal.

## Solution

Define a versioned envelope (`{schema_version, type, payload}`). Reserve namespaces for extensions (`x-vendor.foo`, `extensions: {...}`). Old clients ignore unknown extensions. Bumps to schema_version are the only breaking-change signal.

## Structure

```
Producer -> Envelope {schema_version, type, payload, extensions: {x-vendor.*}} -> Client: known version -> validate core payload; unknown extension -> ignore; schema_version bump -> treat as breaking change
```

## Diagram

```mermaid
classDiagram
  class Envelope {
    +schema_version
    +type
    +payload
  }
  class Extensions {
    +x-vendor.foo
    +x-vendor.bar
  }
  Envelope o-- Extensions : extensions
  note for Envelope "Old clients ignore unknown extensions;\nschema_version bump = breaking change"
```

## Example scenario

A typed event stream between agent and client ships v1; six months later the client team needs three new fields and a vendor-specific extension. Without extensibility the schema breaks every old client. The team had used a versioned envelope (`{schema_version, type, payload, extensions}`) with reserved `x-vendor.*` namespaces from day one; adding the new fields and extensions ships without breaking older clients, and a `schema_version` bump is reserved for genuine incompatibilities.

## Consequences

**Benefits**

- Long-lived format with low breakage.
- Per-vendor extensions don't pollute the core.

**Liabilities**

- Extension proliferation is a real risk.
- Versioning discipline must be enforced socially or technically.

## Failure modes

- Extension sprawl — every vendor adds its own `x-` fields, nobody retires them, and the payload fills with overlapping extensions.
- Silent breaking change — a producer changes the meaning of a core field without bumping schema_version, and old clients misread it.
- Cross-namespace reliance — a client starts depending on another vendor's extension field, and breaks when that vendor changes it.
- Typo as extension — a misspelled field lands in the extensions block, is ignored by clients, and the intended value is lost without an error.

## What this pattern constrains

Clients cannot rely on extension fields outside their declared namespace.

## Applicability

**Use when**

- Schemas are long-lived and will accumulate fields over time.
- Multiple clients of different ages must coexist with the same data format.
- Breaking-change cost across clients is high.

**Do not use when**

- The schema is internal, short-lived, and a single client owns it.
- Strict validation of all fields is required (no unknown extensions allowed).
- Versioning discipline cannot be enforced and the envelope would rot.

## Components

- Versioned envelope — wraps payloads with schema_version, type, and payload so breaking changes are explicit
- Reserved extension namespace — declared range (e.g. x-vendor.*, extensions: {...}) where new fields can land without colliding
- Forward-compatible reader — ignores unknown extension keys instead of erroring on them
- Schema-version arbiter — enforces that only schema_version bumps signal breaking changes
- Vendor-extension registry — optional governance layer recording which vendor owns which namespace

## Tools

- Protocol Buffers with reserved field numbers — language-neutral schema with built-in forward compatibility
- JSON Schema or OpenAPI with x-* extension keys — declares the reserved namespace inside the contract
- Schema-evolution linter — flags additions that would require a schema_version bump

## Evaluation metrics

- Old-client read success rate after additions — fraction of pre-change clients that still parse new payloads cleanly
- Breaking-change incidence per release — should approach zero between schema_version bumps
- Extension-namespace collision count — distinct vendors writing to the same x-* key; flags governance gaps
- Unknown-field drop rate — extensions silently lost on round-trip, which defeats the pattern
- Schema-version cadence — how often genuine breaking changes ship; informs deprecation policy

## Known uses

- **Weft** _available_ — Versioned envelope: {weft_version, type, exported_at, exported_from, items}.

## Related patterns

- _complements_ **Polymorphic Record**
- _complements_ **Translation Layer**

## References

- [Protocol Buffers backwards compatibility](https://protobuf.dev/programming-guides/proto3/#updating)
