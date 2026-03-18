"""
SOP Orchestrator Node for LangGraph Research System.

Executes multi-agent SOP pipelines with state handoff between agents.
Each agent in the pipeline is loaded, its tools executed, and results
accumulated for the next agent in the chain.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from src.langgraph.state import ResearchState

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def sop_orchestrator_node(state: ResearchState) -> ResearchState:
    """Execute multi-agent SOP pipeline sequentially.

    For SOP:SOP_NAME targets, this node:
      1. Resolves the SOP pipeline from SOP_REGISTRY
      2. Iterates through each agent in the pipeline
      3. Loads agent config and tools for each step
      4. Executes tools with accumulated context
      5. Saves intermediate results to SDP directories
      6. Accumulates all agent outputs for the final response

    This replaces the single-agent SOP handling in agent_loading_node
    with true multi-agent orchestration.
    """
    from src.langgraph.nodes.router import SOP_REGISTRY
    from src.langgraph.nodes.agent_loader import load_agent
    from src.langgraph.tools_integration import get_tools_for_agent
    from src.langgraph.tool_executor import execute_tools_parallel

    target_agent = state.get("target_agent", "")
    if not target_agent.startswith("SOP:"):
        state["execution_log"].append(
            "[SOP] Not an SOP target, skipping orchestrator"
        )
        return state

    sop_name = target_agent.replace("SOP:", "")
    sop_info = SOP_REGISTRY.get(sop_name, {})
    pipeline = sop_info.get("pipeline", [])
    description = sop_info.get("description", "")

    if not pipeline:
        state["execution_log"].append(
            f"[SOP] Pipeline '{sop_name}' not found or empty"
        )
        state["response"] = f"ERROR: SOP '{sop_name}' has no pipeline defined"
        return state

    state["sop_pipeline"] = pipeline
    state["execution_log"].append(
        f"[SOP] Starting pipeline: {sop_name} ({len(pipeline)} agents: {' → '.join(pipeline)})"
    )

    accumulated_context = ""
    all_tool_results = []
    all_tool_errors = []

    for i, agent_name in enumerate(pipeline):
        state["sop_current_step"] = i + 1

        # Load agent config
        config = load_agent(agent_name)
        if not config:
            state["execution_log"].append(
                f"[SOP] Step {i + 1}: Agent '{agent_name}' not found, skipping"
            )
            continue

        # Get tools for this agent
        tools = get_tools_for_agent(agent_name)

        state["execution_log"].append(
            f"[SOP] Step {i + 1}/{len(pipeline)}: {agent_name} "
            f"({len(tools)} tools)"
        )

        # Execute tools if available
        if tools:
            query = state.get("optimized_message") or state.get("user_message", "")
            # Add accumulated context to help tools
            if accumulated_context:
                query = f"{query}\n\nContext from previous agents:\n{accumulated_context[:2000]}"

            try:
                results, errors = execute_tools_parallel(
                    tools_info=tools,
                    query=query,
                    agent_config=config,
                )
                all_tool_results.extend(results)
                all_tool_errors.extend(errors)

                # Build result summary for this agent
                success_results = [
                    r for r in results if r.get("status") == "success"
                ]
                if success_results:
                    import json

                    for r in success_results:
                        try:
                            result_str = json.dumps(
                                r.get("result", ""), default=str
                            )[:3000]
                        except (TypeError, ValueError):
                            result_str = str(r.get("result", ""))[:3000]
                        accumulated_context += (
                            f"\n\n## Output from {agent_name} ({r.get('tool_name', '?')}):\n"
                            f"{result_str}"
                        )
            except Exception as exc:
                state["execution_log"].append(
                    f"[SOP] Step {i + 1}: Tool execution failed: {exc}"
                )
                logger.warning(
                    "SOP tool execution failed for %s: %s", agent_name, exc
                )
        else:
            # Agent has no auto-tools — record its persona
            accumulated_context += (
                f"\n\n## Agent {agent_name} (persona-only):\n"
                f"Role: {config.get('role', 'N/A')}\n"
                f"Goal: {config.get('goal', 'N/A')}\n"
            )

        # Save intermediate result to SDP directory
        sdp_dir = config.get("sdp_output_dir", "")
        if sdp_dir:
            try:
                sdp_path = PROJECT_ROOT / sdp_dir
                sdp_path.mkdir(parents=True, exist_ok=True)
                intermediate_file = sdp_path / f"sop_{sop_name}_step{i + 1}.md"
                with open(intermediate_file, "w", encoding="utf-8") as f:
                    f.write(
                        f"# SOP: {sop_name} — Step {i + 1}: {agent_name}\n\n"
                        f"{accumulated_context[-3000:]}\n"
                    )
                state["execution_log"].append(
                    f"[SOP] Saved intermediate to {intermediate_file}"
                )
            except Exception as exc:
                logger.debug("SOP intermediate save failed: %s", exc)

    # Update state with accumulated results
    state["sop_accumulated_context"] = accumulated_context
    state["tool_results"] = all_tool_results
    state["tool_errors"] = all_tool_errors

    # Set agent_config and agent_prompt from the LAST agent in pipeline
    last_config = load_agent(pipeline[-1])
    if last_config:
        state["agent_config"] = last_config
        sop_header = (
            f"# SOP PIPELINE COMPLETE: {sop_name}\n"
            f"# Description: {description}\n"
            f"# Agents executed: {' → '.join(pipeline)}\n"
            f"# Total tool results: {len(all_tool_results)}\n"
            f"{'=' * 60}\n\n"
        )
        state["agent_prompt"] = sop_header + last_config.get("system_prompt", "")

    state["execution_log"].append(
        f"[SOP] Pipeline complete: {len(all_tool_results)} results, "
        f"{len(all_tool_errors)} errors"
    )

    return state
