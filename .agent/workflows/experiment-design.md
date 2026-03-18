---
description: Design quantitative experiments with hardware profiling
---

# Experiment Design Workflow (SOP_QUANT_EXPERIMENT)

**Use when:** Designing and running quantitative experiments.

---

## Step 1: Experiment Design

### 1.1 Research Design Type

- Randomized controlled trial
- Quasi-experimental
- Pre-post design
- Factorial design

### 1.2 Variables

| Type | Variable | Measurement |
|------|----------|-------------|
| Independent | [X] | [How measured] |
| Dependent | [Y] | [How measured] |
| Control | [C] | [How controlled] |

### 1.3 Hypotheses

- H1: [Hypothesis 1]
- H0: [Null hypothesis]

---

## Step 2: Hardware Profiling (if computational)

For ML/simulation experiments:

- GPU requirements
- Memory requirements
- Expected runtime
- Parallelization options

---

## Step 3: Protocol Development

Detailed step-by-step protocol:

1. Environment setup
2. Data preparation
3. Experiment execution
4. Data collection
5. Cleanup

---

## Step 4: Execution

Run the experiment:

- Monitor progress
- Log intermediate results
- Handle failures gracefully

---

## Step 5: Exploratory Data Analysis

Initial analysis:

- Descriptive statistics
- Distribution checks
- Outlier detection

```python
from src.tools import calculate_descriptive_stats
stats = calculate_descriptive_stats(data)
```

---

## Step 6: Statistical Analysis

Hypothesis testing:

- Normality tests
- Appropriate statistical tests
- Effect size calculation
- Confidence intervals

```python
from src.tools import independent_t_test, correlation
```

---

## Step 7: Visualization

Create result visualizations:

- Distribution plots
- Comparison charts
- Effect visualizations

---

## Output Artifacts

| File | Location |
|------|----------|
| experiment_design.md | 4_Methodology_Design/ |
| experiment_protocol.md | 5_Experiments_Simulations/ |
| raw_results.csv | 6_Analysis_Results/ |
| statistical_analysis.md | 6_Analysis_Results/ |

---



---

## Agent Routing

> **Primary Agent**: `MethodologyExperimentDesigner`
> Load agent config: `agents/MethodologyExperimentDesigner.json`

## Trigger Phrases

- "Design an experiment for [TOPIC]"
- "Run quantitative experiment"
- "Statistical experiment design"

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
