---
description: Design surveys and questionnaires for qualitative research
---

# Survey Design Workflow (SOP_QUAL_STUDY)

**Use when:** Creating surveys, questionnaires, or interview protocols.

---

## Step 1: Research Protocol

Define the qualitative approach:

- Survey research
- Interview study
- Focus groups
- Mixed methods

---

## Step 2: Instrument Development

### 2.1 Question Types

- Demographic questions
- Likert scale items (5-point, 7-point)
- Open-ended questions
- Multiple choice
- Ranking questions

### 2.2 Scale Development

| Construct | Items | Scale Type | Source/Adapted |
|-----------|-------|------------|----------------|
| [Construct 1] | 5 items | 7-point Likert | [Citation] |

### 2.3 Question Wording

- Clear and unambiguous
- Avoid leading questions
- Appropriate reading level

---

## Step 3: Validity & Reliability

### Content Validity

- Expert review
- Pilot testing

### Construct Validity

- Exploratory Factor Analysis (EFA)
- Confirmatory Factor Analysis (CFA)

### Reliability

- Cronbach's alpha target: > 0.7
- Test-retest reliability

---

## Step 4: Sampling Strategy

- Target population
- Sample size calculation
- Recruitment method
- Inclusion/exclusion criteria

---

## Step 5: Data Collection

- Survey platform (Qualtrics, Google Forms, etc.)
- Distribution channels
- Response monitoring
- Follow-up reminders

---

## Step 6: Qualitative Analysis

### For Open-Ended Responses

- Thematic coding
- Grounded theory approach
- Inter-rater reliability

### For Quantitative Items

- Descriptive statistics
- Factor analysis
- Reliability analysis

---

## Step 7: Synthesis

Integrate qualitative and quantitative findings:

- Theme identification
- Pattern analysis
- Quotation selection

---

## Output Artifacts

| File | Location |
|------|----------|
| survey_instrument.md | 4_Methodology_Design/ |
| codebook.md | 4_Methodology_Design/ |
| thematic_analysis.md | 6_Analysis_Results/ |

---



---

## Agent Routing

> **Primary Agent**: `SurveyDesignerAnalyst`
> Load agent config: `agents/SurveyDesignerAnalyst.json`

## Trigger Phrases

- "Design a survey for [TOPIC]"
- "Create questionnaire"
- "Interview protocol for [RESEARCH]"

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
