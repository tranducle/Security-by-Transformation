#!/bin/bash
# CM-OS Memory Boot (Unix)
# Usage: bash .ai_memory/scripts/memory.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEM_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== CM-OS Memory Boot ==="

python3 "$SCRIPT_DIR/scan_repo.py"
python3 "$SCRIPT_DIR/git_context.py"
python3 "$SCRIPT_DIR/session_memory.py" start
python3 "$SCRIPT_DIR/memory_pack.py"

echo "=== CM-OS Ready ==="
