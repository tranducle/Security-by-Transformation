#!/usr/bin/env python3
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
            files.append({"path": rel.replace("\\", "/"), "size": size})
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
