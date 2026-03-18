"""
Knowledge Depth Tools
Analyze knowledge density, distill insights, test arguments, extract cores.
Used by: KnowledgeCompressionAuditor, InsightDistiller, ArgumentLoadTester, CanonicalCoreExtractor
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import Counter


@dataclass
class InsightCandidate:
    text: str
    section: str
    insight_type: str  # finding, implication, contribution, methodology
    quotability_score: float
    standalone: bool


@dataclass
class ArgumentLink:
    claim: str
    supports: str
    link_type: str  # logical, empirical, analogical, authoritative
    strength: float


# ─── KnowledgeCompressionAuditor functions ───

def calculate_information_density(text: str) -> Dict:
    """Calculate information density metrics paragraph by paragraph.

    Args:
        text: Full manuscript text

    Returns:
        Dict with avg_density, paragraphs, redundancy_score
    """
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 50]
    results = []

    for i, para in enumerate(paragraphs):
        words = para.split()
        word_count = len(words)
        unique_words = len(set(w.lower() for w in words))
        sentences = re.split(r'[.!?]+', para)
        sentence_count = len([s for s in sentences if len(s.strip()) > 10])

        claim_markers = ['we show', 'we find', 'results', 'demonstrates',
                        'contributes', 'proposes', 'introduces']
        claims = sum(1 for m in claim_markers if m in para.lower())

        lexical_diversity = unique_words / max(word_count, 1)
        info_density = (claims * 2 + lexical_diversity * 5) / max(sentence_count, 1)

        results.append({
            "paragraph_index": i,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "unique_word_ratio": round(lexical_diversity, 3),
            "claims_detected": claims,
            "density_score": round(info_density, 2),
            "assessment": (
                "DENSE" if info_density > 3
                else "NORMAL" if info_density > 1
                else "SPARSE"
            )
        })

    total_density = sum(r["density_score"] for r in results)
    avg = round(total_density / max(len(results), 1), 2)

    return {
        "paragraph_count": len(results),
        "avg_density": avg,
        "paragraphs": results,
        "overall": "DENSE" if avg > 3 else "NORMAL" if avg > 1 else "SPARSE"
    }


def detect_redundant_passages(text: str, threshold: float = 0.6) -> List[Dict]:
    """Detect passages with redundant or repeated content.

    Args:
        text: Full manuscript text
        threshold: Similarity threshold (0-1)

    Returns:
        List of redundancy pairs with para_a, para_b, overlap_ratio
    """
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text)
                  if len(p.strip()) > 50]
    redundancies = []

    for i in range(len(paragraphs)):
        words_i = set(paragraphs[i].lower().split())
        for j in range(i + 1, min(i + 10, len(paragraphs))):
            words_j = set(paragraphs[j].lower().split())
            overlap = len(words_i & words_j)
            total = len(words_i | words_j)
            ratio = overlap / max(total, 1)

            if ratio > threshold:
                redundancies.append({
                    "para_a": i,
                    "para_b": j,
                    "overlap_ratio": round(ratio, 3),
                    "shared_word_count": overlap,
                    "preview_a": paragraphs[i][:80],
                    "preview_b": paragraphs[j][:80],
                    "suggestion": "Merge or remove duplicate content"
                })

    return redundancies


def calculate_compression_ratio(text: str) -> Dict:
    """Calculate how much the manuscript could be compressed.

    Args:
        text: Full manuscript text

    Returns:
        Dict with current_length, estimated_compressed, ratio, verbose_sections
    """
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 30]
    verbose = []

    filler_phrases = ['it is worth noting that', 'it should be noted that',
                     'it is important to mention', 'as mentioned earlier',
                     'as discussed above', 'in this paper we',
                     'the rest of this paper', 'the remainder of this']

    total_words = sum(len(p.split()) for p in paragraphs)
    filler_words = 0

    for i, para in enumerate(paragraphs):
        para_lower = para.lower()
        filler_count = sum(1 for f in filler_phrases if f in para_lower)
        if filler_count > 0:
            est_filler = filler_count * 8
            filler_words += est_filler
            verbose.append({
                "paragraph_index": i,
                "filler_count": filler_count,
                "estimated_removable_words": est_filler,
                "preview": para[:80]
            })

    ratio = round((total_words - filler_words) / max(total_words, 1), 3)
    return {
        "current_word_count": total_words,
        "estimated_compressed": total_words - filler_words,
        "compression_ratio": ratio,
        "filler_word_count": filler_words,
        "verbose_sections": verbose,
        "verdict": "VERBOSE" if ratio < 0.9 else "NORMAL" if ratio < 0.95 else "CONCISE"
    }


# ─── InsightDistiller functions ───

def distill_key_insights(text: str, max_insights: int = 10) -> List[InsightCandidate]:
    """Distill the most quotable and impactful insights.

    Args:
        text: Full manuscript text
        max_insights: Maximum insights to return

    Returns:
        List of InsightCandidate sorted by quotability
    """
    insight_markers = {
        'finding': ['we find that', 'our results show', 'we discover',
                   'we observe that', 'experiments reveal'],
        'implication': ['this implies', 'this suggests', 'implications for',
                       'this means that', 'consequence'],
        'contribution': ['we contribute', 'our contribution', 'we introduce',
                        'we propose', 'novel approach'],
        'methodology': ['our method', 'our approach', 'we design',
                       'our framework', 'our algorithm']
    }

    candidates = []
    current_section = "Unknown"

    for line in text.split('\n'):
        stripped = line.strip()
        if re.match(r'^#{1,3}\s+', stripped):
            current_section = re.sub(r'^#{1,3}\s+', '', stripped).strip()
            continue

        line_lower = stripped.lower()
        for itype, markers in insight_markers.items():
            for marker in markers:
                if marker in line_lower and len(stripped) > 40:
                    words = stripped.split()
                    standalone = len(words) <= 30
                    quotability = min(1.0, (
                        (0.3 if standalone else 0) +
                        (0.3 if itype == 'finding' else 0.2) +
                        (0.2 if any(w in line_lower for w in ['novel', 'first', 'new', 'significant']) else 0) +
                        (0.2 if len(words) >= 10 else 0.1)
                    ))

                    candidates.append(InsightCandidate(
                        text=stripped[:250],
                        section=current_section,
                        insight_type=itype,
                        quotability_score=round(quotability, 2),
                        standalone=standalone
                    ))
                    break

    candidates.sort(key=lambda c: c.quotability_score, reverse=True)
    return candidates[:max_insights]


def generate_insight_report(insights: List[InsightCandidate]) -> str:
    """Generate a distilled insights report.

    Args:
        insights: Output of distill_key_insights

    Returns:
        Formatted markdown report
    """
    lines = ["# Distilled Insights Report\n"]
    lines.append(f"## {len(insights)} key insights extracted\n")

    for i, ins in enumerate(insights, 1):
        lines.append(f"### {i}. [{ins.insight_type.upper()}] (score: {ins.quotability_score})")
        lines.append(f"> {ins.text}")
        lines.append(f"- Section: {ins.section}")
        lines.append(f"- Standalone quotable: {'Yes' if ins.standalone else 'No'}\n")

    return "\n".join(lines)


# ─── ArgumentLoadTester functions ───

def extract_argument_chain(text: str) -> List[ArgumentLink]:
    """Extract the chain of arguments (claims supporting claims).

    Args:
        text: Full manuscript text

    Returns:
        List of ArgumentLink with claim, supports, link_type, strength
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chain = []
    prev_claim = None

    connective_map = {
        'logical': ['therefore', 'thus', 'hence', 'consequently',
                    'it follows', 'this means'],
        'empirical': ['our experiments show', 'results confirm',
                     'table shows', 'figure demonstrates'],
        'analogical': ['similarly', 'analogous to', 'like',
                      'in the same way', 'just as'],
        'authoritative': ['according to', 'as shown by', 'prior work',
                         'previous studies']
    }

    for sent in sentences:
        sent_lower = sent.lower().strip()
        if len(sent_lower) < 20:
            continue

        link_type = None
        for ltype, connectives in connective_map.items():
            if any(c in sent_lower for c in connectives):
                link_type = ltype
                break

        if link_type and prev_claim:
            strength = {'logical': 0.9, 'empirical': 0.95,
                       'analogical': 0.6, 'authoritative': 0.7}.get(link_type, 0.5)
            chain.append(ArgumentLink(
                claim=sent.strip()[:200],
                supports=prev_claim[:200],
                link_type=link_type,
                strength=strength
            ))

        # Track claims for chain building
        claim_markers = ['we argue', 'we claim', 'we show', 'our results',
                        'we find', 'we propose']
        if any(m in sent_lower for m in claim_markers):
            prev_claim = sent.strip()

    return chain


def test_argument_robustness(chain: List[ArgumentLink]) -> Dict:
    """Test the robustness of the argument chain.

    Args:
        chain: Output of extract_argument_chain

    Returns:
        Dict with chain_length, weakest_link, overall_strength, gaps
    """
    if not chain:
        return {"chain_length": 0, "weakest_link": None,
                "overall_strength": 0, "gaps": ["No argument chain detected"]}

    strengths = [link.strength for link in chain]
    weakest_idx = strengths.index(min(strengths))

    gaps = []
    for link in chain:
        if link.strength < 0.7:
            gaps.append({
                "claim": link.claim[:80],
                "link_type": link.link_type,
                "strength": link.strength,
                "issue": f"Weak {link.link_type} link (strength {link.strength})"
            })

    type_counts = Counter(link.link_type for link in chain)
    if type_counts.get('authoritative', 0) > len(chain) * 0.5:
        gaps.append({
            "claim": "Overall",
            "link_type": "authoritative",
            "strength": 0.5,
            "issue": "Over-reliance on authority rather than empirical evidence"
        })

    overall = sum(strengths) / len(strengths)

    return {
        "chain_length": len(chain),
        "weakest_link": {
            "index": weakest_idx,
            "claim": chain[weakest_idx].claim[:80],
            "strength": chain[weakest_idx].strength
        },
        "overall_strength": round(overall, 2),
        "link_type_distribution": dict(type_counts),
        "gaps": gaps,
        "verdict": "ROBUST" if overall > 0.8 else "MODERATE" if overall > 0.6 else "FRAGILE"
    }


# ─── CanonicalCoreExtractor functions ───

def extract_canonical_core(text: str) -> Dict:
    """Extract the absolute core of the paper in minimal form.

    Args:
        text: Full manuscript text

    Returns:
        Dict with core_claim, core_method, core_result, core_contribution
    """
    def find_first_match(markers: List[str]) -> Optional[str]:
        for line in text.split('\n'):
            line_lower = line.lower().strip()
            for marker in markers:
                if marker in line_lower and len(line.strip()) > 30:
                    return line.strip()[:300]
        return None

    core = {
        "core_claim": find_first_match([
            'we propose', 'we introduce', 'this paper presents',
            'we present', 'our approach'
        ]) or "No core claim detected",
        "core_method": find_first_match([
            'our method', 'our approach', 'we design', 'our framework',
            'our algorithm', 'our model'
        ]) or "No core method detected",
        "core_result": find_first_match([
            'our results show', 'we achieve', 'outperforms',
            'state-of-the-art', 'improvement of'
        ]) or "No core result detected",
        "core_contribution": find_first_match([
            'contribution', 'we contribute', 'our contribution',
            'this work contributes'
        ]) or "No core contribution detected"
    }

    completeness = sum(1 for v in core.values() if "No core" not in v) / 4
    core["completeness_score"] = round(completeness, 2)
    core["verdict"] = ("COMPLETE" if completeness >= 0.75
                       else "PARTIAL" if completeness >= 0.5
                       else "INCOMPLETE")

    return core


def generate_one_page_summary(core: Dict, text: str) -> str:
    """Generate a one-page summary from the canonical core.

    Args:
        core: Output of extract_canonical_core
        text: Full manuscript text (for additional context)

    Returns:
        Formatted one-page summary as markdown
    """
    lines = ["# One-Page Summary\n"]
    lines.append(f"**Completeness:** {core.get('completeness_score', 0)} "
                 f"({core.get('verdict', 'UNKNOWN')})\n")

    sections = [
        ("Core Claim", "core_claim"),
        ("Method", "core_method"),
        ("Key Result", "core_result"),
        ("Contribution", "core_contribution")
    ]

    for title, key in sections:
        lines.append(f"## {title}")
        lines.append(f"{core.get(key, 'Not detected')}\n")

    return "\n".join(lines)
