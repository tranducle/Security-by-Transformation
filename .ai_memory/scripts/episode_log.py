#!/usr/bin/env python3
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
        f.write(f"[{timestamp}] {msg}\n")
    print(f"Logged: {msg}")

if __name__ == "__main__":
    main()
