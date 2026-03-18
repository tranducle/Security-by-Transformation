---
description: Research discovery workflow for projects without a specific title - comprehensive literature search, gap analysis, title proposal with novelty check
---
<!-- SOP: SOP_IDEA_DISCOVERY -->


# Research Discovery Workflow (SOP_RESEARCH_DISCOVERY)

**Use when:** User wants to start a research project but does NOT have a specific research title yet.

---

## Prerequisites

- User provides a **broad topic area** (e.g., "healthcare cybersecurity", "federated learning in IoT")
- Project directory created with SDP structure

---

## Step 1: Comprehensive Literature Search (5 Recent Years)

### 1.1 Academic Database Search

Search these sources for papers from the last 5 years:

```python
from src.tools import (
    search_openalex_sync,
    search_google_scholar,
    search_scopus_sync,
    search_semantic_scholar_sync,
    format_papers_as_markdown,
)

query = "[USER_TOPIC]"
# Search ALL 4 academic databases (Academic-First Policy)
openalex_papers = search_openalex_sync(query, limit=50)
scholar_papers = search_google_scholar(query, limit=50)
scopus_papers = search_scopus_sync(query, limit=50)
semantic_papers = search_semantic_scholar_sync(query, limit=50, year_from=2020)
```

### 1.2 General Web Search

Search for industry reports, white papers, practitioner insights:

- Search: "[USER_TOPIC] trends 2024 2025"
- Search: "[USER_TOPIC] challenges industry report"
- Search: "[USER_TOPIC] state of the art review"

### 1.3 Save Results

- Save to: `2_Literature_Review/literature_search_results.md`
- Create: `2_Literature_Review/references.bib` with all citations

---

## Step 2: Compare, Synthesize, Summarize

### 2.1 Create Literature Matrix

| Paper | Year | Method | Key Finding | Gap Mentioned |
|-------|------|--------|-------------|---------------|
| ... | ... | ... | ... | ... |

### 2.2 Identify Themes

Group papers by:

- Methodology used
- Sub-topics addressed
- Types of contributions (framework, empirical, tool)

### 2.3 Synthesis Document

- Save to: `2_Literature_Review/literature_synthesis.md`
- Include: Key trends, dominant methodologies, emerging topics

---

## Step 3: Research Gap Analysis

### 3.1 Gap Identification

Analyze literature for:

- **Methodological gaps**: What methods haven't been applied?
- **Contextual gaps**: What contexts/domains unexplored?
- **Temporal gaps**: What's outdated and needs updating?
- **Theoretical gaps**: What theories not yet integrated?

### 3.2 Gap Prioritization

Rate each gap:

- Significance (1-5)
- Feasibility (1-5)
- Novelty potential (1-5)

### 3.3 Save Results

- Save to: `2_Literature_Review/research_gaps.md`

---

## Step 4: Propose Research Titles

### 4.1 Generate Title Candidates

Based on top 3-5 gaps, propose:

- 5-7 potential research titles
- For each title:
  - Gap addressed
  - Potential contribution
  - Methodology hint
  - Why novel

### 4.2 Format

```markdown
## Proposed Title 1: [TITLE]
- **Gap Addressed:** ...
- **Contribution:** ...
- **Method:** ...
- **Novelty Justification:** ...
```

### 4.3 Save Results

- Save to: `1_Strategic_Plan/proposed_titles.md`

---

## Step 5: Novelty Check

### 5.1 Per-Title Search

For EACH proposed title, search:

```
"[exact title keywords]" OR "[key concept 1]" AND "[key concept 2]"
```

### 5.2 Prior Art Analysis

Check if similar work exists:

- If YES: Document overlap, differentiate or drop title
- If NO: Strong novelty indicator

### 5.3 Update Titles

- Remove duplicated ideas
- Strengthen differentiation for retained titles

### 5.4 Save Results

- Update: `1_Strategic_Plan/proposed_titles.md` with novelty analysis

---

## Step 6: Final Title Selection (3 Options)

### 6.1 Present to User

Present exactly 3 titles with:

- Full title
- Research questions (2-3 each)
- Expected contribution
- Feasibility assessment
- Novelty confidence (High/Medium/Low)

### 6.2 User Decision

Ask user to:

- Select one title, OR
- Request more research on specific direction

---

## Step 7: Detailed Research Plan

### 7.1 If User Selects Title

Create detailed plan with subsubsubsection level:

```markdown
# Research Plan: [SELECTED TITLE]

## 1. Introduction
### 1.1 Background
#### 1.1.1 Problem Context
##### 1.1.1.1 Industry Statistics
##### 1.1.1.2 Current Solutions
#### 1.1.2 Research Motivation
...
```

### 7.2 Plan Components

- Research Questions
- Theoretical Framework
- Methodology (with substeps)
- Data Collection Plan
- Analysis Plan
- Expected Outcomes
- Timeline (Gantt chart description)
- Risk Analysis

### 7.3 Save Results

- Save to: `1_Strategic_Plan/detailed_research_plan.md`
- Update: `2_Literature_Review/references.bib`

---

## Output Artifacts

| File | Location | Purpose |
|------|----------|---------|
| `literature_search_results.md` | 2_Literature_Review/ | Raw search results |
| `references.bib` | 2_Literature_Review/ | All citations |
| `literature_synthesis.md` | 2_Literature_Review/ | Themes & trends |
| `research_gaps.md` | 2_Literature_Review/ | Identified gaps |
| `proposed_titles.md` | 1_Strategic_Plan/ | Title proposals |
| `detailed_research_plan.md` | 1_Strategic_Plan/ | Final plan |

---



---

## Agent Routing

> **Primary Agent**: `LiteratureHunter`
> Load agent config: `agents/LiteratureHunter.json`

## Trigger Phrases

- "I want to start research on [TOPIC] but don't have a title"
- "Help me find a research topic in [AREA]"
- "What are the gaps in [FIELD]?"
- "I need research ideas for [DOMAIN]"

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
