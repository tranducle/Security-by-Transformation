"""
Human-in-the-Loop Approval Node for LangGraph Research System.

Checks whether the target agent requires human approval before executing.
High-risk agents (e.g., AutoExperimentRunner, LatexPaperGenerator) will
pause the pipeline and inject an approval prompt into the response.

In the Antigravity context, this manifests as a prominent warning message
that the host AI presents to the user before proceeding.
"""

import logging
from typing import Any, Dict, Set

from src.langgraph.state import ResearchState

logger = logging.getLogger(__name__)

# Agents whose actions are potentially destructive or irreversible
HIGH_RISK_AGENTS: Set[str] = {
    "AutoExperimentRunner",            # launches autonomous experiments
    "LatexPaperGenerator",             # generates submission-ready papers
    "PublicationReadyWriter",          # writes final manuscripts
    "ReproducibilityArtifactEngineer", # creates Docker configs
}

# Actions that trigger approval regardless of agent
HIGH_RISK_TOOL_CATEGORIES = frozenset({"auto_experiment"})


def _check_requires_approval(state: ResearchState) -> bool:
    """Determine if the current agent/action requires human approval.

    Checks three sources:
      1. Agent JSON field: requires_human_approval = true
      2. Agent name in HIGH_RISK_AGENTS set
      3. Any loaded tool belongs to a high-risk category
    """
    agent_name = state.get("target_agent") or ""
    agent_config = state.get("agent_config") or {}

    # Check 1: Agent JSON flag
    if agent_config.get("requires_human_approval"):
        return True

    # Check 2: Known high-risk agents (strip SOP: prefix)
    clean_name = agent_name.replace("SOP:", "")
    if clean_name in HIGH_RISK_AGENTS:
        return True

    # Check 3: High-risk tools loaded
    tools_available = state.get("tools_available") or []
    for tool_info in tools_available:
        if isinstance(tool_info, dict):
            category = tool_info.get("category", "")
            if category in HIGH_RISK_TOOL_CATEGORIES:
                return True

    return False


def _build_approval_reason(state: ResearchState) -> str:
    """Build a human-readable reason for why approval is needed."""
    agent_name = state.get("target_agent", "Unknown")
    agent_config = state.get("agent_config") or {}

    reasons = []

    if agent_name.replace("SOP:", "") in HIGH_RISK_AGENTS:
        reasons.append(f"Agent '{agent_name}' is classified as high-risk")

    if agent_config.get("requires_human_approval"):
        reasons.append("Agent configuration explicitly requires approval")

    tools_available = state.get("tools_available") or []
    risky_tools = [
        t.get("name", "?")
        for t in tools_available
        if isinstance(t, dict) and t.get("category", "") in HIGH_RISK_TOOL_CATEGORIES
    ]
    if risky_tools:
        reasons.append(f"High-risk tools loaded: {', '.join(risky_tools)}")

    return "; ".join(reasons) if reasons else "High-risk action detected"


def human_approval_node(state: ResearchState) -> ResearchState:
    """LangGraph node: check if human approval is required.

    If approval is needed:
      - Sets requires_approval=True, approval_status="pending"
      - Injects a prominent approval message into the response
      - The conditional edge routes to output_builder (skipping tool_execution)

    If no approval needed:
      - Sets requires_approval=False, approval_status="approved"
      - Pipeline continues to tool_execution normally
    """
    needs_approval = _check_requires_approval(state)

    if needs_approval:
        reason = _build_approval_reason(state)
        agent_name = state.get("target_agent", "Unknown")
        user_message = state.get("user_message", "")

        state["requires_approval"] = True
        state["approval_status"] = "pending"
        state["approval_reason"] = reason

        # Build approval prompt for host AI to present
        approval_message = (
            f"\n\n⚠️ **REQUIRES USER APPROVAL** ⚠️\n\n"
            f"**Agent:** {agent_name}\n"
            f"**Reason:** {reason}\n"
            f"**User Request:** {user_message[:200]}{'...' if len(user_message) > 200 else ''}\n\n"
            f"This action requires your explicit approval before proceeding.\n"
            f"Please confirm: **approve** or **reject** this action.\n\n"
            f"---\n"
        )

        # Inject into response for host AI to show user
        existing_response = state.get("response") or ""
        state["response"] = approval_message + existing_response

        state["execution_log"].append(
            f"[APPROVAL] Pending — {reason}. Pipeline paused."
        )
        logger.info("Human approval required for %s: %s", agent_name, reason)
    else:
        state["requires_approval"] = False
        state["approval_status"] = "approved"
        state["approval_reason"] = None

        state["execution_log"].append(
            "[APPROVAL] Not required — proceeding to tool execution"
        )

    return state


def should_proceed_after_approval(state: ResearchState) -> str:
    """Conditional edge function: proceed or skip to output.

    Returns:
        "proceed" — approval granted or not needed, continue to tool_execution
        "reject"  — approval pending/rejected, skip to output_builder
    """
    status = state.get("approval_status")

    if status == "approved":
        return "proceed"
    else:
        return "reject"
