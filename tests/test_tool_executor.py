"""Tests for tool execution engine."""

import sys
import time
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.langgraph.tool_executor import (
    execute_tool_sync,
    execute_tools_parallel,
    clear_cache,
)


def _fast_tool(query: str = "test") -> dict:
    return {"papers": [{"title": f"Result for {query}"}]}


def _slow_tool(query: str = "test") -> dict:
    time.sleep(5)
    return {"data": "slow"}


def _failing_tool(query: str = "test") -> dict:
    raise RuntimeError("API unavailable")


class TestExecuteToolSync(unittest.TestCase):
    def setUp(self):
        clear_cache()

    def test_success(self):
        result = execute_tool_sync("test_fast", _fast_tool, {"query": "cybersecurity"})
        self.assertEqual(result["status"], "success")
        self.assertIn("papers", result["result"])
        self.assertGreater(result["duration_ms"], 0)

    def test_error_captured(self):
        result = execute_tool_sync("test_fail", _failing_tool, {"query": "x"})
        self.assertEqual(result["status"], "error")
        self.assertIn("API unavailable", result["error"])
        self.assertIsNone(result["result"])

    def test_timeout_via_parallel(self):
        tasks = [{"tool_name": "slow", "func": _slow_tool, "kwargs": {"query": "x"}}]
        cfg = {"tool_timeout": 1, "tool_retries": 0, "parallel_tools": False}
        results = execute_tools_parallel(tasks, config=cfg)
        self.assertEqual(len(results), 1)

    def test_caching(self):
        r1 = execute_tool_sync("test_fast", _fast_tool, {"query": "same"})
        r2 = execute_tool_sync("test_fast", _fast_tool, {"query": "same"})
        self.assertEqual(r1["result"], r2["result"])
        self.assertLess(r2["duration_ms"], r1["duration_ms"])

    def test_empty_args(self):
        result = execute_tool_sync("test_fast", _fast_tool, {})
        self.assertEqual(result["status"], "success")


class TestExecuteToolsParallel(unittest.TestCase):
    def setUp(self):
        clear_cache()

    def test_parallel_multiple(self):
        tasks = [
            {"tool_name": "fast_1", "func": _fast_tool, "kwargs": {"query": "a"}},
            {"tool_name": "fast_2", "func": _fast_tool, "kwargs": {"query": "b"}},
        ]
        results = execute_tools_parallel(tasks)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r["status"] == "success" for r in results))

    def test_parallel_mixed_success_failure(self):
        tasks = [
            {"tool_name": "good", "func": _fast_tool, "kwargs": {"query": "ok"}},
            {"tool_name": "bad", "func": _failing_tool, "kwargs": {"query": "x"}},
        ]
        results = execute_tools_parallel(tasks)
        statuses = {r["tool_name"]: r["status"] for r in results}
        self.assertEqual(statuses["good"], "success")
        self.assertEqual(statuses["bad"], "error")

    def test_parallel_empty(self):
        results = execute_tools_parallel([])
        self.assertEqual(results, [])

    def test_sequential_mode(self):
        tasks = [
            {"tool_name": "f1", "func": _fast_tool, "kwargs": {"query": "a"}},
        ]
        cfg = {"tool_timeout": 30, "tool_retries": 0, "parallel_tools": False}
        results = execute_tools_parallel(tasks, config=cfg)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["status"], "success")


if __name__ == "__main__":
    unittest.main()
