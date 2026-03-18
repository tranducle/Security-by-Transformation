"""
Checkpoint Saver Node for LangGraph Research System.

Auto-saves session state after every pipeline execution to
`.ai_memory/SESSION_STATE.md`, ensuring context persists across sessions.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from src.langgraph.state import ResearchState

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def checkpoint_saver_node(state: ResearchState) -> ResearchState:
    """Save execution checkpoint to SESSION_STATE.md.

    Appends a structured record of the current pipeline execution including:
      - Agent name and domain
      - Tools used and their status
      - Quality assessment result
      - Timestamp

    This directly addresses the context-loss bottleneck by auto-persisting
    execution history that the AI can re-read at session start.
    """
    agent = state.get("target_agent", "Unknown")
    domain = state.get("target_domain", "Unknown")
    tool_results = state.get("tool_results", [])
    validation = state.get("validation_result") or {}

    checkpoint = {
        "agent": agent,
        "domain": domain,
        "tools_used": [r.get("tool_name", "?") for r in tool_results],
        "tools_success": sum(
            1 for r in tool_results if r.get("status") == "success"
        ),
        "quality_passed": validation.get("passed", True),
        "timestamp": datetime.now().isoformat(),
        "user_message": (state.get("user_message") or "")[:200],
    }

    # Append to SESSION_STATE.md
    session_path = PROJECT_ROOT / ".ai_memory" / "SESSION_STATE.md"
    try:
        session_path.parent.mkdir(parents=True, exist_ok=True)

        # Build the checkpoint entry
        lines = [
            f"\n## Pipeline Execution: {checkpoint['agent']}",
            f"- **Time:** {checkpoint['timestamp']}",
            f"- **Domain:** {checkpoint['domain']}",
            f"- **Request:** {checkpoint['user_message']}",
            f"- **Tools:** {checkpoint['tools_used']}",
            f"- **Success:** {checkpoint['tools_success']}/{len(tool_results)}",
            f"- **Quality:** {'PASS' if checkpoint['quality_passed'] else 'FAIL'}",
            "",
        ]

        with open(session_path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines))

        state["checkpoint_saved"] = True
        state["execution_log"].append(
            f"[CHECKPOINT] Saved execution record to {session_path}"
        )
        logger.info("Checkpoint saved for %s to %s", agent, session_path)

    except Exception as exc:
        logger.warning("Could not save checkpoint: %s", exc)
        state["execution_log"].append(
            f"[CHECKPOINT] Failed to save: {exc}"
        )

    return state
