#!/usr/bin/env python3
"""
Agent Router — Level 3 Enforcement
====================================
Analyzes a user query and returns the best-matching agent(s) from agents/*.json.
Uses keyword matching from each agent's triggers.keywords field.

Usage:
    python .agent/scripts/route.py "find papers on cybersecurity in SMEs"
    python .agent/scripts/route.py --top 3 "write methodology section"
    python .agent/scripts/route.py --show-prompt "literature review"
"""

import os
import sys
import json
import re
import unicodedata
from collections import defaultdict

# ============================================================================
# VIETNAMESE -> ENGLISH TRANSLATION (from src/langgraph/nodes/router.py)
# ============================================================================

VI_TO_EN = {
    # Research & Discovery
    "tim bai bao": "find papers", "tim tai lieu": "literature",
    "tim kiem": "search", "tim": "find", "nghien cuu": "research",
    "bai bao": "papers", "tai lieu": "literature",
    "tong quan": "systematic review", "khoang trong": "research gap",
    "y tuong": "research idea", "du lieu": "dataset",
    "kiem tra moi": "novelty check",
    # Methodology & Analysis
    "phuong phap": "methodology", "thiet ke thi nghiem": "experiment design",
    "thi nghiem": "experiment", "thong ke": "statistics",
    "phan tich": "analyze", "khao sat": "survey",
    "dinh luong": "quantitative", "dinh tinh": "qualitative",
    "mo hinh toan": "math model", "ly thuyet tro choi": "game theory",
    "nhan qua": "causal",
    # Security & Risk
    "bao mat": "security", "rui ro": "risk", "de doa": "threat model",
    "tan cong": "attack", "phong thu": "defense",
    "ma hoa": "encryption", "tuan thu": "compliance",
    # Writing & Synthesis
    "viet bai": "write paper", "ban thao": "manuscript", "nhap": "draft",
    "de cuong": "paper outline", "tong hop": "synthesize",
    "tom tat": "summary", "chinh sua": "revise manuscript",
    "tai tro": "grant", "de xuat": "proposal",
    "tai lieu tham khao": "references", "trich dan": "citation",
    # Coding & Engineering
    "lap trinh": "programming", "sua loi": "debug",
    "xay dung": "implement", "tien xu ly du lieu": "preprocess data",
    "tien xu ly": "preprocess",
    # Visualization
    "bieu do": "chart", "hinh anh": "figure", "do thi": "plot",
    "trinh bay": "presentation", "so do": "flowchart",
    # Review & Quality
    "danh gia": "review", "kiem tra": "check", "xac minh": "verify",
    "phan bien": "critical review", "chat luong": "quality", "tap chi": "journal",
    # Strategy & Management
    "ke hoach": "plan", "lo trinh": "roadmap", "chien luoc": "strategy",
    "tien do": "progress", "muc tieu": "milestone",
    # Innovation
    "dong nao": "brainstorm", "sang tao": "creative",
    # Autonomous Experiment
    "trien khai thuc nghiem": "auto experiment",
    "chay thuc nghiem tu dong": "autonomous experiment",
}

_VI_KEYS_SORTED = sorted(VI_TO_EN.keys(), key=len, reverse=True)


def _normalize_vietnamese(text):
    """Remove Vietnamese diacritical marks for fuzzy matching."""
    text = text.replace("đ", "d").replace("Đ", "D")
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def translate_query(query):
    """Translate Vietnamese keywords in a query to English equivalents."""
    normalized = _normalize_vietnamese(query)
    translated = normalized
    for vi_key in _VI_KEYS_SORTED:
        if vi_key in translated:
            translated = translated.replace(vi_key, VI_TO_EN[vi_key])
    if translated != normalized:
        return translated, True
    return query.lower(), False


def get_agents_dir():
    """Locate agents/ directory from script location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(script_dir))
    agents_dir = os.path.join(root, "agents")
    if not os.path.isdir(agents_dir):
        print(f"ERROR: agents/ directory not found at {agents_dir}")
        sys.exit(1)
    return agents_dir

def load_all_agents(agents_dir):
    """Load all agent JSON files and extract routing info."""
    agents = []
    for fname in os.listdir(agents_dir):
        if not fname.endswith(".json"):
            continue
        filepath = os.path.join(agents_dir, fname)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            triggers = data.get("triggers", {})
            keywords = triggers.get("keywords", [])
            agents.append({
                "name": data.get("name", fname.replace(".json", "")),
                "domain": data.get("domain", "Unknown"),
                "role": data.get("role", ""),
                "goal": data.get("goal", ""),
                "keywords": [kw.lower() for kw in keywords],
                "priority": triggers.get("priority", 5),
                "is_domain_lead": data.get("is_domain_lead", False),
                "tools": [t.get("name", "") for t in data.get("tools", [])],
                "file": fname,
                "has_system_prompt": bool(data.get("system_prompt", "")),
                "system_prompt_preview": (data.get("system_prompt", "") or "")[:300],
            })
        except (json.JSONDecodeError, KeyError) as e:
            pass  # Skip malformed files
    return agents

def score_agent(agent, query_lower, query_words):
    """Score an agent against a query. Higher = better match."""
    score = 0
    matched_keywords = []

    for kw in agent["keywords"]:
        if kw in query_lower:
            # Exact phrase match (higher value)
            score += 10
            matched_keywords.append(kw)
        else:
            # Check word-level overlap
            kw_words = set(kw.split())
            overlap = kw_words & query_words
            if len(overlap) >= 1 and len(overlap) >= len(kw_words) * 0.5:
                score += 5 * len(overlap)
                matched_keywords.append(f"~{kw}")

    # Bonus for domain leads
    if agent["is_domain_lead"] and score > 0:
        score += 3

    # Priority bonus
    if score > 0:
        score += agent["priority"]

    return score, matched_keywords

def route(query, agents, top_n=3):
    """Route a query to the best-matching agents. Supports Vietnamese."""
    translated, was_vietnamese = translate_query(query)
    query_lower = translated
    query_words = set(re.findall(r'\w+', query_lower))

    results = []
    for agent in agents:
        score, matched = score_agent(agent, query_lower, query_words)
        if score > 0:
            results.append((score, matched, agent))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_n]

def format_result(rank, score, matched, agent, show_prompt=False):
    """Format a single routing result."""
    lead = " [DOMAIN LEAD]" if agent["is_domain_lead"] else ""
    tools_str = ", ".join(agent["tools"][:5]) if agent["tools"] else "(no tools)"

    lines = [
        f"  #{rank} {agent['name']}{lead}  (score: {score})",
        f"      Domain:   {agent['domain']}",
        f"      Role:     {agent['role'][:80]}",
        f"      Matched:  {', '.join(matched)}",
        f"      Tools:    {tools_str}",
        f"      File:     agents/{agent['file']}",
    ]
    if show_prompt and agent["has_system_prompt"]:
        lines.append(f"      Prompt:   {agent['system_prompt_preview']}...")
    return "\n".join(lines)

def main():
    # Fix Windows cp1252 encoding for Vietnamese output
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Parse args
    show_prompt = "--show-prompt" in sys.argv
    top_n = 3

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for i, a in enumerate(sys.argv[1:]):
        if a == "--top" and i + 2 < len(sys.argv):
            try:
                top_n = int(sys.argv[i + 2])
            except ValueError:
                pass

    if not args:
        print("Usage: python route.py [--show-prompt] [--top N] \"your query here\"")
        print("\nExamples:")
        print('  python route.py "find papers on cybersecurity"')
        print('  python route.py --show-prompt "write methodology section"')
        print('  python route.py --top 5 "analyze survey data with statistics"')
        sys.exit(0)

    query = " ".join(args)
    agents_dir = get_agents_dir()
    agents = load_all_agents(agents_dir)

    # Show translation info
    translated, was_vietnamese = translate_query(query)
    print(f"Query: \"{query}\"")
    if was_vietnamese:
        print(f"Translated: \"{translated}\"")
    print(f"Agents loaded: {len(agents)}")
    print(f"{'='*60}")

    results = route(query, agents, top_n)

    if not results:
        print("\n  No matching agents found.")
        print("  The query may not contain research-related keywords.")
        print("  Tip: Use domain-specific terms from the routing table.")
    else:
        print(f"\n  Top {len(results)} matches:\n")
        for i, (score, matched, agent) in enumerate(results, 1):
            print(format_result(i, score, matched, agent, show_prompt))
            print()

    # Always print the recommended action
    if results:
        best = results[0][2]
        print(f"{'='*60}")
        print(f"RECOMMENDED: Read agents/{best['file']}")
        print(f"ACTION:      Adopt {best['name']} persona for this task")
        if best["tools"]:
            print(f"TOOLS:       Use {', '.join(best['tools'][:3])}")

if __name__ == "__main__":
    main()
