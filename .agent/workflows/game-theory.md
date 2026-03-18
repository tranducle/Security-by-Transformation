---
description: Game theory analysis for strategic interactions
---

# Game Theory Analysis Workflow (SOP_GAME_THEORY_ANALYSIS)

**Use when:** Modeling strategic interactions between agents.

---

## Step 1: Game Formulation

### Players

- Identify all strategic agents
- Define player roles

### Strategies

| Player | Available Strategies |
|--------|---------------------|
| Player 1 | {s₁, s₂, ...} |
| Player 2 | {t₁, t₂, ...} |

### Payoffs

Define utility/payoff functions for each player.

---

## Step 2: Game Type Classification

| Type | Characteristics |
|------|-----------------|
| **Static** | Simultaneous moves |
| **Dynamic** | Sequential moves |
| **Complete Info** | All players know payoffs |
| **Incomplete Info** | Bayesian game |
| **Cooperative** | Binding agreements |
| **Non-cooperative** | No binding agreements |
| **Zero-sum** | One's gain = other's loss |
| **Non-zero-sum** | Variable total |

---

## Step 3: Game Representation

### Normal Form (Matrix)

```
           Player 2
           s₁    s₂
Player 1  ┌─────┬─────┐
    s₁    │(a,b)│(c,d)│
          ├─────┼─────┤
    s₂    │(e,f)│(g,h)│
          └─────┴─────┘
```

### Extensive Form (Tree)

For sequential games with decision nodes.

---

## Step 4: Equilibrium Analysis

### Nash Equilibrium

Find strategy profiles where no player benefits from unilateral deviation.

### Subgame Perfect Equilibrium

For dynamic games, use backward induction.

### Mixed Strategy Equilibrium

When pure strategy NE doesn't exist.

---

## Step 5: Attacker-Defender Games

For security applications:

- Define attack strategies
- Define defense strategies
- Model information asymmetry
- Calculate optimal strategies

---

## Step 6: Outcome Evaluation

- Expected payoffs
- Social welfare analysis
- Efficiency assessment
- Fairness considerations

---

## Step 7: Scenario Projection

- Sensitivity to parameter changes
- Multiple equilibria interpretation
- Policy recommendations

---

## Output Artifacts

| File | Location |
|------|----------|
| game_formulation.md | 3_Theoretical_Framework/ |
| equilibrium_analysis.md | 6_Analysis_Results/ |
| strategic_recommendations.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `GameTheoryStrategist`
> Load agent config: `agents/GameTheoryStrategist.json`

## Trigger Phrases

- "Game theory analysis for [SCENARIO]"
- "Find Nash equilibrium"
- "Attacker-defender model"

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
