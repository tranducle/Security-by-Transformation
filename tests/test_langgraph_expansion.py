"""
Tests for new LangGraph expansion nodes:
  - validate_output_node
  - checkpoint_saver_node
  - context_compressor_node
  - sop_orchestrator_node
  - Expanded ResearchState fields
  - Conditional routing (single vs SOP)
  - Quality gate retry loop
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.langgraph.state import ResearchState, create_initial_state


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def base_state():
    """Create a base state for testing."""
    state = create_initial_state("Find papers about cybersecurity for SMEs")
    # Set up a minimal agent config for validation
    state["agent_config"] = {
        "name": "LiteratureHunter",
        "tools": ["search_openalex"],
        "output_schema": {"findings": "desc", "methodology": "desc"},
    }
    state["target_agent"] = "LiteratureHunter"
    state["target_domain"] = "Research & Discovery"
    return state


@pytest.fixture
def state_with_results(base_state):
    """State with tool results populated."""
    base_state["tool_results"] = [
        {"tool_name": "search_openalex", "status": "success", "result": {"papers": [1, 2, 3]}},
    ]
    base_state["response"] = (
        "Here are the findings from the literature search on cybersecurity for SMEs. "
        "The findings section covers recent trends. "
        "The methodology used was a systematic keyword search. " * 5
    )
    return base_state


@pytest.fixture
def state_with_empty_response(base_state):
    """State with an empty/short response — should fail validation."""
    base_state["response"] = "OK"
    base_state["tool_results"] = []
    return base_state


# ===========================================================================
# Test: ResearchState new fields
# ===========================================================================


class TestResearchStateExpansion:
    """Verify the new fields exist and have correct defaults."""

    def test_new_fields_exist(self):
        state = create_initial_state("test")
        assert "retry_count" in state
        assert "validation_result" in state
        assert "sop_pipeline" in state
        assert "sop_current_step" in state
        assert "sop_accumulated_context" in state
        assert "context_compressed" in state
        assert "checkpoint_saved" in state

    def test_defaults(self):
        state = create_initial_state("test")
        assert state["retry_count"] == 0
        assert state["validation_result"] is None
        assert state["sop_pipeline"] is None
        assert state["sop_current_step"] == 0
        assert state["sop_accumulated_context"] is None
        assert state["context_compressed"] is False
        assert state["checkpoint_saved"] is False


# ===========================================================================
# Test: validate_output_node
# ===========================================================================


class TestValidateOutputNode:
    """Test the quality gate node."""

    def test_passes_good_output(self, state_with_results):
        from src.langgraph.nodes.validate_output import validate_output_node

        result = validate_output_node(state_with_results)
        assert result["validation_result"]["passed"] is True
        assert all(result["validation_result"]["checks"].values())

    def test_fails_short_output(self, state_with_empty_response):
        from src.langgraph.nodes.validate_output import validate_output_node

        result = validate_output_node(state_with_empty_response)
        assert result["validation_result"]["passed"] is False
        assert result["validation_result"]["checks"]["has_content"] is False

    def test_fails_hallucination_output(self, state_with_results):
        from src.langgraph.nodes.validate_output import validate_output_node

        state_with_results["response"] = (
            "I don't have access to a database right now. " * 10
        )
        result = validate_output_node(state_with_results)
        assert result["validation_result"]["checks"]["no_hallucination"] is False

    def test_retry_increments_count(self, state_with_empty_response):
        from src.langgraph.nodes.validate_output import validate_output_node

        assert state_with_empty_response["retry_count"] == 0
        result = validate_output_node(state_with_empty_response)
        assert result["retry_count"] == 1

    def test_max_retries_exhausted(self, state_with_empty_response):
        from src.langgraph.nodes.validate_output import validate_output_node

        state_with_empty_response["retry_count"] = 2
        result = validate_output_node(state_with_empty_response)
        # At retry_count=2, should pass through with warning
        assert "[VALIDATE] Max retries exhausted" in result["execution_log"][-1]

    def test_should_retry_pass(self, state_with_results):
        from src.langgraph.nodes.validate_output import (
            validate_output_node,
            should_retry,
        )

        state = validate_output_node(state_with_results)
        assert should_retry(state) == "pass"

    def test_should_retry_retry(self, state_with_empty_response):
        from src.langgraph.nodes.validate_output import (
            validate_output_node,
            should_retry,
        )

        state = validate_output_node(state_with_empty_response)
        assert should_retry(state) == "retry"

    def test_should_retry_max_exhausted(self, state_with_empty_response):
        """When validate_output_node exhausts retries, it sets passed=True
        (forced pass), so should_retry should return 'pass'."""
        from src.langgraph.nodes.validate_output import (
            validate_output_node,
            should_retry,
        )

        state_with_empty_response["retry_count"] = 2
        state = validate_output_node(state_with_empty_response)
        # validate_output_node should force pass after max retries
        assert state["validation_result"]["passed"] is True
        assert state["validation_result"].get("forced_pass") is True
        assert should_retry(state) == "pass"

    def test_tools_check_passes_when_no_tools_required(self, base_state):
        from src.langgraph.nodes.validate_output import validate_output_node

        base_state["agent_config"]["tools"] = []
        base_state["response"] = "A long enough response that passes content check. " * 5
        result = validate_output_node(base_state)
        assert result["validation_result"]["checks"]["tools_used"] is True

    def test_schema_match_passes_with_keywords(self, state_with_results):
        from src.langgraph.nodes.validate_output import validate_output_node

        result = validate_output_node(state_with_results)
        assert result["validation_result"]["checks"]["schema_match"] is True


# ===========================================================================
# Test: checkpoint_saver_node
# ===========================================================================


class TestCheckpointSaverNode:
    """Test session state persistence."""

    def test_creates_checkpoint_file(self, state_with_results, tmp_path):
        from src.langgraph.nodes import checkpoint_saver

        # Patch PROJECT_ROOT to use temp dir
        with patch.object(checkpoint_saver, "PROJECT_ROOT", tmp_path):
            result = checkpoint_saver.checkpoint_saver_node(state_with_results)

        assert result["checkpoint_saved"] is True
        session_file = tmp_path / ".ai_memory" / "SESSION_STATE.md"
        assert session_file.exists()

        content = session_file.read_text(encoding="utf-8")
        assert "LiteratureHunter" in content
        assert "Research & Discovery" in content

    def test_appends_to_existing_file(self, state_with_results, tmp_path):
        from src.langgraph.nodes import checkpoint_saver

        # Create a pre-existing file
        mem_dir = tmp_path / ".ai_memory"
        mem_dir.mkdir()
        (mem_dir / "SESSION_STATE.md").write_text("# Existing content\n", encoding="utf-8")

        with patch.object(checkpoint_saver, "PROJECT_ROOT", tmp_path):
            checkpoint_saver.checkpoint_saver_node(state_with_results)

        content = (mem_dir / "SESSION_STATE.md").read_text(encoding="utf-8")
        assert "# Existing content" in content
        assert "LiteratureHunter" in content

    def test_logs_on_failure(self, state_with_results):
        from src.langgraph.nodes import checkpoint_saver

        # Use an invalid path to force failure
        with patch.object(
            checkpoint_saver, "PROJECT_ROOT", Path("/nonexistent/path/that/wont/exist")
        ):
            result = checkpoint_saver.checkpoint_saver_node(state_with_results)

        assert "[CHECKPOINT] Failed to save" in result["execution_log"][-1]


# ===========================================================================
# Test: context_compressor_node
# ===========================================================================


class TestContextCompressorNode:
    """Test context compression logic."""

    def test_no_compression_needed(self, base_state):
        from src.langgraph.nodes.context_compressor import context_compressor_node

        base_state["memory_context"] = {"key": "small value"}
        result = context_compressor_node(base_state)
        assert result["context_compressed"] is False
        assert "[COMPRESS] Context within budget" in result["execution_log"][-1]

    def test_compression_triggers_on_large_context(self, base_state):
        from src.langgraph.nodes.context_compressor import context_compressor_node

        # Create a huge context that exceeds the 50k char limit
        base_state["memory_context"] = {
            "huge_field": "x" * 60000,
            "another_field": ["item_" + str(i) for i in range(100)],
        }
        result = context_compressor_node(base_state)
        assert result["context_compressed"] is True
        assert "[COMPRESS] Context reduced" in result["execution_log"][-1]

    def test_no_crash_on_none_memory(self, base_state):
        from src.langgraph.nodes.context_compressor import context_compressor_node

        base_state["memory_context"] = None
        result = context_compressor_node(base_state)
        assert result["context_compressed"] is False

    def test_truncates_long_strings(self):
        from src.langgraph.nodes.context_compressor import _summarize_memory

        mem = {"long_key": "a" * 5000}
        compressed = _summarize_memory(mem)
        assert len(compressed["long_key"]) < 5000
        assert "truncated" in compressed["long_key"]

    def test_truncates_long_lists(self):
        from src.langgraph.nodes.context_compressor import _summarize_memory

        mem = {"big_list": list(range(50))}
        compressed = _summarize_memory(mem)
        assert len(compressed["big_list"]) <= 11  # 10 items + summary


# ===========================================================================
# Test: Conditional routing
# ===========================================================================


class TestConditionalRouting:
    """Test the _route_after_routing conditional edge function."""

    def test_routes_single_agent(self, base_state):
        from src.langgraph.graph import _route_after_routing

        base_state["target_agent"] = "LiteratureHunter"
        assert _route_after_routing(base_state) == "single"

    def test_routes_sop_pipeline(self, base_state):
        from src.langgraph.graph import _route_after_routing

        base_state["target_agent"] = "SOP:ComprehensiveLitReview"
        assert _route_after_routing(base_state) == "sop"

    def test_routes_empty_agent(self, base_state):
        from src.langgraph.graph import _route_after_routing

        base_state["target_agent"] = ""
        assert _route_after_routing(base_state) == "single"


# ===========================================================================
# Test: Fallback pipeline (run_without_langgraph)
# ===========================================================================


class TestFallbackPipeline:
    """Test that run_without_langgraph includes new nodes."""

    @patch("src.langgraph.graph.feedback_detection_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.prompt_optimization_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.keyword_extraction_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.routing_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.agent_loading_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.tools_loading_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.memory_loading_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.context_compressor_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.tool_execution_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.validate_output_node")
    @patch("src.langgraph.graph.output_builder_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.checkpoint_saver_node", side_effect=lambda s: s)
    def test_fallback_calls_new_nodes(
        self,
        mock_checkpoint,
        mock_output,
        mock_validate,
        mock_tool_exec,
        mock_compress,
        mock_memory,
        mock_tools,
        mock_agent,
        mock_route,
        mock_keywords,
        mock_optimize,
        mock_feedback,
    ):
        from src.langgraph.graph import run_without_langgraph

        # Make validate pass immediately
        def validate_stub(s):
            s["validation_result"] = {"passed": True}
            return s

        mock_validate.side_effect = validate_stub

        result = run_without_langgraph("test query")

        # Verify new nodes were called
        mock_compress.assert_called_once()
        mock_validate.assert_called_once()
        mock_checkpoint.assert_called_once()

    @patch("src.langgraph.graph.feedback_detection_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.prompt_optimization_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.keyword_extraction_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.routing_node")
    @patch("src.langgraph.graph.sop_orchestrator_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.validate_output_node")
    @patch("src.langgraph.graph.output_builder_node", side_effect=lambda s: s)
    @patch("src.langgraph.graph.checkpoint_saver_node", side_effect=lambda s: s)
    def test_fallback_sop_path(
        self,
        mock_checkpoint,
        mock_output,
        mock_validate,
        mock_sop,
        mock_route,
        mock_keywords,
        mock_optimize,
        mock_feedback,
    ):
        from src.langgraph.graph import run_without_langgraph

        # Make routing return SOP target
        def route_stub(s):
            s["target_agent"] = "SOP:ComprehensiveLitReview"
            return s

        mock_route.side_effect = route_stub

        def validate_stub(s):
            s["validation_result"] = {"passed": True}
            return s

        mock_validate.side_effect = validate_stub

        result = run_without_langgraph("do a comprehensive literature review")

        mock_sop.assert_called_once()
        mock_checkpoint.assert_called_once()


# ===========================================================================
# Test: Graph compilation
# ===========================================================================


class TestGraphCompilation:
    """Test that the graph compiles with new nodes and edges."""

    def test_graph_compiles(self):
        """Verify graph.py compiles without errors."""
        from src.langgraph.graph import invalidate_graph_cache

        invalidate_graph_cache()

        try:
            from src.langgraph.graph import create_research_graph

            graph = create_research_graph()
            # Graph is None if langgraph not installed — that's OK
            if graph is not None:
                assert graph is not None
        except ImportError:
            pytest.skip("langgraph not installed")

    def test_graph_has_human_approval_node(self):
        """Verify graph has the human_approval node after Phase 5."""
        from src.langgraph.graph import invalidate_graph_cache, create_research_graph

        invalidate_graph_cache()
        graph = create_research_graph()
        if graph is not None:
            node_names = list(graph.nodes.keys())
            assert "human_approval" in node_names


# ===========================================================================
# Test: Human Approval Node (Phase 5)
# ===========================================================================


class TestHumanApprovalNode:
    """Test the human-in-the-loop approval gate."""

    def test_normal_agent_approved(self, base_state):
        from src.langgraph.nodes.human_approval import human_approval_node

        base_state["target_agent"] = "LiteratureHunter"
        base_state["agent_config"] = {"name": "LiteratureHunter", "tools": []}
        result = human_approval_node(base_state)
        assert result["requires_approval"] is False
        assert result["approval_status"] == "approved"

    def test_high_risk_agent_pending(self, base_state):
        from src.langgraph.nodes.human_approval import human_approval_node

        base_state["target_agent"] = "AutoExperimentRunner"
        base_state["agent_config"] = {"name": "AutoExperimentRunner", "tools": ["launch_autonomous"]}
        result = human_approval_node(base_state)
        assert result["requires_approval"] is True
        assert result["approval_status"] == "pending"
        assert "REQUIRES USER APPROVAL" in (result.get("response") or "")

    def test_agent_config_flag(self, base_state):
        from src.langgraph.nodes.human_approval import human_approval_node

        base_state["target_agent"] = "CustomAgent"
        base_state["agent_config"] = {
            "name": "CustomAgent",
            "requires_human_approval": True,
            "tools": [],
        }
        result = human_approval_node(base_state)
        assert result["requires_approval"] is True
        assert result["approval_status"] == "pending"

    def test_high_risk_tool_category(self, base_state):
        from src.langgraph.nodes.human_approval import human_approval_node

        base_state["target_agent"] = "SomeAgent"
        base_state["agent_config"] = {"name": "SomeAgent", "tools": []}
        base_state["tools_available"] = [
            {"name": "launch_autonomous", "category": "auto_experiment"}
        ]
        result = human_approval_node(base_state)
        assert result["requires_approval"] is True

    def test_should_proceed_approved(self, base_state):
        from src.langgraph.nodes.human_approval import should_proceed_after_approval

        base_state["approval_status"] = "approved"
        assert should_proceed_after_approval(base_state) == "proceed"

    def test_should_proceed_pending(self, base_state):
        from src.langgraph.nodes.human_approval import should_proceed_after_approval

        base_state["approval_status"] = "pending"
        assert should_proceed_after_approval(base_state) == "reject"

    def test_approval_reason_populated(self, base_state):
        from src.langgraph.nodes.human_approval import human_approval_node

        base_state["target_agent"] = "AutoExperimentRunner"
        base_state["agent_config"] = {"name": "AutoExperimentRunner", "tools": []}
        result = human_approval_node(base_state)
        assert result["approval_reason"] is not None
        assert "high-risk" in result["approval_reason"]


# ===========================================================================
# Test: Tool Grouping (Phase 5)
# ===========================================================================


class TestToolGrouping:
    """Test tool grouping by category for parallel execution."""

    def test_group_tools_by_category(self):
        from src.langgraph.nodes.tool_execution_node import _execute_with_grouping

        # Create mock tools with tool_name
        tools = [
            {"tool_name": "search_openalex_sync", "func": lambda **kw: {"papers": []}, "kwargs": {"query": "test"}},
            {"tool_name": "search_semantic_scholar_sync", "func": lambda **kw: {"papers": []}, "kwargs": {"query": "test"}},
            {"tool_name": "lookup_doi", "func": lambda **kw: {"doi": "10.1"}, "kwargs": {"doi": "10.1"}},
        ]
        # Should not crash — just verify it returns results
        with patch("src.langgraph.nodes.tool_execution_node.execute_tools_parallel") as mock_parallel:
            mock_parallel.return_value = [
                {"tool_name": "t", "status": "success", "result": {}, "args": {}, "duration_ms": 1, "error": None}
            ]
            results = _execute_with_grouping(tools, {"parallel_tools": True, "tool_timeout": 5, "tool_retries": 0})
            # Should be called twice (literature group + writing group)
            assert mock_parallel.call_count == 2

    def test_single_category_flat_parallel(self):
        from src.langgraph.nodes.tool_execution_node import _execute_with_grouping

        tools = [
            {"tool_name": "search_openalex_sync", "func": lambda **kw: {}, "kwargs": {}},
            {"tool_name": "search_semantic_scholar_sync", "func": lambda **kw: {}, "kwargs": {}},
        ]
        with patch("src.langgraph.nodes.tool_execution_node.execute_tools_parallel") as mock_parallel:
            mock_parallel.return_value = []
            _execute_with_grouping(tools, {"parallel_tools": True, "tool_timeout": 5, "tool_retries": 0})
            # Single category → one call to parallel
            assert mock_parallel.call_count == 1

    def test_get_tool_category(self):
        from src.langgraph.tools_integration import get_tool_category

        assert get_tool_category("search_openalex_sync") == "literature"
        assert get_tool_category("verify_equation") == "wolfram"
        assert get_tool_category("nonexistent_tool") == "general"


# ===========================================================================
# Test: Dynamic Replanning (Phase 5)
# ===========================================================================


class TestDynamicReplanning:
    """Test fallback tool execution when primary tools fail."""

    def test_replan_finds_fallback(self):
        from src.langgraph.nodes.tool_execution_node import _replan_failed_tools

        failed = [{"tool_name": "search_scopus_sync", "status": "error", "args": {"query": "test"}}]

        with patch("src.langgraph.nodes.tool_execution_node.get_tool_callable") as mock_callable:
            mock_func = MagicMock(return_value={"papers": [1, 2]})
            mock_callable.return_value = mock_func

            with patch("src.langgraph.nodes.tool_execution_node.execute_tool_sync") as mock_exec:
                mock_exec.return_value = {
                    "tool_name": "search_openalex_sync",
                    "status": "success",
                    "result": {"papers": [1, 2]},
                    "args": {"query": "test"},
                    "duration_ms": 100,
                    "error": None,
                }

                results, log = _replan_failed_tools(failed, "test query", {"tool_timeout": 5, "tool_retries": 0})
                assert len(results) == 1
                assert results[0]["status"] == "success"
                assert len(log) == 1
                assert "search_scopus_sync failed" in log[0]

    def test_replan_no_fallback_available(self):
        from src.langgraph.nodes.tool_execution_node import _replan_failed_tools

        failed = [{"tool_name": "unknown_tool", "status": "error", "args": {}}]
        results, log = _replan_failed_tools(failed, "test", {"tool_timeout": 5, "tool_retries": 0})
        assert len(results) == 0
        assert len(log) == 0

    def test_replan_skips_already_tried(self):
        from src.langgraph.nodes.tool_execution_node import _replan_failed_tools

        # Both scopus and openalex failed — should not retry openalex
        failed = [
            {"tool_name": "search_scopus_sync", "status": "error", "args": {"query": "q"}},
            {"tool_name": "search_openalex_sync", "status": "error", "args": {"query": "q"}},
        ]

        with patch("src.langgraph.nodes.tool_execution_node.get_tool_callable") as mock_callable:
            mock_func = MagicMock(return_value={"papers": []})
            mock_callable.return_value = mock_func

            with patch("src.langgraph.nodes.tool_execution_node.execute_tool_sync") as mock_exec:
                mock_exec.return_value = {"tool_name": "x", "status": "success", "result": {}, "args": {}, "duration_ms": 0, "error": None}
                results, log = _replan_failed_tools(failed, "q", {"tool_timeout": 5, "tool_retries": 0})
                # search_openalex_sync is in failed_results so should be skipped as fallback for scopus
                for entry in log:
                    assert "search_openalex_sync" not in entry or "search_scopus" not in entry


# ===========================================================================
# Test: New State Fields (Phase 5)
# ===========================================================================


class TestNewStateFieldsPhase5:
    """Verify the new Phase 5 fields exist and have correct defaults."""

    def test_approval_fields_exist(self):
        state = create_initial_state("test")
        assert state["requires_approval"] is False
        assert state["approval_status"] is None
        assert state["approval_reason"] is None

    def test_replan_fields_exist(self):
        state = create_initial_state("test")
        assert state["replan_count"] == 0
        assert state["replan_log"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

