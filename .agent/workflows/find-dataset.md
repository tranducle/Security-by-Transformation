---
description: Find datasets for research projects
---

# Dataset Discovery Workflow (SOP_DATA_ACQUISITION)

**Use when:** You need to find existing datasets for your research.

---

## Step 1: Requirements Definition

Define dataset requirements:

- Data type (tabular, text, images, time series)
- Domain (healthcare, security, finance, etc.)
- Size requirements
- Temporal requirements
- Access requirements (open, licensed, request-based)

---

## Step 2: Multi-Source Search

### Academic Repositories

- UCI Machine Learning Repository
- Kaggle Datasets
- Google Dataset Search
- Papers With Code Datasets
- Harvard Dataverse

### Domain-Specific

- Healthcare: MIMIC, PhysioNet, CMS
- Security: CICIDS, NSL-KDD, UNSW-NB15
- NLP: HuggingFace Datasets
- Computer Vision: ImageNet, COCO

### Government & Public

- data.gov
- EU Open Data Portal
- World Bank Data

---

## Step 3: Dataset Evaluation

For each candidate dataset:

| Criterion | Assessment |
|-----------|------------|
| Size | Sufficient for methodology? |
| Features | Contains required variables? |
| Quality | Missing values, outliers? |
| Recency | Up-to-date enough? |
| Access | Open or obtainable? |
| Documentation | Well-documented? |
| Ethics | IRB/consent issues? |

---

## Step 4: Feasibility Check

Verify methodology compatibility:

- Can proposed methods work with this data?
- Are there enough samples?
- Is data format compatible with tools?

---

## Step 5: EDA Preview

For top dataset candidates:

- Load sample data
- Check distributions
- Identify potential issues
- Estimate preprocessing effort

---

## Step 6: Documentation

Document selected datasets:

```markdown
## Dataset: [NAME]
- **Source:** [URL]
- **Size:** [rows x columns]
- **Access:** Open/Licensed/Request
- **Citation:** [BibTeX]
- **Preprocessing Notes:** ...
```

---

## Output Artifacts

| File | Location |
|------|----------|
| dataset_search_results.md | 4_Methodology_Design/ |
| selected_datasets.md | 4_Methodology_Design/ |
| eda_preview.md | 6_Analysis_Results/ |

---



---

## Agent Routing

> **Primary Agent**: `DatasetResearchSpecialist`
> Load agent config: `agents/DatasetResearchSpecialist.json`

## Trigger Phrases

- "Find datasets for [RESEARCH]"
- "What datasets exist for [TOPIC]?"
- "I need data for [PROJECT]"

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
