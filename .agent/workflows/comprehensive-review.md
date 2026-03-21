---
description: Comprehensive peer review simulation using SOP_COMPREHENSIVE_REVIEW — reviewer simulation, rigor audit, and rebuttal preparation
---

# Comprehensive Review Workflow (SOP_COMPREHENSIVE_REVIEW)

**Use when:** You want a full simulated peer review process — multiple reviewer personas, rigor auditing, and pre-prepared rebuttal strategies.

---

## Step 1: Standard Peer Review

> **Agent:** `PeerReviewer`

- Assess originality and contribution
- Evaluate methodology soundness
- Check evidence quality and completeness
- Review writing quality and organization
- Score overall recommendation (accept/minor/major/reject)

---

## Step 2: Harsh Reviewer Simulation

> **Agents:** `ReviewerSimulator` + `HarshReviewer`

Simulate adversarial reviewers:

- **Reviewer 2** (skeptical methodologist)
- **Reviewer 3** (domain expert looking for gaps)
- **Area Chair** (assessing fit and significance)

For each persona:
- Generate specific criticisms
- Identify weakest arguments
- Flag potential fatal flaws
- Score using venue-specific criteria

---

## Step 3: Rigor & Soundness Audit

> **Agent:** `FeasibilityRigorSoundnessChecker`

- Verify experimental rigor against standards
- Check statistical soundness
- Assess reproducibility
- Evaluate threat to validity
- Score feasibility of claimed results

---

## Step 4: Response Strategy

> **Agent:** `ReviewerStrategist`

- Organize criticisms by severity (critical, major, minor)
- Draft point-by-point rebuttal templates
- Identify manuscript changes needed
- Create revision priority matrix
- Draft response letter framework

---

## Output Artifacts

| File | Location |
|------|----------|
| peer_review.md | 8_Project_Management/reviews/ |
| simulated_reviews.md | 8_Project_Management/reviews/ |
| rigor_audit.md | 8_Project_Management/reviews/ |
| rebuttal_strategy.md | 8_Project_Management/reviews/ |

---

## Agent Routing

> **Pipeline**: `PeerReviewer` → `ReviewerSimulator` / `HarshReviewer` → `FeasibilityRigorSoundnessChecker` → `ReviewerStrategist`

## Trigger Phrases

- "Comprehensive review"
- "Full review simulation"
- "Simulate all reviewers"
- "Pre-submission review"
- "Review and prepare rebuttal"

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
