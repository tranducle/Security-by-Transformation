---
description: Synchronize project tracking files (logs, diary, milestones)
---

# Sync Project Status

Use this workflow to update all project tracking files at once.

## When to Use

- At the END of a work session
- Before presenting results to supervisor
- When you notice logs are out of date
- Before `/daily-summary`

## Auto-Trigger Rules

> **IMPORTANT**: This workflow should be triggered AUTOMATICALLY (no user prompt needed) after:
>
> - `/write-paper` or `/paper-outline` completes
> - `/literature-search` completes
> - `/experiment-design` completes
> - `/systematic-review` completes
> - `/peer-review` completes  
> - Any session ending with `/daily-summary`
>
> The AI MUST run at minimum the **Quick Sync** (Steps 1-2 + session save) after these workflows.

## Steps

### 1. Update Project Log

Add entry to `8_Project_Management/project_log.md`:

```markdown
### Entry [N]: [DATE] - [SESSION_DESCRIPTION]

**Actions:**
- [List actions performed this session]

**Artifacts:**
- [List files created/modified]
```

### 2. Update Milestone Tracker

Review `8_Project_Management/milestone_tracker.md`:

- Change ⬜ → 🔄 for in-progress items
- Change 🔄 → ✅ for completed items
- Add completion dates

### 3. Update Research Diary

If significant insight occurred, add entry to `0_Project_Admin/research_diary.md`:

- Research direction changes
- Key findings
- Methodology decisions

### 4. Update Prompt History

Add recent prompts to `8_Project_Management/prompt_history.md`

### 5. Update Research Plan

If `1_Strategic_Plan/research_plan.md` exists:

- Update status of completed phases
- Add notes on any changes

### 6. Update Decision Log

If key decisions were made:

- Add to `8_Project_Management/decision_log.md`

### 7. Save Session State (Auto)

// turbo

```bash
python .ai_memory/scripts/save_session_state.py
```

This generates `.ai_memory/SESSION_STATE.md` so the next AI session can instantly resume via `/init`.

---

## Quick Sync (Minimal)

For quick updates, at minimum:

1. ✅ Update project_log.md with session summary
2. ✅ Update milestone_tracker.md status
3. ✅ Run `python .ai_memory/scripts/save_session_state.py`

---

## Trigger Phrases

- "/sync"
- "Update logs"
- "Sync project status"
- "Update tracking files"
- "Save progress"

---

// turbo-all
