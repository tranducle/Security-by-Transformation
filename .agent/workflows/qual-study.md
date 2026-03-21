---
description: Conduct qualitative research studies using SOP_QUAL_STUDY — from protocol design through thematic analysis and synthesis
---

# Qualitative Study Workflow (SOP_QUAL_STUDY)

**Use when:** Conducting qualitative research — interviews, focus groups, case studies, or thematic analysis.

---

## Step 1: Research Protocol Design

> **Agent:** `MethodologyArchitect`

- Define qualitative methodology (grounded theory, phenomenology, ethnography, case study)
- Determine sampling strategy (purposeful, snowball, theoretical)
- Design data collection protocol
- Establish trustworthiness criteria (credibility, transferability, dependability, confirmability)
- Prepare IRB/ethics documentation

---

## Step 2: Instrument Design

> **Agent:** `SurveyDesignerAnalyst`

- Design interview guides or survey questionnaires
- Create semi-structured interview protocol
- Design Likert scale instruments (if mixed methods)
- Pilot test questions
- Validate instrument reliability

**For interviews:**
- Opening, core, and closing question sets
- Probing strategies
- Timeline and logistics

**For surveys:**
- Likert scale design
- EFA/CFA preparation
- Response validation rules

---

## Step 3: Qualitative Coding & Thematic Analysis

> **Agent:** `QualitativeCoder`

- Transcribe and organize data
- Open coding (initial codes)
- Axial coding (categories and relationships)
- Selective coding (core themes)
- Generate code book with definitions
- Inter-rater reliability check (if applicable)

**Analysis approaches:**
- Thematic analysis (Braun & Clarke)
- Grounded theory (Strauss & Corbin)
- Content analysis
- Narrative analysis

---

## Step 4: Synthesis & Reporting

> **Agent:** `DocumentSynthesizer`

- Synthesize findings into coherent narrative
- Create theme hierarchy with supporting quotes
- Generate conceptual framework/model
- Write findings section with thick description
- Discuss implications and transferability

---

## Output Artifacts

| File | Location |
|------|----------|
| qual_protocol.md | 4_Methodology_Design/ |
| interview_guide.md | 4_Methodology_Design/ |
| codebook.md | 6_Analysis_Results/ |
| thematic_analysis.md | 6_Analysis_Results/ |
| qual_findings.md | 7_Manuscript_Draft/ |

---

## Agent Routing

> **Primary Agent**: `MethodologyArchitect`
> **Pipeline**: `MethodologyArchitect` → `SurveyDesignerAnalyst` → `QualitativeCoder` → `DocumentSynthesizer`

## Trigger Phrases

- "Qualitative study"
- "Interview study"
- "Thematic analysis"
- "Grounded theory research"
- "Design interview protocol"
- "Qualitative coding"

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
