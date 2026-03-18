"""
Validate Output Node for LangGraph Research System.

Quality gate that checks agent output meets quality criteria before returning.
Supports retry logic — if validation fails and retry_count < 2, the pipeline
loops back to tool_execution.
"""

import logging
from typing import Any, Dict, Optional

from src.langgraph.state import ResearchState

logger = logging.getLogger(__name__)


def _validate_against_schema(
    output: str, schema: Optional[Dict[str, Any]]
) -> bool:
    """Check if output loosely matches the expected output_schema keys.

    This is a lightweight heuristic — it checks whether the output text
    mentions the major section headings defined in the schema.
    """
    if not schema:
        return True

    # output_schema in agent JSON is a dict of section → description
    # We check if the output mentions at least half the section names
    section_names = list(schema.keys()) if isinstance(schema, dict) else []
    if not section_names:
        return True

    hits = sum(1 for s in section_names if s.lower() in output.lower())
    return hits >= max(1, len(section_names) // 2)


def validate_output_node(state: ResearchState) -> ResearchState:
    """Validate output quality before returning.

    Checks performed:
      1. has_content   — response is non-trivial (> 50 chars, relaxed for tool-less agents)
      2. no_hallucination — doesn't contain "I don't have access" type phrases
      3. tools_used    — if agent has tools, at least one produced a result
      4. schema_match  — output loosely matches agent's output_schema
    """
    agent_config = state.get("agent_config") or {}
    output = state.get("response") or ""
    schema = agent_config.get("output_schema")
    tool_results = state.get("tool_results", [])
    agent_tools = agent_config.get("tools", [])

    # Relaxed content threshold: agents without tools (persona-only) may
    # produce output entirely through the host AI, so we accept shorter text
    content_threshold = 100 if agent_tools else 50

    # Run quality checks
    checks: Dict[str, bool] = {
        "has_content": len(output) > content_threshold,
        "no_hallucination": not any(
            phrase in output
            for phrase in [
                "I don't have access",
                "I cannot access",
                "I'm unable to",
                "as an AI",
            ]
        ),
        "tools_used": (
            not agent_tools  # no tools required → auto-pass
            or any(r.get("status") == "success" for r in tool_results)
        ),
        "schema_match": _validate_against_schema(output, schema),
    }

    passed = all(checks.values())
    retry_count = state.get("retry_count", 0)

    if passed:
        state["validation_result"] = {
            "passed": True,
            "checks": checks,
            "retry_count": retry_count,
        }
        state["execution_log"].append(
            f"[VALIDATE] All quality checks passed: {checks}"
        )
    elif retry_count < 2:
        state["retry_count"] = retry_count + 1
        state["validation_result"] = {
            "passed": False,
            "checks": checks,
            "retry_count": retry_count + 1,
        }
        state["execution_log"].append(
            f"[RETRY #{retry_count + 1}] Quality check failed: {checks}"
        )
    else:
        # Max retries exhausted — force pass with a warning
        state["validation_result"] = {
            "passed": True,  # Force pass to prevent infinite retry
            "checks": checks,
            "retry_count": retry_count,
            "forced_pass": True,
        }
        state["execution_log"].append(
            f"[VALIDATE] Max retries exhausted, passing with warnings: {checks}"
        )

    # Populate quality_assessment for backward compat with output_builder
    if not state.get("quality_assessment"):
        state["quality_assessment"] = {
            "quality_score": 1.0 if passed else 0.5,
            "issues": [
                f"Validation check failed: {k}"
                for k, v in checks.items()
                if not v
            ],
            "auto_lessons": [],
        }

    return state


def should_retry(state: ResearchState) -> str:
    """Conditional edge function: decide whether to retry or pass.

    Returns:
        "pass"  — validation passed (including forced pass on max retries)
        "retry" — validation failed AND retries remain
    """
    validation = state.get("validation_result") or {}
    passed = validation.get("passed", True)

    if passed:
        return "pass"
    else:
        return "retry"
