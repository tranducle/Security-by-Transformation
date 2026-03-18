---
description: Analyze complex systems using systems thinking
---

# Systems Analysis Workflow (SOP_SYSTEMS_ANALYSIS)

**Use when:** Analyzing complex systems with feedback loops and dynamics.

---

## Step 1: System Boundary

Define the system:

- What's included?
- What's external (environment)?
- Key stakeholders

---

## Step 2: Component Mapping

Identify system elements:

- Key actors/entities
- Resources/stocks
- Processes/flows
- Information channels

---

## Step 3: Feedback Loop Identification

Map feedback dynamics:

### Reinforcing Loops (R)

- Positive feedback
- Growth or decline amplification

### Balancing Loops (B)

- Negative feedback
- Goal-seeking behavior

---

## Step 4: Causal Loop Diagram

Create visual representation:

```
┌─────────┐    +     ┌─────────┐
│ Factor A │───────→│ Factor B │
└─────────┘          └────┬────┘
     ↑                    │
     │        +           │
     └────────────────────┘
           (R) Growth Loop
```

---

## Step 5: Causal Pathway Analysis

Trace cause-effect chains:

- Direct effects
- Indirect effects
- Delays
- Non-linear relationships

---

## Step 6: Scenario Forecasting

Project system behavior:

- Business as usual
- Best case
- Worst case
- Policy interventions

---

## Step 7: Visualization

Create system diagrams:

- Causal loop diagrams
- Stock-flow diagrams
- Rich pictures

---

## Step 8: Recommendations

Based on system understanding:

- Leverage points
- Intervention strategies
- Risk areas

---

## Output Artifacts

| File | Location |
|------|----------|
| system_map.md | 3_Theoretical_Framework/ |
| causal_analysis.md | 6_Analysis_Results/ |
| scenarios.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `SystemDynamicsMapper`
> Load agent config: `agents/SystemDynamicsMapper.json`

## Trigger Phrases

- "Analyze [SYSTEM] as a complex system"
- "Map feedback loops in [AREA]"
- "Systems thinking for [PROBLEM]"

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
