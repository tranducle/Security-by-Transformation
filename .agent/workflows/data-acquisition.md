---
description: Find, evaluate, and prepare datasets for research using SOP_DATA_ACQUISITION — from discovery through preprocessing
---

# Data Acquisition Workflow (SOP_DATA_ACQUISITION)

**Use when:** You need to find datasets, evaluate their suitability, perform EDA, and preprocess data for research.

---

## Step 1: Dataset Discovery

> **Agent:** `DatasetResearchSpecialist`

Search for relevant datasets:

- Academic repositories (UCI, Kaggle, Papers With Code)
- Government data portals (data.gov, EU Open Data)
- Domain-specific sources (PhysioNet, ImageNet, MITRE)
- Industry benchmarks and shared datasets
- Check licensing and availability

**Output:** Candidate dataset list with metadata

---

## Step 2: Feasibility Assessment

> **Agent:** `MethodologyArchitect`

Evaluate each candidate dataset:

| Dataset | Size | Features | Quality | License | Fit Score |
|---------|------|----------|---------|---------|-----------|
| Dataset A | N rows | F features | High/Med/Low | MIT/CC/etc | 1-5 |

- Does it match research questions?
- Is the sample size sufficient for the methodology?
- Are there ethical concerns?

---

## Step 3: Exploratory Data Analysis

> **Agent:** `DataMetricsAnalyst`

Perform initial EDA:

- Descriptive statistics (mean, median, std, quartiles)
- Missing value analysis
- Distribution analysis (normality, skewness)
- Correlation matrix
- Class balance check (for classification tasks)
- Outlier detection

**Output:** `6_Analysis_Results/eda_report.md`

---

## Step 4: Data Preprocessing

> **Agent:** `DataPreprocessingEngineer`

Prepare data for analysis/training:

- Handle missing values (imputation strategy)
- Feature encoding (one-hot, label, ordinal)
- Normalization/standardization
- Train/val/test split
- Data augmentation (if needed)
- SMOTE for imbalanced classes (if needed)

**Output:** Preprocessing pipeline code + processed data

---

## Step 5: Track & Log

> **Agent:** `ProjectStateKeeper`

Update project tracking with:

- Datasets selected and rationale
- EDA key findings
- Preprocessing decisions
- Data quality assessment

---

## Output Artifacts

| File | Location |
|------|----------|
| dataset_candidates.md | 2_Literature_Review/ |
| eda_report.md | 6_Analysis_Results/ |
| preprocessing_pipeline.py | 5_Experiments_Simulations/ |
| data_quality_report.md | 6_Analysis_Results/ |

---

## Agent Routing

> **Primary Agent**: `DatasetResearchSpecialist`
> Load agent config: `agents/DatasetResearchSpecialist.json`
> **Pipeline**: `DatasetResearchSpecialist` → `MethodologyArchitect` → `DataMetricsAnalyst` → `DataPreprocessingEngineer` → `ProjectStateKeeper`

## Trigger Phrases

- "Find datasets for [TOPIC]"
- "Data acquisition for my research"
- "I need data for [METHODOLOGY]"
- "Collect data for [PROJECT]"

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
