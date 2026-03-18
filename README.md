# AI Research Agent System

<div align="center">

**Version 6.0**

*A Tool-Executing Multi-Agent System for Academic Research*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agents: 116](https://img.shields.io/badge/agents-116-green.svg)]()

</div>

---

## Overview

The AI Research Agent System is a production-ready, multi-agent pipeline that automates the complete academic research lifecycle. With **116 specialized AI agents** organized into 10 strategic domains, the system **auto-executes tools** (API searches, file operations, computations) and delivers structured results for an external AI host to synthesize.

**No LLM API keys required** — works with any AI host (Antigravity, OpenCode, Gemini CLI, Claude Code) that provides the LLM.

### Key Features

- **116 Specialized Agents** — Comprehensive coverage of research tasks
- **Tool Auto-Execution** — API searches, computations, and file ops run automatically
- **Structured Output** — Agent context + real tool results packaged for host AI synthesis
- **LangGraph Pipeline** — Deterministic routing with graph-based orchestration
- **34 Research Workflows** — From literature review to manuscript submission
- **Natural Language Interface** — No need to memorize agent names or workflows
- **CLI Integration** — Works with Antigravity, Claude Code, Gemini CLI, and OpenCode
- **Extensible Architecture** — Easy to add new agents and workflows

---

## Quick Start

**For detailed installation and running instructions, see [`INSTALL.md`](INSTALL.md).**

### TL;DR

```bash
pip install -r requirements.txt

python3 run_agent.py -i
```

### Pipeline Architecture

```
User Request → optimize_prompt → extract_keywords → route → load_agent
  → load_tools → load_memory → tool_execution → output_builder → Structured Output
```

The host AI receives structured output containing agent context, real tool results, memory context, and synthesis instructions.

---

## Documentation

| Document | Description |
|----------|-------------|
| **[INSTALL.md](INSTALL.md)** | Installation guide and how to run the system |
| **[How_to_Use_the_AI_AGENT_System.md](How_to_Use_the_AI_AGENT_System.md)** | Usage workflows and examples |
| **[CLI_INTEGRATION.md](CLI_INTEGRATION.md)** | Integration with AI assistants |

---

## Agent Categories

The system organizes 116 agents into 14 functional categories:

| Category | Key Functions |
|----------|---------------|
| **Strategy & Planning** | Project scoping, innovation, grant proposals |
| **Literature & Research** | Multi-source literature search, synthesis |
| **Methodology & Statistics** | Research design, statistical analysis, surveys |
| **Cybersecurity** | Security architecture, threat modeling, compliance |
| **Human Factors** | Psychology, behavioral analysis, game theory |
| **Business & Risk** | Cost-benefit analysis, insurance, supply chain |
| **Data & Analysis** | Data processing, metrics, visualization |
| **Implementation & Code** | PyTorch models, reproducibility, frameworks |
| **Output & Visualization** | Papers, presentations, figures, LaTeX |
| **Quality Assurance** | Peer review, citation verification, novelty checking |
| **Synthesis & Documentation** | Multi-source synthesis, reference management |
| **Research Support** | Gap analysis, ideation, brainstorming |
| **Project Management** | State tracking, planning, progress monitoring |
| **Specialized Analysis** | SLR protocols, scenario forecasting |

---

## Directory Structure

```
ResearchAgentSystem/
├── .agent/workflows/       # 34 research workflows
├── src/
│   ├── langgraph/         # Pipeline engine (graph, nodes, tool executor)
│   ├── core/              # Constants, base exceptions
│   ├── tools/             # Callable tool functions
│   ├── schemas/           # Agent definition schemas
│   └── utils/             # Configuration utilities
├── agents/                 # 116 JSON agent definitions
├── AI_Agents_YAML/         # YAML agents + MasterOrchestrator
├── tests/                  # Test suite (57 tests)
├── run_agent.py            # Main entry point
├── config.yaml             # System configuration
└── requirements.txt        # Python dependencies
```

---

## License

This project is licensed under the MIT License.

---

## Author

**Dr. Tran Duc Le**  
Assistant Professor  
Department of Mathematics, Statistics and Computer Science  
University of Wisconsin-Stout  
Menomonie, WI, USA

**Contact:** <let@uwstout.edu>

---

<div align="center">

**Built with ❤️ for the Research Community**

*Empowering researchers with AI-driven automation*

</div>
