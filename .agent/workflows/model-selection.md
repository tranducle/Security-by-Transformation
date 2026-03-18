---
description: Model selection and capability comparison for research tasks
---

# Sop Model Selection Workflow (SOP_MODEL_SELECTION)

**Use when:** Model selection and capability comparison for research tasks

---

## Step 1: ModelCapabilityRouter

> **Agent**: `ModelCapabilityRouter`
> Load agent config: `agents/ModelCapabilityRouter.json`

## Step 2: MethodologyExperimentDesigner

> **Agent**: `MethodologyExperimentDesigner`
> Load agent config: `agents/MethodologyExperimentDesigner.json`

## Step 3: PyTorchImplementer

> **Agent**: `PyTorchImplementer`
> Load agent config: `agents/PyTorchImplementer.json`

## Step 4: ExperimentConductor

> **Agent**: `ExperimentConductor`
> Load agent config: `agents/ExperimentConductor.json`

---

## Agent Routing

> **SOP Pipeline**: `SOP_MODEL_SELECTION` (4 agents)

## Trigger Phrases

- "model selection"
- "which model"
- "choose model"

---

## Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if milestone status changed
> 3. Log significant decisions to `8_Project_Management/decision_log.md`
>
> **Quick command**: Run `/sync` to update all files at once.
