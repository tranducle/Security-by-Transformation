"""Tests for analysis tools."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.tools.analysis_tools import (
    calculate_descriptive_stats,
    independent_t_test,
    correlation,
    generate_stats_report,
    StatResult,
)


class TestCalculateDescriptiveStats(unittest.TestCase):
    """Tests for calculate_descriptive_stats function."""

    def test_basic_stats(self):
        """Test basic statistical calculation."""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = calculate_descriptive_stats(data)
        self.assertEqual(result["n"], 5)
        self.assertEqual(result["mean"], 3.0)
        self.assertEqual(result["median"], 3.0)
        self.assertEqual(result["min"], 1.0)
        self.assertEqual(result["max"], 5.0)

    def test_single_element(self):
        """Test with single element array."""
        data = [5.0]
        result = calculate_descriptive_stats(data)
        self.assertEqual(result["n"], 1)
        self.assertEqual(result["mean"], 5.0)
        self.assertEqual(result["std"], 0.0)

    def test_empty_array(self):
        """Test with empty array returns empty dict."""
        data = []
        result = calculate_descriptive_stats(data)
        self.assertEqual(result, {})

    def test_negative_values(self):
        """Test with negative values."""
        data = [-2.0, -1.0, 0.0, 1.0, 2.0]
        result = calculate_descriptive_stats(data)
        self.assertEqual(result["mean"], 0.0)
        self.assertEqual(result["min"], -2.0)
        self.assertEqual(result["max"], 2.0)


class TestIndependentTTest(unittest.TestCase):
    """Tests for independent_t_test function."""

    def test_significant_difference(self):
        """Test with significantly different groups."""
        group1 = [10.0, 12.0, 14.0, 16.0, 18.0]
        group2 = [20.0, 22.0, 24.0, 26.0, 28.0]
        result = independent_t_test(group1, group2)
        self.assertIsInstance(result, StatResult)
        self.assertEqual(result.test_name, "Independent Samples t-test")
        self.assertIsInstance(result.statistic, float)
        self.assertIsInstance(result.p_value, float)
        self.assertLess(result.p_value, 0.05)  # Significant difference

    def test_no_significant_difference(self):
        """Test with similar groups."""
        group1 = [10.0, 11.0, 12.0, 13.0, 14.0]
        group2 = [10.5, 11.5, 12.5, 13.5, 14.5]
        result = independent_t_test(group1, group2, alpha=0.001)
        self.assertIsInstance(result, StatResult)
        # These groups are similar, should not be significant at very low alpha
        self.assertGreater(result.p_value, 0.001)

    def test_empty_group_raises_error(self):
        """Test that empty group raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            independent_t_test([], [1.0, 2.0])
        self.assertIn("at least one element", str(ctx.exception))

    def test_single_element_raises_error(self):
        """Test that single element group raises ValueError (need variance)."""
        with self.assertRaises(ValueError) as ctx:
            independent_t_test([1.0], [2.0, 3.0])
        self.assertIn("at least 2 elements", str(ctx.exception))

    def test_both_groups_empty_raises_error(self):
        """Test that both empty groups raises ValueError."""
        with self.assertRaises(ValueError):
            independent_t_test([], [])

    def test_result_to_dict(self):
        """Test StatResult.to_dict() method."""
        group1 = [1.0, 2.0, 3.0]
        group2 = [4.0, 5.0, 6.0]
        result = independent_t_test(group1, group2)
        result_dict = result.to_dict()
        self.assertIn("test_name", result_dict)
        self.assertIn("statistic", result_dict)
        self.assertIn("p_value", result_dict)


class TestCorrelation(unittest.TestCase):
    """Tests for correlation function."""

    def test_perfect_positive_correlation(self):
        """Test with perfectly correlated data."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.0, 4.0, 6.0, 8.0, 10.0]
        r, p = correlation(x, y)
        self.assertAlmostEqual(r, 1.0, places=5)

    def test_perfect_negative_correlation(self):
        """Test with negatively correlated data."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [10.0, 8.0, 6.0, 4.0, 2.0]
        r, p = correlation(x, y)
        self.assertAlmostEqual(r, -1.0, places=5)

    def test_no_correlation_constant(self):
        """Test with constant data (undefined correlation)."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [5.0, 5.0, 5.0, 5.0, 5.0]
        r, p = correlation(x, y)
        # With constant data, correlation should be 0 (or handled gracefully)
        self.assertIsInstance(r, float)

    def test_empty_arrays_raises_error(self):
        """Test that empty arrays raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            correlation([], [])
        self.assertIn("3 data points", str(ctx.exception))

    def test_single_element_raises_error(self):
        """Test that less than 3 elements raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            correlation([1.0, 2.0], [2.0, 3.0])
        self.assertIn("3 data points", str(ctx.exception))

    def test_unequal_lengths(self):
        """Test with unequal length arrays."""
        x = [1.0, 2.0, 3.0]
        y = [1.0, 2.0]
        with self.assertRaises(ValueError):
            correlation(x, y)


class TestGenerateStatsReport(unittest.TestCase):
    """Tests for generate_stats_report function."""

    def test_report_generation(self):
        """Test basic report generation."""
        data = {
            "group1": [1.0, 2.0, 3.0, 4.0, 5.0],
            "group2": [2.0, 3.0, 4.0, 5.0, 6.0],
        }
        report = generate_stats_report(data)
        self.assertIn("# Statistical Analysis Report", report)
        self.assertIn("Descriptive Statistics", report)

    def test_empty_data(self):
        """Test with empty data dictionary."""
        report = generate_stats_report({})
        self.assertIsNotNone(report)


if __name__ == "__main__":
    unittest.main()