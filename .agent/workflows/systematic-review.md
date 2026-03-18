---
description: Systematic Literature Review following PRISMA protocol
---

# Systematic Literature Review Workflow (SOP_SYSTEMATIC_REVIEW)

**Use when:** Conducting a formal systematic literature review for publication.

---

## Prerequisites

- Defined research question or topic
- Project directory with SDP structure

---

## Step 1: Protocol Design

Design the SLR protocol using PRISMA guidelines:

1. Define inclusion/exclusion criteria
2. Specify databases to search (OpenAlex, Google Scholar, Scopus, Semantic Scholar)
3. Set date range (recommend: last 5 years minimum)
4. Define quality assessment criteria

**Output:** `2_Literature_Review/slr_protocol.md`

---

## Step 2: Literature Search

Execute multi-database search across ALL 4 academic databases:

```python
from src.tools.literature_tools import (
    search_openalex_sync,
    search_google_scholar,
    search_scopus_sync,
    search_semantic_scholar_sync,
    format_papers_as_markdown,
)

query = "[QUERY]"

# Search all 4 databases for comprehensive coverage
openalex_papers = search_openalex_sync(query, limit=100)
scholar_papers = search_google_scholar(query, limit=100)
scopus_papers = search_scopus_sync(query, limit=100)
semantic_papers = search_semantic_scholar_sync(query, limit=100)
```

**Search Strategy:**

- **OpenAlex** — Broadest open access coverage
- **Google Scholar** — Widest reach including grey literature
- **Scopus** — High-quality peer-reviewed sources
- **Semantic Scholar** — AI/CS-focused with citation graphs
- Grey literature (industry reports, white papers)
- Backward/forward citation chaining

**Output:** `2_Literature_Review/search_results.md`, `2_Literature_Review/references.bib`

---

## Step 3: Screening & Selection

### 3.1 Title/Abstract Screening

- Apply inclusion/exclusion criteria
- Document reasons for exclusion

### 3.2 Full-Text Review

- Retrieve full texts of included papers
- Second-round screening

**Output:** `2_Literature_Review/prisma_flowchart.md`

---

## Step 4: Citation Verification

Verify source authenticity:

- Check DOIs are valid
- Verify paper existence
- Flag potential hallucinations

```python
from src.tools import lookup_doi
# Verify each citation
```

---

## Step 5: Data Extraction & Analysis

### 5.1 Create Extraction Matrix

| Paper | Year | Method | Sample | Key Findings | Quality Score |
|-------|------|--------|--------|--------------|---------------|

### 5.2 Thematic Synthesis

- Group by themes
- Identify patterns
- Note contradictions

**Output:** `2_Literature_Review/extraction_matrix.md`

---

## Step 6: Synthesis & Reporting

### 6.1 Narrative Synthesis

- Summarize findings by theme
- Discuss methodological quality
- Identify gaps

### 6.2 Dialectical Analysis (Optional)

- Present thesis/antithesis perspectives
- Synthesize balanced view

**Output:** `2_Literature_Review/synthesis_report.md`

---

## Step 7: Quality Audit

Final review of the SLR:

- Check PRISMA compliance
- Verify all citations
- Peer review the synthesis

---

## Output Artifacts

| File | Location | Purpose |
|------|----------|---------|
| slr_protocol.md | 2_Literature_Review/ | Protocol design |
| search_results.md | 2_Literature_Review/ | Raw search output |
| references.bib | 2_Literature_Review/ | All citations |
| prisma_flowchart.md | 2_Literature_Review/ | Selection process |
| extraction_matrix.md | 2_Literature_Review/ | Data extraction |
| synthesis_report.md | 2_Literature_Review/ | Final synthesis |

---



---

## Agent Routing

> **Primary Agent**: `SLRProtocolDroid`
> Load agent config: `agents/SLRProtocolDroid.json`

## Trigger Phrases

- "Do a systematic review on [TOPIC]"
- "PRISMA review for [TOPIC]"
- "Systematic literature review"

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
