---
description: Boot/checkpoint session memory - prevents AI from forgetting context
---

# Memory Management Workflow

CM-OS (Codebase Memory OS) provides persistent memory across sessions and prevents context loss during long sessions.

## Quick Commands

| Command | Action |
|---------|--------|
| `/memory` | Full memory boot (read below) |
| `/memory:checkpoint` | Save current work state |
| `/memory:refresh` | Re-read session context |
| `/memory:close` | End session properly |
| `/memory:status` | Check memory status |

---

## /memory - Full Memory Boot

Run this when starting a new session or after `/init`:

### Step 1: Generate Memory Pack

// turbo

```powershell
# Windows (use Bypass to avoid execution policy issues)
powershell -ExecutionPolicy Bypass -File .\.ai_memory\scripts\memory.ps1
```

For Unix:

```bash
bash .ai_memory/scripts/memory.sh
```

### Step 2: Read Memory Pack

**MANDATORY: Read this file to restore your context:**

```
READ FILE: .ai_memory/packs/MEMORY_PACK.md
```

**What you'll learn from MEMORY_PACK:**

| Section | Content |
|---------|---------|
| §1 Task State | Current goals, active tasks |
| §2-4 Summaries | Project/System/Modules overview |
| §5 Repo Atlas | File structure, dependencies |
| §6 Git Context | Branch, recent commits, changes |
| §7 Command Trace | Recent terminal commands |
| §8 Episodes | What you did in previous sessions |
| §9 Next Action | How to continue work |
| §10 Auto-Checkpoint | Memory maintenance protocol |

### Step 3: Reset Checkpoint Counter

// turbo

```bash
python .ai_memory/scripts/auto_checkpoint.py reset
```

---

## /memory:checkpoint - Save Work State

Run this before taking breaks or switching tasks:

// turbo

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File .\.ai_memory\scripts\checkpoint.ps1
```

For Unix:

```bash
bash .ai_memory/scripts/checkpoint.sh
```

This saves:

- Repository scan (file structure)
- Git context (branch, status, diff)
- Updated MEMORY_PACK.md

---

## /memory:refresh - Re-read Context

Run this when you feel you've "forgotten" earlier context:

// turbo

```bash
python .ai_memory/scripts/session_memory.py refresh
```

This outputs a compact summary of:

- Earlier work (compressed)
- Recent context (last 3 exchanges)
- Current task focus

---

## /memory:close - End Session Properly

Run this before ending a work session:

### Step 1: Save Final Checkpoint

// turbo

```powershell
powershell -ExecutionPolicy Bypass -File .\.ai_memory\scripts\checkpoint.ps1
```

### Step 2: Log What You Did

```bash
python .ai_memory/scripts/episode_log.py add \
    "What was the goal" \
    "Files/symbols changed" \
    "Key decisions made" \
    "Verification/proof" \
    "What to do next"
```

**Example:**

```bash
python .ai_memory/scripts/episode_log.py add \
    "Integrated CM-OS into init workflow" \
    ".agent/workflows/init.md, memory.md" \
    "Added 3 new steps: boot, read, checkpoint" \
    "All scripts tested successfully" \
    "Test full init workflow in new session"
```

### Step 3: Update Task State (Optional)

Edit `.ai_memory/tasks/state.json` to update:

- `current_goal`
- `active_tasks`
- Task status

---

## /memory:status - Check Memory Status

// turbo

```bash
python .ai_memory/scripts/auto_checkpoint.py status
```

**Example output:**

```
==================================================
📊 AUTO-CHECKPOINT STATUS
==================================================
  Response count:      3/5
  Checkpoint interval: Every 5 responses
  Refresh interval:    Every 10 responses
--------------------------------------------------
  Total checkpoints:   12
  Total refreshes:     3
  Last checkpoint:     2026-01-15T22:10:00
==================================================
```

---

## Continuous Memory Protocol

> [!IMPORTANT]
> Run this at the **START of EVERY response** to prevent memory loss:

```bash
python .ai_memory/scripts/auto_checkpoint.py tick-q
```

### Output Meanings

| Output | Meaning | Action Required |
|--------|---------|-----------------|
| `📝 [MEM:2/5]` | Counter at 2/5 | None, continue working |
| `💾 SAVED#5` | Checkpoint done | Memory saved, counter reset |
| `🔄 REFRESH_NEEDED` | Context may be stale | Run `/memory:refresh` |

### When REFRESH_NEEDED Appears

```bash
python .ai_memory/scripts/session_memory.py refresh
```

This prevents the AI from "forgetting" earlier context in long sessions.

---

## Memory Architecture

```
.ai_memory/
├── tasks/state.json          # Working memory (current goals)
├── summaries/
│   ├── L4_project.md         # Project intent
│   ├── L3_system.md          # Architecture
│   └── L2_modules.md         # Modules overview
├── episodes/
│   ├── episodes.sqlite       # Action history database
│   └── trace.log             # Command trace
├── atlas/
│   ├── repo_map.json         # File index
│   ├── deps.json             # Dependencies
│   └── git_context.json      # Git state
├── packs/
│   ├── MEMORY_PACK.md        # Full memory (read this!)
│   └── MEMORY_PACK.compact.md # Smaller version
├── session/
│   └── current_session.json  # Current session state
└── scripts/                   # Memory tools
```

---

## Best Practices

1. **Always read MEMORY_PACK** at session start
2. **Run tick-q every response** to track memory state
3. **Checkpoint before task switches** to preserve context
4. **Log episodes** for important decisions
5. **Update L4/L3/L2 summaries** when project evolves

---

## Troubleshooting

### Memory Pack Not Generated

```bash
# Check if scripts exist
ls .ai_memory/scripts/

# Run manually
python .ai_memory/scripts/scan_repo.py
python .ai_memory/scripts/git_context.py
python .ai_memory/scripts/memory_pack.py
```

### Episode Database Issues

```bash
# View recent episodes
python .ai_memory/scripts/episode_log.py tail 5

# Initialize new database
python .ai_memory/scripts/episode_log.py init
```

### Session Memory Not Working

```bash
# Check session status
python .ai_memory/scripts/session_memory.py status

# Clear and restart
python .ai_memory/scripts/session_memory.py clear
```
