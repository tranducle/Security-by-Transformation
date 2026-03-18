"""
Epistemic Analysis Tools
Classify claims by epistemic tier and detect unauthorized jumps.
Used by: EpistemicBoundaryMapper, CausalClaimGatekeeper
"""

import re
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Dict, Optional, Tuple


class EpistemicTier(IntEnum):
    OBSERVATION = 1
    PATTERN = 2
    INFERENCE = 3
    CAUSAL_CLAIM = 4
    SPECULATION = 5
    RECOMMENDATION = 6
    GENERALIZATION = 7


TIER_LABELS = {
    1: "Observation", 2: "Pattern/Correlation", 3: "Inference",
    4: "Causal Claim", 5: "Speculation", 6: "Recommendation",
    7: "Generalization"
}


@dataclass
class EpistemicStatement:
    text: str
    section: str
    line_number: int
    claim_tier: int
    evidence_tier: int
    is_jump: bool
    jump_severity: Optional[str] = None  # CRITICAL, MAJOR, MINOR


@dataclass
class CausalStatement:
    text: str
    section: str
    causal_words: List[str]
    evidence_type: str  # RCT, quasi-exp, observational, none
    verdict: str  # JUSTIFIED, OVERCLAIM, NEEDS_HEDGE


# ─── EpistemicBoundaryMapper functions ───

TIER_MARKERS = {
    1: ['we measured', 'we observed', 'data shows', 'the dataset contains',
        'we collected', 'table shows', 'figure shows'],
    2: ['correlates with', 'is associated with', 'pattern', 'trend',
        'co-occurs', 'relationship between', 'varies with'],
    3: ['suggests', 'indicates', 'implies', 'likely', 'appears to',
        'evidence supports', 'consistent with'],
    4: ['causes', 'leads to', 'results in', 'drives', 'determines',
        'produces', 'effect of', 'impact of', 'influences'],
    5: ['may', 'might', 'could potentially', 'it is possible',
        'we speculate', 'we conjecture', 'hypothetically'],
    6: ['should adopt', 'we recommend', 'practitioners should',
        'organizations must', 'policy implications'],
    7: ['universally', 'always', 'in all cases', 'generally applicable',
        'across all domains', 'fundamental principle'],
}


def classify_epistemic_tier(statement: str) -> Dict:
    """Classify a statement by its epistemic tier (1-7).

    Tier hierarchy: Observation(1) → Pattern(2) → Inference(3) →
    Causal(4) → Speculation(5) → Recommendation(6) → Generalization(7)

    Args:
        statement: The assertive statement to classify

    Returns:
        Dict with tier (int), label (str), markers_found (list), confidence (float)
    """
    s = statement.lower()
    tier_scores = {}

    for tier, markers in TIER_MARKERS.items():
        matches = [m for m in markers if m in s]
        if matches:
            tier_scores[tier] = len(matches)

    if not tier_scores:
        return {"tier": 3, "label": "Inference", "markers_found": [],
                "confidence": 0.3}

    best_tier = max(tier_scores, key=tier_scores.get)
    return {
        "tier": best_tier,
        "label": TIER_LABELS[best_tier],
        "markers_found": [m for m in TIER_MARKERS[best_tier] if m in s],
        "confidence": min(tier_scores[best_tier] / 3.0, 1.0)
    }


def detect_epistemic_jumps(
    statements: List[Dict],
    max_safe_jump: int = 1
) -> List[Dict]:
    """Detect unauthorized jumps between epistemic tiers.

    A jump occurs when claim_tier > evidence_tier + max_safe_jump.

    Args:
        statements: List of dicts with 'text', 'claim_tier', 'evidence_tier'
        max_safe_jump: Maximum allowed tier gap (default 1)

    Returns:
        List of jump dicts with text, claim_tier, evidence_tier, gap, severity
    """
    jumps = []
    for stmt in statements:
        gap = stmt.get("claim_tier", 0) - stmt.get("evidence_tier", 0)
        if gap > max_safe_jump:
            if gap >= 3:
                severity = "CRITICAL"
            elif gap >= 2:
                severity = "MAJOR"
            else:
                severity = "MINOR"

            jumps.append({
                "text": stmt.get("text", ""),
                "section": stmt.get("section", "Unknown"),
                "claim_tier": stmt["claim_tier"],
                "claim_label": TIER_LABELS.get(stmt["claim_tier"], "?"),
                "evidence_tier": stmt["evidence_tier"],
                "evidence_label": TIER_LABELS.get(stmt["evidence_tier"], "?"),
                "gap": gap,
                "severity": severity,
                "suggestion": f"Downgrade claim to Tier {stmt['evidence_tier'] + max_safe_jump} "
                              f"({TIER_LABELS.get(stmt['evidence_tier'] + max_safe_jump, '?')}) "
                              f"or add Tier {stmt['claim_tier']} evidence."
            })

    return sorted(jumps, key=lambda j: {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}[j["severity"]])


def map_certainty_levels(text: str) -> Dict:
    """Map the distribution of certainty/hedging words across the text.

    Args:
        text: Full manuscript text

    Returns:
        Dict with certainty_words, hedging_words, ratio, section_distribution
    """
    certainty = ['clearly', 'demonstrates', 'proves', 'establishes',
                 'confirms', 'shows that', 'certainly', 'undoubtedly',
                 'definitively', 'without question']
    hedging = ['may', 'might', 'could', 'possibly', 'suggests',
               'appears', 'seems', 'arguably', 'tentatively',
               'potentially', 'to some extent']

    text_lower = text.lower()
    c_found = [(w, len(re.findall(r'\b' + re.escape(w) + r'\b', text_lower)))
               for w in certainty]
    h_found = [(w, len(re.findall(r'\b' + re.escape(w) + r'\b', text_lower)))
               for w in hedging]

    c_total = sum(c for _, c in c_found)
    h_total = sum(c for _, c in h_found)

    return {
        "certainty_words": {w: c for w, c in c_found if c > 0},
        "hedging_words": {w: c for w, c in h_found if c > 0},
        "certainty_count": c_total,
        "hedging_count": h_total,
        "ratio": round(c_total / max(h_total, 1), 2),
        "assessment": (
            "over-certain" if c_total > h_total * 2
            else "well-balanced" if 0.5 <= c_total / max(h_total, 1) <= 2
            else "over-hedged"
        )
    }


def generate_epistemic_report(
    jumps: List[Dict],
    tier_distribution: Dict,
    certainty_map: Dict
) -> str:
    """Generate a markdown epistemic boundary report.

    Args:
        jumps: Output of detect_epistemic_jumps
        tier_distribution: Count of statements per tier
        certainty_map: Output of map_certainty_levels

    Returns:
        Formatted markdown report string
    """
    lines = ["# Epistemic Boundary Map\n"]
    critical = sum(1 for j in jumps if j["severity"] == "CRITICAL")
    major = sum(1 for j in jumps if j["severity"] == "MAJOR")

    lines.append(f"## Summary: {len(jumps)} jumps detected "
                 f"({critical} critical, {major} major)\n")
    lines.append(f"**Certainty balance:** {certainty_map.get('assessment', 'unknown')}\n")

    if jumps:
        lines.append("## Dangerous Jumps\n")
        lines.append("| # | Severity | Claim Tier | Evidence Tier | Gap | Section |")
        lines.append("|---|----------|-----------|--------------|-----|---------|")
        for i, j in enumerate(jumps, 1):
            lines.append(f"| {i} | {j['severity']} | "
                        f"{j['claim_label']} | {j['evidence_label']} | "
                        f"{j['gap']} | {j.get('section', '?')} |")

    return "\n".join(lines)


# ─── CausalClaimGatekeeper functions ───

CAUSAL_LANGUAGE = {
    'strong': ['causes', 'leads to', 'results in', 'drives', 'determines',
               'produces', 'effect of'],
    'moderate': ['influences', 'impacts', 'contributes to', 'affects',
                 'shapes', 'predicts'],
    'hedge': ['is associated with', 'correlates with', 'co-occurs with',
              'is related to']
}

CAUSAL_DESIGNS = {
    'RCT': ['randomized', 'random assignment', 'control group', 'RCT',
            'randomized controlled'],
    'quasi_experimental': ['difference-in-differences', 'DiD', 'instrumental variable',
                          'regression discontinuity', 'natural experiment',
                          'propensity score'],
    'observational': ['observational', 'cross-sectional', 'survey', 'regression',
                     'correlation', 'panel data']
}


def extract_causal_language(text: str) -> List[Dict]:
    """Extract sentences with causal language and classify strength.

    Args:
        text: Full manuscript text

    Returns:
        List of dicts with sentence, causal_words, strength, line_number
    """
    results = []
    for i, line in enumerate(text.split('\n'), 1):
        sentences = re.split(r'(?<=[.!?])\s+', line)
        for sent in sentences:
            s_lower = sent.lower()
            found_words = []
            strength = None

            for level, words in CAUSAL_LANGUAGE.items():
                for w in words:
                    if w in s_lower:
                        found_words.append(w)
                        if strength is None or \
                           ['hedge', 'moderate', 'strong'].index(level) > \
                           ['hedge', 'moderate', 'strong'].index(strength):
                            strength = level

            if found_words:
                results.append({
                    "sentence": sent.strip(),
                    "causal_words": found_words,
                    "strength": strength,
                    "line_number": i
                })

    return results


def assess_causal_evidence(
    causal_claims: List[Dict],
    methodology_text: str
) -> List[Dict]:
    """Assess whether causal language is justified by the research design.

    Args:
        causal_claims: Output of extract_causal_language
        methodology_text: Text from methodology section

    Returns:
        List of dicts with sentence, causal_strength, design_type, verdict
    """
    meth_lower = methodology_text.lower()
    design = 'observational'
    for dtype, markers in CAUSAL_DESIGNS.items():
        if any(m in meth_lower for m in markers):
            design = dtype
            break

    design_strength = {'RCT': 'strong', 'quasi_experimental': 'moderate',
                       'observational': 'hedge'}
    max_justified = design_strength.get(design, 'hedge')

    strength_order = ['hedge', 'moderate', 'strong']
    results = []
    for claim in causal_claims:
        claim_idx = strength_order.index(claim['strength'])
        max_idx = strength_order.index(max_justified)

        if claim_idx > max_idx:
            verdict = "OVERCLAIM"
        elif claim_idx == max_idx:
            verdict = "JUSTIFIED"
        else:
            verdict = "JUSTIFIED"

        results.append({
            "sentence": claim["sentence"],
            "causal_strength": claim["strength"],
            "design_type": design,
            "design_supports": max_justified,
            "verdict": verdict,
            "fix": (f"Soften to '{strength_order[max_idx]}' language"
                    if verdict == "OVERCLAIM" else None)
        })

    return results


def generate_causal_audit(
    assessments: List[Dict]
) -> str:
    """Generate a causal claims audit report.

    Args:
        assessments: Output of assess_causal_evidence

    Returns:
        Formatted markdown report string
    """
    overclaims = [a for a in assessments if a["verdict"] == "OVERCLAIM"]
    lines = ["# Causal Claims Audit\n"]
    lines.append(f"## Summary: {len(assessments)} causal claims, "
                 f"{len(overclaims)} overclaims\n")
    lines.append(f"**Research design:** {assessments[0]['design_type'] if assessments else 'unknown'}\n")

    if overclaims:
        lines.append("## Overclaims\n")
        for i, oc in enumerate(overclaims, 1):
            lines.append(f"### {i}. {oc['sentence'][:80]}...")
            lines.append(f"- **Claim strength:** {oc['causal_strength']}")
            lines.append(f"- **Design supports:** {oc['design_supports']}")
            lines.append(f"- **Fix:** {oc['fix']}\n")

    return "\n".join(lines)
