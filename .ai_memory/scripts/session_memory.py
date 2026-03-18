#!/usr/bin/env python3
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
