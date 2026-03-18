---
description: Write complete manuscript from outline to submission-ready paper
---

# Write Paper Workflow (SOP_MANUSCRIPT_PREP)

**Use when:** Writing a complete academic paper.

---

## Step 1: Outline Verification

Load or create paper outline:

- If exists: Load from `7_Manuscript_Draft/paper_outline.md`
- If not: Run `/paper-outline` first

---

## Step 2: Venue Selection

Select target journal/conference:

- Impact factor consideration
- Scope alignment
- Formatting requirements
- Open access options
- Timeline requirements

---

## Step 3: Format Selection

Choose output format:

- **Markdown:** For flexibility, easy editing
- **LaTeX:** For formal publication, precise formatting

If LaTeX:

- Download journal template
- Set up document structure

---

## Step 4: Section-by-Section Writing

Write each section with citation checks:

### For Each Section

1. Draft section content
2. Search for citations using ALL 4 databases:
   - `search_openalex_sync` — Broadest open coverage
   - `search_google_scholar` — Widest reach
   - `search_scopus_sync` — Peer-reviewed quality
   - `search_semantic_scholar_sync` — Citation graphs
3. Insert citations as `(Author, Year)` in-text format
4. Verify citations exist using `lookup_doi`
5. Generate BibTeX entries using `doi_to_bibtex`
6. Update `references.bib`

```python
from src.tools.literature_tools import (
    search_openalex_sync,
    search_google_scholar,
    search_scopus_sync,
    search_semantic_scholar_sync,
)
from src.tools.literature_tools import lookup_doi, doi_to_bibtex
# Search, verify, and add citations for each claim
```

---

## Step 5: Writing Order (Recommended)

1. **Methods** - Most concrete, write first
2. **Results** - Report findings
3. **Discussion** - Interpret results
4. **Introduction** - Now you know your story
5. **Conclusion** - Summarize
6. **Abstract** - Final distillation
7. **Title** - Capture essence

---

## Step 6: Style Polishing

Improve writing quality:

- Clarity and conciseness
- Academic tone
- Active voice where appropriate
- Consistent terminology
- Transition between sections

---

## Step 7: Citation Audit

Final citation verification:

- All claims supported
- No hallucinated references
- BibTeX entries complete
- DOIs verified

---

## Step 8: Internal Review

Self-critique:

- Logical flow
- Argument strength
- Evidence sufficiency
- Contribution clarity

---

## Step 9: Pre-Submission Hardening (Recommended)

Before submission, harden your paper with specialized agents:

- Run `/harden-paper` to activate the full `SOP_PAPER_HARDENING` pipeline (10 agents)
- Or run individual agents:
  - `CitationVulnerabilityScanner` — Check citation-claim mismatches
  - `StatisticalSanityProsecutor` — Audit statistical methods
  - `TerminologyDriftDetector` — Fix terminology drift
  - `ScopeCreepGuillotine` — Cut unfocused content
  - `ScholarlyToneEqualizer` — Calibrate epistemic tone
  - `SubmissionPersonaSimulator` — Simulate reviewer personas
  - `TableCompressionEngine` — Consolidate redundant tables
  - `EquationReadabilityInspector` — Audit equation necessity
  - `AppendixValueSorter` — Optimize main vs appendix

---

## Output Artifacts

| File | Location |
|------|----------|
| manuscript.md / manuscript.tex | 7_Manuscript_Draft/ |
| references.bib | 7_Manuscript_Draft/ |
| figures/ | 7_Manuscript_Draft/ |

---

## 📋 Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` (mark "First Draft" or section complete)
> 3. For methodology/direction decisions, update `8_Project_Management/decision_log.md`
>
> **Quick command**: Run `/sync` to update all files at once.

---

## Trigger Phrases

- "Write my paper"
- "Draft manuscript for [TOPIC]"
- "Help me write the [SECTION] section"
