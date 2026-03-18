"""
Structural Analysis Tools
Analyze paper structure: claim-evidence graphs, cognitive load, rhetorical skeleton.
Used by: ContributionDependencyGrapher, ReaderCognitiveLoadSimulator, RhetoricalSkeletonExtractor
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class ClaimEvidencePair:
    claim_id: str
    claim_text: str
    evidence_ids: List[str]
    section: str
    strength: str  # STRONG, MODERATE, WEAK, UNSUPPORTED


@dataclass
class DependencyNode:
    node_id: str
    node_type: str  # CONTRIBUTION, CLAIM, EXPERIMENT, ASSUMPTION, LIMITATION
    text: str
    edges_to: List[str] = field(default_factory=list)


@dataclass
class CognitiveLoadPoint:
    section: str
    paragraph_index: int
    concept_density: float
    notation_shifts: int
    inference_length: int
    load_level: str  # LOW, MODERATE, HIGH, OVERLOAD


# ─── ContributionDependencyGrapher functions ───

def extract_claims_and_evidence(text: str) -> List[ClaimEvidencePair]:
    """Extract claims and map them to supporting evidence.

    Args:
        text: Full manuscript text

    Returns:
        List of ClaimEvidencePair with claim, evidence, section, strength
    """
    claim_markers = ['we show', 'we demonstrate', 'we find', 'we propose',
                     'our results', 'this paper contributes', 'we argue',
                     'our approach', 'we introduce', 'contributes by']
    evidence_markers = ['table', 'figure', 'fig.', 'tab.', 'experiment',
                       'result shows', 'as shown', r'section \d', 'appendix']

    pairs = []
    current_section = "Unknown"
    claim_counter = 0

    for line in text.split('\n'):
        stripped = line.strip()
        if re.match(r'^#{1,3}\s+', stripped) or re.match(r'^\\(sub)?section', stripped):
            current_section = re.sub(r'^#{1,3}\s+|^\\(sub)?section\{|\}$', '', stripped).strip()
            continue

        line_lower = stripped.lower()
        if any(cm in line_lower for cm in claim_markers):
            claim_counter += 1
            claim_id = f"CL{claim_counter}"

            evidence_found = []
            for em in evidence_markers:
                if re.search(em, line_lower):
                    evidence_found.append(em.upper())

            if evidence_found:
                strength = "STRONG" if len(evidence_found) >= 2 else "MODERATE"
            else:
                strength = "UNSUPPORTED"

            pairs.append(ClaimEvidencePair(
                claim_id=claim_id,
                claim_text=stripped[:200],
                evidence_ids=evidence_found,
                section=current_section,
                strength=strength
            ))

    return pairs


def build_dependency_graph(
    claims: List[ClaimEvidencePair],
    contributions: List[str] = None,
    limitations: List[str] = None
) -> Dict:
    """Build a dependency graph: contributions→claims→evidence→limitations.

    Args:
        claims: Output of extract_claims_and_evidence
        contributions: Optional list of contribution statements from abstract
        limitations: Optional list of limitation statements

    Returns:
        Dict with nodes (list), edges (list), mermaid_diagram (str)
    """
    nodes = []
    edges = []

    for i, c in enumerate(contributions or [], 1):
        nodes.append({"id": f"C{i}", "type": "CONTRIBUTION", "text": c[:100]})

    for cl in claims:
        nodes.append({"id": cl.claim_id, "type": "CLAIM", "text": cl.claim_text[:100]})
        for ev in cl.evidence_ids:
            ev_id = f"E_{ev}"
            if not any(n["id"] == ev_id for n in nodes):
                nodes.append({"id": ev_id, "type": "EVIDENCE", "text": ev})
            edges.append({"from": cl.claim_id, "to": ev_id, "type": "supported_by"})

    for i, lim in enumerate(limitations or [], 1):
        lid = f"L{i}"
        nodes.append({"id": lid, "type": "LIMITATION", "text": lim[:100]})

    # Build mermaid
    mermaid = ["graph TD"]
    for n in nodes:
        shape = {"CONTRIBUTION": "{{", "CLAIM": "[", "EVIDENCE": "(",
                 "LIMITATION": ">"}.get(n["type"], "[")
        close = {"CONTRIBUTION": "}}", "CLAIM": "]", "EVIDENCE": ")",
                 "LIMITATION": "]"}.get(n["type"], "]")
        label = n["text"][:50].replace('"', "'")
        mermaid.append(f'    {n["id"]}{shape}"{label}"{close}')

    for e in edges:
        mermaid.append(f'    {e["from"]} -->|{e["type"]}| {e["to"]}')

    return {
        "nodes": nodes,
        "edges": edges,
        "mermaid_diagram": "\n".join(mermaid),
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "contributions": sum(1 for n in nodes if n["type"] == "CONTRIBUTION"),
            "claims": sum(1 for n in nodes if n["type"] == "CLAIM"),
            "evidence": sum(1 for n in nodes if n["type"] == "EVIDENCE")
        }
    }


def detect_orphan_contributions(graph: Dict) -> List[Dict]:
    """Find contributions without supporting evidence chains.

    Args:
        graph: Output of build_dependency_graph

    Returns:
        List of orphan contributions with id, text, issue
    """
    edge_targets = {e["to"] for e in graph.get("edges", [])}
    edge_sources = {e["from"] for e in graph.get("edges", [])}

    orphans = []
    for node in graph.get("nodes", []):
        if node["type"] == "CONTRIBUTION":
            if node["id"] not in edge_sources and node["id"] not in edge_targets:
                orphans.append({
                    "id": node["id"],
                    "text": node["text"],
                    "issue": "No edges to/from this contribution — completely disconnected"
                })

    unsupported_claims = []
    for node in graph.get("nodes", []):
        if node["type"] == "CLAIM":
            if node["id"] not in edge_sources:
                unsupported_claims.append({
                    "id": node["id"],
                    "text": node["text"],
                    "issue": "Claim has no supporting evidence edge"
                })

    return orphans + unsupported_claims


# ─── ReaderCognitiveLoadSimulator functions ───

def measure_concept_density(text: str) -> List[Dict]:
    """Measure new concept introductions per paragraph.

    Args:
        text: Full manuscript text

    Returns:
        List of dicts per paragraph with section, density, new_terms
    """
    paragraphs = re.split(r'\n\s*\n', text)
    all_terms_seen = set()
    results = []

    technical_pattern = re.compile(r'\b[A-Z][a-zA-Z]*(?:[A-Z][a-z]+)+\b')  # CamelCase
    acronym_pattern = re.compile(r'\b[A-Z]{2,6}\b')

    for i, para in enumerate(paragraphs):
        if len(para.strip()) < 50:
            continue

        terms = set(technical_pattern.findall(para)) | set(acronym_pattern.findall(para))
        new_terms = terms - all_terms_seen
        all_terms_seen |= terms

        word_count = len(para.split())
        density = len(new_terms) / max(word_count / 100, 1)

        results.append({
            "paragraph_index": i,
            "word_count": word_count,
            "new_terms": sorted(new_terms)[:10],
            "new_term_count": len(new_terms),
            "density_per_100_words": round(density, 2),
            "load_level": (
                "OVERLOAD" if density > 5
                else "HIGH" if density > 3
                else "MODERATE" if density > 1.5
                else "LOW"
            )
        })

    return results


def detect_notation_shifts(text: str) -> List[Dict]:
    """Detect where mathematical notation changes without transition.

    Args:
        text: Full manuscript text

    Returns:
        List of notation shift locations with old_notation, new_notation, line
    """
    math_patterns = re.findall(r'\$([^$]+)\$', text)
    shifts = []
    prev_vars = set()

    for i, expr in enumerate(math_patterns):
        current_vars = set(re.findall(r'[a-zA-Z](?:_[a-zA-Z0-9]+)?', expr))
        if prev_vars and current_vars:
            new_vars = current_vars - prev_vars
            if len(new_vars) > 2:
                shifts.append({
                    "position": i,
                    "expression": expr[:80],
                    "new_variables": sorted(new_vars),
                    "shift_count": len(new_vars),
                    "severity": "HIGH" if len(new_vars) > 3 else "MODERATE"
                })
        prev_vars = current_vars

    return shifts


def generate_cognitive_load_map(
    density_results: List[Dict],
    notation_shifts: List[Dict]
) -> str:
    """Generate a cognitive load heat map as markdown.

    Args:
        density_results: Output of measure_concept_density
        notation_shifts: Output of detect_notation_shifts

    Returns:
        Formatted markdown report
    """
    overloads = [d for d in density_results if d["load_level"] in ("HIGH", "OVERLOAD")]
    lines = ["# Cognitive Load Map\n"]
    lines.append(f"## Summary: {len(overloads)} high-load paragraphs, "
                 f"{len(notation_shifts)} notation shifts\n")

    if overloads:
        lines.append("## Overload Points\n")
        lines.append("| Paragraph | Load | New Terms | Density |")
        lines.append("|-----------|------|-----------|---------|")
        for d in overloads:
            lines.append(f"| {d['paragraph_index']} | {d['load_level']} | "
                        f"{d['new_term_count']} | {d['density_per_100_words']}/100w |")

    return "\n".join(lines)


# ─── RhetoricalSkeletonExtractor functions ───

RHETORICAL_ROLES = {
    'gap_statement': ['however', 'nevertheless', 'despite', 'gap', 'limitation',
                     'yet no study', 'remains unclear', 'little is known'],
    'claim': ['we show', 'we demonstrate', 'we propose', 'we argue',
             'our contribution', 'we introduce'],
    'evidence': ['table', 'figure', 'results show', 'experiment', 'as shown in'],
    'concession': ['although', 'while', 'admittedly', 'we acknowledge',
                  'limitation of', 'caveat'],
    'transition': ['next', 'furthermore', 'in addition', 'building on',
                  'turning to', 'we now'],
    'framing': ['is important because', 'critical for', 'essential for',
               'growing interest in', 'recent advances']
}


def identify_rhetorical_motif(text: str) -> List[Dict]:
    """Identify the rhetorical role of each paragraph.

    Args:
        text: Full manuscript text

    Returns:
        List of dicts with paragraph_index, role, confidence, markers_found
    """
    paragraphs = re.split(r'\n\s*\n', text)
    results = []

    for i, para in enumerate(paragraphs):
        if len(para.strip()) < 30:
            continue

        para_lower = para.lower()
        role_scores = {}
        role_markers = {}

        for role, markers in RHETORICAL_ROLES.items():
            found = [m for m in markers if m in para_lower]
            if found:
                role_scores[role] = len(found)
                role_markers[role] = found

        if role_scores:
            best_role = max(role_scores, key=role_scores.get)
            results.append({
                "paragraph_index": i,
                "role": best_role,
                "confidence": min(role_scores[best_role] / 3, 1.0),
                "markers_found": role_markers[best_role],
                "preview": para.strip()[:80]
            })
        else:
            results.append({
                "paragraph_index": i,
                "role": "exposition",
                "confidence": 0.3,
                "markers_found": [],
                "preview": para.strip()[:80]
            })

    return results


def detect_narrative_fractures(motifs: List[Dict]) -> List[Dict]:
    """Detect where the rhetorical flow breaks unexpectedly.

    Args:
        motifs: Output of identify_rhetorical_motif

    Returns:
        List of fracture points with location, from_role, to_role, severity
    """
    EXPECTED_FLOWS = {
        'framing': ['gap_statement', 'claim', 'transition'],
        'gap_statement': ['claim', 'transition'],
        'claim': ['evidence', 'transition'],
        'evidence': ['claim', 'concession', 'transition'],
        'concession': ['claim', 'evidence', 'transition'],
        'transition': ['claim', 'evidence', 'framing'],
    }

    fractures = []
    for i in range(len(motifs) - 1):
        current = motifs[i]["role"]
        next_role = motifs[i + 1]["role"]
        expected = EXPECTED_FLOWS.get(current, [])

        if expected and next_role not in expected and next_role != "exposition":
            fractures.append({
                "paragraph_index": motifs[i + 1]["paragraph_index"],
                "from_role": current,
                "to_role": next_role,
                "expected": expected,
                "severity": "HIGH" if current == "claim" and next_role not in ["evidence"] else "MODERATE",
                "suggestion": f"After '{current}', expected {expected}, got '{next_role}'"
            })

    return fractures
