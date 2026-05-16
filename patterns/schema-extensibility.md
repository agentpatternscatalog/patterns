# Schema Extensibility

**Also known as:** Reserved Fields, Namespaced Extensions

**Category:** Structure & Data  
**Status in practice:** mature

## Intent

Build schemas that evolve without breaking old clients via reserved namespaces and extension blocks.

## Context

Long-lived data formats accumulate fields; rigid schemas force breaking changes that cascade through clients.

## Problem

Rigid schemas break when fields are added; permissive schemas become incoherent.

## Forces

- Old clients should ignore new fields, not error.
- New fields should be discoverable, not hidden.
- Versioning policy must be agreed upfront.


## Applicability

**Use when**

- Schemas are long-lived and will accumulate fields over time.
- Multiple clients of different ages must coexist with the same data format.
- Breaking-change cost across clients is high.

**Do not use when**

- The schema is internal, short-lived, and a single client owns it.
- Strict validation of all fields is required (no unknown extensions allowed).
- Versioning discipline cannot be enforced and the envelope would rot.

## Therefore

Therefore: wrap payloads in a versioned envelope with reserved extension namespaces, so that old clients ignore new fields and `schema_version` becomes the only breaking-change signal.

## Solution

Define a versioned envelope (`{schema_version, type, payload}`). Reserve namespaces for extensions (`x-vendor.foo`, `extensions: {...}`). Old clients ignore unknown extensions. Bumps to schema_version are the only breaking-change signal.

## Variants

- **Reserved field numbers** — Protobuf-style: reserve numeric tags up front so future fields cannot collide with old ones (Protocol Buffers).
- **Vendor-namespaced extensions** — Allow `x-vendor.foo` keys outside the core schema; old clients ignore unknown `x-` keys (OpenAPI, JSON Schema).
- **Versioned envelope** — Wrap payload in `{schema_version, type, payload}`; bumps to `schema_version` are the only breaking-change signal.

## Example scenario

A typed event stream between agent and client ships v1; six months later the client team needs three new fields and a vendor-specific extension. Without extensibility the schema breaks every old client. The team had used a versioned envelope (`{schema_version, type, payload, extensions}`) with reserved `x-vendor.*` namespaces from day one; adding the new fields and extensions ships without breaking older clients, and a `schema_version` bump is reserved for genuine incompatibilities.

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

## Consequences

**Benefits**

- Long-lived format with low breakage.
- Per-vendor extensions don't pollute the core.

**Liabilities**

- Extension proliferation is a real risk.
- Versioning discipline must be enforced socially or technically.

## What this pattern constrains

Clients cannot rely on extension fields outside their declared namespace.

## Known uses

- **Weft** — *Available*. Versioned envelope: {weft_version, type, exported_at, exported_from, items}.

## Related patterns

- *complements* → [polymorphic-record](polymorphic-record.md)
- *complements* → [translation-layer](translation-layer.md)

## References

- (doc) *Protocol Buffers backwards compatibility*, <https://protobuf.dev/programming-guides/proto3/#updating>

**Tags:** schema, extensibility, versioning
