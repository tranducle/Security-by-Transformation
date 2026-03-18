# ResearchAgentSystemv14 - Installation Guide

## Quick Start

### 1. Extract the Archive

Extract `AIAGENTSYSTEM.zip` to your desired location.

### 2. Install Python Dependencies

```bash
# Navigate to the directory
cd AIAGENTSYSTEM

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys (Optional)

The system comes with a pre-configured `.env` file. If you need to update API keys:

Edit `.env` and add your keys:

```
SERPAPI_KEY=your_key_here
SEMANTIC_SCHOLAR_KEY=your_key_here
SCOPUS_API_KEY=your_key_here
```

### 4. Run the System

#### Option A: Quick Start with AI Assistant (Recommended)

**Windows:**

```cmd
start_research_assistant.bat
```

**Linux/Mac:**

```bash
chmod +x start_research_assistant.sh
./start_research_assistant.sh
```

This will:

1. Check if API keys are configured (run setup if needed)
2. Let you choose between geminicli or claude-code
3. Launch your chosen AI assistant with MasterOrchestrator integration

#### Option B: Direct Python Execution

```bash
# Interactive mode
python run_agent.py -i

# Single query
python run_agent.py "Find papers on federated learning from 2023-2024"

# List all agents
python run_agent.py --list-agents

# Show system status
python run_agent.py --status
```

## Directory Structure

```
AIAGENTSYSTEM/
├── src/                    # Source code
│   ├── core/              # Core agent classes
│   ├── loaders/           # Agent definition loaders
│   ├── execution/         # Orchestrator and routing
│   ├── apis/              # External API clients
│   ├── context/           # State management
│   ├── cli/               # Command-line interface
│   └── utils/             # Utilities
├── AI_Agents_YAML/        # Agent definitions (YAML format)
├── agents/                # Agent definitions (108 agents, JSON format)
├── run_agent.py           # Main entry point
├── setup_api_keys.py      # API key configuration script
├── requirements.txt       # Python dependencies
├── config.yaml            # System configuration
├── .env                   # API keys (pre-configured)
├── README.md              # Project documentation
└── How_to_Use_the_AI_AGENT_System.md  # Usage guide
```

## Troubleshooting

### Import Errors

If you encounter import errors, make sure you're running from the `AIAGENTSYSTEM` directory:

```bash
cd AIAGENTSYSTEM
python run_agent.py -i
```

### Missing Dependencies

Install missing packages:

```bash
pip install python-dotenv PyYAML aiohttp click rich pandas beautifulsoup4 lxml pybtex colorlog
```

### API Key Errors

Run the setup script to configure API keys:

```bash
python setup_api_keys.py
```

## System Requirements

- Python 3.8 or higher
- 4GB RAM minimum
- Internet connection (for API calls)

## Features

- **108 Specialized Agents** for research tasks
- **Interactive Mode** for conversational interaction
- **Natural Language Routing** - no need to memorize agent names
- **3-Tier Delegation** - coordinators manage specialist agents
- **API Integration** - Google Scholar, Semantic Scholar, Scopus

## First Time Usage: Initialize AI Context

When starting a new session in **Antigravity**, **Claude Code**, or **Geminicli**, type:

```
/init
```

This command makes the AI read all context files and understand the agent system before you start working. After initialization, the AI will know:

- The MasterOrchestrator and how it routes requests
- All 108 available agents and their capabilities
- The 3-tier delegation hierarchy

---

## Next Steps

1. Read [How_to_Use_the_AI_AGENT_System.md](How_to_Use_the_AI_AGENT_System.md) for detailed usage
2. Read [CLI_INTEGRATION.md](CLI_INTEGRATION.md) for AI assistant integration
3. Run `start_research_assistant.bat` (or `.sh`) to start with AI assistant
4. Type `/init` in your AI assistant to load the system context

## Verification

After installation, verify the system is complete:

**Windows:**

```cmd
# Check agent definitions exist
dir AI_Agents_YAML
REM Should show 100+ .yaml files

# Check Python modules
dir src
REM Should show: core, loaders, execution, apis, context, cli, utils

# List available agents
python run_agent.py --list-agents
REM Should show 108 agents
```

**Linux/Mac:**

```bash
# Check agent definitions exist
ls AI_Agents_YAML | wc -l
# Should show 100+

# Check Python modules
ls src
# Should show: core, loaders, execution, apis, context, cli, utils

# List available agents
python run_agent.py --list-agents
# Should show 108 agents
```
