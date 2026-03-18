# LangGraph Integration Plan for Research Agent System

## Vision

Build a **Python-based LangGraph orchestration layer** that:

- Runs inside **Antigravity IDE** via terminal commands
- **Code-enforces** routing to correct agents (no reliance on AI memory)
- Uses all **108 existing agents** from `agents/` directory
- Integrates with existing tools in `src/tools/`

---

## The Problem We're Solving

The AI frequently "forgets" routing rules and agent standards, causing:

1. Tasks routed to wrong agents
2. Agent-specific design standards ignored
3. Inconsistent output quality

**LangGraph solution:** Routing logic is in Python code, not dependent on AI memory.

---

## Architecture Overview

```
User Message → LangGraph Router → Agent Loader → Memory Update → Output
     ↓              ↓                  ↓              ↓           ↓
  "create      Keyword match      Load JSON     Save state    Print agent
   tikz"       → TikZPlotter      system_prompt              + prompt
```

---

## Directory Structure

```
src/langgraph/
├── __init__.py
├── graph.py              # Main StateGraph definition
├── state.py              # TypedDict for state schema
├── cli.py                # CLI entry point for Antigravity
├── nodes/
│   ├── router.py         # Keyword-based routing
│   ├── agent_loader.py   # Load agent JSON
│   └── memory.py         # Save/load memory
└── config/
    └── routing_rules.json
```

---

## Key Files to Create

### 1. `state.py` - State Schema

```python
from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    user_message: str
    keywords: List[str]
    target_domain: str
    target_agent: str
    agent_prompt: str
    response: str
```

### 2. `router.py` - Routing Node

- Parse MasterOrchestrator.json Section 6
- Map keywords → agents
- Return target agent

### 3. `cli.py` - CLI Interface

```bash
python -m src.langgraph.cli "your request here"
```

Output: Agent name + system_prompt for Antigravity to adopt.

---

## Integration with Antigravity

1. User sends request in Antigravity
2. AI invokes: `python -m src.langgraph.cli "request"`
3. LangGraph returns: agent + prompt
4. AI adopts the prompt and executes

---

## Assets to Leverage

- 108 Agents in `agents/*.json`
- MasterOrchestrator.json (Section 6 = routing rules)
- mem0_loader.py (memory logic)
- .memory/memory.json (storage)

---

## Success Criteria

- [ ] All 10 domains correctly routed
- [ ] CLI works in Antigravity terminal
- [ ] Memory persists across sessions
- [ ] TikZPlotter correctly triggered for "tikz" keyword

---

## Getting Started

1. Run `/init` to load context
2. Create `src/langgraph/` directory structure
3. Implement nodes one by one
4. Test with CLI commands
