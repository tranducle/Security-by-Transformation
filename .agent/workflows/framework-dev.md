---
description: Design and develop research frameworks and system architectures
---

# Sop Framework Dev Workflow (SOP_FRAMEWORK_DEV)

**Use when:** Design and develop research frameworks and system architectures

---

## Step 1: FrameworkArchitect

> **Agent**: `FrameworkArchitect`
> Load agent config: `agents/FrameworkArchitect.json`

## Step 2: PyTorchImplementer

> **Agent**: `PyTorchImplementer`
> Load agent config: `agents/PyTorchImplementer.json`

## Step 3: FrameworkValidationArchitect

> **Agent**: `FrameworkValidationArchitect`
> Load agent config: `agents/FrameworkValidationArchitect.json`

## Step 4: FileIntegrator

> **Agent**: `FileIntegrator`
> Load agent config: `agents/FileIntegrator.json`

---

## Agent Routing

> **SOP Pipeline**: `SOP_FRAMEWORK_DEV` (4 agents)

## Trigger Phrases

- "build framework"
- "framework development"

---

## Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if milestone status changed
> 3. Log significant decisions to `8_Project_Management/decision_log.md`
>
> **Quick command**: Run `/sync` to update all files at once.
