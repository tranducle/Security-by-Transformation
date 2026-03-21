---
description: Self-repair pipeline using SOP_SELF_REPAIR — find flaws, fix agents, and refine prompts
---

# Self-Repair Workflow (SOP_SELF_REPAIR)

**Use when:** The agent system needs self-diagnosis and improvement — fixing broken agents, improving prompts, or addressing system-level issues.

---

## Step 1: Flaw Detection

> **Agent:** `PeerReviewer`

- Audit recent agent outputs for quality issues
- Identify reasoning failures or hallucinations
- Check for consistency across agent outputs
- Flag agents producing below-par results
- Generate diagnostic report

---

## Step 2: Agent System Repair

> **Agent:** `AgentSystemArchitect`

- Analyze the failing agent's configuration
- Identify root cause (prompt issue, tool misconfiguration, routing error)
- Propose and implement fixes:
  - Update agent JSON configuration
  - Fix tool integration
  - Adjust routing triggers
  - Update system prompt components
- Validate fix against test cases

---

## Step 3: Prompt Refinement

> **Agent:** `PromptOptimizer`

- Optimize the repaired agent's prompts
- Apply prompt engineering best practices
- Test with sample inputs
- Compare output quality before/after
- Document optimization rationale

---

## Output Artifacts

| File | Location |
|------|----------|
| diagnostic_report.md | 8_Project_Management/ |
| repair_log.md | 8_Project_Management/ |
| optimized_prompts.md | 8_Project_Management/ |

---

## Agent Routing

> **Pipeline**: `PeerReviewer` → `AgentSystemArchitect` → `PromptOptimizer`

## Trigger Phrases

- "Self repair"
- "Fix agent system"
- "Improve agent"
- "Repair broken agent"
- "System self-diagnosis"

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
