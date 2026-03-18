#!/usr/bin/env python3
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
