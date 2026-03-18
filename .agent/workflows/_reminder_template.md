---
description: Standard reminder template to append to all workflows
---

# Standard Post-Workflow Reminder

**COPY THIS SECTION TO THE END OF EVERY WORKFLOW:**

```markdown
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

---
```

## Workflows That Need This Reminder

### HIGH PRIORITY (Major outputs)

- [x] `/project-kickoff` - Already has reminder
- [ ] `/write-paper`
- [ ] `/literature-search`
- [ ] `/experiment-design`
- [ ] `/paper-outline`
- [ ] `/research-plan`

### MEDIUM PRIORITY (Significant work)

- [ ] `/gap-analysis`
- [ ] `/systematic-review`
- [ ] `/peer-review`
- [ ] `/citation-audit`
- [ ] `/threat-model`

### LOW PRIORITY (Quick tasks)

- [ ] `/figures`
- [ ] `/brainstorm`
- [ ] `/find-dataset`
