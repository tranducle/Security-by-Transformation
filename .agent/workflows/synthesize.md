---
description: Synthesize information from multiple sources into coherent report
---

# Synthesis Report Workflow (SOP_SYNTHESIS_REPORTING)

**Use when:** Combining multiple sources into a unified report.

---

## Step 1: Source Gathering

Collect all sources:

- Academic papers
- Industry reports
- News articles
- Interview transcripts
- Meeting notes

---

## Step 2: Source Organization

Categorize sources:

| Source | Type | Key Topic | Quality |
|--------|------|-----------|---------|
| [Source 1] | Academic | [Topic] | High |
| [Source 2] | Industry | [Topic] | Medium |

---

## Step 3: Key Point Extraction

From each source, extract:

- Main arguments
- Supporting evidence
- Methodology used
- Conclusions
- Limitations

---

## Step 4: Theme Identification

Identify cross-cutting themes:

- Agreements across sources
- Contradictions
- Gaps in coverage
- Emerging patterns

---

## Step 5: Synthesis Writing

Create integrated narrative:

- Don't just summarize each source
- Weave sources together by theme
- Present balanced view
- Highlight consensus and debate

---

## Step 6: Title & Abstract

Generate:

- Compelling title
- Concise abstract/executive summary
- Key takeaways list

---

## Step 7: Formatting

Format for purpose:

- Executive summary for stakeholders
- Academic style for publication
- Report format for documentation

---

## Output Artifacts

| File | Location |
|------|----------|
| synthesis_report.md | 2_Literature_Review/ |
| source_matrix.md | 2_Literature_Review/ |

---



---

## Agent Routing

> **Primary Agent**: `DeepSynthesizer`
> Load agent config: `agents/DeepSynthesizer.json`

## Trigger Phrases

- "Synthesize these sources"
- "Create a summary report"
- "Combine findings from [SOURCES]"

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
