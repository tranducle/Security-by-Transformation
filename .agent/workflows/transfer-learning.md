---
description: Transfer learning and cross-domain research adaptation workflows
---

# Sop Transfer Learning Workflow (SOP_TRANSFER_LEARNING)

**Use when:** Transfer learning and cross-domain research adaptation workflows

---

## Step 1: MethodologyExperimentDesigner

> **Agent**: `MethodologyExperimentDesigner`
> Load agent config: `agents/MethodologyExperimentDesigner.json`

## Step 2: CrossDomainTransferHybridizationAgent

> **Agent**: `CrossDomainTransferHybridizationAgent`
> Load agent config: `agents/CrossDomainTransferHybridizationAgent.json`

## Step 3: PyTorchImplementer

> **Agent**: `PyTorchImplementer`
> Load agent config: `agents/PyTorchImplementer.json`

## Step 4: DataMetricsAnalyst

> **Agent**: `DataMetricsAnalyst`
> Load agent config: `agents/DataMetricsAnalyst.json`

---

## Agent Routing

> **SOP Pipeline**: `SOP_TRANSFER_LEARNING` (4 agents)

## Trigger Phrases

- "transfer learning"
- "domain adaptation"
- "cross domain"

---

## Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if milestone status changed
> 3. Log significant decisions to `8_Project_Management/decision_log.md`
>
> **Quick command**: Run `/sync` to update all files at once.
