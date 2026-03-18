#!/usr/bin/env python3
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
