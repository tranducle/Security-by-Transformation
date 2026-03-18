---
description: Create paper outline from research artifacts
---

# Paper Outline Workflow (SOP_PAPER_OUTLINE)

**Use when:** You have research artifacts and need a structured paper outline.

---

## Step 1: Artifacts Verification

Check that you have:

- [ ] Research questions/objectives
- [ ] Literature review completed
- [ ] Methodology defined
- [ ] Data collected/analyzed
- [ ] Key findings documented

---

## Step 2: Structure Selection

Choose paper structure based on discipline:

### Standard IMRAD

1. Introduction
2. Methods
3. Results
4. Discussion

### Extended Structure

1. Introduction
2. Background/Literature
3. Methodology
4. Results
5. Discussion
6. Conclusion

### Design Science

1. Introduction
2. Related Work
3. Design & Implementation
4. Evaluation
5. Discussion
6. Conclusion

---

## Step 3: Hierarchical Outline

Create detailed outline with subsections:

```markdown
# 1. Introduction
## 1.1 Problem Statement
## 1.2 Research Questions
## 1.3 Contributions
## 1.4 Paper Organization

# 2. Literature Review
## 2.1 Theme 1
### 2.1.1 Sub-theme
## 2.2 Theme 2
## 2.3 Research Gap

# 3. Methodology
## 3.1 Research Design
## 3.2 Data Collection
## 3.3 Analysis Methods
...
```

---

## Step 4: Artifact Mapping

Map existing artifacts to sections:

| Section | Artifact Source |
|---------|----------------|
| Abstract | 6_Analysis_Results/key_findings.md |
| Lit Review | 2_Literature_Review/synthesis.md |
| Methodology | 4_Methodology_Design/protocol.md |
| Results | 6_Analysis_Results/analysis.md |

---

## Step 5: User Review

Present outline for approval:

- Structure appropriate?
- Missing sections?
- Balance between sections?
- Flow logical?

---

## Step 6: Refinement

Based on feedback:

- Adjust section order
- Add/remove subsections
- Clarify section purposes

---

## Output Artifacts

| File | Location |
|------|----------|
| paper_outline.md | 7_Manuscript_Draft/ |
| artifact_map.md | 7_Manuscript_Draft/ |

---



---

## Agent Routing

> **Primary Agent**: `PaperOutlineArchitect`
> Load agent config: `agents/PaperOutlineArchitect.json`

## Trigger Phrases

- "Create paper outline"
- "Structure my paper"
- "Outline for [TOPIC] paper"

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
