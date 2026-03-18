"""Pipeline performance benchmarks.

Measures pipeline latency without LLM calls (tool auto-execution only).
Gates:
  - p95 no-tool pipeline: <= 2.0s
  - p95 with-tool pipeline: <= 10.0s (API-dependent)
"""

import statistics
import sys
import time
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestPipelineLatency(unittest.TestCase):
    ITERATIONS = 5

    def _measure(self, message: str) -> list:
        from src.langgraph.graph import run_without_langgraph

        times = []
        for _ in range(self.ITERATIONS):
            start = time.perf_counter()
            run_without_langgraph(message)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        return times

    def _p95(self, times: list) -> float:
        sorted_t = sorted(times)
        idx = int(len(sorted_t) * 0.95)
        return sorted_t[min(idx, len(sorted_t) - 1)]

    def test_no_tool_latency(self):
        times = self._measure("help me brainstorm research ideas")
        p95 = self._p95(times)
        avg = statistics.mean(times)
        print(
            f"\n  No-tool pipeline: avg={avg:.3f}s p95={p95:.3f}s (n={self.ITERATIONS})"
        )
        self.assertLessEqual(p95, 2.0, f"p95={p95:.3f}s exceeds 2.0s gate")

    def test_tool_pipeline_latency(self):
        times = self._measure("find literature on deep reinforcement learning")
        p95 = self._p95(times)
        avg = statistics.mean(times)
        print(
            f"\n  With-tool pipeline: avg={avg:.3f}s p95={p95:.3f}s (n={self.ITERATIONS})"
        )
        self.assertLessEqual(p95, 15.0, f"p95={p95:.3f}s exceeds 15.0s gate")

    def test_graph_compilation_time(self):
        from src.langgraph.graph import invalidate_graph_cache, create_research_graph

        invalidate_graph_cache()
        start = time.perf_counter()
        create_research_graph()
        elapsed = time.perf_counter() - start
        print(f"\n  Graph compilation: {elapsed:.3f}s")
        self.assertLessEqual(
            elapsed, 1.0, f"Compilation took {elapsed:.3f}s, exceeds 1.0s"
        )


if __name__ == "__main__":
    unittest.main()
