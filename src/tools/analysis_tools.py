"""
Analysis and Statistics Tools
Tools for data analysis, statistical tests, and metrics.
"""

import json
import logging
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

# Try to import scipy for accurate statistical functions
try:
    from scipy import stats as scipy_stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    logger.warning("scipy not available, using approximate statistical functions")


@dataclass  
class StatResult:
    """Result of a statistical test."""
    test_name: str
    statistic: float
    p_value: float
    effect_size: Optional[float] = None
    conclusion: str = ""
    details: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_name": self.test_name,
            "statistic": self.statistic,
            "p_value": self.p_value,
            "effect_size": self.effect_size,
            "conclusion": self.conclusion,
            "details": self.details or {},
        }
    
    def to_markdown(self) -> str:
        sig = "✅ Significant" if self.p_value < 0.05 else "❌ Not Significant"
        effect = f", Effect Size: {self.effect_size:.3f}" if self.effect_size else ""
        return f"**{self.test_name}**: {self.statistic:.4f} (p={self.p_value:.4f}{effect}) → {sig}"


def calculate_descriptive_stats(data: List[float]) -> Dict[str, float]:
    """
    Calculate descriptive statistics for a list of numbers.
    
    Args:
        data: List of numeric values
    
    Returns:
        Dictionary with n, mean, std, min, max, median
    """
    if not data:
        return {}
    
    n = len(data)
    mean = sum(data) / n
    
    # Variance and std
    variance = sum((x - mean) ** 2 for x in data) / (n - 1) if n > 1 else 0
    std = variance ** 0.5
    
    # Sorted for median and quartiles
    sorted_data = sorted(data)
    
    if n % 2 == 0:
        median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        median = sorted_data[n//2]
    
    return {
        "n": n,
        "mean": mean,
        "std": std,
        "min": sorted_data[0],
        "max": sorted_data[-1],
        "median": median,
    }


def independent_t_test(
    group1: List[float],
    group2: List[float],
    alpha: float = 0.05,
) -> StatResult:
    """
    Perform independent samples t-test.
    
    Args:
        group1: First group data
        group2: Second group data
        alpha: Significance level
    
    Returns:
        StatResult with t-statistic, p-value, effect size (Cohen's d)

    Raises:
        ValueError: If groups are empty or have insufficient data
    """
    # Input validation - prevent division by zero
    if not group1 or not group2:
        raise ValueError("Both groups must have at least one element")
    if len(group1) < 2 or len(group2) < 2:
        raise ValueError(
            "Both groups must have at least 2 elements for variance calculation. "
            f"Got group1={len(group1)} elements, group2={len(group2)} elements"
        )

    n1, n2 = len(group1), len(group2)
    mean1 = sum(group1) / n1
    mean2 = sum(group2) / n2
    
    var1 = sum((x - mean1) ** 2 for x in group1) / (n1 - 1)
    var2 = sum((x - mean2) ** 2 for x in group2) / (n2 - 1)
    
    # Pooled standard error
    se = ((var1 / n1) + (var2 / n2)) ** 0.5
    
    # t-statistic
    t_stat = (mean1 - mean2) / se if se > 0 else 0
    
    # Degrees of freedom (Welch-Satterthwaite)
    df = ((var1/n1 + var2/n2)**2) / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))
    
    # Cohen's d
    pooled_std = (((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2)) ** 0.5
    cohens_d = abs(mean1 - mean2) / pooled_std if pooled_std > 0 else 0

    # Calculate p-value - use scipy for accuracy if available
    if HAS_SCIPY:
        # Use Welch's t-test from scipy for accurate p-values
        scipy_result = scipy_stats.ttest_ind(group1, group2, equal_var=False)
        p_value = scipy_result.pvalue
        t_stat = scipy_result.statistic
        df = scipy_result.df if hasattr(scipy_result, 'df') else df
    else:
        # Fallback to approximation (less accurate for small samples)
        p_value = 2 * (1 - _t_cdf_approx(abs(t_stat), df))
    
    significant = p_value < alpha
    conclusion = f"{'Reject' if significant else 'Fail to reject'} null hypothesis at α={alpha}"
    
    return StatResult(
        test_name="Independent Samples t-test",
        statistic=t_stat,
        p_value=p_value,
        effect_size=cohens_d,
        conclusion=conclusion,
        details={"df": df, "mean1": mean1, "mean2": mean2, "n1": n1, "n2": n2},
    )


def _t_cdf_approx(t: float, df: float) -> float:
    """
    Calculate t-distribution CDF.

    Uses scipy.stats for accuracy when available, otherwise falls back
    to normal approximation for large df or rough approximation for small df.

    Args:
        t: t-statistic value
        df: degrees of freedom

    Returns:
        CDF value (probability P(T <= t))
    """
    if HAS_SCIPY:
        # Use scipy for accurate calculation
        return scipy_stats.t.cdf(t, df)

    # Fallback: Use normal approximation for large df
    if df > 30:
        from math import erf
        return 0.5 * (1 + erf(t / 2**0.5))
    # Rough approximation for small df (less accurate)
    x = df / (df + t**2)
    return 0.5 + 0.5 * (1 - x**(df/2)) * (1 if t > 0 else -1)


def correlation(x: List[float], y: List[float]) -> Tuple[float, float]:
    """
    Calculate Pearson correlation coefficient.

    Args:
        x: First variable
        y: Second variable

    Returns:
        Tuple of (correlation coefficient r, p-value)

    Raises:
        ValueError: If inputs have different lengths or insufficient data
    """
    n = len(x)
    if n != len(y):
        raise ValueError(f"x and y must have same length. Got x={n}, y={len(y)}")
    if n < 3:
        raise ValueError(f"Need at least 3 data points for correlation. Got {n}")

    # Use scipy for accurate calculation if available
    if HAS_SCIPY:
        r, p_value = scipy_stats.pearsonr(x, y)
        return r, p_value

    # Fallback: manual calculation
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denom_x = sum((xi - mean_x) ** 2 for xi in x) ** 0.5
    denom_y = sum((yi - mean_y) ** 2 for yi in y) ** 0.5

    if denom_x * denom_y == 0:
        logger.warning("Constant data detected - correlation undefined")
        return 0.0, 1.0

    r = numerator / (denom_x * denom_y)

    # t-test for correlation significance
    t = r * ((n - 2) / (1 - r**2)) ** 0.5 if abs(r) < 1 else 0
    p_value = 2 * (1 - _t_cdf_approx(abs(t), n - 2))

    return r, p_value
    p_value = 2 * (1 - _t_cdf_approx(abs(t), n - 2))
    
    return r, p_value


def generate_stats_report(
    data: Dict[str, List[float]],
    comparisons: List[Tuple[str, str]] = None,
) -> str:
    """
    Generate a markdown statistics report.
    
    Args:
        data: Dictionary mapping variable names to data lists
        comparisons: Optional list of (var1, var2) pairs to compare
    
    Returns:
        Markdown formatted report
    """
    lines = ["# Statistical Analysis Report\n"]
    
    # Descriptive statistics
    lines.append("## Descriptive Statistics\n")
    lines.append("| Variable | N | Mean | SD | Min | Max | Median |")
    lines.append("|----------|---|------|----|----|-----|--------|")
    
    for var_name, values in data.items():
        stats = calculate_descriptive_stats(values)
        lines.append(
            f"| {var_name} | {stats['n']} | {stats['mean']:.2f} | "
            f"{stats['std']:.2f} | {stats['min']:.2f} | {stats['max']:.2f} | "
            f"{stats['median']:.2f} |"
        )
    
    # Comparisons
    if comparisons:
        lines.append("\n## Group Comparisons\n")
        for var1, var2 in comparisons:
            if var1 in data and var2 in data:
                result = independent_t_test(data[var1], data[var2])
                lines.append(f"### {var1} vs {var2}")
                lines.append(result.to_markdown())
                lines.append("")
    
    return "\n".join(lines)


# Tool metadata for agent integration
ANALYSIS_TOOLS = [
    {
        "name": "calculate_descriptive_stats",
        "description": "Calculate descriptive statistics (mean, std, median, etc.) for numeric data.",
        "function": calculate_descriptive_stats,
        "parameters": [
            {"name": "data", "type": "array", "description": "List of numbers", "required": True},
        ],
    },
    {
        "name": "independent_t_test",
        "description": "Perform independent samples t-test between two groups.",
        "function": independent_t_test,
        "parameters": [
            {"name": "group1", "type": "array", "description": "First group data", "required": True},
            {"name": "group2", "type": "array", "description": "Second group data", "required": True},
            {"name": "alpha", "type": "number", "description": "Significance level", "required": False, "default": 0.05},
        ],
    },
    {
        "name": "correlation",
        "description": "Calculate Pearson correlation coefficient between two variables.",
        "function": correlation,
        "parameters": [
            {"name": "x", "type": "array", "description": "First variable", "required": True},
            {"name": "y", "type": "array", "description": "Second variable", "required": True},
        ],
    },
    {
        "name": "generate_stats_report",
        "description": "Generate a markdown statistics report from data.",
        "function": generate_stats_report,
        "parameters": [
            {"name": "data", "type": "object", "description": "Dict of variable names to data arrays", "required": True},
            {"name": "comparisons", "type": "array", "description": "List of (var1, var2) pairs to compare", "required": False},
        ],
    },
]
