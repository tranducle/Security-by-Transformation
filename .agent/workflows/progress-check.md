---
description: Check project progress against milestones
---

# Progress Check Workflow (SOP_PROGRESS_TRACKING)

**Use when:** Reviewing project status and milestones.

---

## Step 1: Milestone Review

Check current milestones:

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Lit Review Complete | Week 4 | ✓ Done | |
| Methodology Final | Week 6 | 🔄 In Progress | |
| Data Collection | Week 10 | ⏳ Pending | |

---

## Step 2: Task Status

Review active tasks:

- Completed since last check
- Currently in progress
- Blocked/waiting
- Not yet started

---

## Step 3: Artifact Inventory

Check deliverables:

| Deliverable | Location | Status |
|-------------|----------|--------|
| Literature synthesis | 2_Literature_Review/ | Complete |
| Methodology doc | 4_Methodology_Design/ | Draft |
| Data files | 5_Experiments/ | Not started |

---

## Step 4: Resource Check

Assess resources:

- Time: On track? Ahead? Behind?
- Tools: Everything available?
- Access: Data/resources accessible?
- Support: Help needed?

---

## Step 5: Risk Update

Review risks:

- New risks emerged?
- Existing risks changed?
- Mitigations working?

---

## Step 6: Log Update

Update project log:

- Progress summary
- Decisions made
- Issues encountered
- Next priorities

---

## Step 7: Reporting

Generate status report:

```markdown
## Weekly Progress Report

**Period:** [DATE RANGE]

### Completed
- [Item 1]
- [Item 2]

### In Progress
- [Item 3] - 70%

### Blockers
- None / [Description]

### Next Week Focus
- [Priority 1]
- [Priority 2]

### Overall Status: 🟢 On Track / 🟡 At Risk / 🔴 Behind
```

---

## Output Artifacts

| File | Location |
|------|----------|
| progress_report_YYYYMMDD.md | 8_Project_Management/ |
| project_log.md (updated) | 8_Project_Management/ |

---



---

## Agent Routing

> **Primary Agent**: `ProgressTracker`
> Load agent config: `agents/ProgressTracker.json`

## Trigger Phrases

- "Check project progress"
- "Status update"
- "Where are we on [PROJECT]?"

---

## 📋 Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if milestone status changed
> 3. Log significant decisions to `8_Project_Management/decision_log.md`
> 4. For major insights, update `0_Project_Admin/research_diary.md`
>
> **Quick command**: Run `/sync` to update all files at once.
