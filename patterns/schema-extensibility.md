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

## Solution

Define a versioned envelope (`{schema_version, type, payload}`). Reserve namespaces for extensions (`x-vendor.foo`, `extensions: {...}`). Old clients ignore unknown extensions. Bumps to schema_version are the only breaking-change signal.

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
