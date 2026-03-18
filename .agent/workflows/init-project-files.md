---
description: Initialize project management files at project start
---

# Initialize Project Management Files

This workflow creates all required files in `8_Project_Management/` and initializes `0_Project_Admin/` for proper research tracking.

## Auto-Detection: When to Run

**RUN THIS WORKFLOW IF ANY OF THESE ARE TRUE:**

1. `8_Project_Management/` directory is **empty** or doesn't exist
2. `8_Project_Management/project_log.md` is **missing**
3. `0_Project_Admin/research_diary.md` is **missing**
4. Starting a **NEW research project** in a new directory
5. User calls `/project-kickoff`

**DO NOT RUN IF:**

- All 4 files already exist in `8_Project_Management/`
- Just switching to an existing project (files already there)

## Auto-Trigger in /init

When `/init` is called, the MasterOrchestrator should:

```
1. Check if 8_Project_Management/ has files
2. IF empty: Auto-run this workflow
3. ELSE: Skip (files already exist)
```

---

## Steps

### 1. Create Project Log

Create `8_Project_Management/project_log.md`:

```markdown
# Project Activity Log

## Project: [PROJECT_NAME]
## Started: [DATE]

---

### Session Log

| Date | Session | Actions Performed | Agents Used | Artifacts Created |
|------|---------|-------------------|-------------|-------------------|
| | | | | |

---

## Detailed Entries

(Entries will be added after each major action)
```

### 2. Create Prompt History

Create `8_Project_Management/prompt_history.md`:

```markdown
# Prompt History

## Project: [PROJECT_NAME]

| # | Date | Summary | Domain Routed | Action Taken |
|---|------|---------|---------------|--------------|
| | | | | |
```

### 3. Create Milestone Tracker

Create `8_Project_Management/milestone_tracker.md`:

```markdown
# Milestone Tracker

## Project: [PROJECT_NAME]

| Milestone | Target Date | Status | Completed Date | Notes |
|-----------|-------------|--------|----------------|-------|
| Literature Review | | ⬜ Pending | | |
| Methodology Design | | ⬜ Pending | | |
| Analysis Complete | | ⬜ Pending | | |
| First Draft | | ⬜ Pending | | |
| Submission Ready | | ⬜ Pending | | |

### Status Legend
- ⬜ Pending
- 🔄 In Progress  
- ✅ Complete
- ⏸️ Blocked
```

### 4. Create Decision Log

Create `8_Project_Management/decision_log.md`:

```markdown
# Decision Log

## Project: [PROJECT_NAME]

| # | Date | Decision | Rationale | Alternatives Considered | Impact |
|---|------|----------|-----------|------------------------|--------|
| | | | | | |
```

### 5. Initialize Research Diary

Ensure `0_Project_Admin/research_diary.md` exists with project header.

---

## When to RE-RUN This Workflow

| Scenario | Action |
|----------|--------|
| Files deleted accidentally | Re-run to recreate |
| New project in same folder | Re-run with new project name |
| Switching to old project | DO NOT re-run (files exist) |
| After /init on new session | Auto-check triggers this if needed |

---

// turbo-all
All steps in this workflow can be auto-run as they only create files.

---

## Post-Execution Checklist

- [ ] 4 files exist in 8_Project_Management/
- [ ] research_diary.md has project header
- [ ] All files have correct project name
