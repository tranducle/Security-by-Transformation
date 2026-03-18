"""
Metric & Operationalization Tools
Detect gaps between theoretical constructs and their measured proxies.
Used by: MetricSemanticsAuditor, OperationalizationGapDetector, SOTAInflationDetector
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class MetricUsage:
    metric_name: str
    section: str
    context: str
    is_primary: bool


@dataclass
class ConceptMetricPair:
    concept: str
    metric: str
    validity: str  # STRONG, MODERATE, WEAK, MISSING
    explanation: str


@dataclass
class OperationalizationGap:
    concept: str
    issue: str
    severity: str
    suggestion: str


# ─── MetricSemanticsAuditor functions ───

def extract_metrics_used(text: str) -> List[MetricUsage]:
    """Extract all evaluation metrics mentioned in the manuscript.

    Detects common ML/stats metrics and their usage context.

    Args:
        text: Full manuscript text

    Returns:
        List of MetricUsage with metric_name, section, context, is_primary
    """
    known_metrics = [
        'accuracy', 'precision', 'recall', 'f1', 'f1-score', 'f-measure',
        'auc', 'roc', 'auroc', 'auprc', 'map', 'ndcg', 'mrr',
        'mse', 'rmse', 'mae', 'mape', 'r-squared', 'r²',
        'bleu', 'rouge', 'meteor', 'perplexity', 'fid',
        "cohen's kappa", 'cronbach', 'icc',
        'p-value', 'effect size', "cohen's d", 'odds ratio'
    ]

    results = []
    current_section = "Unknown"

    for line in text.split('\n'):
        if re.match(r'^#{1,3}\s+', line) or re.match(r'^\\(sub)?section\{', line):
            current_section = re.sub(r'^#{1,3}\s+|^\\(sub)?section\{|\}$', '', line).strip()
            continue

        line_lower = line.lower()
        for metric in known_metrics:
            if metric in line_lower:
                is_primary = any(w in line_lower for w in
                               ['primary', 'main metric', 'we use', 'evaluated using',
                                'measured by', 'key metric'])
                results.append(MetricUsage(
                    metric_name=metric,
                    section=current_section,
                    context=line.strip()[:150],
                    is_primary=is_primary
                ))

    return results


def audit_metric_semantics(
    metrics: List[MetricUsage],
    task_type: str = "classification"
) -> List[Dict]:
    """Check if metrics are semantically appropriate for the task.

    Args:
        metrics: List of MetricUsage from extract_metrics_used
        task_type: classification, regression, generation, ranking, etc.

    Returns:
        List of dicts with metric, appropriate (bool), reason, suggestion
    """
    appropriateness = {
        "classification": {
            "good": ["f1", "precision", "recall", "auc", "auroc", "cohen's kappa"],
            "caution": ["accuracy"],
            "bad": ["mse", "rmse", "mae", "bleu", "rouge"]
        },
        "regression": {
            "good": ["mse", "rmse", "mae", "r-squared", "r²", "mape"],
            "caution": [],
            "bad": ["accuracy", "f1", "precision", "recall", "auc"]
        },
        "generation": {
            "good": ["bleu", "rouge", "meteor", "perplexity", "fid"],
            "caution": ["accuracy"],
            "bad": ["mse", "rmse"]
        }
    }

    task_rules = appropriateness.get(task_type, {})
    results = []

    seen = set()
    for m in metrics:
        if m.metric_name in seen:
            continue
        seen.add(m.metric_name)

        if m.metric_name in task_rules.get("bad", []):
            results.append({
                "metric": m.metric_name, "appropriate": False,
                "reason": f"Not suitable for {task_type} tasks",
                "suggestion": f"Use: {', '.join(task_rules.get('good', [])[:3])}"
            })
        elif m.metric_name in task_rules.get("caution", []):
            results.append({
                "metric": m.metric_name, "appropriate": True,
                "reason": f"Acceptable but can be misleading for {task_type}",
                "suggestion": "Add complementary metrics for balanced view"
            })
        else:
            results.append({
                "metric": m.metric_name, "appropriate": True,
                "reason": "Appropriate for task type", "suggestion": None
            })

    return results


def detect_metric_masking(
    metrics: List[MetricUsage],
    results_text: str
) -> List[Dict]:
    """Detect when favorable metrics mask unfavorable performance.

    Args:
        metrics: List of MetricUsage
        results_text: Text from results section

    Returns:
        List of masking issues with metric, issue, severity
    """
    issues = []
    metric_names = {m.metric_name for m in metrics}

    # Check: accuracy without class-level metrics on imbalanced data
    if 'accuracy' in metric_names and not metric_names & {'f1', 'precision', 'recall'}:
        if any(w in results_text.lower() for w in ['imbalanced', 'skewed', 'rare class',
                                                     'minority']):
            issues.append({
                "metric": "accuracy",
                "issue": "Accuracy used on imbalanced data without per-class metrics",
                "severity": "CRITICAL",
                "fix": "Add F1, precision, recall per class"
            })

    # Check: only aggregate metrics, no per-class breakdown
    if any(m in metric_names for m in ['accuracy', 'f1']) and \
       'per-class' not in results_text.lower() and \
       'per class' not in results_text.lower():
        issues.append({
            "metric": "aggregate_only",
            "issue": "Only aggregate metrics reported — may hide poor performance on subgroups",
            "severity": "HIGH",
            "fix": "Add per-class or per-group breakdown"
        })

    return issues


# ─── OperationalizationGapDetector functions ───

def extract_concepts_and_metrics(text: str) -> List[ConceptMetricPair]:
    """Extract theoretical concepts and their measured proxies.

    Args:
        text: Full manuscript text

    Returns:
        List of ConceptMetricPair with concept, metric, validity, explanation
    """
    concept_indicators = ['defined as', 'conceptualized as', 'refers to',
                         'operationalized as', 'measured by', 'proxied by',
                         'captured by', 'assessed using']
    pairs = []

    for line in text.split('\n'):
        line_lower = line.lower()
        for indicator in concept_indicators:
            if indicator in line_lower:
                parts = line_lower.split(indicator)
                if len(parts) >= 2:
                    concept = parts[0].strip().split('.')[-1].strip()[:80]
                    metric = parts[1].strip().split('.')[0].strip()[:80]
                    if concept and metric:
                        pairs.append(ConceptMetricPair(
                            concept=concept,
                            metric=metric,
                            validity="MODERATE",
                            explanation=f"Found via '{indicator}'"
                        ))

    return pairs


def assess_operationalization_validity(
    pairs: List[ConceptMetricPair]
) -> List[Dict]:
    """Assess whether metrics validly capture their theoretical concepts.

    Args:
        pairs: List of concept-metric pairs

    Returns:
        List of validity assessments
    """
    results = []
    for pair in pairs:
        issues = []

        # Check for overly simplistic operationalization
        simple_metrics = ['binary', 'yes/no', 'count', 'dummy']
        if any(s in pair.metric.lower() for s in simple_metrics):
            issues.append("Simplistic binary proxy for complex construct")

        # Check for single-item measurement
        if any(w in pair.metric.lower() for w in ['single item', 'one question', 'single question']):
            issues.append("Single-item measure — low reliability")

        validity = "WEAK" if issues else "MODERATE"
        results.append({
            "concept": pair.concept,
            "metric": pair.metric,
            "validity": validity,
            "issues": issues,
            "recommendation": "Consider multi-item validated scale" if issues else "Acceptable"
        })

    return results


def generate_gap_report(
    pairs: List[ConceptMetricPair],
    validity_results: List[Dict]
) -> str:
    """Generate operationalization gap report.

    Args:
        pairs: Concept-metric pairs
        validity_results: Output of assess_operationalization_validity

    Returns:
        Formatted markdown report
    """
    weak = sum(1 for v in validity_results if v["validity"] == "WEAK")
    lines = ["# Operationalization Gap Report\n"]
    lines.append(f"## Summary: {len(pairs)} concept-metric pairs, {weak} weak\n")

    lines.append("| Concept | Metric | Validity | Issues |")
    lines.append("|---------|--------|----------|--------|")
    for v in validity_results:
        issues_str = "; ".join(v["issues"]) if v["issues"] else "—"
        lines.append(f"| {v['concept'][:30]} | {v['metric'][:30]} | "
                    f"{v['validity']} | {issues_str} |")

    return "\n".join(lines)
