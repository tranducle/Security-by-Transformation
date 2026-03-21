---
description: Generate synthesis reports from multiple sources using SOP_SYNTHESIS_REPORTING — gather, summarize, title, and format
---

# Synthesis Report Workflow (SOP_SYNTHESIS_REPORTING)

**Use when:** Combining findings from multiple sources into a coherent, publication-ready synthesis report.

---

## Step 1: Multi-Source Gathering

> **Agent:** `MultiSourceSynthesizer`

- Collect and organize source materials (papers, reports, data, notes)
- Identify overlapping themes and contradictions
- Create source comparison matrix
- Map evidence chains across sources

---

## Step 2: Summarization

> **Agent:** `SummarizerSynthesizer`

- Generate structured summaries per source
- Identify key findings, methods, and conclusions
- Create cross-source thematic summaries
- Highlight consensus and divergence points

---

## Step 3: Title & Abstract Generation

> **Agent:** `AbstractTitleGenerator`

- Generate compelling title options
- Write informative abstract
- Create executive summary
- Draft key takeaway bullets

---

## Step 4: Publication-Ready Formatting

> **Agent:** `PublicationReadyWriter`

- Format into publication-ready report
- Ensure academic writing standards
- Add proper citations and references
- Create table of contents
- Final polish and consistency check

---

## Output Artifacts

| File | Location |
|------|----------|
| synthesis_report.md | 6_Analysis_Results/ |
| executive_summary.md | 7_Manuscript_Draft/ |

---

## Agent Routing

> **Pipeline**: `MultiSourceSynthesizer` → `SummarizerSynthesizer` → `AbstractTitleGenerator` → `PublicationReadyWriter`

## Trigger Phrases

- "Synthesis report"
- "Combine sources into report"
- "Multi-source synthesis"
- "Synthesize findings"

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
