"""
Deployment Assessment Tools
Evaluate deployment friction, temporal validity, and dataset provenance.
Used by: DeploymentFrictionEstimator, TemporalValidityInspector, DatasetProvenanceExaminer
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class DeploymentBarrier:
    barrier_type: str
    description: str
    severity: str
    mitigation: str


@dataclass
class TemporalEntity:
    name: str
    entity_type: str  # dataset, model, library, benchmark
    version: str
    release_year: Optional[int]
    is_stale: bool
    staleness_reason: Optional[str]


DEPLOYMENT_CHECKLIST = {
    "compute": ["GPU", "TPU", "memory", "RAM", "VRAM", "compute",
                "training time", "inference time", "latency"],
    "data": ["proprietary data", "private dataset", "licensed",
            "restricted access", "not publicly available"],
    "expertise": ["hyperparameter tuning", "architecture search",
                 "domain expertise", "manual annotation", "labeling"],
    "infrastructure": ["distributed", "cluster", "cloud", "API",
                      "deployment", "serving", "kubernetes", "docker"],
    "reproducibility": ["random seed", "reproducib", "code available",
                       "open source", "github"],
}


def score_deployment_friction(text: str) -> Dict:
    """Score how difficult it would be to deploy this research.

    Args:
        text: Full manuscript text

    Returns:
        Dict with total_score, barriers, category_scores, verdict
    """
    text_lower = text.lower()
    barriers = []
    category_scores = {}

    for category, markers in DEPLOYMENT_CHECKLIST.items():
        found = [m for m in markers if m in text_lower]
        score = len(found)
        category_scores[category] = {
            "markers_found": found,
            "friction_score": min(score, 5)
        }

        if category == "data" and found:
            barriers.append(DeploymentBarrier(
                barrier_type="DATA_ACCESS",
                description=f"Data barriers: {', '.join(found)}",
                severity="HIGH",
                mitigation="Provide synthetic data alternative or public proxy"
            ))
        if category == "compute" and len(found) >= 3:
            barriers.append(DeploymentBarrier(
                barrier_type="COMPUTE_COST",
                description="Heavy compute requirements detected",
                severity="HIGH",
                mitigation="Provide model distillation or lighter variant"
            ))

    total = sum(cs["friction_score"] for cs in category_scores.values())
    verdict = ("LOW_FRICTION" if total <= 5
               else "MODERATE_FRICTION" if total <= 10
               else "HIGH_FRICTION")

    return {
        "total_score": total,
        "max_possible": 25,
        "verdict": verdict,
        "category_scores": category_scores,
        "barriers": [{"type": b.barrier_type, "description": b.description,
                      "severity": b.severity, "mitigation": b.mitigation}
                     for b in barriers]
    }


def identify_adoption_barriers(text: str) -> List[Dict]:
    """Identify specific barriers to industry adoption.

    Args:
        text: Full manuscript text

    Returns:
        List of barrier dicts with type, evidence, severity, suggestion
    """
    barriers = []
    text_lower = text.lower()

    checks = [
        ("NO_CODE", "code avail", not any(w in text_lower for w in
         ["github", "code available", "open source", "repository"]),
         "HIGH", "Release code and trained models"),
        ("NO_BENCHMARK", "standard benchmark", not any(w in text_lower for w in
         ["benchmark", "standard dataset", "public dataset"]),
         "MEDIUM", "Evaluate on standard benchmarks"),
        ("HIGH_COMPLEXITY", "implementation complexity",
         any(w in text_lower for w in ["complex pipeline", "multi-stage",
             "requires expertise"]),
         "HIGH", "Provide simplified version or API"),
        ("LIMITED_GENERALIZATION", "domain-specific",
         any(w in text_lower for w in ["domain-specific", "only applies to",
             "limited to", "single domain"]),
         "MEDIUM", "Discuss transfer to other domains"),
    ]

    for check_type, desc, condition, severity, suggestion in checks:
        if condition:
            barriers.append({
                "type": check_type,
                "description": desc,
                "severity": severity,
                "suggestion": suggestion
            })

    return barriers


def inspect_temporal_validity(text: str) -> List[Dict]:
    """Check temporal validity of references, datasets, and models.

    Args:
        text: Full manuscript text

    Returns:
        List of temporal issues with entity, year, staleness
    """
    issues = []
    current_year = datetime.now().year

    year_refs = re.findall(r'\((?:\w+(?:\s+(?:et\s+al\.?|and|\&)\s*\w+)?,?\s*)(\d{4})\)', text)
    if year_refs:
        years = [int(y) for y in year_refs if 1990 <= int(y) <= current_year]
        if years:
            median_year = sorted(years)[len(years) // 2]
            old_refs = sum(1 for y in years if y < current_year - 5)
            if old_refs > len(years) * 0.5:
                issues.append({
                    "entity": "Reference base",
                    "type": "citations",
                    "median_year": median_year,
                    "old_percentage": round(old_refs / len(years) * 100, 1),
                    "issue": f"Median ref year {median_year}, {old_refs}/{len(years)} older than 5 years",
                    "severity": "MEDIUM",
                    "suggestion": "Add recent (2022+) references"
                })

    stale_models = ['bert-base', 'resnet-50', 'vgg', 'word2vec', 'glove',
                    'lstm', 'gru', 'alexnet']
    for model in stale_models:
        if model in text.lower():
            issues.append({
                "entity": model,
                "type": "model",
                "issue": f"Potentially outdated model: {model}",
                "severity": "LOW",
                "suggestion": "Compare with modern alternatives"
            })

    return issues


def assess_dataset_provenance(text: str) -> List[Dict]:
    """Assess licensing, versioning, and provenance of datasets.

    Args:
        text: Full manuscript text

    Returns:
        List of provenance issues
    """
    issues = []
    text_lower = text.lower()

    if not any(w in text_lower for w in ['license', 'creative commons', 'mit license',
                                          'apache', 'GPL', 'open data']):
        issues.append({
            "type": "MISSING_LICENSE",
            "issue": "No dataset license mentioned",
            "severity": "HIGH",
            "suggestion": "State the license for each dataset used"
        })

    if not any(w in text_lower for w in ['version', 'v1.', 'v2.', 'release']):
        issues.append({
            "type": "MISSING_VERSION",
            "issue": "No dataset version specified",
            "severity": "MEDIUM",
            "suggestion": "Specify exact version/release date of datasets"
        })

    if not any(w in text_lower for w in ['ethics', 'ethical', 'consent', 'privacy',
                                          'anonymiz', 'de-identif']):
        issues.append({
            "type": "MISSING_ETHICS",
            "issue": "No ethical considerations for data mentioned",
            "severity": "MEDIUM" if "patient" in text_lower or "user" in text_lower else "LOW",
            "suggestion": "Add ethical considerations for data collection"
        })

    return issues


def generate_deployment_report(
    friction: Dict,
    barriers: List[Dict],
    temporal: List[Dict],
    provenance: List[Dict]
) -> str:
    """Generate deployment readiness report.

    Args:
        friction: Output of score_deployment_friction
        barriers: Output of identify_adoption_barriers
        temporal: Output of inspect_temporal_validity
        provenance: Output of assess_dataset_provenance

    Returns:
        Formatted markdown report
    """
    lines = ["# Deployment Readiness Report\n"]
    lines.append(f"## Friction Score: {friction['total_score']}/{friction['max_possible']} "
                 f"({friction['verdict']})\n")

    if barriers:
        lines.append("## Adoption Barriers\n")
        for b in barriers:
            lines.append(f"- **{b['type']}** ({b['severity']}): {b['description']}")
            lines.append(f"  - Fix: {b['suggestion']}")

    if temporal:
        lines.append("\n## Temporal Issues\n")
        for t in temporal:
            lines.append(f"- **{t['entity']}** ({t['severity']}): {t['issue']}")

    if provenance:
        lines.append("\n## Provenance Issues\n")
        for p in provenance:
            lines.append(f"- **{p['type']}** ({p['severity']}): {p['issue']}")

    return "\n".join(lines)


def calculate_research_debt(text: str) -> Dict:
    """Calculate accumulated research debt indicators.

    Args:
        text: Full manuscript text

    Returns:
        Dict with debt_score, indicators, verdict
    """
    indicators = []
    text_lower = text.lower()

    future_work_phrases = re.findall(r'future work|future research|remains to be|left for future',
                                     text_lower)
    if len(future_work_phrases) > 3:
        indicators.append({
            "type": "EXCESSIVE_FUTURE_WORK",
            "count": len(future_work_phrases),
            "severity": "MEDIUM"
        })

    assumption_phrases = re.findall(r'we assume|assuming that|under the assumption', text_lower)
    if len(assumption_phrases) > 5:
        indicators.append({
            "type": "MANY_ASSUMPTIONS",
            "count": len(assumption_phrases),
            "severity": "HIGH"
        })

    score = sum(2 if i["severity"] == "HIGH" else 1 for i in indicators)
    return {
        "debt_score": score,
        "indicators": indicators,
        "verdict": "LOW" if score <= 2 else "MODERATE" if score <= 5 else "HIGH"
    }
