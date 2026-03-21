---
description: Run quantitative experiments end-to-end using SOP_QUANT_EXPERIMENT — from design through statistical analysis and visualization
---

# Quantitative Experiment Workflow (SOP_QUANT_EXPERIMENT)

**Use when:** Running a complete quantitative experiment — designing, preprocessing data, executing, analyzing, and visualizing results.

---

## Step 1: Experiment Design & Hardware Profile

> **Agent:** `MethodologyExperimentDesigner`

- Define independent, dependent, and control variables
- Choose experimental design (RCT, quasi-experimental, factorial)
- Determine sample size via power analysis
- Profile hardware requirements (GPU, RAM, storage)
- Set hyperparameter search space (if ML)

---

## Step 2: Methodology Protocol

> **Agent:** `MethodologyArchitect`

- Formalize research protocol
- Define metrics and evaluation criteria
- Establish baseline comparisons
- Document assumptions and constraints
- Create reproducibility checklist

---

## Step 3: Data Preprocessing

> **Agent:** `DataPreprocessingEngineer`

- Clean and validate data
- Handle missing values, outliers
- Feature engineering and selection
- Train/val/test split strategy
- Generate preprocessing pipeline code

---

## Step 4: Experiment Execution

> **Agent:** `ExperimentConductor`

- Execute experiment with tracking (MLflow/W&B compatible)
- Monitor convergence and early stopping
- Log all hyperparameters and metrics
- Capture intermediate checkpoints

---

## Step 5: Exploratory Data Analysis

> **Agent:** `DataMetricsAnalyst`

- Analyze raw results
- Compute performance metrics
- Compare against baselines
- Identify patterns and anomalies

---

## Step 6: Statistical Analysis

> **Agent:** `StatisticalAnalyst`

- Hypothesis testing (t-test, ANOVA, Wilcoxon, etc.)
- Confidence intervals
- Effect size calculation (Cohen's d, η²)
- Robustness checks and sensitivity analysis
- Multiple comparison corrections (Bonferroni, FDR)

---

## Step 7: Results Visualization

> **Agent:** `ResultVisualizer`

- Performance comparison charts
- Ablation study plots
- Confusion matrices and ROC curves
- Statistical significance annotations

---

## Output Artifacts

| File | Location |
|------|----------|
| experiment_design.md | 4_Methodology_Design/ |
| experiment_results.md | 6_Analysis_Results/ |
| statistical_analysis.md | 6_Analysis_Results/ |
| figures/ | 6_Analysis_Results/figures/ |

---

## Agent Routing

> **Primary Agent**: `MethodologyExperimentDesigner`
> **Pipeline**: `MethodologyExperimentDesigner` → `MethodologyArchitect` → `DataPreprocessingEngineer` → `ExperimentConductor` → `DataMetricsAnalyst` → `StatisticalAnalyst` → `ResultVisualizer`

## Trigger Phrases

- "Run experiment"
- "Quantitative experiment"
- "Execute experiment pipeline"
- "Full experiment workflow"

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
