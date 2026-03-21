---
description: Discover research ideas when starting without a topic — uses JournalIdeaScout to analyze trends and generate novel ideas with SOP_IDEA_DISCOVERY
---

# Research Idea Discovery Workflow (SOP_IDEA_DISCOVERY)

**Use when:** Starting a new research project without a specific topic, looking for trending ideas, or exploring new directions.

---

## Step 1: Journal & Trend Analysis

> **Agent:** `JournalIdeaScout`

Analyze target journal scope, recent publications, and trending topics:

- Scan top journals in the target domain
- Identify emerging themes and under-explored areas
- Map citation velocity to spot rising topics
- Cross-reference with conference proceedings (ICML, NeurIPS, IEEE S&P, etc.)

**Output:** 3-5 research ideas with novelty justification

---

## Step 2: User Selection

Present ideas to the user with:

| # | Idea | Domain | Novelty Score | Feasibility |
|---|------|--------|---------------|-------------|
| 1 | [Idea A] | [Field] | High/Med/Low | High/Med/Low |
| 2 | [Idea B] | [Field] | High/Med/Low | High/Med/Low |

**User selects one idea to develop.**

---

## Step 3: Scope Development

> **Agent:** `ResearchScoper`

Develop the selected idea into a research scope:

- Define research questions (RQs)
- Identify target population/context
- Set boundaries and limitations
- Propose a working title

---

## Step 4: Research Plan Generation

> **Agent:** `ResearchPlanGenerator`

Create a comprehensive research plan:

- Work Breakdown Structure (WBS)
- Timeline with milestones
- Resource requirements
- Risk assessment
- Required datasets and tools

**Output:** `1_Strategic_Plan/research_plan.md`

---

## Step 5: Auto-Update Research Diary

System automatically updates `0_Project_Admin/research_diary.md` with:

- Selected idea and rationale
- Research questions
- Initial scope boundaries

---

## Output Artifacts

| File | Location |
|------|----------|
| research_ideas.md | 1_Strategic_Plan/ |
| research_scope.md | 1_Strategic_Plan/ |
| research_plan.md | 1_Strategic_Plan/ |

---

## Agent Routing

> **Primary Agent**: `JournalIdeaScout`
> Load agent config: `agents/JournalIdeaScout.json`
> **Secondary**: `ResearchScoper`, `ResearchPlanGenerator`

## Trigger Phrases

- "Find me a research topic"
- "What should I research?"
- "New project idea"
- "Trending topics in [FIELD]"
- "I don't have a topic yet"
- "Research idea discovery"

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
