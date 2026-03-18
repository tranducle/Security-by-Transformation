---
description: Comprehensive peer review and critique of manuscripts
---

# Peer Review Workflow (SOP_COMPREHENSIVE_REVIEW)

**Use when:** You want thorough critique of your paper before submission.

---

## Step 1: Initial Review

Read the paper for:

- Overall impression
- Main argument
- Key contributions
- General issues

---

## Step 2: Detailed Critique

Section-by-section review:

### Title & Abstract

- Accurate representation?
- Key findings included?
- Searchable keywords?

### Introduction

- Problem clearly stated?
- Motivation compelling?
- Gap well-articulated?
- Contributions clear?

### Literature Review

- Comprehensive coverage?
- Recent papers included?
- Organized logically?
- Gap leads to RQ?

### Methodology

- Replicable?
- Appropriate for RQ?
- Limitations acknowledged?
- Rigorous design?

### Results

- Complete reporting?
- Appropriate statistics?
- Clear visualizations?
- Objective presentation?

### Discussion

- Results properly interpreted?
- Implications discussed?
- Limitations addressed?
- Comparison to prior work?

### Conclusion

- Summarizes key findings?
- Contributions restated?
- Future work suggested?

---

## Step 3: Harsh Reviewer Simulation

Imagine strictest Reviewer 2:

- What could they criticize?
- What's the weakest point?
- What might lead to rejection?

---

## Step 4: Rigor & Soundness Check

Verify:

- Logic validity
- Statistical correctness
- Claim-evidence alignment
- Internal consistency

---

## Step 5: Response Strategy

For each issue identified:

- Priority (critical, major, minor)
- Suggested fix
- Time estimate

---

## Step 6: Deep Analysis with Specialist Agents (Optional)

Run targeted specialist agents for deeper analysis:

- **MethodologicalConfounderHunter** — Find hidden confounders in experimental design
- **BaselineFairnessAuditor** — Audit baseline comparison fairness
- **CounterfactualReframer** — Generate counterfactual tests for claims
- **CitationVulnerabilityScanner** — Check citation-claim alignment
- **StatisticalSanityProsecutor** — Audit statistical rigor
- **FigureArgumentArchitect** — Assess if figures serve the argument
- **ScholarlyToneEqualizer** — Check epistemic calibration of language

Or run the full pipeline: `/harden-paper`

---

## Output Artifacts

| File | Location |
|------|----------|
| review_report.md | 7_Manuscript_Draft/ |
| revision_plan.md | 8_Project_Management/ |

---



---

## Agent Routing

> **Primary Agent**: `PeerReviewer`
> Load agent config: `agents/PeerReviewer.json`

## Trigger Phrases

- "Review my paper"
- "Critique this manuscript"
- "What would reviewers say?"

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
