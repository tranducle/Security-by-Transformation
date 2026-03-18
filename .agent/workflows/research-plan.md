---
description: Create a detailed research plan with work breakdown
---

# Research Plan Creation Workflow (SOP_RESEARCH_PLAN_CREATION)

**Use when:** You have a research title and need a comprehensive plan.

---

## Prerequisites Check

Before creating the plan, verify you have:

- [ ] Research title
- [ ] Research questions
- [ ] Literature review (key papers)
- [ ] Identified gaps
- [ ] Novelty justification

**If missing prerequisites:** Run `/research-discovery` first.

---

## Step 1: Research Framing

### 1.1 Problem Statement

- What problem are you solving?
- Why is it important?
- Who benefits?

### 1.2 Research Questions

- RQ1: [Main question]
- RQ2: [Sub-question]
- RQ3: [Sub-question]

### 1.3 Objectives

- Primary objective
- Secondary objectives

---

## Step 2: Theoretical Framework

Define the theoretical foundation:

- Key theories/models used
- Conceptual framework diagram
- Hypotheses (if applicable)

---

## Step 3: Methodology Design

### 3.1 Research Design

- Type: Quantitative/Qualitative/Mixed
- Approach: Experimental/Survey/Case Study/Design Science

### 3.2 Data Collection

- Sources
- Sampling strategy
- Collection methods

### 3.3 Analysis Methods

- Statistical tests (if quant)
- Coding approach (if qual)
- Validation strategy

---

## Step 4: Work Breakdown Structure (WBS)

Create hierarchical task breakdown:

```markdown
## 1. Literature Review
### 1.1 Database Search
#### 1.1.1 Semantic Scholar
#### 1.1.2 Google Scholar
### 1.2 Synthesis
#### 1.2.1 Theme identification
#### 1.2.2 Gap mapping

## 2. Methodology
### 2.1 Design
#### 2.1.1 Variable definition
#### 2.1.2 Instrument development
...
```

---

## Step 5: Timeline (Gantt)

| Phase | Tasks | Duration | Start | End |
|-------|-------|----------|-------|-----|
| Phase 1: Foundation | Lit review, setup | 2 weeks | Week 1 | Week 2 |
| Phase 2: Collection | Data gathering | 4 weeks | Week 3 | Week 6 |
| Phase 3: Analysis | Processing, stats | 3 weeks | Week 7 | Week 9 |
| Phase 4: Writing | Draft, revision | 3 weeks | Week 10 | Week 12 |

---

## Step 6: Resource Planning

- Required tools/software
- Data access requirements
- Budget estimate (if applicable)
- Collaboration needs

---

## Step 7: Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data unavailable | Medium | High | Alternative sources |
| Time overrun | High | Medium | Buffer time |

---

## Output Artifacts

| File | Location |
|------|----------|
| research_plan.md | 1_Strategic_Plan/ |
| wbs.md | 1_Strategic_Plan/ |
| timeline.md | 8_Project_Management/ |
| risk_analysis.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `ResearchPlanGenerator`
> Load agent config: `agents/ResearchPlanGenerator.json`

## Trigger Phrases

- "Create research plan for [TITLE]"
- "Make a detailed plan"
- "Work breakdown structure for my research"

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
