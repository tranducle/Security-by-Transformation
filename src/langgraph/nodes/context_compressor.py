"""
Context Compressor Node for LangGraph Research System.

Compresses memory context if it exceeds a character threshold, preventing
token budget exhaustion during tool execution.
"""

import logging
from typing import Any, Dict

from src.langgraph.state import ResearchState

logger = logging.getLogger(__name__)

# Threshold in characters (roughly 4 chars per token → 50k chars ≈ 12.5k tokens)
CONTEXT_CHAR_LIMIT = 50000


def _summarize_memory(memory: Dict[str, Any]) -> Dict[str, Any]:
    """Create a compact summary of memory context.

    Keeps structural keys but truncates large values.
    """
    MAX_VALUE_CHARS = 2000

    def _truncate(val: Any, max_chars: int = MAX_VALUE_CHARS) -> Any:
        if isinstance(val, str) and len(val) > max_chars:
            return val[:max_chars] + f"... [truncated, {len(val)} total chars]"
        if isinstance(val, dict):
            return {k: _truncate(v, max_chars) for k, v in val.items()}
        if isinstance(val, list):
            if len(val) > 10:
                return [_truncate(v, max_chars) for v in val[:10]] + [
                    f"... [{len(val) - 10} more items]"
                ]
            return [_truncate(v, max_chars) for v in val]
        return val

    return _truncate(memory)


def context_compressor_node(state: ResearchState) -> ResearchState:
    """Compress context if approaching token limits.

    Measures the serialized size of memory_context and compresses it
    if it exceeds CONTEXT_CHAR_LIMIT. This runs between load_memory
    and tool_execution to ensure tools operate within budget.
    """
    memory = state.get("memory_context")
    if not memory:
        return state

    try:
        import json

        total_chars = len(json.dumps(memory, default=str))
    except (TypeError, ValueError):
        total_chars = len(str(memory))

    if total_chars > CONTEXT_CHAR_LIMIT:
        compressed = _summarize_memory(memory)

        try:
            import json

            new_chars = len(json.dumps(compressed, default=str))
        except (TypeError, ValueError):
            new_chars = len(str(compressed))

        state["memory_context"] = compressed
        state["context_compressed"] = True
        state["execution_log"].append(
            f"[COMPRESS] Context reduced from {total_chars:,} to {new_chars:,} chars "
            f"({100 - (new_chars * 100 // total_chars)}% reduction)"
        )
        logger.info(
            "Context compressed: %d → %d chars", total_chars, new_chars
        )
    else:
        state["execution_log"].append(
            f"[COMPRESS] Context within budget ({total_chars:,} chars, limit {CONTEXT_CHAR_LIMIT:,})"
        )

    return state
