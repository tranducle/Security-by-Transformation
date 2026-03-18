#!/bin/bash
# CM-OS Checkpoint (Unix)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Saving Checkpoint ==="
python3 "$SCRIPT_DIR/scan_repo.py"
python3 "$SCRIPT_DIR/git_context.py"
python3 "$SCRIPT_DIR/memory_pack.py"
python3 "$SCRIPT_DIR/save_session_state.py"
python3 "$SCRIPT_DIR/episode_log.py" "Checkpoint saved"
echo "=== Checkpoint Complete ==="
