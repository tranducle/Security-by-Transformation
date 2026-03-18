---
description: Conduct a literature search on a research topic using the agent system
---

# Literature Search Workflow

This workflow uses the Research Agent System to find academic papers on a topic.

## Prerequisites

- Research API keys available in `.env` (SERPAPI_KEY, SEMANTIC_SCHOLAR_KEY, SCOPUS_API_KEY)
- Python dependencies installed

## Steps

### 1. Understand the Query

Parse the user's request to extract:

- **Topic**: Main research topic
- **Year range**: If specified (e.g., 2023-2025)
- **Discipline**: If specified (e.g., computer science, medicine)
- **Limit**: Number of papers desired (default 10)

### 2. Execute Multi-Database Search

Search ALL 4 academic databases for comprehensive coverage:

```python
from src.tools.literature_tools import (
    search_openalex_sync,
    search_google_scholar,
    search_scopus_sync,
    search_semantic_scholar_sync,
    format_papers_as_markdown,
)

query = "QUERY_HERE"

# Search all 4 databases
openalex_papers = search_openalex_sync(query, limit=10)
scholar_papers = search_google_scholar(query, limit=10)
scopus_papers = search_scopus_sync(query, limit=10)
semantic_papers = search_semantic_scholar_sync(query, limit=10)
```

**Database priority order:**
1. **OpenAlex** — Broadest open coverage
2. **Google Scholar** — Widest reach including grey literature
3. **Scopus** — High-quality peer-reviewed sources
4. **Semantic Scholar** — AI/CS-focused with citation graphs

### 3. Deduplicate & Merge

Combine results from all databases, removing duplicates by DOI or title similarity.

### 4. Save Results

Save the search results to the appropriate directory:

- `2_Literature_Review/search_results_TOPIC.md` - Markdown summary
- `2_Literature_Review/search_results_TOPIC.json` - Full JSON data

### 5. Synthesize (Optional)

If user requests synthesis, route to `DeepSynthesizer` agent:

- Analyze themes across papers
- Identify research gaps
- Generate summary report

## Output Format

Return results as:

1. **Summary table**: Title, Authors, Year, Citations, Source Database
2. **Key themes**: Common topics across papers
3. **Recommended reads**: Top 3-5 most relevant papers

## Example Usage

User: "Find papers on federated learning in healthcare from 2023-2025"

Action:

```python
openalex_papers = search_openalex_sync("federated learning healthcare privacy", limit=15)
scholar_papers = search_google_scholar("federated learning healthcare privacy", limit=15)
scopus_papers = search_scopus_sync("federated learning healthcare privacy", limit=15)
semantic_papers = search_semantic_scholar_sync("federated learning healthcare privacy", limit=15)
```

---

## 📋 Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if "Literature Review" milestone changed
> 3. For key findings, add to `0_Project_Admin/research_diary.md`
>
> **Quick command**: Run `/sync` to update all files at once.
