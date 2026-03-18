---
description: Identify research gaps in a field or topic
---

# Gap Analysis Workflow (SOP_GAP_ANALYSIS)

**Use when:** You want to identify research opportunities and gaps in existing literature.

---

## Step 1: Literature Foundation

Search existing research (5 years):

```python
from src.tools import (
    search_openalex_sync,
    search_google_scholar,
    search_scopus_sync,
    search_semantic_scholar_sync,
    format_papers_as_markdown,
)

query = "[TOPIC]"
# Search ALL 4 academic databases for comprehensive coverage
openalex_papers = search_openalex_sync(query, limit=50)
scholar_papers = search_google_scholar(query, limit=50)
scopus_papers = search_scopus_sync(query, limit=50)
semantic_papers = search_semantic_scholar_sync(query, limit=50, year_from=2020)
```

Also search:

- Web for industry reports and trends
- Recent conference proceedings
- PhD dissertations in the field

---

## Step 2: Boundary Mapping

Define the research landscape:

- What sub-areas exist?
- What methodologies dominate?
- What contexts have been studied?

**Create:** Research landscape map

---

## Step 3: Gap Identification

Analyze literature for gaps:

### Types of Gaps

| Gap Type | Question | Example |
|----------|----------|---------|
| **Methodological** | What methods haven't been applied? | "No qualitative studies on X" |
| **Contextual** | What settings unexplored? | "No studies in healthcare SMEs" |
| **Temporal** | What's outdated? | "Last study was 2018" |
| **Theoretical** | What theories not integrated? | "No game theory perspective" |
| **Population** | Who hasn't been studied? | "No focus on developing countries" |

---

## Step 4: Gap Prioritization

Rate each gap (1-5 scale):

| Gap | Significance | Feasibility | Novelty | Total |
|-----|--------------|-------------|---------|-------|
| Gap 1 | 5 | 4 | 4 | 13 |
| Gap 2 | 4 | 5 | 3 | 12 |

---

## Step 5: Opportunity Framing

For top 3-5 gaps, develop:

- Potential research questions
- Possible contributions
- Required resources
- Risk assessment

---

## Step 6: Innovation Suggestions

Generate research ideas to address gaps:

- What new approaches could work?
- What cross-disciplinary insights apply?
- What emerging technologies enable new research?

---

## Output Artifacts

| File | Location |
|------|----------|
| research_gaps.md | 2_Literature_Review/ |
| gap_prioritization.md | 1_Strategic_Plan/ |
| research_opportunities.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `GapScout`
> Load agent config: `agents/GapScout.json`

## Trigger Phrases

- "What are the research gaps in [FIELD]?"
- "Find gaps in [TOPIC]"
- "Research opportunities in [AREA]"

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
