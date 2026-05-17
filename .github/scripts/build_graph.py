#!/usr/bin/env python3
"""Generate patterns.graph.json — a derived, machine-readable view of the catalog as a typed graph.

Nodes: one per pattern (id, name, category, status_in_practice, aliases).
Edges: one per related[] entry (source, target, relation).

Consumers (graph queries, CI checks, architecture review tools) can build on this without
parsing the full pattern shapes. Source of truth remains patterns-src/ shards / patterns.json.

Run locally: python3 .github/scripts/build_graph.py [out_dir]
Reads:  patterns-src/*.json (via build_patterns_json structure) or patterns.json if present.
Writes: <out_dir>/patterns.graph.json  (default: repo root)
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC_PATTERNS_JSON = ROOT / "patterns.json"
SRC_DIR = ROOT / "patterns-src"


def load_patterns() -> tuple[list[dict], str, str]:
    """Prefer patterns.json if available; else build from shards in patterns-src/."""
    if SRC_PATTERNS_JSON.exists():
        data = json.loads(SRC_PATTERNS_JSON.read_text())
        return data["patterns"], data.get("version", "0.0.0"), data.get("license", "CC-BY-4.0")
    patterns: list[dict] = []
    seen_ids: set[str] = set()
    for shard_path in sorted(SRC_DIR.glob("*.json")):
        shard = json.loads(shard_path.read_text())
        for p in shard["patterns"]:
            if p["id"] in seen_ids:
                raise SystemExit(f"duplicate pattern id: {p['id']}")
            seen_ids.add(p["id"])
            patterns.append(p)
    patterns.sort(key=lambda p: (p["category"], p["id"]))
    return patterns, "0.0.0", "CC-BY-4.0"


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    patterns, version, license_ = load_patterns()

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

    seen_ids = {p["id"] for p in patterns}
    edges = [
        {
            "source": p["id"],
            "target": r["pattern"],
            "relation": r["relation"],
        }
        for p in patterns
        for r in p.get("related", [])
        if r["pattern"] in seen_ids
    ]

    out = {
        "$schema": "./patterns.graph.schema.json",
        "version": version,
        "updated": date.today().isoformat(),
        "license": license_,
        "source": "patterns.json",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }
    out_path = out_dir / "patterns.graph.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out_path.relative_to(ROOT)}  ({len(nodes)} nodes, {len(edges)} edges)")


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    build(out_dir)


if __name__ == "__main__":
    main()
