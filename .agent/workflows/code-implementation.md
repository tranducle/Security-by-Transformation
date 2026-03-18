---
description: Implement research code, frameworks, and reproducibility artifacts
---

# Sop Code Implementation Workflow (SOP_CODE_IMPLEMENTATION)

**Use when:** Implement research code, frameworks, and reproducibility artifacts

---

## Step 1: MethodologyExperimentDesigner

> **Agent**: `MethodologyExperimentDesigner`
> Load agent config: `agents/MethodologyExperimentDesigner.json`

## Step 2: MethodologyArchitect

> **Agent**: `MethodologyArchitect`
> Load agent config: `agents/MethodologyArchitect.json`

## Step 3: PyTorchImplementer

> **Agent**: `PyTorchImplementer`
> Load agent config: `agents/PyTorchImplementer.json`

## Step 4: ReproducibilityArtifactEngineer

> **Agent**: `ReproducibilityArtifactEngineer`
> Load agent config: `agents/ReproducibilityArtifactEngineer.json`

---

## Agent Routing

> **SOP Pipeline**: `SOP_CODE_IMPLEMENTATION` (4 agents)

## Trigger Phrases

- "implement code"
- "code implementation"
- "build model"
- "viết code"
- "lập trình"

---

## Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if milestone status changed
> 3. Log significant decisions to `8_Project_Management/decision_log.md`
>
> **Quick command**: Run `/sync` to update all files at once.
