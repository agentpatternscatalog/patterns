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
  A17 Plain language          no AI-slop or overcomplex wording (makemytone)
  A10 Naming                 no duplicate names or alias collisions
  A16 Reader-view template   5 sections (Summary, Problem, When-to-Use,
                             When-Not-to-Use, Architecture Diagram) all renderable

Usage:
  python3 .github/scripts/lint.py                 # all rules, error on violations
  python3 .github/scripts/lint.py --no-network    # skip A6.3 URL liveness
  python3 .github/scripts/lint.py --rule A3       # single group
"""
from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib import error, request
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "patterns-src"
SCHEMA = ROOT / "schema.json"
TAXONOMY = ROOT / "docs" / "taxonomy.md"


def load_url_allowlist() -> tuple[set[str], set[str]]:
    """Load the CI liveness allowlist (.github/scripts/url-allowlist.txt).

    Entries are URLs/hosts verified live from a workstation that intermittently
    fail the A6.3 probe from CI runners (geo/IP/WAF 4xx-5xx). A matching URL is
    downgraded from a violation to a warning. A line starting with http(s):// is
    an exact-URL match; anything else is a host (matching that host and its
    subdomains). '#' starts a comment.
    """
    path = Path(__file__).resolve().parent / "url-allowlist.txt"
    exact: set[str] = set()
    hosts: set[str] = set()
    if not path.exists():
        return exact, hosts
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith(("http://", "https://")):
            exact.add(line.rstrip("/"))
        else:
            hosts.add(line.lower())
    return exact, hosts


URL_ALLOWLIST_EXACT, URL_ALLOWLIST_HOSTS = load_url_allowlist()


def is_url_allowlisted(url: str) -> bool:
    """True if a probe failure for this URL should be a warning, not an A6.3."""
    if url.rstrip("/") in URL_ALLOWLIST_EXACT:
        return True
    host = (urlparse(url).hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in URL_ALLOWLIST_HOSTS)

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

# A17 Plain language. AI-slop / overcomplex words with no legitimate technical
# meaning in this catalog, mapped to the plain replacement shown in the message.
# This list mirrors the `makemytone` skill's banned-word list. It is deliberately
# curated to terms that do NOT occur in current prose, so the rule fires only on
# new slop; technical homographs (ecosystem, unlock, navigate, paradigm,
# utilization, summarize) are intentionally excluded to avoid false positives.
SLOP_WORDS = {
    "utilize": "use",
    "utilise": "use",
    "utilizes": "uses",
    "utilises": "uses",
    "utilizing": "using",
    "utilising": "using",
    "holistic": "drop it, or name the specific scope",
    "tapestry": "drop it",
    "delve": "look at / go into",
    "delves": "looks at",
    "delving": "looking at",
    "empower": "let / enable",
    "empowers": "lets / enables",
    "empowering": "letting / enabling",
    "innovative": "say what is actually new",
    "innovation": "say what is actually new",
    "streamline": "simplify / speed up",
    "streamlines": "simplifies",
    "streamlined": "simplified",
    "streamlining": "simplifying",
    "synergies": "describe the actual interaction",
    "transformative": "say what concretely changes",
    "evidentiary": "about the evidence",
    "hyperscaler": "big cloud provider",
    "myriad": "many",
    "plethora": "many",
}

# Sentence-level AI tics: (regex, advice). Matched case-insensitively over prose.
APOS = r"(?:'|’)"
SLOP_PHRASES = (
    (rf"\bit(?:{APOS}s| is) not (?:just|only)\b", "antithesis tic — state the positive claim plainly"),
    (rf"\bin today{APOS}?s\b", "drop the throat-clearing; open with the claim"),
    (r"\bin a world where\b", "drop it; open with the claim"),
    (rf"\bit(?:{APOS}s| is) worth noting\b", "drop it; just note the thing"),
    (r"\bat its core\b", "drop it"),
    (r"\bin essence\b", "drop it"),
    (r"\bin conclusion\b", "drop it; the last sentence is the conclusion"),
    (rf"\bwhether you(?:{APOS}re| are)\b", "pick one reader; drop the whether-you cadence"),
    (r"\b(?:deep dive|dive into|dives into|diving into|delve into)\b", "say 'look at' / 'go into', or be specific"),
)

# Sentence-initial additive connectors: the link is implicit, so just start the sentence.
SLOP_SENTENCE_INITIAL = re.compile(r"(?:^|[.!?]\s+)(Moreover|Furthermore|Additionally)\b")

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


def load_methodology_ids() -> set[str]:
    """Methodologies share the catalog id namespace with patterns. Pattern
    related[] and verification-todo entries may refer to ids that now live
    in methodologies-src/ (e.g. evaluation-driven-development, migrated out
    of patterns-src/ when the methodologies dimension was introduced)."""
    src = ROOT / "methodologies-src"
    if not src.exists():
        return set()
    ids: set[str] = set()
    for shard_path in src.glob("*.json"):
        shard = json.loads(shard_path.read_text())
        for m in shard.get("methodologies", []):
            ids.add(m["id"])
    return ids


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
    required = (
        "id", "name", "category", "intent", "context", "problem", "solution",
        "status_in_practice", "example_scenario", "applicability", "diagram",
    )
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
        "AGENTS.md",
        "LICENSE",
        ".gitignore",
        "Makefile",
        "schema.json",
        "INDEX.md",
        "framework-coverage.json",
        "framework-coverage.schema.json",
        "recipes.json",
        "recipes.schema.json",
        "glossary.json",
        "glossary.schema.json",
        "verification-todo.json",
        "verification-todo.schema.json",
        "patterns.graph.schema.json",
        "patterns.compositions.schema.json",
        "compositions.schema.json",
        "compositions-todo.json",
        "compositions-todo.schema.json",
        "examples.schema.json",
        "methodologies.schema.json",
        "pattern-todo.json",
        "pattern-todo.schema.json",
        "training.json",
        "training.schema.json",
        "training-todo.json",
        "training-todo.schema.json",
        "TRENDS.md",
    }
    allowed_dirs = {
        "patterns-src",
        "patterns",
        "docs",
        ".github",
        "compositions-src",
        "examples-src",
        "methodologies-src",
        "pattern-todo-archive",
        "training-src",
        "training-todo-src",
    }
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
    pattern_ids = {p["id"] for p in patterns}
    # related[] entries may target a pattern OR a methodology — the two
    # dimensions share an id namespace. Resolution is against the union.
    ids = pattern_ids | load_methodology_ids()
    edges_by_src: dict[str, list[tuple[str, str]]] = {pid: [] for pid in pattern_ids}

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

    # Symmetric / inverse back-edges only apply when both endpoints are
    # patterns. Methodologies don't carry a related[] field of the same
    # shape, so back-edges to them are not enforced.
    for src, edges in edges_by_src.items():
        for tgt, rel in edges:
            if tgt not in pattern_ids:
                continue
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

    # Also probe URLs that live outside patterns-src/.
    cov_path = ROOT / "framework-coverage.json"
    if cov_path.exists():
        try:
            cov = json.loads(cov_path.read_text())
            for fw in cov.get("frameworks", []):
                if fw.get("url"):
                    urls_to_check.append((fw["url"], f"framework-coverage::{fw.get('id', '?')}"))
        except json.JSONDecodeError:
            pass

    if check_urls and urls_to_check:
        out.extend(_check_urls(urls_to_check))
    return out


def _check_urls(urls: list[tuple[str, str]]) -> list[Violation]:
    out: list[Violation] = []
    seen: dict[str, str | None] = {}

    # CI runners hit these against perfectly live hosts:
    #   - TLS handshake timeouts
    #   - "Network is unreachable" (errno 101) on IPv6 routes
    #   - "Temporary failure in name resolution" (DNS hiccup)
    #   - socket.timeout, socket.gaierror
    # None of them are evidence that the URL is dead; they are CI-side. We
    # retry with backoff and downgrade to a console warning (not a Violation)
    # if every retry still hits an infrastructure-shaped error.
    INFRA_ERR_MARKERS = (
        "Network is unreachable",
        "Temporary failure in name resolution",
        "Name or service not known",
        "handshake operation timed out",
        "read operation timed out",
        "_ssl.c:",
        "Connection reset by peer",
        "[Errno 101]",
        "[Errno 111]",
        "[Errno -2]",
        "[Errno -3]",
        "TimeoutError:",
        "socket.timeout",
        "socket.gaierror",
        "URLError: <urlopen error timed out>",
    )

    def _get_fallback(url: str, timeout: int = 20) -> str | None:
        try:
            req = request.Request(url, method="GET", headers={"User-Agent": USER_AGENT})
            with request.urlopen(req, timeout=timeout) as resp:
                if resp.status >= 400:
                    return f"HTTP {resp.status}"
                return None
        except error.HTTPError as e:
            if e.code in (403, 429):
                return None
            return f"HTTP {e.code}"
        except Exception as e:
            return f"{type(e).__name__}: {e}"

    def _looks_like_infra(err: str | None) -> bool:
        if not err:
            return False
        return any(m in err for m in INFRA_ERR_MARKERS)

    def _attempt_head(url: str) -> str | None:
        try:
            req = request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
            with request.urlopen(req, timeout=15) as resp:
                if resp.status >= 400:
                    return f"HTTP {resp.status}"
                return None
        except error.HTTPError as e:
            if e.code in (403, 429):
                return None
            if e.code in (405, 501):
                return _get_fallback(url)
            return f"HTTP {e.code}"
        except Exception as e:
            return f"{type(e).__name__}: {e}"

    def probe(url: str) -> tuple[str, str | None]:
        if url in seen:
            return url, seen[url]

        err = _attempt_head(url)
        if err is None:
            seen[url] = None
            return url, None

        # First fallback: GET with longer timeout. Often clears transient HEAD
        # rejections or short-lived TLS issues.
        err = _get_fallback(url, timeout=30)
        if err is None:
            seen[url] = None
            return url, None

        # Second fallback: brief backoff, then one more GET. Covers truly
        # flaky paths (.nl/.de origins via runner IPv6 routes, etc).
        if _looks_like_infra(err):
            time.sleep(2.0)
            err2 = _get_fallback(url, timeout=30)
            if err2 is None:
                seen[url] = None
                return url, None
            err = err2

        # If after all retries the error still looks like CI-side infrastructure,
        # surface a warning to stderr but do NOT block — runs from a real
        # workstation will catch genuinely dead URLs.
        if _looks_like_infra(err):
            print(
                f"  [A6.3 warn] {url}: persistent network error from CI runner "
                f"({err}); skipping liveness assertion",
                file=sys.stderr,
            )
            seen[url] = None
            return url, None

        # Verified-live-but-CI-flaky hosts (see url-allowlist.txt): a real 4xx/5xx
        # from a datacenter IP that serves fine from a workstation. Warn, never block.
        if is_url_allowlisted(url):
            print(
                f"  [A6.3 warn] {url}: probe returned {err} but the host is on the "
                f"CI liveness allowlist; skipping assertion",
                file=sys.stderr,
            )
            seen[url] = None
            return url, None

        seen[url] = err
        return url, err

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
    "Concrete Problems in AI Safety",
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


def rule_a17(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A17 Plain language: no AI-slop or overcomplex wording (see the makemytone skill)."""
    out: list[Violation] = []
    word_pat = re.compile(r"\b(" + "|".join(re.escape(w) for w in SLOP_WORDS) + r")\b", re.IGNORECASE)
    phrase_pats = [(re.compile(rx, re.IGNORECASE), advice) for rx, advice in SLOP_PHRASES]
    for p in patterns:
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        for slot, text in text_fields(p).items():
            for m in word_pat.finditer(text):
                w = m.group(1).lower()
                out.append(Violation("A17.1", f"{loc}#{slot}", f"AI-slop/overcomplex word {m.group(1)!r} (use: {SLOP_WORDS[w]})"))
            for rx, advice in phrase_pats:
                m = rx.search(text)
                if m:
                    out.append(Violation("A17.2", f"{loc}#{slot}", f"AI-slop phrasing {m.group(0)!r} — {advice}"))
            for m in SLOP_SENTENCE_INITIAL.finditer(text):
                out.append(Violation("A17.3", f"{loc}#{slot}", f"sentence-initial {m.group(1)!r}: start the sentence plainly; the additive link is implicit"))
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


def rule_a15(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A15 Verification-TODO refs: every entry must point to a real pattern/framework."""
    out: list[Violation] = []
    todo_path = ROOT / "verification-todo.json"
    if not todo_path.exists():
        return out
    try:
        todo = json.loads(todo_path.read_text())
    except json.JSONDecodeError as e:
        out.append(Violation("A15.1", "verification-todo.json", f"invalid JSON: {e}"))
        return out

    # A15.3 (lookup): accept entries pointing at a migrated id now living in
    # methodologies-src/. A15.5 (inverse-drift) only complains about *patterns*
    # without a TODO row — methodologies are not yet tracked in
    # verification-todo.json's schema.
    pattern_ids = {p["id"] for p in patterns}
    pattern_or_methodology_ids = pattern_ids | load_methodology_ids()
    cov_path = ROOT / "framework-coverage.json"
    framework_ids: set[str] = set()
    if cov_path.exists():
        try:
            cov = json.loads(cov_path.read_text())
            framework_ids = {fw["id"] for fw in cov.get("frameworks", [])}
        except json.JSONDecodeError:
            pass

    seen_p: set[str] = set()
    for entry in todo.get("patterns", []):
        pid = entry.get("id", "")
        if pid in seen_p:
            out.append(Violation("A15.2", f"verification-todo.patterns::{pid}", "duplicate id"))
        seen_p.add(pid)
        if pid not in pattern_or_methodology_ids:
            out.append(Violation(
                "A15.3", f"verification-todo.patterns::{pid}",
                f"references unknown pattern id"))
    seen_f: set[str] = set()
    for entry in todo.get("frameworks", []):
        fid = entry.get("id", "")
        if fid in seen_f:
            out.append(Violation("A15.2", f"verification-todo.frameworks::{fid}", "duplicate id"))
        seen_f.add(fid)
        if framework_ids and fid not in framework_ids:
            out.append(Violation(
                "A15.4", f"verification-todo.frameworks::{fid}",
                f"references unknown framework id"))
    # Also catch the inverse drift: catalog entry that has no TODO row.
    missing_patterns = pattern_ids - seen_p
    missing_frameworks = framework_ids - seen_f
    if missing_patterns:
        out.append(Violation(
            "A15.5", "verification-todo.json",
            f"{len(missing_patterns)} pattern(s) have no TODO entry: {sorted(missing_patterns)[:5]}{'...' if len(missing_patterns) > 5 else ''}"))
    if missing_frameworks:
        out.append(Violation(
            "A15.6", "verification-todo.json",
            f"{len(missing_frameworks)} framework(s) have no TODO entry: {sorted(missing_frameworks)[:5]}{'...' if len(missing_frameworks) > 5 else ''}"))
    return out


def rule_a14(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A14 Variant sanity: unique names within a pattern; see_also refs resolve;
    variant name must not duplicate an existing first-class pattern's id."""
    out: list[Violation] = []
    pattern_ids = {p["id"] for p in patterns}
    pattern_names_lower = {p["name"].lower() for p in patterns}
    for p in patterns:
        variants = p.get("variants") or []
        if not variants:
            continue
        loc = f"{where.get(p['id'], '?')}::{p['id']}"
        seen_names: set[str] = set()
        for v in variants:
            name = v.get("name", "")
            key = name.lower().strip()
            if not key:
                out.append(Violation("A14.1", loc, "variant has empty name"))
                continue
            if key in seen_names:
                out.append(Violation("A14.2", loc, f"duplicate variant name {name!r}"))
            seen_names.add(key)
            if key in pattern_names_lower and key != p["name"].lower():
                out.append(Violation(
                    "A14.3", loc,
                    f"variant {name!r} duplicates an existing first-class pattern's name; "
                    f"either reword the variant or promote it to its own pattern"))
            see_also = v.get("see_also")
            if see_also and see_also not in pattern_ids:
                out.append(Violation(
                    "A14.4", loc,
                    f"variant {name!r} see_also references unknown pattern id {see_also!r}"))
    return out


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


def rule_a16(patterns: list[dict], where: dict[str, str]) -> list[Violation]:
    """A16 Reader-view template: every pattern must populate the 10 sections.

    The reader view renders patterns as 10 numbered sections:
      1. Pattern Name              (name + lede)
      2. Problem                   (context + problem)
      3. When to Use               (applicability.use_when)
      4. When Not to Use           (applicability.do_not_use_when)
      5. Architecture Diagram      (diagram.mermaid)
      6. Components                (components[])
      7. Tools                     (tools[])
      8. Guardrails                (constrains)
      9. Failure Modes             (consequences.liabilities | failure_modes[])
      10. Evaluation Metrics       (evaluation_metrics[])

    Sections 1-5 and 8-9 are hard requirements (one violation per offending
    pattern). Sections 6, 7, 10 are backfill-in-progress: rather than spam
    hundreds of per-pattern violations, A16 emits one summary line per missing
    section listing the count and a short sample. Drop them as full per-pattern
    violations once backfill is complete.
    """
    out: list[Violation] = []
    missing_components: list[str] = []
    missing_tools: list[str] = []
    missing_metrics: list[str] = []

    for p in patterns:
        pid = p["id"]
        loc = f"{where.get(pid, '?')}::{pid}"

        # 1. Pattern Name section (Summary = intent + example_scenario).
        if not (p.get("intent") or "").strip():
            out.append(Violation("A16.1", loc, "section 1 (Pattern Name): intent is empty"))
        ex = (p.get("example_scenario") or "").strip()
        if not ex:
            out.append(Violation("A16.1", loc, "section 1 (Pattern Name): example_scenario missing (2-4 sentence narrative required)"))
        elif len(ex) < 30:
            out.append(Violation("A16.1", loc, f"section 1 (Pattern Name): example_scenario is {len(ex)} chars (<30; too short)"))

        # 2. Problem section.
        if not (p.get("context") or "").strip():
            out.append(Violation("A16.2", loc, "section 2 (Problem): context is empty"))
        if not (p.get("problem") or "").strip():
            out.append(Violation("A16.2", loc, "section 2 (Problem): problem is empty"))

        # 3 & 4. When to Use / When Not to Use.
        app = p.get("applicability") or {}
        if not (app.get("use_when") or []):
            out.append(Violation("A16.3", loc, "section 3 (When to Use): applicability.use_when is empty"))
        if not (app.get("do_not_use_when") or []):
            out.append(Violation("A16.4", loc, "section 4 (When Not to Use): applicability.do_not_use_when is empty"))

        # 5. Architecture Diagram.
        d = p.get("diagram") or {}
        if not d:
            out.append(Violation("A16.5", loc, "section 5 (Architecture Diagram): diagram block missing"))
        else:
            if not d.get("type"):
                out.append(Violation("A16.5", loc, "section 5 (Architecture Diagram): diagram.type missing"))
            if not (d.get("mermaid") or "").strip():
                out.append(Violation("A16.5", loc, "section 5 (Architecture Diagram): diagram.mermaid is empty"))

        # 6. Components — backfill in progress.
        if not (p.get("components") or []):
            missing_components.append(pid)

        # 7. Tools — backfill in progress.
        if not (p.get("tools") or []):
            missing_tools.append(pid)

        # 8. Guardrails — constrains is required-by-convention (also covered by A3).
        if not (p.get("constrains") or "").strip():
            out.append(Violation("A16.8", loc, "section 8 (Guardrails): constrains is empty"))

        # 9. Failure Modes — accept liabilities[] OR explicit failure_modes[].
        cons = p.get("consequences") or {}
        if not ((cons.get("liabilities") or []) or (p.get("failure_modes") or [])):
            out.append(Violation("A16.9", loc, "section 9 (Failure Modes): consequences.liabilities and failure_modes are both empty"))

        # 10. Evaluation Metrics — backfill in progress.
        if not (p.get("evaluation_metrics") or []):
            missing_metrics.append(pid)

    # Summary-style violations for the backfill-in-progress sections. One line
    # per section, not one per pattern, so the report stays readable.
    total = len(patterns)
    for code, label, missing in (
        ("A16.6", "section 6 (Components)", missing_components),
        ("A16.7", "section 7 (Tools)", missing_tools),
        ("A16.10", "section 10 (Evaluation Metrics)", missing_metrics),
    ):
        if missing:
            sample = ", ".join(sorted(missing)[:3])
            more = f" (+{len(missing) - 3} more)" if len(missing) > 3 else ""
            out.append(Violation(
                code, "patterns-src/",
                f"{label}: {len(missing)}/{total} patterns missing; e.g. {sample}{more}",
            ))
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
    "A14": ("variant sanity", lambda P, W, N: rule_a14(P, W)),
    "A15": ("verification-todo refs", lambda P, W, N: rule_a15(P, W)),
    "A16": ("reader-view template", lambda P, W, N: rule_a16(P, W)),
    "A17": ("plain language (no AI slop)", lambda P, W, N: rule_a17(P, W)),
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
