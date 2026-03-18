"""Integration tests for the LangGraph research pipeline."""

import sys
import time
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestPipelineImports(unittest.TestCase):
    def test_graph_imports(self):
        from src.langgraph.graph import (
            create_research_graph,
            run_graph,
            run_without_langgraph,
            invalidate_graph_cache,
        )

    def test_state_imports(self):
        from src.langgraph.state import (
            ResearchState,
            ToolResult,
            ExecutionMetadata,
            create_initial_state,
        )

    def test_node_imports(self):
        from src.langgraph.nodes import (
            route_request,
            load_agent,
            load_memory,
            tool_execution_node,
            output_builder_node,
            init_context_modules,
            get_context_snapshot,
        )

    def test_tool_executor_imports(self):
        from src.langgraph.tool_executor import (
            execute_tool_sync,
            execute_tools_parallel,
            clear_cache,
        )

    def test_tools_integration_imports(self):
        from src.langgraph.tools_integration import (
            get_tools_for_agent,
            get_tool_names_for_agent,
        )


class TestInitialState(unittest.TestCase):
    def test_create_initial_state_fields(self):
        from src.langgraph.state import create_initial_state

        state = create_initial_state("test message")
        self.assertEqual(state["user_message"], "test message")
        self.assertIsInstance(state["keywords"], list)
        self.assertIsInstance(state["execution_log"], list)
        self.assertIsInstance(state["tool_results"], list)
        self.assertIsInstance(state["tool_errors"], list)
        self.assertEqual(len(state["tool_results"]), 0)


try:
    import langgraph as _lg
    _HAS_LANGGRAPH = True
except ImportError:
    _HAS_LANGGRAPH = False


@unittest.skipIf(not _HAS_LANGGRAPH, "langgraph not installed")
class TestGraphCompilation(unittest.TestCase):
    def test_graph_compiles(self):
        from src.langgraph.graph import create_research_graph, invalidate_graph_cache

        invalidate_graph_cache()
        graph = create_research_graph()
        self.assertIsNotNone(graph)

    def test_graph_singleton(self):
        from src.langgraph.graph import create_research_graph

        g1 = create_research_graph()
        g2 = create_research_graph()
        self.assertIs(g1, g2)


class TestPipelineNoTools(unittest.TestCase):
    """Agent without tools — pipeline should complete with empty tool_results."""

    def test_brainstorm_agent_no_tools(self):
        from src.langgraph.graph import run_graph

        result = run_graph("help me brainstorm ideas for a research project")
        self.assertIn("structured_output", result)
        so = result["structured_output"]
        self.assertIn("agent_context", so)
        self.assertIn("tool_results", so)
        self.assertIsInstance(so["tool_results"], list)
        self.assertIn("synthesis_instructions", so)

    def test_response_generated(self):
        from src.langgraph.graph import run_graph

        result = run_graph("help me brainstorm ideas")
        self.assertIn("response", result)
        self.assertIsInstance(result["response"], str)
        self.assertGreater(len(result["response"]), 10)


class TestStructuredOutputSchema(unittest.TestCase):
    REQUIRED_KEYS = [
        "agent_context",
        "user_request",
        "tool_results",
        "tool_errors",
        "memory_context",
        "execution_metadata",
        "requires_approval",
        "synthesis_instructions",
    ]

    def test_structured_output_has_all_keys(self):
        from src.langgraph.graph import run_graph

        result = run_graph("find literature on machine learning")
        so = result.get("structured_output", {})
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, so, f"Missing key: {key}")

    def test_execution_metadata_fields(self):
        from src.langgraph.graph import run_graph

        result = run_graph("find literature on machine learning")
        meta = result.get("structured_output", {}).get("execution_metadata", {})
        self.assertIn("tools_executed", meta)
        self.assertIn("total_duration_ms", meta)
        self.assertIn("pipeline_route", meta)


class TestErrorHandling(unittest.TestCase):
    def test_unknown_agent_does_not_crash(self):
        from src.langgraph.graph import run_without_langgraph

        result = run_without_langgraph("xyzzy gibberish 42 random")
        self.assertIn("response", result)
        self.assertIn("structured_output", result)

    def test_empty_message(self):
        from src.langgraph.graph import run_without_langgraph

        result = run_without_langgraph("")
        self.assertIn("response", result)


class TestContextModules(unittest.TestCase):
    def test_init_context_modules(self):
        from src.langgraph.nodes.memory import init_context_modules

        status = init_context_modules(".")
        self.assertIn("project_state", status)
        self.assertIn("session_manager", status)
        self.assertIn("research_diary", status)

    def test_get_context_snapshot(self):
        from src.langgraph.nodes.memory import (
            init_context_modules,
            get_context_snapshot,
        )

        init_context_modules(".")
        snap = get_context_snapshot(limit=5)
        self.assertIsInstance(snap, dict)

    def test_memory_loading_node_merges_context(self):
        from src.langgraph.graph import run_graph

        result = run_graph("find literature on AI")
        mc = result.get("memory_context", {})
        self.assertIn("context_modules", mc)


class TestFallbackPipeline(unittest.TestCase):
    def test_run_without_langgraph(self):
        from src.langgraph.graph import run_without_langgraph

        result = run_without_langgraph("find literature on cybersecurity")
        self.assertIn("structured_output", result)
        self.assertIn("response", result)


if __name__ == "__main__":
    unittest.main()
