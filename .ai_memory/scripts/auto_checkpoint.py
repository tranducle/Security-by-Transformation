#!/usr/bin/env python3
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
