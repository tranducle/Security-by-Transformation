---
description: End-to-end research cycle from idea discovery to hardened paper — chains 5 SOPs and 17+ agents into a complete research pipeline
---

# Full Research Cycle Workflow

**Use when:** You want to run the entire research lifecycle from zero — idea → literature → plan → paper → hardened submission.

> ⚠️ **This is a mega-workflow.** It chains 5 SOPs together. Each phase requires user approval before proceeding to the next.

---

## Phase 1: Idea Discovery (SOP_IDEA_DISCOVERY)

> **Agents:** `JournalIdeaScout` → `ResearchScoper`

1. Analyze target journal trends and generate 3-5 research ideas
2. User selects one idea
3. Develop scope, research questions, and working title

**Gate:** User approves research scope before proceeding

---

## Phase 2: Gap Analysis (SOP_GAP_ANALYSIS)

> **Agents:** `LiteratureHunter` → `GapScout` → `GapMapperResearchOpportunityExtractor` → `MissingPartSuggester`

1. Search ALL 4 academic databases (OpenAlex, Google Scholar, Scopus, Semantic Scholar)
2. Identify research gaps and opportunities
3. Validate novelty of selected idea against gaps found
4. Auto-update research diary

**Gate:** User confirms gap analysis and research direction

---

## Phase 3: Research Planning (SOP_RESEARCH_PLAN_CREATION)

> **Agents:** `ResearchPlanGenerator` → `ProjectPlanner` → `ProjectStateKeeper`

1. Create comprehensive research plan with WBS
2. Define milestones and timeline
3. Resource and feasibility assessment
4. Initialize project tracking

**Gate:** User approves research plan

---

## Phase 4: Manuscript Preparation (SOP_MANUSCRIPT_PREP)

> **Agents:** `PaperOutlineArchitect` → `PublicationReadyWriter` / `LatexPaperGenerator` → `PaperWriter` → `CitationIntegrityAuditor` → `WritingStylePolisher`

1. Create paper outline (GATE 2: required before writing)
2. Select venue and format (MD or LaTeX)
3. Draft all sections with per-section citation checks
4. Polish writing style and consistency
5. Full citation audit

**Gate:** User reviews manuscript draft

---

## Phase 5: Paper Hardening (SOP_PAPER_HARDENING)

> **Agents:** `PaperIdentityArchitect` → `NoveltyDeltaCartographer` → `HiddenAssumptionAssassin` → `MinimalDecisiveExperimentDesigner` → `ClaimEvidenceLedger` → `GeneralizationBreaker` → `NegativeResultsAlchemist` → `ReproducibilityForensicsInvestigator` → `ReviewerWarGamer` → `CrossDisciplinaryImportSmuggler`

1. Full 10-agent hardening pipeline
2. Generate comprehensive hardening report
3. Apply recommended revisions

---

## Total Agent Count: 17-20+ agents across 5 phases

## Output Artifacts

| File | Phase | Location |
|------|-------|----------|
| research_ideas.md | 1 | 1_Strategic_Plan/ |
| research_gaps.md | 2 | 2_Literature_Review/ |
| research_plan.md | 3 | 1_Strategic_Plan/ |
| paper_outline.md | 4 | 7_Manuscript_Draft/ |
| manuscript.md/tex | 4 | 7_Manuscript_Draft/ |
| hardening_report.md | 5 | 8_Project_Management/ |

---

## Trigger Phrases

- "Full research cycle"
- "End-to-end research"
- "Complete research pipeline"
- "Research from scratch"
- "Zero to paper"

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
