---
description: Prepare a paper for journal submission using 4 chained SOPs — hardening, citation audit, comprehensive review, and BibTeX optimization (15+ agents)
---

# Paper-to-Submission Workflow

**Use when:** Your manuscript draft is complete and you want to prepare it for journal submission through systematic hardening, citation verification, peer review simulation, and final polishing.

> ⚠️ **This is a mega-workflow.** It chains 4 SOPs into a submission-readiness pipeline.

---

## Phase 1: Paper Hardening (SOP_PAPER_HARDENING)

> **10 Agents** — Sequential hardening pipeline

1. **PaperIdentityArchitect** — Define contribution identity
2. **NoveltyDeltaCartographer** — Map novelty delta
3. **HiddenAssumptionAssassin** — Expose weak assumptions
4. **MinimalDecisiveExperimentDesigner** — Verify experiment sufficiency
5. **ClaimEvidenceLedger** — Audit claim-evidence alignment
6. **GeneralizationBreaker** — Test boundary conditions
7. **NegativeResultsAlchemist** — Transform limitations into insights
8. **ReproducibilityForensicsInvestigator** — Audit reproducibility
9. **ReviewerWarGamer** — Simulate reviewer attacks
10. **CrossDisciplinaryImportSmuggler** — Find cross-field strengtheners

**Output:** Hardening report with recommended revisions
**Action:** Apply critical revisions before proceeding

---

## Phase 2: Citation Audit (SOP_CITATION_AUDIT)

> **6 Agents** — 3-pass citation verification

For each of 3 passes:
1. `CitationIntegrityAuditor` — Deep audit of all citations
2. `GoogleScholarSearch` — Verify title/author accuracy
3. `SemanticSearch` — Verify DOI/citation graph
4. `ScopusSearch` — Verify venue/impact factor
5. `CitationVerifier` — Quality check per citation

Then:
6. `ReferenceManager` — Fix BibTeX entries

**Output:** Citation audit report + cleaned `references.bib`

---

## Phase 3: Comprehensive Review (SOP_COMPREHENSIVE_REVIEW)

> **4 Agents** — Multi-persona review simulation

1. `PeerReviewer` — Standard review
2. `HarshReviewer` — Adversarial Reviewer #2
3. `FeasibilityRigorSoundnessChecker` — Rigor audit
4. `ReviewerStrategist` — Pre-emptive rebuttal strategy

**Output:** Simulated reviews + rebuttal preparation

---

## Phase 4: Final Polish (SOP_BIBTEX_OPTIMIZATION + Polish)

> **2 Agents** — Final optimization

1. `BibTeXOptimizer` — Find missing DOIs, use doi2bib.org API
2. `WritingStylePolisher` — Final prose refinement

**Output:** Submission-ready manuscript

---

## Total Agent Count: 15-20+ agents across 4 phases

## Submission Checklist

- [ ] All hardening recommendations addressed
- [ ] Citations verified (3-pass audit)
- [ ] Simulated reviews addressed
- [ ] BibTeX optimized with DOIs
- [ ] Writing polished
- [ ] Format matches target venue
- [ ] Cover letter drafted
- [ ] Supplementary materials prepared

## Output Artifacts

| File | Phase | Location |
|------|-------|----------|
| hardening_report.md | 1 | 8_Project_Management/ |
| citation_audit.md | 2 | 8_Project_Management/ |
| references.bib | 2 | 7_Manuscript_Draft/ |
| simulated_reviews.md | 3 | 8_Project_Management/reviews/ |
| rebuttal_strategy.md | 3 | 8_Project_Management/reviews/ |
| final_manuscript | 4 | 7_Manuscript_Draft/ |

---

## Trigger Phrases

- "Prepare for submission"
- "Submission ready"
- "Final paper check"
- "Paper to submission"
- "Pre-submission pipeline"

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
