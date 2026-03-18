---
description: Write grant proposals and funding applications
---

# Grant Proposal Workflow (SOP_GRANT_APPLICATION)

**Use when:** Writing a grant proposal or funding application.

---

## Step 1: Funding Opportunity Analysis

Analyze the call:

- Funding agency priorities
- Eligibility requirements
- Budget constraints
- Timeline
- Evaluation criteria

---

## Step 2: Proposal Structure

Standard grant components:

### Executive Summary

- Problem significance
- Proposed solution
- Expected outcomes
- Budget overview

### Project Narrative

1. **Significance**
   - Problem importance
   - Literature gap
   - Potential impact

2. **Innovation**
   - Novel approach
   - Differentiation from prior work

3. **Approach**
   - Research design
   - Methodology
   - Timeline
   - Risk mitigation

4. **Preliminary Data** (if applicable)
   - Feasibility evidence
   - Pilot results

---

## Step 3: Budget Development

| Category | Amount | Justification |
|----------|--------|---------------|
| Personnel | $X | PI (Y% effort), RA (100%) |
| Equipment | $X | [Specific items] |
| Travel | $X | Conference presentations |
| Other | $X | Publication fees, etc. |
| Indirect | $X | University rate |
| **Total** | $XXX | |

---

## Step 4: Feasibility Assessment

Resource audit:

- Personnel available
- Equipment access
- Institutional support
- Collaboration needs

---

## Step 5: Writing & Polish

Draft each section:

- Clear and compelling narrative
- Specific and measurable objectives
- Realistic timeline
- Comprehensive risk mitigation

---

## Step 6: Compliance Check

Verify:

- Page limits respected
- Required sections included
- Format requirements met
- Signatures obtained

---

## Output Artifacts

| File | Location |
|------|----------|
| grant_narrative.md | 7_Manuscript_Draft/ |
| budget.md | 8_Project_Management/ |
| timeline.md | 8_Project_Management/ |

---



---

---

# Part 2: Paper-to-Program Grant Translation (SOP_GRANT_TRANSLATION)

**Use when:** Translating a completed research paper into a competitive grant proposal for NSF, NIH, DOE, or DoD.

---

## Phase 1: Paper Intake & Distillation

> **Agent:** `PaperToProgramDistiller` → `PaperToProgramGrantArchitect`

- Extract core scientific contributions
- Identify fundable kernels from published results
- Separate "what was done" from "what can be proposed"

## Phase 2: Grantability Triage

> **Agent:** `GrantabilityDiagnostician`

- Score paper readiness (1-5) across: novelty, feasibility, significance
- Identify gaps (preliminary data, broader impacts, scale)
- Generate Pre-Proposal Diagnostic Report

## Phase 3: Sponsor Fit Mapping

> **Agent:** `SponsorFitCartographer`

- Map paper to NSF divisions, NIH institutes, DOE offices, DoD BAAs
- Score fit per agency (1-5 match quality)
- Output: Sponsor Fit Matrix + recommended programs

## Phase 4: Program Expansion Architecture

> **Agent:** `ProgramExpansionArchitect`

- Transform single paper results into 3-5 year research program
- Design scalable future work (new datasets, domains, methods)
- Create Expansion Blueprint with milestone chain

## Phase 5: Specific Aims Composition

> **Agent:** `SpecificAimsComposer`

- Write 1-page Specific Aims per agency format
- Ensure each aim is independently fundable
- Verify no single-point-of-failure dependencies

## Phase 6: Innovation & Significance Reframing

> **Agent:** `InnovationSignificanceReframer`

- Reframe academic novelty as programmatic significance
- Position contribution using sponsor language
- Generate Innovation/Significance section drafts

## Phase 7: Workplan & Milestones

> **Agent:** `WorkplanMilestoneEngineer`

- Design detailed workplan with decision gates
- Create Gantt chart with go/no-go checkpoints
- Build risk mitigation protocols

## Phase 8: Broader Impacts Translation

> **Agent:** `BroaderImpactTranslator` + `BroaderImpactsConstructor`

- Convert academic contributions to societal impact
- Design workforce development plans
- Create K-12/URM engagement strategies

## Phase 9: Proposal Stress Testing

> **Agent:** `ProposalStressTester`

- Simulate NSF/NIH/DOE panel review
- Test each aim for independence and feasibility
- Generate attack vectors and defense strategies

## Phase 10: Final Packaging

> **Agent:** `PaperToProgramGrantArchitect` (Final Assembly)

- Compile all sections into agency-specific format
- Verify compliance with page limits and requirements
- Produce submission-ready package

---

## PPGA Output Artifacts

| File | Location |
|------|----------|
| diagnostic_report.md | 1_Strategic_Plan/grant_strategy/ |
| sponsor_fit_matrix.md | 1_Strategic_Plan/grant_strategy/ |
| specific_aims.md | 7_Manuscript_Draft/grant_drafts/ |
| grant_narrative.md | 7_Manuscript_Draft/grant_drafts/ |
| workplan_gantt.md | 8_Project_Management/grant_plans/ |
| broader_impacts.md | 7_Manuscript_Draft/grant_drafts/ |
| stress_test_report.md | 8_Project_Management/grant_plans/ |

---

## Agent Routing

### SOP_GRANT_APPLICATION (Simple)
> **Primary Agent**: `GrantProposalStrategist`
> Load agent config: `agents/GrantProposalStrategist.json`

### SOP_GRANT_TRANSLATION (Paper → Program)
> **Primary Agent**: `PaperToProgramGrantArchitect`
> Load agent config: `agents/PaperToProgramGrantArchitect.json`

## Trigger Phrases

### SOP_GRANT_APPLICATION
- "Write grant proposal for [TOPIC]"
- "Funding application"

### SOP_GRANT_TRANSLATION
- "Paper to grant", "paper to proposal"
- "PPGA", "grant architect"
- "Translate paper to NSF/NIH/DOE/DoD proposal"
- "Convert my paper to a fundable program"
- "Chuyển paper thành đề xuất tài trợ"

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
