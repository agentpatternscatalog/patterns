#!/usr/bin/env python3
"""Generate patterns.graph.json — a derived, machine-readable view of the catalog as a typed graph.

Nodes: one per pattern (id, name, category, status, aliases), plus a lightweight node for
each methodology that a pattern's related[] edge points at (category "methodology"). The
catalog deliberately lets related[] cross the pattern↔methodology layer boundary (e.g.
evaluation-driven-development), so the graph carries those targets as nodes rather than
silently dropping the edges.

Edges: one per related[] entry (source, target, relation) whose target resolves to a
pattern or methodology id.

Source of truth is patterns-src/ (and methodologies-src/ for cross-layer targets). This
script always builds from those shards; it never reads the derived patterns.json, so the
graph cannot inherit staleness from a sibling build artifact.

Run locally: python3 .github/scripts/build_graph.py [out_dir]
Reads:  patterns-src/*.json, methodologies-src/*.json
Writes: <out_dir>/patterns.graph.json  (default: repo root)
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PATTERNS_SRC = ROOT / "patterns-src"
METHODOLOGIES_SRC = ROOT / "methodologies-src"

VERSION = "0.2.0"
LICENSE = "CC-BY-4.0"


def load_patterns() -> list[dict]:
    """Build the pattern list from patterns-src/ shards (the source of truth)."""
    patterns: list[dict] = []
    seen_ids: set[str] = set()
    for shard_path in sorted(PATTERNS_SRC.glob("*.json")):
        shard = json.loads(shard_path.read_text())
        for p in shard["patterns"]:
            if p["id"] in seen_ids:
                raise SystemExit(f"duplicate pattern id: {p['id']}")
            seen_ids.add(p["id"])
            patterns.append(p)
    patterns.sort(key=lambda p: (p["category"], p["id"]))
    return patterns


def load_methodology_names() -> dict[str, str]:
    """id -> name for methodologies. related[] may target these (cross-layer links)."""
    names: dict[str, str] = {}
    if not METHODOLOGIES_SRC.exists():
        return names
    for shard_path in sorted(METHODOLOGIES_SRC.glob("*.json")):
        shard = json.loads(shard_path.read_text())
        for m in shard.get("methodologies", []):
            if "id" in m:
                names[m["id"]] = m.get("name", m["id"])
    return names


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    patterns = load_patterns()
    methodology_names = load_methodology_names()

    pattern_ids = {p["id"] for p in patterns}
    methodology_ids = set(methodology_names)

    nodes = [
        {
            "id": p["id"],
            "name": p["name"],
            "category": p["category"],
            "status": p.get("status_in_practice", "unknown"),
            "aliases": p.get("aliases", []),
        }
        for p in patterns
    ]

    # Collect methodology targets actually referenced by a related[] edge, and emit a
    # lightweight node for each so cross-layer edges resolve instead of being dropped.
    referenced_methodologies: set[str] = set()
    edges: list[dict] = []
    dropped: list[tuple[str, str, str]] = []
    for p in patterns:
        for r in p.get("related", []):
            tgt, rel = r["pattern"], r["relation"]
            if tgt in pattern_ids:
                edges.append({"source": p["id"], "target": tgt, "relation": rel})
            elif tgt in methodology_ids:
                referenced_methodologies.add(tgt)
                edges.append({"source": p["id"], "target": tgt, "relation": rel})
            else:
                dropped.append((p["id"], tgt, rel))

    for mid in sorted(referenced_methodologies):
        nodes.append(
            {
                "id": mid,
                "name": methodology_names[mid],
                "category": "methodology",
                "status": "unknown",
                "aliases": [],
            }
        )

    out = {
        "$schema": "./patterns.graph.schema.json",
        "version": VERSION,
        "updated": date.today().isoformat(),
        "license": LICENSE,
        "source": "patterns-src/, methodologies-src/",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }
    out_path = out_dir / "patterns.graph.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    try:
        display = out_path.relative_to(ROOT)
    except ValueError:
        display = out_path
    print(
        f"wrote {display}  ({len(nodes)} nodes "
        f"[{len(referenced_methodologies)} methodology], {len(edges)} edges)"
    )
    if dropped:
        print(f"WARNING: {len(dropped)} related[] edges target unknown ids:")
        for src, tgt, rel in dropped[:20]:
            print(f"  {src} -{rel}-> {tgt}")
        raise SystemExit(1)


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    build(out_dir)


if __name__ == "__main__":
    main()
