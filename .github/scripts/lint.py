#!/usr/bin/env python3
"""Lint the patterns catalog against its stated aspirations.

Rules are grouped to match the README's framing:

  A1  GoF/POSA form          schema validity, required slots, unique kebab id
  A2  Pure data              no scripts at repo root (CI scripts under .github/ ok)
  A3  Constraint-first       constrains slot present and reads as a restriction
  A4  Typed graph            edges resolve, no self-edges, symmetric where required
  A5  Categorization         category matches shard, taxonomy and shards in sync
  A6  Evidence               known_uses non-empty, references typed, URLs live
  A7  Prose shape            intent is one sentence, prose slots are not bullets
  A8  Vocabulary             "the model"/"the LLM", never "the AI"
  A9  Tone                   no emoji, no hype words, neutral voice
  A10 Naming                 no duplicate names or alias collisions

Usage:
  python3 .github/scripts/lint.py                 # all rules, error on violations
  python3 .github/scripts/lint.py --no-network    # skip A6.3 URL liveness
  python3 .github/scripts/lint.py --rule A3       # single group
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "patterns-src"
SCHEMA = ROOT / "schema.json"
TAXONOMY = ROOT / "docs" / "taxonomy.md"

PROSE_SLOTS = ("intent", "context", "problem", "solution", "constrains")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
KEBAB_RE = re.compile(r"^[a-z0-9-]+$")
URL_RE = re.compile(r"https?://[^\s'\"<>)]+", re.IGNORECASE)

CONSTRAINT_MARKERS = (
    # explicit negation
    "cannot",
    "can't",
    "must not",
    "may not",
    "is not",
    "are not",
    "do not",
    "does not",
    "did not",
    "have no",
    "has no",
    "no ",
    "never",
    "without",
    " not ",
    "neither",
    "untrusted",
    # imperative / required precondition
    "must",
    "only when",
    "only after",
    "only if",
    "only ",
    "before ",
    "is required",
    "are required",
    "is bound",
    "are bound",
    "bounded",
    "is constrained",
    "are constrained",
    "is replaced",
    "are replaced",
    # rejection / refusal language
    "forbid",
    "reject",
    "halt",
    "terminate",
    "block",
    "deny",
    "denied",
    "refuse",
    "prevent",
    "restrict",
    "fail",
    "rejected",
    "exceed",
    "cut off",
    # state/scope restrictions
    "read-only",
    "frozen",
    "no longer",
    "is not allowed",
    "not permitted",
    "off-limits",
    "out of scope",
    "regardless",
    "unless",
    "rather than",
    "at most",
    "advisory",
)

HYPE_WORDS = (
    "revolutionary",
    "powerful",
    "cutting-edge",
    "leverage",
    "leverages",
    "leveraging",
    "seamless",
    "seamlessly",
    "robust",
    "synergy",
    "groundbreaking",
    "next-generation",
    "next-gen",
    "best-in-class",
    "effortless",
    "effortlessly",
    "magical",
    "delight",
    "game-changer",
    "game-changing",
    "world-class",
    "state-of-the-art",
    "supercharge",
    "unleash",
    "blazing-fast",
)

NEUTRAL_VOICE_FORBIDDEN = (
    r"\bwe\b",
    r"\bour\b",
    r"\byou\b",
    r"\byour\b",
)

SYMMETRIC_RELATIONS = ("alternative-to", "composes-with", "complements", "conflicts-with")
INVERSE_PAIRS = (("uses", "used-by"), ("specialises", "generalises"))

USER_AGENT = "agentic-patterns-catalog-linter/1.0 (+https://github.com/nissen-consulting/agentic-patterns)"


# ---------- helpers ----------------------------------------------------------


class Violation:
    __slots__ = ("rule", "where", "msg")

    def __init__(self, rule: str, where: str, msg: str) -> None:
        self.rule = rule
        self.where = where
        self.msg = msg

    def __str__(self) -> str:
        return f"[{self.rule}] {self.where}: {self.msg}"


def load_shards() -> tuple[list[dict], dict[str, str]]:
    """Return (patterns, id_to_shard) — patterns flat-listed, location preserved."""
    patterns: list[dict] = []
    where: dict[str, str] = {}
    for shard_path in sorted(SRC.glob("*.json")):
        shard = json.loads(shard_path.read_text())
        for p in shard["patterns"]:
            patterns.append(p)
            where[p["id"]] = shard_path.name
    return patterns, where


def text_fields(p: dict) -> dict[str, str]:
    out = {}
    for slot in PROSE_SLOTS:
        v = p.get(slot)
        if isinstance(v, str):
            out[slot] = v
    forces = p.get("forces") or []
    if forces:
        out["forces"] = " ".join(forces)
    return out


def has_emoji(s: str) -> bool:
    for ch in s:
        if unicodedata.category(ch).startswith("So"):
            return True
        if 0x1F300 <= ord(ch) <= 0x1FAFF:
            return True
    return False


# ---------- rules ------------------------------------------------------------


def rule_a1(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A1 GoF/POSA form: schema, required slots, kebab id."""
    out: list[Violation] = []
    required = ("id", "name", "category", "intent", "context", "problem", "solution", "status_in_practice")
    seen: dict[str, str] = {}

    try:
        import jsonschema  # type: ignore
        schema = json.loads(SCHEMA.read_text())
        validator = jsonschema.Draft202012Validator(schema)
    except ImportError:
        validator = None
        out.append(Violation("A1.1", "lint env", "jsonschema not installed; skipping schema validation"))

    for p in patterns:
        pid = p.get("id", "<no-id>")
        loc = f"{where.get(pid, '?')}::{pid}"
        for slot in required:
            v = p.get(slot)
            if v is None or (isinstance(v, str) and not v.strip()):
                out.append(Violation("A1.2", loc, f"required slot {slot!r} missing or empty"))
        if "id" in p:
            if pid in seen:
                out.append(Violation("A1.3", loc, f"duplicate id (also in {seen[pid]})"))
            else:
                seen[pid] = where.get(pid, "?")
            if not ID_RE.match(pid):
                out.append(Violation("A1.4", loc, f"id {pid!r} is not kebab-case"))
        if validator is not None:
            for err in validator.iter_errors(p):
                path = "/".join(str(x) for x in err.absolute_path) or "<root>"
                out.append(Violation("A1.1", loc, f"schema: {path}: {err.message}"))
    return out


def rule_a2() -> list[Violation]:
    """A2 Pure data: no scripts at repo root (checks tracked files only)."""
    import subprocess

    out: list[Violation] = []
    try:
        tracked = subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True
        ).splitlines()
    except (OSError, subprocess.CalledProcessError):
        return out

    root_files = [t for t in tracked if "/" not in t]
    root_dirs = {t.split("/", 1)[0] for t in tracked if "/" in t}

    script_exts = (".py", ".sh", ".js", ".ts", ".rb")
    for f in root_files:
        if f.endswith(script_exts):
            out.append(Violation("A2.1", f, "script at repo root (move to .github/scripts/)"))

    allowed_top = {
        "README.md",
        "LICENSE",
        ".gitignore",
        "schema.json",
        "INDEX.md",
        "framework-coverage.json",
        "framework-coverage.schema.json",
        "recipes.json",
        "recipes.schema.json",
        "glossary.json",
        "glossary.schema.json",
    }
    allowed_dirs = {"patterns-src", "patterns", "docs", ".github"}
    for f in root_files:
        if f not in allowed_top:
            out.append(Violation("A2.2", f, "unexpected tracked file at repo root"))
    for d in root_dirs:
        if d not in allowed_dirs:
            out.append(Violation("A2.2", d + "/", "unexpected tracked directory at repo root"))
    return out


def rule_a3(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A3 Constraint-first: every pattern declares what it forbids the model."""
    out: list[Violation] = []
    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        c = p.get("constrains")
        if not isinstance(c, str) or not c.strip():
            out.append(Violation("A3.1", loc, "constrains slot missing or empty (required-by-convention)"))
            continue
        low = c.lower()
        if not any(m in low for m in CONSTRAINT_MARKERS):
            out.append(Violation(
                "A3.2", loc,
                f"constrains reads as a benefit, not a restriction: {c!r}",
            ))
    return out


def rule_a4(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A4 Typed graph: edges resolve, no self-edges, symmetric/inverse correctness."""
    out: list[Violation] = []
    ids = {p["id"] for p in patterns}
    edges_by_src: dict[str, list[tuple[str, str]]] = {pid: [] for pid in ids}

    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        for e in p.get("related") or []:
            tgt = e.get("pattern")
            rel = e.get("relation")
            if not tgt or not rel:
                out.append(Violation("A4.1", loc, f"malformed related entry: {e}"))
                continue
            if tgt not in ids:
                out.append(Violation("A4.1", loc, f"related target {tgt!r} (relation={rel}) does not exist"))
                continue
            if tgt == p["id"]:
                out.append(Violation("A4.2", loc, f"self-edge ({rel} -> self)"))
                continue
            edges_by_src[p["id"]].append((tgt, rel))

    for src, edges in edges_by_src.items():
        for tgt, rel in edges:
            if rel in SYMMETRIC_RELATIONS:
                if not any(t == src and r == rel for t, r in edges_by_src.get(tgt, [])):
                    out.append(Violation(
                        "A4.3", f"{src}",
                        f"{rel} -> {tgt} not mirrored from {tgt}",
                    ))
            for a, b in INVERSE_PAIRS:
                if rel == a:
                    if not any(t == src and r == b for t, r in edges_by_src.get(tgt, [])):
                        out.append(Violation(
                            "A4.4", f"{src}",
                            f"{a} -> {tgt} but {tgt} has no {b} -> {src}",
                        ))
                elif rel == b:
                    if not any(t == src and r == a for t, r in edges_by_src.get(tgt, [])):
                        out.append(Violation(
                            "A4.4", f"{src}",
                            f"{b} -> {tgt} but {tgt} has no {a} -> {src}",
                        ))
    return out


def rule_a5(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A5 Categorization: pattern.category == shard slug, taxonomy in sync."""
    out: list[Violation] = []
    for p in patterns:
        shard_name = where[p["id"]]
        expected = shard_name.removesuffix(".json")
        if p.get("category") != expected:
            out.append(Violation(
                "A5.1", f"{shard_name}::{p['id']}",
                f"category {p.get('category')!r} != shard slug {expected!r}",
            ))

    shard_cats = {p.removesuffix(".json") for p in (s.name for s in SRC.glob("*.json"))}
    if TAXONOMY.exists():
        text = TAXONOMY.read_text()
        slugs = set(re.findall(r"\*\*([a-z][a-z0-9-]+)\*\*", text))
        slugs |= set(re.findall(r"(?m)^##\s+([a-z][a-z0-9-]+)\s*$", text))
        slugs |= set(re.findall(r"`([a-z][a-z0-9-]+)`", text))
        missing_in_taxonomy = shard_cats - slugs
        extra_in_taxonomy = (slugs - shard_cats) & {s for s in slugs if "-" in s or s.islower()}
        if missing_in_taxonomy:
            out.append(Violation(
                "A5.2", "docs/taxonomy.md",
                f"shards present but not mentioned in taxonomy: {sorted(missing_in_taxonomy)}",
            ))
    return out


def rule_a6(patterns: list[dict], where: dict[str, str], check_urls: bool) -> list[Violation]:
    """A6 Evidence: known_uses non-empty, references typed, URLs live (refs + known_uses)."""
    out: list[Violation] = []
    urls_to_check: list[tuple[str, str]] = []  # (url, location)

    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        ku = p.get("known_uses") or []
        if not ku:
            out.append(Violation("A6.1", loc, "known_uses is empty"))
        for k in ku:
            url = k.get("url")
            if url:
                urls_to_check.append((url, f"{loc} known_uses({k.get('system','')})"))
        refs = p.get("references") or []
        if not refs:
            out.append(Violation("A6.2", loc, "references is empty (need at least one paper/product/repo)"))
        for r in refs:
            t = r.get("type")
            if t not in {"paper", "product", "repo", "blog", "talk", "spec", "book", "doc"}:
                out.append(Violation("A6.2", loc, f"reference type {t!r} not in allowed set"))
            url = r.get("url")
            if url:
                urls_to_check.append((url, f"{loc} ({r.get('title') or r.get('type')})"))
            else:
                # A6.4 (hard fail): every reference must have a URL.
                # If a reference can't be linked to a verifiable source,
                # remove it rather than ship an unlinked entry.
                out.append(Violation(
                    "A6.4", loc,
                    f"reference {r.get('title') or r.get('type')!r} has no url (URL is mandatory)"))

    if check_urls and urls_to_check:
        out.extend(_check_urls(urls_to_check))
    return out


def _check_urls(urls: list[tuple[str, str]]) -> list[Violation]:
    out: list[Violation] = []
    seen: dict[str, str | None] = {}

    def probe(url: str) -> tuple[str, str | None]:
        if url in seen:
            return url, seen[url]
        try:
            req = request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
            with request.urlopen(req, timeout=15) as resp:
                code = resp.status
                if code >= 400:
                    raise error.HTTPError(url, code, "HEAD failed", resp.headers, None)
                seen[url] = None
                return url, None
        except error.HTTPError as e:
            # 403/429 commonly mean "URL exists but anti-bot blocked the check"
            # rather than "URL is dead". Treat them as alive — the link is
            # reachable from a real browser.
            if e.code in (403, 429):
                seen[url] = None
                return url, None
            if e.code in (405, 501):
                try:
                    req = request.Request(url, method="GET", headers={"User-Agent": USER_AGENT})
                    with request.urlopen(req, timeout=20) as resp:
                        if resp.status >= 400:
                            seen[url] = f"HTTP {resp.status}"
                            return url, seen[url]
                        seen[url] = None
                        return url, None
                except Exception as ee:
                    seen[url] = f"{type(ee).__name__}: {ee}"
                    return url, seen[url]
            seen[url] = f"HTTP {e.code}"
            return url, seen[url]
        except Exception as e:
            seen[url] = f"{type(e).__name__}: {e}"
            return url, seen[url]

    unique = sorted({u for u, _ in urls})
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(probe, u): u for u in unique}
        for f in as_completed(futures):
            f.result()

    for url, loc in urls:
        err = seen.get(url)
        if err:
            out.append(Violation("A6.3", loc, f"dead URL {url}: {err}"))
    return out


ABBREV_BEFORE_PERIOD = re.compile(
    r"\b(?:e\.g|i\.e|etc|vs|cf|Mr|Mrs|Ms|Dr|Jr|Sr|St|Inc|Ltd|Co|Corp|Fig|No|al)\.\s+",
    re.IGNORECASE,
)


def _count_sentences(text: str) -> int:
    masked = ABBREV_BEFORE_PERIOD.sub(lambda m: m.group(0).replace(".", "\x00"), text)
    parts = [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", masked) if s.strip()]
    return len(parts)


def rule_a7(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A7 Prose shape: intent one sentence, prose slots not bullets."""
    out: list[Violation] = []
    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        intent = (p.get("intent") or "").strip()
        if intent:
            n = _count_sentences(intent)
            if n > 1:
                out.append(Violation("A7.1", loc, f"intent has {n} sentences; expected 1"))
            if intent.lstrip().startswith(("- ", "* ")):
                out.append(Violation("A7.1", loc, "intent starts with a bullet"))
            if len(intent.split()) > 35:
                out.append(Violation("A7.3", loc, f"intent is {len(intent.split())} words (>35)"))
        for slot in ("context", "problem", "solution"):
            v = (p.get(slot) or "").strip()
            if v.lstrip().startswith(("- ", "* ", "1.", "1)")):
                out.append(Violation("A7.2", loc, f"{slot} starts as a bullet/numbered list"))
    return out


PROPER_NOUNS_WITH_AI = (
    "EU AI Act",
    "AI Act",
    "AI Safety Institute",
    "Open AI",
    "OpenAI",
    "GenAI",
    "xAI",
    "AI21",
    "AGI",
    "AI-User",
    "AI-Assistant",
)


def rule_a8(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A8 Vocabulary: never 'the AI'."""
    out: list[Violation] = []
    pat = re.compile(r"\b(?:the|an)\s+AI\b")
    standalone = re.compile(r"(?<![A-Za-z])AI(?![A-Za-z])")
    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        for slot, text in text_fields(p).items():
            scrubbed = text
            for noun in PROPER_NOUNS_WITH_AI:
                scrubbed = scrubbed.replace(noun, "")
            if pat.search(scrubbed):
                out.append(Violation("A8.1", f"{loc}#{slot}", "found 'the AI' / 'an AI' (use 'the model' or 'the LLM')"))
            elif standalone.search(scrubbed) and not re.search(r"\bAPI\b", scrubbed):
                out.append(Violation("A8.1", f"{loc}#{slot}", "standalone 'AI' (use 'the model' or 'the LLM')"))
    return out


def rule_a9(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A9 Tone: no emoji, no hype, neutral voice."""
    out: list[Violation] = []
    hype_pat = re.compile(r"\b(" + "|".join(re.escape(w) for w in HYPE_WORDS) + r")\b", re.IGNORECASE)
    voice_pats = [re.compile(p, re.IGNORECASE) for p in NEUTRAL_VOICE_FORBIDDEN]
    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        for slot, text in text_fields(p).items():
            if has_emoji(text):
                out.append(Violation("A9.1", f"{loc}#{slot}", "contains emoji"))
            for m in hype_pat.finditer(text):
                out.append(Violation("A9.2", f"{loc}#{slot}", f"hype word: {m.group(1)!r}"))
            for vp in voice_pats:
                m = vp.search(text)
                if m:
                    out.append(Violation("A9.3", f"{loc}#{slot}", f"non-neutral voice: {m.group(0)!r}"))
                    break
    return out


def rule_a10(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A10 Naming: unique names, no alias collisions."""
    out: list[Violation] = []
    name_to_id: dict[str, str] = {}
    alias_to_id: dict[str, str] = {}
    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        name = p.get("name", "")
        if name in name_to_id:
            out.append(Violation("A10.1", loc, f"duplicate name {name!r} (also in {name_to_id[name]})"))
        else:
            name_to_id[name] = p["id"]
        for a in p.get("aliases") or []:
            if a in alias_to_id and alias_to_id[a] != p["id"]:
                out.append(Violation("A10.2", loc, f"alias {a!r} collides with {alias_to_id[a]}"))
            alias_to_id[a] = p["id"]
            if a in name_to_id and name_to_id[a] != p["id"]:
                out.append(Violation("A10.3", loc, f"alias {a!r} equals canonical name of {name_to_id[a]}"))
    return out


# ---------- runner -----------------------------------------------------------


def rule_a11(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A11 Framework coverage: schema-valid, pattern ids resolve, vendor required.

    A11.1 invalid JSON
    A11.2 duplicate framework id
    A11.3 coverage references unknown pattern id
    A11.4 framework missing vendor (team / company that builds it)
    A11.5 framework fails framework-coverage.schema.json validation
    """
    out: list[Violation] = []
    cov_path = ROOT / "framework-coverage.json"
    cov_schema_path = ROOT / "framework-coverage.schema.json"
    if not cov_path.exists():
        return out
    try:
        cov = json.loads(cov_path.read_text())
    except json.JSONDecodeError as e:
        out.append(Violation("A11.1", "framework-coverage.json", f"invalid JSON: {e}"))
        return out

    # Schema validation (catches missing vendor + any other required-field gap).
    if cov_schema_path.exists():
        try:
            import jsonschema  # type: ignore
            schema = json.loads(cov_schema_path.read_text())
            validator = jsonschema.Draft202012Validator(schema)
            for err in validator.iter_errors(cov):
                path = "/".join(str(x) for x in err.absolute_path) or "<root>"
                out.append(Violation("A11.5", f"framework-coverage::{path}", err.message))
        except ImportError:
            out.append(Violation("A11.5", "lint env", "jsonschema not installed; skipping framework-coverage schema validation"))

    pattern_ids = {p["id"] for p in patterns}
    fw_ids: set[str] = set()
    for fw in cov.get("frameworks", []):
        fid = fw.get("id", "<no-id>")
        if fid in fw_ids:
            out.append(Violation("A11.2", f"framework-coverage::{fid}", "duplicate framework id"))
        fw_ids.add(fid)
        # Vendor must be present and non-empty: every framework needs a clear
        # owner (team or company). Schema enforces it too; this gives a
        # nicer message for the common case.
        vendor = fw.get("vendor")
        if not isinstance(vendor, str) or not vendor.strip():
            out.append(Violation(
                "A11.4", f"framework-coverage::{fid}",
                "missing or empty `vendor` (team / company that builds the framework)",
            ))
        for pid in (fw.get("coverage") or {}):
            if pid not in pattern_ids:
                out.append(Violation(
                    "A11.3", f"framework-coverage::{fid}",
                    f"coverage references unknown pattern id {pid!r}",
                ))
    return out


DIAGRAM_KEYWORDS = {
    "sequence": ("sequenceDiagram",),
    "flow": ("flowchart", "graph"),
    "class": ("classDiagram",),
    "state": ("stateDiagram", "stateDiagram-v2"),
    "graph": ("graph", "flowchart"),
}


def rule_a13(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A13 Diagram sanity: diagram.mermaid first non-empty line must match diagram.type."""
    out: list[Violation] = []
    for p in patterns:
        d = p.get("diagram")
        if not d:
            continue
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        m = (d.get("mermaid") or "").lstrip()
        if not m:
            out.append(Violation("A13.1", loc, "diagram.mermaid is empty"))
            continue
        first_line = m.splitlines()[0].strip()
        first_word = first_line.split()[0] if first_line else ""
        expected = DIAGRAM_KEYWORDS.get(d.get("type", ""), ())
        if not any(first_word.startswith(k) for k in expected):
            out.append(Violation(
                "A13.2", loc,
                f"diagram.mermaid begins with {first_word!r}; expected one of {list(expected)} for type {d.get('type')!r}",
            ))
    return out


def rule_a12(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A12 Recipes: pattern ids in recipes.json must resolve; recipe ids unique."""
    out: list[Violation] = []
    rec_path = ROOT / "recipes.json"
    if not rec_path.exists():
        return out
    try:
        rec = json.loads(rec_path.read_text())
    except json.JSONDecodeError as e:
        out.append(Violation("A12.1", "recipes.json", f"invalid JSON: {e}"))
        return out

    pattern_ids = {p["id"] for p in patterns}
    rec_ids: set[str] = set()
    for r in rec.get("recipes", []):
        rid = r.get("id", "<no-id>")
        if rid in rec_ids:
            out.append(Violation("A12.2", f"recipes::{rid}", "duplicate recipe id"))
        rec_ids.add(rid)
        seen_members: set[str] = set()
        for m in r.get("members", []):
            pid = m.get("pattern", "")
            if pid not in pattern_ids:
                out.append(Violation(
                    "A12.3", f"recipes::{rid}",
                    f"member references unknown pattern id {pid!r}",
                ))
            if pid in seen_members:
                out.append(Violation(
                    "A12.4", f"recipes::{rid}",
                    f"member {pid!r} listed more than once",
                ))
            seen_members.add(pid)
    return out


RULES = {
    "A1": ("schema/structure", lambda P, W, N: rule_a1(P, W)),
    "A2": ("repo hygiene", lambda P, W, N: rule_a2()),
    "A3": ("constraint-first", lambda P, W, N: rule_a3(P, W)),
    "A4": ("typed graph", lambda P, W, N: rule_a4(P, W)),
    "A5": ("categorization", lambda P, W, N: rule_a5(P, W)),
    "A6": ("evidence + URL liveness", lambda P, W, N: rule_a6(P, W, N)),
    "A7": ("prose shape", lambda P, W, N: rule_a7(P, W)),
    "A8": ("vocabulary", lambda P, W, N: rule_a8(P, W)),
    "A9": ("tone", lambda P, W, N: rule_a9(P, W)),
    "A10": ("naming", lambda P, W, N: rule_a10(P, W)),
    "A11": ("framework coverage refs", lambda P, W, N: rule_a11(P, W)),
    "A12": ("recipe pattern refs", lambda P, W, N: rule_a12(P, W)),
    "A13": ("diagram sanity", lambda P, W, N: rule_a13(P, W)),
}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", action="append", help="run only listed rule groups (e.g. --rule A3 --rule A4)")
    ap.add_argument("--no-network", action="store_true", help="skip A6.3 URL liveness check")
    args = ap.parse_args(argv)

    patterns, where = load_shards()
    selected = args.rule or list(RULES)
    unknown = set(selected) - set(RULES)
    if unknown:
        print(f"unknown rule groups: {sorted(unknown)}", file=sys.stderr)
        return 2

    violations: list[Violation] = []
    for key in selected:
        label, fn = RULES[key]
        vs = fn(patterns, where, not args.no_network)
        for v in vs:
            violations.append(v)
        print(f"  {key} {label}: {len(vs)} violation(s)", file=sys.stderr)

    if not violations:
        print(f"OK — {len(patterns)} patterns, all selected rules pass", file=sys.stderr)
        return 0

    by_rule: dict[str, list[Violation]] = {}
    for v in violations:
        by_rule.setdefault(v.rule, []).append(v)
    for rule in sorted(by_rule):
        print(f"\n--- {rule} ({len(by_rule[rule])}) ---")
        for v in by_rule[rule]:
            print(v)
    print(f"\n{len(violations)} total violation(s) across {len(by_rule)} rule(s)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
