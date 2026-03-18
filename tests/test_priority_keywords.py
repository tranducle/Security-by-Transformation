"""Tests for priority keyword routing in router.py.

These tests verify that the priority keywords added in experiments #2-10
correctly override semantic SOP matching and direct keyword matching.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.langgraph.nodes.router import route_request


class TestPriorityKeywordRouting(unittest.TestCase):
    """Verify that priority keywords resolve to correct agents."""

    # Exp#2 priority keywords
    def test_ttest_routes_to_statistician(self):
        _, agent, _ = route_request("analyze data with t-test")
        self.assertEqual(agent, "StatisticalAnalyst")

    def test_anova_routes_to_statistician(self):
        _, agent, _ = route_request("run anova significance test")
        self.assertEqual(agent, "StatisticalAnalyst")

    def test_pvalue_routes_to_statistician(self):
        _, agent, _ = route_request("check the p-value of my results")
        self.assertEqual(agent, "StatisticalAnalyst")

    def test_brainstorm_routes_to_facilitator(self):
        _, agent, _ = route_request("brainstorm ideas for my thesis")
        self.assertEqual(agent, "BrainstormingFacilitator")

    def test_abstract_routes_to_generator(self):
        _, agent, _ = route_request("write paper abstract for my study")
        self.assertEqual(agent, "AbstractTitleGenerator")

    # Exp#7 priority keywords
    def test_docx_routes_to_converter(self):
        _, agent, _ = route_request("convert my docx file to markdown")
        self.assertEqual(agent, "FileToMarkdownConverter")

    def test_harsh_routes_to_harsh_reviewer(self):
        _, agent, _ = route_request("simulate harsh reviewer feedback")
        self.assertEqual(agent, "HarshReviewer")

    def test_visualize_results_routes_to_visualizer(self):
        _, agent, _ = route_request("visualize my experiment results")
        self.assertEqual(agent, "ResultVisualizer")

    def test_research_gap_routes_to_gapscout(self):
        _, agent, _ = route_request("find research gap in this field")
        self.assertEqual(agent, "GapScout")

    # Exp#10 priority keywords
    def test_debug_routes_to_coder(self):
        _, agent, _ = route_request("debug my pytorch training loop")
        self.assertEqual(agent, "CoderReproAgent")

    def test_daily_summary_routes_to_summarizer(self):
        _, agent, _ = route_request("create daily research summary")
        self.assertEqual(agent, "DailySummarizer")

    def test_proof_routes_to_math_auditor(self):
        _, agent, _ = route_request("check this proof for errors")
        self.assertEqual(agent, "MathProofAuditor")


class TestPriorityOverridesSemanticSOP(unittest.TestCase):
    """Verify priority keywords take precedence over SOP semantic matching."""

    def test_brainstorm_not_sop(self):
        """brainstorm should go to BrainstormingFacilitator, not SOP_IDEATION_SESSION."""
        _, agent, _ = route_request("brainstorm research ideas")
        self.assertNotIn("SOP", agent)
        self.assertEqual(agent, "BrainstormingFacilitator")

    def test_ttest_not_sop(self):
        """t-test should go to StatisticalAnalyst, not SOP_QUANT_EXPERIMENT."""
        _, agent, _ = route_request("I need to run a t-test on my data")
        self.assertNotIn("SOP", agent)
        self.assertEqual(agent, "StatisticalAnalyst")

    def test_debug_not_sop(self):
        """debug should go to CoderReproAgent, not SOP_CODE_IMPLEMENTATION."""
        _, agent, _ = route_request("debug this python script")
        self.assertNotIn("SOP", agent)
        self.assertEqual(agent, "CoderReproAgent")


if __name__ == "__main__":
    unittest.main()
