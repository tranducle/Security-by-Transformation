---
description: Initialize new research project with scope and planning
---

# Project Kickoff Workflow (SOP_PROJECT_KICKOFF)

**Use when:** Starting a new research project from scratch.

---

## Step 0: Install Dependencies (FIRST TIME ONLY)

> ⚠️ **Run this on NEW MACHINE or fresh project clone**

// turbo

```bash
pip install -r requirements.txt --quiet 2>$null; pip install mem0ai --quiet 2>$null; echo "Dependencies ready"
```

---

## Step 1: Project Definition

Define basic parameters:

- Project name/title
- Domain/area
- Sponsor/funding (if any)
- Start date
- Target end date

---

## Step 2: Scope Definition

Set project boundaries:

- In scope: What's included
- Out of scope: What's excluded
- Assumptions
- Constraints

---

## Step 3: Research Scope

Define research parameters:

- Research questions (preliminary)
- Expected contributions
- Target publications
- Dataset needs

---

## Step 4: Directory Structure

Create SDP directories (ALL 10 folders):

```
PROJECT_NAME/
├── 0_Project_Admin/           # Research diary, metadata
├── 1_Strategic_Plan/          # Plans, proposals
├── 2_Literature_Review/       # Papers, synthesis
├── 3_Theoretical_Framework/   # Theory, proofs
├── 4_Methodology_Design/      # Method design docs
├── 5_Experiments_Simulations/ # Code, simulation results
├── 6_Analysis_Results/        # Analysis outputs
├── 7_Manuscript_Draft/        # Paper sections
├── 8_Project_Management/      # Logs, tracking
└── 9_Presentation/            # Slides, figures
```

---

## Step 5: Initialize Project Management Files

**CRITICAL: Run /init-project-files workflow here**

This creates:

- `8_Project_Management/project_log.md`
- `8_Project_Management/milestone_tracker.md`
- `8_Project_Management/decision_log.md`
- `8_Project_Management/prompt_history.md`
- Initialize `0_Project_Admin/research_diary.md`

---

## Step 5.5: Initialize Memory System (MANDATORY)

Set up Mem0 for persistent memory:

// turbo

```bash
pip install mem0ai --quiet
python src/tools/mem0_loader.py [PROJECT_ID] --init "[PROJECT_NAME]" "[RESEARCH_TOPIC]"
```

This saves to persistent memory:

- Agent routing rules (keywords → agent mapping)
- Project context (name, topic, status)
- Design standards for key agents

> ⚠️ **This step ensures memory persists across sessions**

---

## Step 6: Work Breakdown

Create initial WBS:

- Major phases
- Key deliverables
- Milestones

---

## Step 7: Strategy Definition

High-level approach:

- Methodology direction
- Key risks
- Critical success factors

---

## Output Artifacts

| File | Location |
|------|----------|
| project_charter.md | 1_Strategic_Plan/ |
| research_diary.md | 0_Project_Admin/ |
| project_log.md | 8_Project_Management/ |
| milestone_tracker.md | 8_Project_Management/ |
| decision_log.md | 8_Project_Management/ |
| prompt_history.md | 8_Project_Management/ |

---

## Post-Kickoff Reminder

> **IMPORTANT**: After EVERY major task in this project, update:
>
> - `8_Project_Management/project_log.md` with actions taken
> - `8_Project_Management/milestone_tracker.md` if milestone status changes
> - `0_Project_Admin/research_diary.md` for significant insights

---

## Step 8: Verify System Ready

> The system uses **Antigravity as MasterOrchestrator** with LangGraph for pipeline execution. No mode selection needed.

```bash
python -m src.langgraph.cli --health
```

---

## Trigger Phrases

- "Start new project on [TOPIC]"
- "Kick off [PROJECT]"
- "Initialize [RESEARCH] project"
