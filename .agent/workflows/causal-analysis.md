---
description: Causal inference analysis using econometric methods
---

# Causal Analysis Workflow (SOP_CAUSAL_ANALYSIS)

**Use when:** Establishing causal relationships in observational data.

---

## Step 1: Causal Question Framing

Define the causal question:

- Treatment/Intervention (X)
- Outcome (Y)
- Potential confounders (Z)
- Causal pathway hypothesis

---

## Step 2: Identification Strategy

Choose appropriate method:

| Method | When to Use | Key Assumption |
|--------|-------------|----------------|
| **Difference-in-Differences (DiD)** | Natural experiment, panel data | Parallel trends |
| **Instrumental Variables (IV)** | Endogeneity concerns | Exclusion restriction |
| **Regression Discontinuity (RDD)** | Threshold-based treatment | Continuity at cutoff |
| **Propensity Score Matching** | Selection bias | Unconfoundedness |
| **Synthetic Control** | Comparative case study | Fit quality |

---

## Step 3: Model Specification

### DiD Example

```
Y_it = α + β(Treatment_i × Post_t) + γX_it + θ_i + λ_t + ε_it
```

### IV Example

```
First Stage: X = π₀ + π₁Z + ν
Second Stage: Y = β₀ + β₁X̂ + ε
```

---

## Step 4: Assumption Testing

### For DiD

- Parallel trends test (pre-treatment)
- Placebo tests

### For IV

- First-stage F-statistic > 10
- Overidentification test (if multiple instruments)

### For RDD

- Manipulation test (McCrary)
- Bandwidth sensitivity

---

## Step 5: Estimation

Run the causal model:

- Point estimates
- Standard errors (clustered if panel)
- Confidence intervals

---

## Step 6: Robustness Checks

- Alternative specifications
- Placebo outcomes
- Sensitivity analysis
- Subgroup analysis

---

## Step 7: Effect Interpretation

- Average Treatment Effect (ATE)
- Effect size interpretation
- Policy implications
- Limitations of causal claim

---

## Output Artifacts

| File | Location |
|------|----------|
| causal_design.md | 4_Methodology_Design/ |
| identification_strategy.md | 4_Methodology_Design/ |
| causal_results.md | 6_Analysis_Results/ |

---



---

## Agent Routing

> **Primary Agent**: `CausalAnalyst`
> Load agent config: `agents/CausalAnalyst.json`

## Trigger Phrases

- "Causal analysis of [X] on [Y]"
- "Difference-in-differences analysis"
- "Does [X] cause [Y]?"

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
