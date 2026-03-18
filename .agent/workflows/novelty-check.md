---
description: Check novelty of research idea against prior art
---

# Novelty Check Workflow (SOP_NOVELTY_DEFENSE)

**Use when:** You have a research idea and want to verify it's novel.

---

## Step 1: Define the Claim

Articulate your contribution clearly:

- What is your main claim?
- What method/approach are you proposing?
- What is unique about your work?

---

## Step 2: Prior Art Search

### Academic Search (All 4 Databases)

```python
from src.tools.literature_tools import (
    search_openalex_sync,
    search_google_scholar,
    search_scopus_sync,
    search_semantic_scholar_sync,
)

query = "[YOUR IDEA KEYWORDS]"

# Search all 4 databases for comprehensive prior art coverage
openalex_papers = search_openalex_sync(query, limit=50)
scholar_papers = search_google_scholar(query, limit=50)
scopus_papers = search_scopus_sync(query, limit=50)
semantic_papers = search_semantic_scholar_sync(query, limit=50)
```

### Patent Search

- Google Patents
- USPTO
- EPO (for Europe)

### Preprints & Working Papers

- arXiv
- SSRN
- ResearchGate

---

## Step 3: Similarity Analysis

For each similar work found:

| Paper | Similarity | Difference | Threat Level |
|-------|------------|------------|--------------|
| [Paper 1] | Method X similar | Different context | Medium |
| [Paper 2] | Same problem | Different approach | Low |

### Threat Levels

- **High:** Very similar, need to differentiate or pivot
- **Medium:** Partial overlap, need clear positioning
- **Low:** Related but distinct contribution

---

## Step 4: Differentiation Strategy

For high/medium threats, develop positioning:

1. **Contextual differentiation:** Different domain/population
2. **Methodological differentiation:** Different approach
3. **Scope differentiation:** Broader/narrower focus
4. **Temporal differentiation:** Updated/extended work

---

## Step 5: Contribution Positioning

Frame your unique contribution:

```markdown
## Contribution Statement

While [PRIOR WORK] addresses [X], our work differs in:
1. [DIFFERENCE 1]
2. [DIFFERENCE 2]

This is the first work to [UNIQUE CLAIM].
```

---

## Step 6: Rebuttal Preparation

Prepare for reviewer questions:

| Potential Critique | Pre-prepared Response |
|-------------------|----------------------|
| "Similar to [X]" | "We differ in..." |
| "Incremental" | "Novel aspects include..." |

---

## Output Artifacts

| File | Location |
|------|----------|
| prior_art_analysis.md | 2_Literature_Review/ |
| novelty_defense.md | 1_Strategic_Plan/ |
| rebuttal_preparation.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `PriorArtNoveltyScanner`
> Load agent config: `agents/PriorArtNoveltyScanner.json`

## Trigger Phrases

- "Check if [IDEA] is novel"
- "Has anyone done [RESEARCH]?"
- "Novelty check for my idea"
- "Prior art search"

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
