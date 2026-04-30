#!/usr/bin/env python3
"""Render the catalog into static HTML pages for GitHub Pages.

Inputs: patterns-src/*.json, recipes.json, framework-coverage.json (optional).
Outputs:
  dist/patterns/<id>.html — one page per pattern, with Mermaid CDN if a diagram is present
  dist/patterns/index.html — browse list grouped by category
  dist/recipes/index.html — recipe list with member pattern links
  dist/frameworks/index.html — framework matrix browser

Run: python3 .github/scripts/render_html.py [out_dir]
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "patterns-src"

CAT_LABEL = {
    "reasoning": "Reasoning",
    "planning-control-flow": "Planning & Control Flow",
    "tool-use-environment": "Tool Use & Environment",
    "retrieval": "Retrieval & RAG",
    "memory": "Memory",
    "multi-agent": "Multi-Agent",
    "verification-reflection": "Verification & Reflection",
    "safety-control": "Safety & Control",
    "routing-composition": "Routing & Composition",
    "governance-observability": "Governance & Observability",
    "structure-data": "Structure & Data",
    "streaming-ux": "Streaming & UX",
    "anti-patterns": "Anti-Patterns",
}

BASE_CSS = """
:root { color-scheme: light dark; }
body { font: 16px/1.55 system-ui, -apple-system, sans-serif; max-width: 52rem; margin: 2.5rem auto; padding: 0 1.25rem; color: #1a1a1a; }
@media (prefers-color-scheme: dark) { body { background: #0d0f12; color: #e6e6e6; } a { color: #6cb6ff; } code, pre { background: #1a1d22 !important; } .meta { color: #9aa0a6 !important; } .nav { color: #9aa0a6 !important; } }
h1 { font-size: 1.9rem; margin-bottom: 0.25rem; }
h2 { font-size: 1.15rem; margin-top: 2rem; padding-bottom: 0.25rem; border-bottom: 1px solid rgba(128,128,128,0.25); }
h3 { font-size: 1rem; }
a { color: #0366d6; text-decoration: none; }
a:hover { text-decoration: underline; }
code { background: #f4f4f4; padding: 0.1em 0.35em; border-radius: 3px; font-size: 0.92em; }
pre { background: #f4f4f4; padding: 0.9rem 1rem; border-radius: 4px; overflow-x: auto; }
pre code { background: transparent; padding: 0; }
.meta { color: #555; font-size: 0.92rem; margin: 0.25rem 0 1rem; }
.nav { color: #555; font-size: 0.9rem; margin: 0 0 2rem; }
.aliases { font-style: italic; color: #555; }
.caption { color: #555; font-size: 0.9rem; margin-top: -0.25rem; margin-bottom: 1rem; }
ul.bullets { padding-left: 1.4rem; }
ul.bullets li { margin: 0.25rem 0; }
.constrains { background: rgba(255, 215, 0, 0.12); border-left: 3px solid #d4a017; padding: 0.6rem 0.9rem; margin: 0.5rem 0 1rem; }
.tag { display: inline-block; background: rgba(0,0,0,0.06); padding: 0.1em 0.5em; border-radius: 3px; font-size: 0.85em; margin-right: 0.3em; }
.cat-list { columns: 2; column-gap: 2rem; }
@media (max-width: 600px) { .cat-list { columns: 1; } }
.mermaid { background: #fff; padding: 0.5rem; border-radius: 4px; }
@media (prefers-color-scheme: dark) { .mermaid { background: #f4f4f4; } }
"""

MERMAID_SCRIPT = """
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'default', securityLevel: 'strict' });
</script>
"""


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def page(title: str, body: str, with_mermaid: bool = False) -> str:
    mermaid_block = MERMAID_SCRIPT if with_mermaid else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>{BASE_CSS}</style>
</head>
<body>
{body}
{mermaid_block}
</body>
</html>
"""


def render_pattern(p: dict, all_ids: set[str]) -> str:
    name = p["name"]
    pid = p["id"]
    cat = p["category"]
    aliases = p.get("aliases") or []
    diagram = p.get("diagram")
    applicability = p.get("applicability") or {}
    consequences = p.get("consequences") or {}

    parts: list[str] = []
    parts.append(f'<p class="nav"><a href="../">&larr; All artifacts</a> &middot; <a href="./">All patterns</a> &middot; <a href="./#{esc(cat)}">{esc(CAT_LABEL.get(cat, cat))}</a></p>')
    parts.append(f"<h1>{esc(name)}</h1>")
    if aliases:
        parts.append(f'<p class="aliases">aka {esc(", ".join(aliases))}</p>')

    meta_bits = [f"category: <code>{esc(cat)}</code>", f"status: <code>{esc(p.get('status_in_practice','—'))}</code>"]
    parts.append(f'<p class="meta">{" &middot; ".join(meta_bits)}</p>')

    parts.append(f"<h2>Intent</h2><p>{esc(p['intent'])}</p>")
    if p.get("example_scenario"):
        parts.append(f"<h2>Example scenario</h2><p class='example-scenario'>{esc(p['example_scenario'])}</p>")
    parts.append(f"<h2>Context</h2><p>{esc(p['context'])}</p>")
    parts.append(f"<h2>Problem</h2><p>{esc(p['problem'])}</p>")

    forces = p.get("forces") or []
    if forces:
        parts.append("<h2>Forces</h2><ul class='bullets'>")
        for f in forces:
            parts.append(f"<li>{esc(f)}</li>")
        parts.append("</ul>")

    parts.append(f"<h2>Solution</h2><p>{esc(p['solution'])}</p>")

    if diagram:
        parts.append("<h2>Diagram</h2>")
        parts.append(f'<pre class="mermaid">{esc(diagram["mermaid"])}</pre>')
        if diagram.get("caption"):
            parts.append(f'<p class="caption">{esc(diagram["caption"])}</p>')
    elif p.get("structure"):
        parts.append(f"<h2>Structure</h2><pre><code>{esc(p['structure'])}</code></pre>")

    variants = p.get("variants") or []
    if variants:
        parts.append("<h2>Variants</h2>")
        for v in variants:
            parts.append(f'<h3>{esc(v["name"])}</h3>')
            parts.append(f'<p>{esc(v["summary"])}</p>')
            if v.get("distinguishing_factor"):
                parts.append(f'<p class="meta">Distinguishing factor: {esc(v["distinguishing_factor"])}</p>')
            if v.get("when_to_use"):
                parts.append(f'<p class="meta">When to use: {esc(v["when_to_use"])}</p>')
            sa = v.get("see_also")
            if sa:
                if sa in all_ids:
                    parts.append(f'<p class="meta">See also: <a href="{esc(sa)}.html">{esc(sa)}</a></p>')
                else:
                    parts.append(f'<p class="meta">See also: <code>{esc(sa)}</code></p>')

    if applicability.get("use_when") or applicability.get("do_not_use_when"):
        parts.append("<h2>Applicability</h2>")
        if applicability.get("use_when"):
            parts.append("<h3>Use when</h3><ul class='bullets'>")
            for b in applicability["use_when"]:
                parts.append(f"<li>{esc(b)}</li>")
            parts.append("</ul>")
        if applicability.get("do_not_use_when"):
            parts.append("<h3>Do not use when</h3><ul class='bullets'>")
            for b in applicability["do_not_use_when"]:
                parts.append(f"<li>{esc(b)}</li>")
            parts.append("</ul>")

    if p.get("constrains"):
        parts.append("<h2>Constrains</h2>")
        parts.append(f'<div class="constrains">{esc(p["constrains"])}</div>')

    if consequences.get("benefits") or consequences.get("liabilities"):
        parts.append("<h2>Consequences</h2>")
        if consequences.get("benefits"):
            parts.append("<h3>Benefits</h3><ul class='bullets'>")
            for b in consequences["benefits"]:
                parts.append(f"<li>{esc(b)}</li>")
            parts.append("</ul>")
        if consequences.get("liabilities"):
            parts.append("<h3>Liabilities</h3><ul class='bullets'>")
            for b in consequences["liabilities"]:
                parts.append(f"<li>{esc(b)}</li>")
            parts.append("</ul>")

    known = p.get("known_uses") or []
    if known:
        parts.append("<h2>Known Uses</h2><ul class='bullets'>")
        for k in known:
            sys_name = esc(k.get("system", ""))
            note = f" — {esc(k['note'])}" if k.get("note") else ""
            url = k.get("url")
            if url:
                sys_html = f'<a href="{esc(url)}" rel="noopener">{sys_name}</a>'
            else:
                sys_html = sys_name
            parts.append(f"<li>{sys_html}{note}</li>")
        parts.append("</ul>")

    related = p.get("related") or []
    if related:
        parts.append("<h2>Related Patterns</h2><ul class='bullets'>")
        for r in related:
            tgt = r.get("pattern", "")
            rel = r.get("relation", "")
            if tgt in all_ids:
                tgt_html = f'<a href="{esc(tgt)}.html">{esc(tgt)}</a>'
            else:
                tgt_html = f"<code>{esc(tgt)}</code>"
            note = f" — {esc(r['note'])}" if r.get("note") else ""
            parts.append(f"<li><code>{esc(rel)}</code> &rarr; {tgt_html}{note}</li>")
        parts.append("</ul>")

    refs = p.get("references") or []
    if refs:
        parts.append("<h2>References</h2><ul class='bullets'>")
        for r in refs:
            title = esc(r.get("title", ""))
            url = r.get("url")
            authors = f" — {esc(r['authors'])}" if r.get("authors") else ""
            year = f" ({r['year']})" if r.get("year") else ""
            type_tag = f' <span class="tag">{esc(r.get("type",""))}</span>'
            if url:
                title_html = f'<a href="{esc(url)}" rel="noopener">{title}</a>'
            else:
                title_html = title
            parts.append(f"<li>{title_html}{authors}{year}{type_tag}</li>")
        parts.append("</ul>")

    body = "\n".join(parts)
    return page(name, body, with_mermaid=bool(diagram))


def render_pattern_index(patterns: list[dict]) -> str:
    by_cat: dict[str, list[dict]] = {}
    for p in patterns:
        by_cat.setdefault(p["category"], []).append(p)

    parts = ['<p class="nav"><a href="../">&larr; All artifacts</a></p>']
    parts.append("<h1>Patterns</h1>")
    parts.append(f"<p class='meta'>{len(patterns)} patterns across {len(by_cat)} categories.</p>")

    for cat in CAT_LABEL:
        items = sorted(by_cat.get(cat, []), key=lambda x: x["name"].lower())
        if not items:
            continue
        parts.append(f'<h2 id="{esc(cat)}">{esc(CAT_LABEL[cat])} <span class="meta">({len(items)})</span></h2>')
        parts.append('<ul class="bullets cat-list">')
        for p in items:
            badge = ""
            if p.get("diagram"):
                badge = ' <span class="tag">diagram</span>'
            parts.append(f'<li><a href="{esc(p["id"])}.html">{esc(p["name"])}</a>{badge}</li>')
        parts.append("</ul>")

    return page("Patterns – Agentic Patterns Catalog", "\n".join(parts))


def render_recipe_index(recipes: dict, all_ids: set[str]) -> str:
    parts = ['<p class="nav"><a href="../">&larr; All artifacts</a></p>']
    parts.append("<h1>Recipes</h1>")
    parts.append(f"<p class='meta'>{recipes.get('description','')}</p>")
    for r in recipes.get("recipes", []):
        parts.append(f'<h2 id="{esc(r["id"])}">{esc(r["name"])}</h2>')
        parts.append(f"<p>{esc(r['description'])}</p>")
        members = r.get("members") or []
        if members:
            parts.append("<ul class='bullets'>")
            for m in members:
                pid = m.get("pattern", "")
                role = m.get("role", "")
                if pid in all_ids:
                    pid_html = f'<a href="../patterns/{esc(pid)}.html">{esc(pid)}</a>'
                else:
                    pid_html = f"<code>{esc(pid)}</code>"
                parts.append(f'<li><span class="tag">{esc(role)}</span> {pid_html}</li>')
            parts.append("</ul>")
    return page("Recipes – Agentic Patterns Catalog", "\n".join(parts))


def render_framework_index(cov: dict, all_ids: set[str]) -> str:
    parts = ['<p class="nav"><a href="../">&larr; All artifacts</a></p>']
    parts.append("<h1>Framework Coverage</h1>")
    parts.append(f"<p class='meta'>{esc(cov.get('description',''))}</p>")
    parts.append(f"<p class='meta'>Last analysis: {esc(cov.get('last_analysis_date','—'))} &middot; {len(cov.get('frameworks',[]))} frameworks.</p>")
    for fw in sorted(cov.get("frameworks", []), key=lambda f: f["name"].lower()):
        fid = fw["id"]
        parts.append(f'<h2 id="{esc(fid)}">{esc(fw["name"])}</h2>')
        meta_bits = []
        if fw.get("vendor"):
            meta_bits.append(f"vendor: {esc(fw['vendor'])}")
        if fw.get("language"):
            meta_bits.append(f"language: {esc(fw['language'])}")
        if fw.get("status"):
            meta_bits.append(f"status: <code>{esc(fw['status'])}</code>")
        if fw.get("url"):
            meta_bits.append(f'<a href="{esc(fw["url"])}" rel="noopener">site</a>')
        meta_bits.append(f"last_analyzed: {esc(fw.get('last_analyzed','—'))}")
        parts.append(f'<p class="meta">{" &middot; ".join(meta_bits)}</p>')
        cov_map = fw.get("coverage") or {}
        if cov_map:
            parts.append("<ul class='bullets'>")
            for pid, val in sorted(cov_map.items()):
                if pid in all_ids:
                    pid_html = f'<a href="../patterns/{esc(pid)}.html">{esc(pid)}</a>'
                else:
                    pid_html = f"<code>{esc(pid)}</code>"
                parts.append(f'<li><span class="tag">{esc(val)}</span> {pid_html}</li>')
            parts.append("</ul>")
    return page("Framework Coverage – Agentic Patterns Catalog", "\n".join(parts))


def main(out_dir: Path) -> None:
    patterns: list[dict] = []
    for shard in sorted(SRC.glob("*.json")):
        d = json.loads(shard.read_text())
        patterns.extend(d["patterns"])
    patterns.sort(key=lambda p: (p["category"], p["id"]))
    all_ids = {p["id"] for p in patterns}

    pat_dir = out_dir / "patterns"
    pat_dir.mkdir(parents=True, exist_ok=True)

    n_diagrams = 0
    for p in patterns:
        if p.get("diagram"):
            n_diagrams += 1
        (pat_dir / f"{p['id']}.html").write_text(render_pattern(p, all_ids))

    (pat_dir / "index.html").write_text(render_pattern_index(patterns))

    recipes_path = ROOT / "recipes.json"
    if recipes_path.exists():
        recipes = json.loads(recipes_path.read_text())
        rec_dir = out_dir / "recipes"
        rec_dir.mkdir(parents=True, exist_ok=True)
        (rec_dir / "index.html").write_text(render_recipe_index(recipes, all_ids))

    cov_path = ROOT / "framework-coverage.json"
    if cov_path.exists():
        cov = json.loads(cov_path.read_text())
        fw_dir = out_dir / "frameworks"
        fw_dir.mkdir(parents=True, exist_ok=True)
        (fw_dir / "index.html").write_text(render_framework_index(cov, all_ids))

    print(f"rendered {len(patterns)} pattern pages ({n_diagrams} with diagrams), recipe index, framework index")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    main(target)
