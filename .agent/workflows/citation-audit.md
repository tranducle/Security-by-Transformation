---
description: Audit citations and fix BibTeX references
---

# Citation Audit Workflow (SOP_CITATION_AUDIT + SOP_BIBTEX_OPTIMIZATION)

**Use when:** Final check of all citations before submission.

---

## Step 1: Citation Inventory

List all citations in manuscript:

- Extract all `[@...]` or `\cite{...}` references
- Count total citations
- Check against bibliography

---

## Step 2: Hallucination Detection

Verify each citation exists using ALL 4 academic databases:

```python
from src.tools.literature_tools import (
    search_openalex_sync,
    search_google_scholar,
    search_scopus_sync,
    search_semantic_scholar_sync,
    lookup_doi,
)
# For each citation, verify:
# 1. Paper exists (search across all 4 databases)
# 2. Authors match
# 3. Year correct
# 4. Journal/venue accurate
```

---

## Step 3: Quality Assessment

Rate citation quality:

| Criterion | Check |
|-----------|-------|
| Recency | Published within 5 years? |
| Relevance | Directly supports claim? |
| Authority | Peer-reviewed source? |
| Availability | Accessible to readers? |

---

## Step 4: BibTeX Optimization

Fix BibTeX entries:

### Missing DOIs

```python
from src.tools.literature_tools import doi_to_bibtex, lookup_doi
from src.tools.literature_tools import (
    search_openalex_sync,
    search_semantic_scholar_sync,
)
# Find missing DOIs by searching OpenAlex and Semantic Scholar
# Then generate BibTeX entries
```

### Entry Completeness

Ensure all entries have:

- Author
- Title
- Journal/booktitle
- Year
- DOI (if available)
- Pages (if applicable)

---

## Step 5: Consistency Check

Verify consistency:

- Author name format (First Last vs Last, First)
- Journal name style (abbreviated vs full)
- URL formatting
- No duplicate entries

---

## Step 6: Citation Style

Match journal requirements:

- APA, IEEE, ACM, Harvard, etc.
- In-text format
- Reference list format

---

## Step 7: Final Bibliography

Produce cleaned `references.bib`:

- All entries complete
- DOIs added
- Consistent formatting
- No duplicates

---

## Step 8: BibTeX Optimization Algorithm

Automatically find missing DOIs and enrich BibTeX entries:

```bash
python src/tools/bibtex_optimizer.py 7_Manuscript_Draft/references_clean.bib
```

This tool:

1. Identifies missing DOIs
2. Queries OpenAlex, Semantic Scholar, Scopus & CrossRef
3. Updates entries with official metadata
4. Generates an optimization report

---

## Output Artifacts

| File | Location |
|------|----------|
| citation_audit.md | 7_Manuscript_Draft/ |
| references.bib (cleaned) | 7_Manuscript_Draft/ |

---



---

## Agent Routing

> **Primary Agent**: `BibTeXOptimizer`
> Load agent config: `agents/BibTeXOptimizer.json`

## Trigger Phrases

- "Check my citations"
- "Audit references"
- "Fix BibTeX file"

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
