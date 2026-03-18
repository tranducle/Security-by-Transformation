"""
Ablation & Error Analysis Tools
Analyze ablation study coverage and mine error taxonomies.
Used by: AblationCoverageOracle, ErrorTaxonomyMiner
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from collections import Counter


@dataclass
class MethodComponent:
    name: str
    component_type: str  # module, preprocessing, loss, augmentation, hyperparameter
    is_core: bool
    description: str


@dataclass
class AblationEntry:
    removed_component: str
    result_change: Optional[float]  # % change
    is_meaningful: bool


@dataclass
class ErrorCase:
    error_id: str
    input_description: str
    expected: str
    actual: str
    error_type: str  # false_positive, false_negative, edge_case, etc.


# ─── AblationCoverageOracle functions ───

def decompose_method_components(method_description: str) -> List[MethodComponent]:
    """Decompose a method description into testable components.

    Args:
        method_description: Text describing the proposed method

    Returns:
        List of MethodComponent with name, type, is_core, description
    """
    component_markers = {
        'module': ['module', 'layer', 'encoder', 'decoder', 'head',
                  'backbone', 'network', 'block', 'branch'],
        'preprocessing': ['preprocessing', 'augmentation', 'normalization',
                         'tokenization', 'embedding', 'feature extraction'],
        'loss': ['loss function', 'objective', 'criterion', 'regularization',
                'penalty', 'constraint'],
        'hyperparameter': ['learning rate', 'dropout', 'batch size',
                          'temperature', 'threshold', 'weight decay'],
        'design': ['attention', 'skip connection', 'residual', 'pooling',
                  'aggregation', 'fusion', 'concatenation']
    }

    components = []
    desc_lower = method_description.lower()
    seen = set()

    for comp_type, markers in component_markers.items():
        for marker in markers:
            if marker in desc_lower and marker not in seen:
                seen.add(marker)
                # Find the sentence containing this marker
                for sent in re.split(r'[.!?]\s+', method_description):
                    if marker in sent.lower():
                        components.append(MethodComponent(
                            name=marker.title(),
                            component_type=comp_type,
                            is_core=(comp_type in ['module', 'loss', 'design']),
                            description=sent.strip()[:150]
                        ))
                        break

    return components


def assess_ablation_coverage(
    components: List[MethodComponent],
    ablations: List[AblationEntry]
) -> Dict:
    """Assess how well ablation study covers method components.

    Args:
        components: Output of decompose_method_components
        ablations: List of ablation experiments conducted

    Returns:
        Dict with coverage_matrix, coverage_score, missing_ablations
    """
    ablated_names = {a.removed_component.lower() for a in ablations}
    coverage = []
    missing = []

    for comp in components:
        covered = comp.name.lower() in ablated_names or \
                  any(comp.name.lower() in a for a in ablated_names)
        coverage.append({
            "component": comp.name,
            "type": comp.component_type,
            "is_core": comp.is_core,
            "covered": covered,
            "priority": "CRITICAL" if comp.is_core and not covered else
                       "HIGH" if not covered else "COVERED"
        })
        if not covered:
            missing.append({
                "component": comp.name,
                "type": comp.component_type,
                "is_core": comp.is_core,
                "reviewer_likelihood": "HIGH" if comp.is_core else "MEDIUM",
                "suggested_experiment": f"Remove/replace {comp.name}, measure impact"
            })

    total = len(components)
    covered_count = sum(1 for c in coverage if c["covered"])

    return {
        "coverage_matrix": coverage,
        "coverage_score": round(covered_count / max(total, 1) * 100, 1),
        "total_components": total,
        "covered_components": covered_count,
        "missing_ablations": missing,
        "interaction_tested": False  # Flag: are component interactions tested?
    }


def detect_missing_ablations(
    components: List[MethodComponent],
    ablations: List[AblationEntry]
) -> List[Dict]:
    """Detect ablations that are performative rather than informative,
    plus missing ablations for core components.

    Args:
        components: Output of decompose_method_components
        ablations: List of ablation experiments conducted

    Returns:
        List of issues with component, issue, severity, suggestion
    """
    flags = []
    ablated_names = {a.removed_component.lower() for a in ablations}

    # Check for missing core ablations
    for comp in components:
        if comp.is_core and comp.name.lower() not in ablated_names:
            flags.append({
                "component": comp.name,
                "issue": f"Core component '{comp.name}' has no ablation study",
                "severity": "CRITICAL",
                "suggestion": f"Remove/replace {comp.name} and measure impact on all metrics"
            })

    # Check for trivial ablations
    for abl in ablations:
        change = abs(abl.result_change) if abl.result_change is not None else 0
        if change < 0.1:
            flags.append({
                "component": abl.removed_component,
                "issue": f"Removing '{abl.removed_component}' changes result by <0.1% — trivial ablation",
                "severity": "MEDIUM",
                "suggestion": "Replace with ablation of a component that actually matters"
            })

    # Check for suspiciously perfect ablations
    if len(ablations) > 3:
        all_negative = all(
            (a.result_change or 0) < 0 for a in ablations
        )
        if all_negative:
            flags.append({
                "component": "ALL",
                "issue": "Every ablation hurts performance — suspiciously perfect",
                "severity": "HIGH",
                "suggestion": "Include at least one component that doesn't help"
            })

    return flags


# ─── ErrorTaxonomyMiner functions ───

def build_error_taxonomy(
    errors: List[Dict]
) -> Dict:
    """Build a hierarchical error taxonomy from error cases.

    Args:
        errors: List of dicts with error_type, input, expected, actual

    Returns:
        Dict with taxonomy tree, statistics, mermaid diagram
    """
    # Cluster by error_type
    clusters: Dict[str, List[Dict]] = {}
    for error in errors:
        key = error.get("error_type", "unknown")
        if key not in clusters:
            clusters[key] = []
        clusters[key].append(error)

    taxonomy = {"name": "All Errors", "children": []}
    total = len(errors)

    for cluster_name, cluster_errors in clusters.items():
        node = {
            "name": cluster_name,
            "count": len(cluster_errors),
            "percentage": round(len(cluster_errors) / max(total, 1) * 100, 1),
            "examples": [str(e.get("input", ""))[:80] for e in cluster_errors[:3]],
            "design_implication": f"Address {cluster_name} errors through targeted improvement"
        }
        taxonomy["children"].append(node)

    # Build mermaid
    mermaid_lines = ["graph TD"]
    mermaid_lines.append(f'    ROOT["All Errors (n={total})"]')
    for child in taxonomy["children"]:
        safe_name = child["name"].replace(" ", "_")
        mermaid_lines.append(
            f'    ROOT --> {safe_name}["{child["name"]} ({child["count"]}, {child["percentage"]}%)"]'
        )

    return {
        "taxonomy": taxonomy,
        "total_errors": total,
        "cluster_count": len(clusters),
        "mermaid_diagram": "\n".join(mermaid_lines)
    }


def map_error_to_component(
    errors: List[Dict],
    components: List[MethodComponent]
) -> List[Dict]:
    """Map errors to the method components most likely responsible.

    Args:
        errors: List of error dicts with error_type, input, description
        components: Output of decompose_method_components

    Returns:
        List of mappings with error_id, likely_component, confidence, reasoning
    """
    mappings = []

    for i, error in enumerate(errors):
        error_desc = str(error.get("input", "")) + " " + str(error.get("actual", ""))
        error_lower = error_desc.lower()

        best_comp = None
        best_score = 0

        for comp in components:
            # Simple keyword overlap scoring
            comp_words = set(comp.name.lower().split()) | set(comp.description.lower().split())
            error_words = set(error_lower.split())
            overlap = len(comp_words & error_words)

            if overlap > best_score:
                best_score = overlap
                best_comp = comp

        if best_comp:
            mappings.append({
                "error_index": i,
                "error_type": error.get("error_type", "unknown"),
                "likely_component": best_comp.name,
                "component_type": best_comp.component_type,
                "confidence": min(best_score / 5, 1.0),
                "reasoning": f"Keyword overlap between error and {best_comp.name} description"
            })
        else:
            mappings.append({
                "error_index": i,
                "error_type": error.get("error_type", "unknown"),
                "likely_component": "Unknown",
                "component_type": "unknown",
                "confidence": 0.0,
                "reasoning": "No component matched error description"
            })

    return mappings


def generate_ablation_report(
    coverage: Dict,
    error_taxonomy: Optional[Dict] = None,
    missing_ablations: Optional[List[Dict]] = None
) -> str:
    """Generate a comprehensive ablation & error analysis report.

    Args:
        coverage: Output of assess_ablation_coverage
        error_taxonomy: Optional output of build_error_taxonomy
        missing_ablations: Optional output of detect_missing_ablations

    Returns:
        Formatted markdown report string
    """
    lines = ["# Ablation & Error Analysis Report\n"]

    # Coverage Summary
    lines.append("## Ablation Coverage Summary\n")
    score = coverage.get("coverage_score", 0)
    total = coverage.get("total_components", 0)
    covered = coverage.get("covered_components", 0)
    lines.append(f"- **Coverage Score:** {score}% ({covered}/{total} components)\n")

    # Missing Ablations
    missing = coverage.get("missing_ablations", [])
    if missing:
        lines.append("## Missing Ablations\n")
        lines.append("| Component | Type | Core? | Priority | Suggestion |")
        lines.append("|-----------|------|-------|----------|------------|")
        for m in missing:
            lines.append(
                f"| {m['component']} | {m['type']} | {m['is_core']} | "
                f"{m['reviewer_likelihood']} | {m['suggested_experiment']} |"
            )
        lines.append("")

    # Issues from detect_missing_ablations
    if missing_ablations:
        lines.append("## Ablation Issues\n")
        for issue in missing_ablations:
            sev = issue.get("severity", "MEDIUM")
            lines.append(f"- **[{sev}]** {issue['issue']}")
            lines.append(f"  - Suggestion: {issue['suggestion']}\n")

    # Error Taxonomy
    if error_taxonomy:
        lines.append("## Error Taxonomy\n")
        lines.append(f"- **Total Errors:** {error_taxonomy.get('total_errors', 0)}")
        lines.append(f"- **Clusters:** {error_taxonomy.get('cluster_count', 0)}\n")
        if "mermaid_diagram" in error_taxonomy:
            lines.append("```mermaid")
            lines.append(error_taxonomy["mermaid_diagram"])
            lines.append("```\n")

    return "\n".join(lines)
