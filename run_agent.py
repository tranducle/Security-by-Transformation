#!/usr/bin/env python3
"""
Research Agent System v6.0 - Main Entry Point

Usage:
    python run_agent.py "Your research query here"
    python run_agent.py -i
    python run_agent.py --list-agents
    python run_agent.py -v "verbose query"

Examples:
    # Run a literature search
    python run_agent.py "Find top 20 papers on federated learning from 2023-2024"

    # Interactive mode
    python run_agent.py -i

    # List all agents
    python run_agent.py --list-agents
"""

import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, src_path)

from src.cli.main import main_sync

if __name__ == "__main__":
    sys.exit(main_sync())
