#!/usr/bin/env python3
"""Concatenate examples-src/<category>.json shards into a single examples.json.

examples-src/ is the source of truth for per-pattern code examples (pseudo +
one entry per supporting framework). This script mirrors build_patterns_json.py
and exists for the same reason: the Pages site and downstream consumers want
one consolidated file, while authors want one shard per category.

Run locally: python3 .github/scripts/build_examples_json.py [out_dir]
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "examples-src"
SCHEMA = ROOT / "examples.schema.json"


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    pattern_examples: list[dict] = []
    seen: set[str] = set()
    if not SRC.exists():
        # examples-src is optional during rollout — patterns ship without
        # examples while the backfill is in progress.
        print(f"no {SRC} dir; skipping examples.json")
        return

    for shard_path in sorted(SRC.glob("*.json")):
        shard = json.loads(shard_path.read_text())
        cat = shard["category"]
        for entry in shard["patterns"]:
            pid = entry["pattern_id"]
            if pid in seen:
                raise SystemExit(f"duplicate pattern_id in examples-src: {pid}")
            seen.add(pid)
            pattern_examples.append({"category": cat, **entry})

    pattern_examples.sort(key=lambda e: (e["category"], e["pattern_id"]))

    out = {
        "$schema": "./examples.schema.json",
        "license": "CC-BY-4.0",
        "patterns": pattern_examples,
    }
    (out_dir / "examples.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    )
    if SCHEMA.exists():
        dst = out_dir / "examples.schema.json"
        if dst.resolve() != SCHEMA.resolve():
            shutil.copy(SCHEMA, dst)

    print(f"built {out_dir/'examples.json'} with {len(pattern_examples)} pattern entries")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    build(target)
