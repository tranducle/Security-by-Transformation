---
description: Structured ideation session using SOP_IDEATION_SESSION — 5-agent creative pipeline for generating, exploring, and prioritizing research ideas
---

# Ideation Session Workflow (SOP_IDEATION_SESSION)

**Use when:** You need a structured brainstorming session to generate novel research ideas, explore design spaces, or find innovative approaches.

---

## Step 1: Idea Generation

> **Agent:** `BrainstormingFacilitator`

Generate diverse ideas using structured techniques:

- **SCAMPER** (Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse)
- **Lateral thinking** — challenge assumptions
- **Analogy transfer** — borrow solutions from other domains
- **Constraint relaxation** — "what if we could...?"

**Output:** 10-20 raw ideas (quantity over quality at this stage)

---

## Step 2: Design Space Exploration

> **Agent:** `IdeaMutationDesignSpaceExplorer`

For each promising idea, explore variants:

- Mutate parameters (scale, scope, domain, method)
- Cross-pollinate between ideas
- Map the design space dimensions
- Identify unexplored regions
- Generate hybrid combinations

---

## Step 3: Feasibility Evaluation

> **Agent:** `OmniThinker`

Evaluate ideas on multiple dimensions:

| Idea | Novelty | Feasibility | Impact | Risk | Total |
|------|---------|-------------|--------|------|-------|
| Idea A | 1-5 | 1-5 | 1-5 | 1-5 | /20 |

- Technical feasibility assessment
- Resource requirement estimation
- Timeline realism check
- Ethical considerations

---

## Step 4: Gap Identification

> **Agent:** `MissingPartSuggester`

For top-ranked ideas, identify what's missing:

- Required datasets or tools
- Missing theoretical foundations
- Collaboration needs
- Preliminary experiments needed
- Potential pitfalls and mitigations

---

## Step 5: Prioritization & Roadmap

> **Agent:** `InnovationStrategist`

Create actionable next steps:

- Rank final ideas by strategic value
- Create implementation roadmap for top 3
- Define success criteria and milestones
- Identify quick wins vs long-term bets
- Auto-update research diary with session outcomes

---

## Output Artifacts

| File | Location |
|------|----------|
| ideation_raw_ideas.md | 1_Strategic_Plan/ |
| design_space_map.md | 1_Strategic_Plan/ |
| idea_evaluation.md | 1_Strategic_Plan/ |
| innovation_roadmap.md | 1_Strategic_Plan/ |

---

## Agent Routing

> **Primary Agent**: `BrainstormingFacilitator`
> **Pipeline**: `BrainstormingFacilitator` → `IdeaMutationDesignSpaceExplorer` → `OmniThinker` → `MissingPartSuggester` → `InnovationStrategist`

## Trigger Phrases

- "Ideation session"
- "Brainstorm session"
- "Generate research ideas"
- "Creative session"
- "Explore design space"
- "Innovation workshop"

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
