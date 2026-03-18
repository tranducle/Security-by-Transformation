---
description: Handle reviewer feedback and manuscript revision
---

# Manuscript Revision Workflow (SOP_MANUSCRIPT_REVISION)

**Use when:** You received reviewer comments and need to revise.

---

## Step 1: Load Documents

Gather all materials:

- Original manuscript
- Review decision letter
- Reviewer 1 comments
- Reviewer 2 comments
- (Additional reviewers if any)

---

## Step 2: Comment Classification

Categorize each comment:

| ID | Reviewer | Comment Summary | Type | Priority |
|----|----------|-----------------|------|----------|
| R1.1 | R1 | Needs more lit review | Major | High |
| R1.2 | R1 | Clarify methodology | Minor | Medium |
| R2.1 | R2 | Statistical concern | Major | Critical |

### Types

- **Major:** Requires substantial revision
- **Minor:** Easy fix
- **Clarification:** Needs explanation only
- **Discretionary:** Optional improvement

---

## Step 3: Revision Strategy

For each comment, decide:

- Accept: Implement as suggested
- Partial: Implement modified version
- Decline: Respectfully disagree (with justification)

---

## Step 4: Paragraph-by-Paragraph Revision

User provides paragraph to revise:

1. Receive original text
2. Identify relevant reviewer comments
3. Revise addressing comments
4. Document changes made

---

## Step 5: Response Letter Drafting

For each reviewer comment:

```markdown
## Reviewer 1, Comment 1

**Original Comment:**
[Quote the comment]

**Response:**
We thank the reviewer for this insightful comment. We have...

**Changes Made:**
Page X, Lines Y-Z: [Description of change]
```

---

## Step 6: Style Polish

Final revision pass:

- Consistency check
- Flow improvement
- Grammar/spelling
- Format compliance

---

## Step 7: Track Changes Document

Produce:

- Clean revised manuscript
- Track changes version
- Response letter

---

## Output Artifacts

| File | Location |
|------|----------|
| manuscript_v2.md | 7_Manuscript_Draft/ |
| response_letter.md | 7_Manuscript_Draft/ |
| revision_log.md | 8_Project_Management/ |

---



---

## Agent Routing

> **Primary Agent**: `ManuscriptReviser`
> Load agent config: `agents/ManuscriptReviser.json`

## Trigger Phrases

- "Revise based on reviewer comments"
- "Handle review feedback"
- "Prepare revision response"

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
