---
description: End-to-end ML data pipeline using SOP_DATA_PREPROCESSING — from model analysis through preprocessing, verification, and training integration
---

# ML Data Pipeline Workflow (SOP_DATA_PREPROCESSING)

**Use when:** Building a complete ML data pipeline — profiling datasets, selecting preprocessing techniques, generating code, and integrating with training loops.

---

## Step 1: Model Analysis & Dataset Profiling

> **Agent:** `DataPreprocessingEngineer`

### Model Analysis
- Analyze target model architecture requirements
- Determine input format, dimensions, and constraints
- Identify required data transformations

### Dataset Profiling
- Statistical summary (shape, dtypes, distributions)
- Missing value pattern analysis
- Class distribution and imbalance detection
- Feature correlation analysis
- Data quality scoring

---

## Step 2: Technique Selection & Code Generation

> **Agent:** `DataPreprocessingEngineer` (continued)

Based on profiling, select and implement:

| Task | Technique Options |
|------|-------------------|
| Missing values | Mean/median/mode, KNN, MICE, drop |
| Encoding | One-hot, label, target, ordinal |
| Scaling | StandardScaler, MinMax, RobustScaler |
| Imbalance | SMOTE, ADASYN, undersampling, class weights |
| Augmentation | Random crop, flip, noise, mixup |
| Feature selection | Variance threshold, mutual info, L1 |

**Output:** Complete preprocessing pipeline code (sklearn/pandas/torch)

---

## Step 3: Transform Verification

> **Agent:** `DataMetricsAnalyst`

- Verify preprocessing correctness
- Compare distributions before/after
- Check for data leakage
- Validate stratified splits
- Generate quality assurance report

---

## Step 4: Training Loop Integration

> **Agent:** `PyTorchImplementer`

- Create PyTorch Dataset and DataLoader
- Integrate preprocessing into training pipeline
- Add data pipeline to experiment config
- Ensure reproducibility (fixed seeds, deterministic transforms)

---

## Output Artifacts

| File | Location |
|------|----------|
| dataset_profile.md | 6_Analysis_Results/ |
| preprocessing_pipeline.py | 5_Experiments_Simulations/ |
| data_quality_report.md | 6_Analysis_Results/ |
| dataloader.py | 5_Experiments_Simulations/ |

---

## Agent Routing

> **Pipeline**: `DataPreprocessingEngineer` → `DataMetricsAnalyst` → `PyTorchImplementer`

## Trigger Phrases

- "Data pipeline"
- "Preprocess data for training"
- "ML data pipeline"
- "Prepare data for model"
- "Build preprocessing pipeline"

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
