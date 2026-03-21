# CLI Integration Guide - AI Research Agent System

## Overview

The AI Research Agent System can be integrated with **gemini** or **claude** to provide a powerful conversational interface for research workflows. This guide explains how to set up and use the integration.

## Quick Start

### Windows Users

1. Open Command Prompt or PowerShell
2. Navigate to the AIAGENTSYSTEM directory
3. Run the startup script:
   ```cmd
   start_research_assistant.bat
   ```
4. Choose your AI assistant (gemini or claude)
5. Start using `@MasterOrchestrator` in your conversation!

### Linux/Mac Users

1. Open Terminal
2. Navigate to the AIAGENTSYSTEM directory
3. Make the script executable (first time only):
   ```bash
   chmod +x start_research_assistant.sh
   ```
4. Run the startup script:
   ```bash
   ./start_research_assistant.sh
   ```
5. Choose your AI assistant (gemini or claude)
6. Start using `@MasterOrchestrator` in your conversation!

## How It Works

```
┌─────────────────────────────────────────────────────┐
│ User Terminal                                       │
│                                                     │
│ $ gemini (or claude)                       │
│                                                     │
│ > @MasterOrchestrator, find papers on federated... │
│                                                     │
│ AI Assistant recognizes @MasterOrchestrator        │
│     ↓                                              │
│ Executes: python run_agent.py "find papers..."     │
│     ↓                                              │
│ Python system routes to appropriate agents         │
│     ↓                                              │
│ Results returned to AI Assistant                   │
│     ↓                                              │
│ Formatted output presented to user                 │
└─────────────────────────────────────────────────────┘
```

## Usage Examples

### Example 1: Literature Search

**You:**
```
@MasterOrchestrator, find papers on federated learning in healthcare from 2023-2024
```

**System Action:**
- Routes to `LiteratureHunter` agent
- Executes Google Scholar, Semantic Scholar, Scopus searches
- Synthesizes results from all sources

**AI Assistant Response:**
```
Found 15 papers on federated learning in healthcare (2023-2024):

1. "Federated Learning for Healthcare Data Analysis" (2024)
   Authors: Smith et al.
   Citations: 42
   DOI: 10.1234/example

2. "Privacy-Preserving ML in Medical Imaging" (2023)
   Authors: Johnson et al.
   Citations: 28
   DOI: 10.1234/example2

[... 13 more papers ...]

Summary: Key trends include differential privacy techniques,
edge computing optimization, and cross-institutional collaboration.
```

### Example 2: Methodology Design

**You:**
```
@MasterOrchestrator, design a methodology section for a survey on AI ethics
```

**System Action:**
- Routes to `MethodologyExperimentDesigner` agent
- Generates comprehensive methodology framework
- Includes participant recruitment, survey design, analysis methods

### Example 3: Paper Review

**You:**
```
@MasterOrchestrator, review my paper at papers/my_draft.pdf
```

**System Action:**
- Routes to `PeerReviewer` coordinator
- Delegates to sub-agents:
  - `HarshReviewer` - Critical feedback
  - `CitationIntegrityAuditor` - Citation verification
  - `MissingPartSuggester` - Structure analysis
- Synthesizes comprehensive review

### Example 4: Data Analysis

**You:**
```
@MasterOrchestrator, analyze the results in results/experiment1.csv
```

**System Action:**
- Routes to `DataMetricsAnalyst` agent
- Verifies statistical calculations
- Generates visualizations
- Validates significance testing

## Direct Python Execution

You can also run the system directly without gemini/claude:

### Interactive Mode
```bash
python run_agent.py -i
```

### Single Query
```bash
python run_agent.py "Find papers on federated learning"
```

### Specific Agent
```bash
python run_agent.py --agent GoogleScholarSearch "deep learning in healthcare"
```

### List Available Agents
```bash
python run_agent.py --list-agents
```

### System Status
```bash
python run_agent.py --status
```

## Available Agent Triggers

The system automatically routes your query to the appropriate agent based on keyword matching. Some common triggers:

| Trigger Phrase | Agent |
|---------------|-------|
| "find papers", "literature search", "search for" | LiteratureHunter |
| "review my paper", "critique this" | PeerReviewer |
| "design experiment", "methodology" | MethodologyExperimentDesigner |
| "analyze data", "verify statistics" | DataMetricsAnalyst |
| "generate figures", "create plots" | FigureGenerator |
| "check citations", "verify references" | CitationIntegrityAuditor |
| "write abstract", "generate title" | AbstractTitleGenerator |
| "find research gaps", "identify opportunities" | GapMapperResearchOpportunityExtractor |

For a complete list, run:
```bash
python run_agent.py --list-agents
```

## Advanced Usage

### Manual Agent Selection

If automatic routing doesn't select the right agent, specify it explicitly:

**With gemini/claude:**
```
@MasterOrchestrator, use the PeerReviewer agent to review my paper
```

**Direct Python:**
```bash
python run_agent.py --agent PeerReviewer "Review papers/my_draft.pdf"
```

### Chaining Multiple Agents

You can request multiple agents in sequence:

```
@MasterOrchestrator:
1. Use LiteratureHunter to find papers on X
2. Use SummarizerSynthesizer to create a summary
3. Use GapMapper to identify research gaps
```

### Providing Context

Give the system context for better results:

```
@MasterOrchestrator, I'm writing a paper on federated learning in healthcare.
First, find recent papers from 2023-2024. Then, analyze the methodology sections
to identify common approaches and gaps.
```

## Configuration

### API Keys

The system requires API keys for research APIs:
- **SerpAPI** - Google Scholar search
- **Semantic Scholar** - Academic paper search
- **Scopus** - Citation database (optional)

API keys are configured automatically when you first run `start_research_assistant.bat` (or `.sh`).

To update keys manually, edit `.env`:
```env
SERPAPI_KEY=your_key_here
SEMANTIC_SCHOLAR_KEY=your_key_here
SCOPUS_API_KEY=your_key_here
```

### System Settings

Edit `config.yaml` to customize:
- Agent directories
- Rate limits
- Logging levels
- Output formats

## Troubleshooting

### "gemini not found"
Install Google Gemini CLI:
```bash
npm install -g @google/generative-ai-cli
# or
pip install gemini
```

### "claude not found"
Install Claude Code CLI:
```bash
npm install -g @anthropic-ai/claude
# or follow instructions at: https://github.com/anthropics/claude
```

### API Rate Limit Errors
The system has built-in rate limiting, but if you hit limits:
1. Wait a few minutes and retry
2. Upgrade your API plan if needed
3. Adjust rate limits in `config.yaml`

### Agent Not Loading
Check agent definitions:
```bash
python run_agent.py --status
```

If an agent fails to load, check the log file:
```bash
cat agent_system.log | grep ERROR
```

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed queries
2. **Use Context**: Give background information about your research
3. **Break Down Complex Tasks**: Split large requests into steps
4. **Iterate**: Refine your query based on initial results
5. **Provide Feedback**: The system learns from your preferences

## Architecture

### 3-Tier Agent Hierarchy

- **Tier 1 (26 Elite Agents)**: Direct access for high-level tasks
  - MasterOrchestrator, LiteratureHunter, PeerReviewer, etc.

- **Tier 2 (6 Coordinators)**: Manage specialist sub-agents
  - LiteratureHunter → [GoogleScholarSearch, SemanticSearch, ScopusSearch]
  - PeerReviewer → [HarshReviewer, CitationIntegrityAuditor, MissingPartSuggester]
  - InnovationStrategist → [GapMapper, IdeaMutation, BrainstormingFacilitator]

- **Tier 3 (77 Specialists)**: Focused, single-purpose agents
  - AbstractTitleGenerator, DataMetricsAnalyst, FigureGenerator, etc.

### Smart Routing

The system uses:
1. **35+ Keyword Triggers**: Regex patterns for automatic routing
2. **20 Standard Operating Playbooks**: Predefined workflows for common tasks
3. **Semantic Similarity**: Fallback matching when no trigger matches

## Support

For issues or questions:
1. Check `agent_system.log` for error details
2. Run `python run_agent.py --status` for system diagnostics
3. Review agent definitions in `AI_Agents_MD/`

## Next Steps

1. Run `start_research_assistant.bat` (or `.sh`)
2. Choose your AI assistant
3. Try: `@MasterOrchestrator, help me find papers on my research topic`
4. Explore available agents: `python run_agent.py --list-agents`
5. Read agent definitions in `AI_Agents_MD/` for detailed capabilities

---

**System Version:** 4.0
**Last Updated:** 2026-01-05
**Total Agents:** 103 specialized research agents
