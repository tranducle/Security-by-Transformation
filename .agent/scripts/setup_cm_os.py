#!/usr/bin/env python3
"""
CM-OS (Context Memory Operating System) Setup Script
=====================================================
Auto-creates the .ai_memory/ directory structure and all required scripts.
Idempotent: safe to run multiple times without side effects.

Usage:
    python .agent/scripts/setup_cm_os.py [--project-root PATH]
"""

import os
import sys
import json
import datetime

def get_project_root():
    """Detect project root from script location or argument."""
    if len(sys.argv) > 2 and sys.argv[1] == "--project-root":
        return sys.argv[2]
    # Walk up from script location: .agent/scripts/ -> project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(script_dir))

def get_project_name(root):
    """Extract project name from directory."""
    return os.path.basename(root)

def ensure_dir(path):
    """Create directory if not exists."""
    os.makedirs(path, exist_ok=True)

def write_if_missing(filepath, content):
    """Write file only if it doesn't exist (preserve existing data)."""
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [NEW] {os.path.relpath(filepath)}")
    else:
        print(f"  [OK]  {os.path.relpath(filepath)} (exists)")

def write_always(filepath, content):
    """Always overwrite (for scripts that should be latest version)."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [SET] {os.path.relpath(filepath)}")

def setup_cm_os():
    root = get_project_root()
    project = get_project_name(root)
    mem_dir = os.path.join(root, ".ai_memory")
    scripts_dir = os.path.join(mem_dir, "scripts")
    now = datetime.datetime.now().isoformat()

    print(f"+{'='*42}+")
    print(f"| CM-OS Setup for: {project:<24}|")
    print(f"+{'='*42}+")
    print()

    # ── 1. Create directory structure ──
    print("[DIR] Creating directory structure...")
    dirs = [
        os.path.join(mem_dir, "tasks"),
        os.path.join(mem_dir, "summaries"),
        os.path.join(mem_dir, "episodes"),
        os.path.join(mem_dir, "atlas"),
        os.path.join(mem_dir, "packs"),
        os.path.join(mem_dir, "session"),
        scripts_dir,
    ]
    for d in dirs:
        ensure_dir(d)

    # ── 2. Create data files (only if missing) ──
    print("\n[DATA] Creating data files...")

    write_if_missing(os.path.join(mem_dir, "tasks", "state.json"), json.dumps({
        "current_goals": [],
        "active_task": None,
        "context": {"project": project},
        "created": now,
        "updated": now
    }, indent=2))

    write_if_missing(os.path.join(mem_dir, "summaries", "L4_project.md"),
        f"# Project Summary: {project}\n\nCreated: {now}\n\n"
        "## Overview\n\n(Auto-generated. Will be updated during /memory boot.)\n")

    write_if_missing(os.path.join(mem_dir, "summaries", "L3_system.md"),
        f"# System Architecture: {project}\n\nCreated: {now}\n\n"
        "## Components\n\n(Will be populated by scan_repo.py.)\n")

    write_if_missing(os.path.join(mem_dir, "summaries", "L2_modules.md"),
        f"# Module Overview: {project}\n\nCreated: {now}\n\n"
        "## Modules\n\n(Will be populated by scan_repo.py.)\n")

    write_if_missing(os.path.join(mem_dir, "episodes", "trace.log"),
        f"# Episode Trace Log - {project}\n# Created: {now}\n\n")

    write_if_missing(os.path.join(mem_dir, "atlas", "repo_map.json"), json.dumps({
        "project": project,
        "root": root,
        "files": [],
        "created": now
    }, indent=2))

    write_if_missing(os.path.join(mem_dir, "atlas", "git_context.json"), json.dumps({
        "branch": None,
        "last_commit": None,
        "diff_summary": None,
        "created": now
    }, indent=2))

    write_if_missing(os.path.join(mem_dir, "session", "current_session.json"), json.dumps({
        "session_id": None,
        "started": None,
        "tick_count": 0,
        "checkpoints": [],
        "created": now
    }, indent=2))

    # ── 3. Create scripts (always update to latest) ──
    print("\n[SCRIPTS] Creating/updating scripts...")

    # --- auto_checkpoint.py ---
    write_always(os.path.join(scripts_dir, "auto_checkpoint.py"), '''#!/usr/bin/env python3
"""Auto-checkpoint tick counter for CM-OS memory system."""
import os, sys, json, datetime

def get_session_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(script_dir), "session", "current_session.json")

def load_session():
    path = get_session_file()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"session_id": None, "started": None, "tick_count": 0, "checkpoints": []}

def save_session(data):
    path = get_session_file()
    data["updated"] = datetime.datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    if len(sys.argv) < 2:
        print("Usage: auto_checkpoint.py <tick-q|status|reset>")
        sys.exit(1)

    cmd = sys.argv[1]
    session = load_session()

    if cmd == "tick-q":
        session["tick_count"] = session.get("tick_count", 0) + 1
        tick = session["tick_count"]
        save_session(session)
        if tick >= 10:
            print(f"REFRESH_NEEDED (tick={tick})")
        elif tick % 5 == 0:
            print(f"CHECKPOINT_SUGGESTED (tick={tick})")
            session["checkpoints"].append(datetime.datetime.now().isoformat())
            save_session(session)
        else:
            print(f"OK (tick={tick})")

    elif cmd == "status":
        print(f"Tick count: {session.get('tick_count', 0)}")
        print(f"Checkpoints: {len(session.get('checkpoints', []))}")
        print(f"Session started: {session.get('started', 'N/A')}")

    elif cmd == "reset":
        session["tick_count"] = 0
        session["started"] = datetime.datetime.now().isoformat()
        session["checkpoints"] = []
        save_session(session)
        print("Session reset.")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
''')

    # --- scan_repo.py ---
    write_always(os.path.join(scripts_dir, "scan_repo.py"), '''#!/usr/bin/env python3
"""Scan repository and build atlas/repo_map.json."""
import os, json, datetime

IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".ai_memory", ".sessions", ".venv", "venv", ".tox"}
IGNORE_EXTS = {".pyc", ".pyo", ".egg-info", ".whl"}

def scan(root, max_files=500):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        for f in filenames:
            if any(f.endswith(ext) for ext in IGNORE_EXTS):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            try:
                size = os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                size = 0
            files.append({"path": rel.replace("\\\\", "/"), "size": size})
            if len(files) >= max_files:
                return files
    return files

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mem_dir = os.path.dirname(script_dir)
    root = os.path.dirname(mem_dir)
    output = os.path.join(mem_dir, "atlas", "repo_map.json")

    files = scan(root)
    data = {
        "project": os.path.basename(root),
        "root": root,
        "file_count": len(files),
        "files": files,
        "scanned": datetime.datetime.now().isoformat()
    }
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Scanned {len(files)} files -> atlas/repo_map.json")

if __name__ == "__main__":
    main()
''')

    # --- git_context.py ---
    write_always(os.path.join(scripts_dir, "git_context.py"), '''#!/usr/bin/env python3
"""Extract git context (branch, recent commits, diff)."""
import os, json, subprocess, datetime

def run_git(args, cwd):
    try:
        result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() if result.returncode == 0 else None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mem_dir = os.path.dirname(script_dir)
    root = os.path.dirname(mem_dir)
    output = os.path.join(mem_dir, "atlas", "git_context.json")

    branch = run_git(["branch", "--show-current"], root)
    last_commit = run_git(["log", "-1", "--format=%H %s"], root)
    diff_stat = run_git(["diff", "--stat"], root)

    data = {
        "branch": branch,
        "last_commit": last_commit,
        "diff_summary": diff_stat,
        "has_git": branch is not None,
        "updated": datetime.datetime.now().isoformat()
    }
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Git context: branch={branch or 'N/A'}")

if __name__ == "__main__":
    main()
''')

    # --- episode_log.py ---
    write_always(os.path.join(scripts_dir, "episode_log.py"), '''#!/usr/bin/env python3
"""Log episode events to trace.log."""
import os, sys, datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: episode_log.py <message>")
        sys.exit(1)

    msg = " ".join(sys.argv[1:])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mem_dir = os.path.dirname(script_dir)
    log_path = os.path.join(mem_dir, "episodes", "trace.log")

    timestamp = datetime.datetime.now().isoformat()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\\n")
    print(f"Logged: {msg}")

if __name__ == "__main__":
    main()
''')

    # --- session_memory.py ---
    write_always(os.path.join(scripts_dir, "session_memory.py"), '''#!/usr/bin/env python3
"""Session context manager — start/stop/query sessions."""
import os, json, datetime, uuid

def get_session_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(script_dir), "session", "current_session.json")

def load():
    path = get_session_file()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save(data):
    with open(get_session_file(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def start():
    data = load()
    data["session_id"] = str(uuid.uuid4())[:8]
    data["started"] = datetime.datetime.now().isoformat()
    data["tick_count"] = 0
    data["checkpoints"] = []
    save(data)
    print(f"Session started: {data['session_id']}")

def status():
    data = load()
    print(f"Session: {data.get('session_id', 'None')}")
    print(f"Started: {data.get('started', 'N/A')}")
    print(f"Ticks: {data.get('tick_count', 0)}")
    print(f"Checkpoints: {len(data.get('checkpoints', []))}")

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "start": start()
    elif cmd == "status": status()
    else: print(f"Usage: session_memory.py <start|status>")
''')

    # --- save_session_state.py ---
    write_always(os.path.join(scripts_dir, "save_session_state.py"), '''#!/usr/bin/env python3
"""Generate SESSION_STATE.md for next session fast-resume."""
import os, json, datetime

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mem_dir = os.path.dirname(script_dir)
    root = os.path.dirname(mem_dir)
    output = os.path.join(root, "SESSION_STATE.md")

    # Gather state
    project = os.path.basename(root)
    now = datetime.datetime.now().isoformat()

    # Read session data
    session = {}
    session_file = os.path.join(mem_dir, "session", "current_session.json")
    if os.path.exists(session_file):
        with open(session_file, "r", encoding="utf-8") as f:
            session = json.load(f)

    # Read task state
    tasks = {}
    task_file = os.path.join(mem_dir, "tasks", "state.json")
    if os.path.exists(task_file):
        with open(task_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)

    # Generate markdown
    md = f"""# SESSION_STATE — {project}

> Auto-generated by save_session_state.py at {now}
> Read this file at the start of a new session to resume context.

## Session Info

- **Session ID**: {session.get('session_id', 'N/A')}
- **Started**: {session.get('started', 'N/A')}
- **Ticks**: {session.get('tick_count', 0)}
- **Checkpoints**: {len(session.get('checkpoints', []))}

## Active Task

- **Task**: {tasks.get('active_task', 'None')}
- **Goals**: {json.dumps(tasks.get('current_goals', []))}

## Quick Resume

1. Read this file
2. Run `/memory:refresh` to load full context
3. Continue from where you left off
"""
    with open(output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"SESSION_STATE.md saved -> {output}")

if __name__ == "__main__":
    main()
''')

    # --- memory_pack.py ---
    write_always(os.path.join(scripts_dir, "memory_pack.py"), '''#!/usr/bin/env python3
"""Generate MEMORY_PACK.md — the single-file brain dump for AI context recovery."""
import os, json, datetime

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, PermissionError):
        return "(not found)"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mem_dir = os.path.dirname(script_dir)
    root = os.path.dirname(mem_dir)
    output = os.path.join(mem_dir, "packs", "MEMORY_PACK.md")

    project = os.path.basename(root)
    now = datetime.datetime.now().isoformat()

    # Gather all summaries
    l4 = read_file(os.path.join(mem_dir, "summaries", "L4_project.md"))
    l3 = read_file(os.path.join(mem_dir, "summaries", "L3_system.md"))

    # Git context
    git_ctx = "(not scanned)"
    git_file = os.path.join(mem_dir, "atlas", "git_context.json")
    if os.path.exists(git_file):
        with open(git_file, "r", encoding="utf-8") as f:
            git = json.load(f)
        git_ctx = f"Branch: {git.get('branch', 'N/A')}, Last commit: {git.get('last_commit', 'N/A')}"

    # Session info
    session_info = "(no active session)"
    sess_file = os.path.join(mem_dir, "session", "current_session.json")
    if os.path.exists(sess_file):
        with open(sess_file, "r", encoding="utf-8") as f:
            sess = json.load(f)
        session_info = f"Session {sess.get('session_id', '?')}, ticks: {sess.get('tick_count', 0)}"

    # Task state
    task_info = "(no active task)"
    task_file = os.path.join(mem_dir, "tasks", "state.json")
    if os.path.exists(task_file):
        with open(task_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        if tasks.get("active_task"):
            task_info = f"Active: {tasks['active_task']}"

    # Episode log (last 20 lines)
    episodes = "(empty)"
    log_file = os.path.join(mem_dir, "episodes", "trace.log")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > 3:  # Skip header
            episodes = "".join(lines[-20:])

    md = f"""# MEMORY_PACK — {project}

> Generated: {now}
> This file is the AI's "brain dump" — read it to recover full context.

## 1. Project Summary
{l4}

## 2. System Architecture
{l3}

## 3. Git Context
{git_ctx}

## 4. Session State
{session_info}

## 5. Active Task
{task_info}

## 6. Recent Activity
```
{episodes}
```

---
*End of MEMORY_PACK. You are now oriented.*
"""
    with open(output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"MEMORY_PACK.md generated -> packs/MEMORY_PACK.md")

if __name__ == "__main__":
    main()
''')

    # --- memory.ps1 (Windows boot) ---
    write_always(os.path.join(scripts_dir, "memory.ps1"), f'''# CM-OS Memory Boot (Windows PowerShell)
# Usage: powershell -File .ai_memory/scripts/memory.ps1

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$memDir = Split-Path -Parent $scriptDir
$rootDir = Split-Path -Parent $memDir

Write-Host "=== CM-OS Memory Boot ===" -ForegroundColor Cyan

# Step 1: Scan repo
Write-Host "Scanning repository..."
python "$scriptDir/scan_repo.py"

# Step 2: Git context
Write-Host "Extracting git context..."
python "$scriptDir/git_context.py"

# Step 3: Reset session
Write-Host "Starting new session..."
python "$scriptDir/session_memory.py" start

# Step 4: Generate MEMORY_PACK
Write-Host "Generating MEMORY_PACK..."
python "$scriptDir/memory_pack.py"

Write-Host "=== CM-OS Ready ===" -ForegroundColor Green
''')

    # --- memory.sh (Unix boot) ---
    write_always(os.path.join(scripts_dir, "memory.sh"), '''#!/bin/bash
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
''')

    # --- checkpoint.ps1 ---
    write_always(os.path.join(scripts_dir, "checkpoint.ps1"), '''# CM-OS Checkpoint (Windows PowerShell)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Saving Checkpoint ===" -ForegroundColor Yellow
python "$scriptDir/scan_repo.py"
python "$scriptDir/git_context.py"
python "$scriptDir/memory_pack.py"
python "$scriptDir/save_session_state.py"
python "$scriptDir/episode_log.py" "Checkpoint saved"
Write-Host "=== Checkpoint Complete ===" -ForegroundColor Green
''')

    # --- checkpoint.sh ---
    write_always(os.path.join(scripts_dir, "checkpoint.sh"), '''#!/bin/bash
# CM-OS Checkpoint (Unix)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Saving Checkpoint ==="
python3 "$SCRIPT_DIR/scan_repo.py"
python3 "$SCRIPT_DIR/git_context.py"
python3 "$SCRIPT_DIR/memory_pack.py"
python3 "$SCRIPT_DIR/save_session_state.py"
python3 "$SCRIPT_DIR/episode_log.py" "Checkpoint saved"
echo "=== Checkpoint Complete ==="
''')

    # ── 4. Summary ──
    print()
    print(f"[OK] CM-OS setup complete!")
    print(f"     Root:    {mem_dir}")
    print(f"     Scripts: {len(os.listdir(scripts_dir))} files")
    print(f"     Test:    python .ai_memory/scripts/auto_checkpoint.py status")
    print(f"     Boot:    powershell -File .ai_memory/scripts/memory.ps1")

if __name__ == "__main__":
    setup_cm_os()
