---
description: Create daily/session research summary
---

# Daily Summary Workflow (SOP_DAILY_SUMMARY)

**Use when:** Ending a research session and need to document progress.

---

## Step 1: Session Review

Review what was accomplished:

- Files created/modified
- Decisions made
- Insights gained
- Questions raised

---

## Step 2: Summary Generation

Create summary document:

```markdown
# Research Session Summary
**Date:** [DATE]
**Duration:** [HOURS]

## Completed
- [Task 1]
- [Task 2]

## Key Insights
- [Insight 1]
- [Insight 2]

## Decisions Made
- [Decision 1]: [Rationale]

## Open Questions
- [Question 1]

## Next Steps
- [ ] [Action 1]
- [ ] [Action 2]
```

---

## Step 3: Artifact Update

Update project artifacts:

- Task checklist
- Timeline/milestones
- Research log

---

## Step 4: File Organization

Ensure files are properly organized:

- Named correctly
- In correct directories
- Version controlled (if applicable)

---

## Step 5: Log Entry

Append to project log:

```markdown
## [DATE]: [SESSION TITLE]

[Summary paragraph]

**Artifacts produced:**
- [artifact1.md]
- [artifact2.md]

**Status:** On track / Ahead / Behind
```

---

## Output Artifacts

| File | Location |
|------|----------|
| session_YYYYMMDD.md | 8_Project_Management/ |
| project_log.md (updated) | 8_Project_Management/ |

---



---

## Agent Routing

> **Primary Agent**: `ProjectStateKeeper`
> Load agent config: `agents/ProjectStateKeeper.json`

## Trigger Phrases

- "Summarize today's work"
- "End of session summary"
- "What did we accomplish?"

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
