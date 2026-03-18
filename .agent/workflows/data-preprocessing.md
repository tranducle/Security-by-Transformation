---
description: Data preprocessing, cleaning, and preparation for analysis
---

# Sop Data Preprocessing Workflow (SOP_DATA_PREPROCESSING)

**Use when:** Data preprocessing, cleaning, and preparation for analysis

---

## Step 1: DataPreprocessingEngineer

> **Agent**: `DataPreprocessingEngineer`
> Load agent config: `agents/DataPreprocessingEngineer.json`

## Step 2: DataMetricsAnalyst

> **Agent**: `DataMetricsAnalyst`
> Load agent config: `agents/DataMetricsAnalyst.json`

## Step 3: PyTorchImplementer

> **Agent**: `PyTorchImplementer`
> Load agent config: `agents/PyTorchImplementer.json`

---

## Agent Routing

> **SOP Pipeline**: `SOP_DATA_PREPROCESSING` (3 agents)

## Trigger Phrases

- "preprocess data"
- "preprocessing pipeline"
- "prepare data for training"
- "tiền xử lý dữ liệu"

---

## Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if milestone status changed
> 3. Log significant decisions to `8_Project_Management/decision_log.md`
>
> **Quick command**: Run `/sync` to update all files at once.
